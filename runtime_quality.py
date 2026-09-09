"""Runtime quality fixes shared by Hangeul Design entry points.

This module keeps the original UI intact while correcting state timing,
prompt diversity, translation behavior, save reporting, custom expert styles,
and clipboard escaping.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import random
import time
import urllib.parse
import urllib.request
from typing import Any, Dict

import streamlit as st
import streamlit.components.v1 as components


VARIANT_AXES = [
    ("centered hero composition", "soft directional studio light", "50mm eye-level", "restrained complementary palette"),
    ("asymmetric editorial composition", "hard side light with controlled shadow", "35mm three-quarter view", "warm accent palette"),
    ("macro-led detail composition", "rim light with soft fill", "85mm close-up", "monochrome palette with one accent"),
    ("wide environmental composition", "natural window light", "24mm contextual view", "muted cinematic palette"),
    ("graphic negative-space composition", "high-key commercial light", "70mm clean product view", "high-contrast brand palette"),
    ("low-angle premium hero composition", "dramatic top and rim light", "50mm low angle", "deep neutral palette with metallic accent"),
    ("top-down structured composition", "large softbox illumination", "top-down camera", "clean tonal palette"),
    ("lifestyle interaction composition", "golden-hour motivated light", "35mm handheld-natural framing", "warm natural palette"),
]

_PENDING_FAVORITE = "_hd_pending_favorite"
_variant_counter = 0


def _stable_seed(*parts: Any) -> int:
    raw = "|".join(str(x) for x in parts).encode("utf-8", errors="ignore")
    return int(hashlib.sha256(raw).hexdigest()[:12], 16)


def _next_variant(subject: str, preset: str, work_mode: str) -> tuple[int, tuple[str, str, str, str]]:
    global _variant_counter
    idx = _variant_counter % len(VARIANT_AXES)
    _variant_counter += 1
    # Stable rotation per input while keeping each batch visibly different.
    offset = _stable_seed(subject, preset, work_mode) % len(VARIANT_AXES)
    real_idx = (idx + offset) % len(VARIANT_AXES)
    return real_idx + 1, VARIANT_AXES[real_idx]


def reset_variant_counter() -> None:
    global _variant_counter
    _variant_counter = 0


def apply_pending_favorite(base_app) -> None:
    item = st.session_state.pop(_PENDING_FAVORITE, None)
    if not item:
        return
    base_app._apply_preset_defaults(item.get("preset", st.session_state.get("preset", "한글 디자인")))
    mapping = {
        "preset": "preset",
        "work_mode": "work_mode",
        "style": "image_style",
        "lighting": "lighting",
        "camera": "camera",
        "aspect": "aspect",
        "pop3d": "pop3d",
        "intensity": "intensity",
        "brand": "brand",
        "prompt_engine": "prompt_engine",
        "expert_subject": "expert_subject",
        "hangul_text": "hangul_text",
        "palette": "palette",
        "continuity": "continuity",
        "detail_density": "detail_density",
    }
    for src, dst in mapping.items():
        if src in item and item[src] is not None:
            st.session_state[dst] = item[src]
    st.toast("템플릿 적용됨", icon="⭐")


def install(base_app) -> None:
    """Install release fixes onto the original app module before rendering widgets."""
    original_quick = base_app._build_prompts
    original_expert = base_app._build_expert_prompt

    def queue_favorite(item: Dict[str, Any]):
        # Do not mutate widget-bound keys after widgets are instantiated.
        st.session_state[_PENDING_FAVORITE] = dict(item)

    def save_favorites(items):
        try:
            os.makedirs(os.path.dirname(base_app.FAV_FILE), exist_ok=True)
            tmp = base_app.FAV_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            os.replace(tmp, base_app.FAV_FILE)
            return True
        except Exception as exc:
            st.error(f"즐겨찾기 저장 실패: {exc}")
            return False

    def save_current(plan):
        favs = list(st.session_state.favorites or [])
        item = {
            "id": base_app._fav_id(),
            "name": f"{plan.get('preset','')}/{plan.get('work_mode','')}/{plan.get('style','')}",
            "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "preset": plan.get("preset"),
            "work_mode": plan.get("work_mode"),
            "style": plan.get("style"),
            "lighting": plan.get("lighting"),
            "camera": plan.get("camera"),
            "aspect": plan.get("aspect"),
            "pop3d": plan.get("pop3d", False),
            "intensity": plan.get("intensity", st.session_state.get("intensity", 55)),
            "brand": plan.get("brand", ""),
            "prompt_engine": plan.get("prompt_engine", st.session_state.get("prompt_engine", "전문가 모드")),
            "expert_subject": plan.get("expert_subject", ""),
            "hangul_text": plan.get("hangul_text", ""),
            "palette": plan.get("palette", ""),
            "continuity": plan.get("continuity", True),
            "detail_density": plan.get("detail_density", 72),
            "image_prompt": plan.get("image_prompt", ""),
            "video_prompt": plan.get("video_prompt", ""),
            "d3_prompt": plan.get("d3_prompt", ""),
        }
        favs.insert(0, item)
        if save_favorites(favs):
            st.session_state.favorites = favs
            st.toast("즐겨찾기에 저장됨", icon="✅")

    def translate_google(text: str, src: str = "auto", dst: str = "en"):
        t = (text or "").strip()
        if not t:
            return "", True
        # Do not send plain ASCII/English text to the translation endpoint.
        if all(ord(ch) < 128 for ch in t):
            return t, True
        cache = st.session_state.setdefault("_hd_translation_cache", {})
        cache_key = f"{src}|{dst}|{t}"
        if cache_key in cache:
            return cache[cache_key], True
        try:
            q = urllib.parse.quote(t)
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={dst}&dt=t&q={q}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
            data = json.loads(raw)
            out = "".join(seg[0] for seg in data[0] if seg and isinstance(seg, list) and seg)
            out = (out or "").strip()
            if out:
                cache[cache_key] = out
                return out, True
        except Exception:
            pass
        return t, False

    def safe_clipboard(label: str, text: str, key: str):
        # JSON encoding prevents JS template-literal / ${...} injection.
        js_text = json.dumps(text or "", ensure_ascii=False)
        safe_label = html.escape(label or "복사")
        safe_id = "".join(ch for ch in key if ch.isalnum() or ch in "_-" )[:80] or "copy"
        block = f"""
        <div style='margin-top:6px'>
          <button id='{safe_id}' style='border:1px solid rgba(49,51,63,.18);border-radius:10px;padding:8px 10px;background:var(--secondary-background-color,#fff);cursor:pointer'>{safe_label}</button>
          <span id='{safe_id}_msg' style='margin-left:8px;font-size:12px'></span>
        </div>
        <script>
        const btn=document.getElementById({json.dumps(safe_id)});
        const msg=document.getElementById({json.dumps(safe_id + '_msg')});
        const payload={js_text};
        btn.addEventListener('click', async()=>{{
          try{{await navigator.clipboard.writeText(payload);msg.textContent='Copied';}}
          catch(e){{msg.textContent='Copy failed';}}
          setTimeout(()=>msg.textContent='',1400);
        }});
        </script>
        """
        components.html(block, height=46)

    def tip_for(preset: str) -> str:
        if preset == "한글 디자인":
            return "Tip: Keep Hangul structure, spacing, and layout hierarchy explicit; verify final typography in a design tool."
        return base_app._tip_for_original(preset) if hasattr(base_app, "_tip_for_original") else "Tip: Keep the visual direction specific and production-oriented."

    def quick_with_variation(*args, **kwargs):
        image_prompt, video_prompt, d3_prompt = original_quick(*args, **kwargs)
        subject = kwargs.get("subject_en", args[0] if args else "")
        preset = kwargs.get("preset", "")
        work_mode = kwargs.get("work_mode", "")
        n, axis = _next_variant(subject, preset, work_mode)
        comp, light, camera, palette = axis
        direction = f" Variant {n}: {comp}; {light}; {camera}; {palette}."
        return image_prompt + direction, video_prompt + direction, d3_prompt + direction

    def expert_with_variation(*args, **kwargs):
        if kwargs.get("style") == "직접입력":
            kwargs = dict(kwargs)
            kwargs["style"] = (st.session_state.get("style_custom") or "").strip() or "custom art direction"
        image_prompt, video_prompt, d3_prompt, blueprint = original_expert(*args, **kwargs)
        subject = kwargs.get("subject_en", args[0] if args else "")
        preset = kwargs.get("preset", "")
        work_mode = kwargs.get("work_mode", "")
        n, axis = _next_variant(subject, preset, work_mode)
        comp, light, camera, palette = axis
        direction = f"Variant {n}: {comp}; {light}; {camera}; {palette}."
        blueprint = blueprint + "\n" + direction
        return image_prompt + " " + direction, video_prompt + " " + direction, d3_prompt + " " + direction, blueprint

    if not hasattr(base_app, "_tip_for_original"):
        base_app._tip_for_original = base_app._tip_for
    base_app._apply_favorite = queue_favorite
    base_app._save_favorites = save_favorites
    base_app._save_current_as_favorite = save_current
    base_app.translate_google = translate_google
    base_app._clipboard_button = safe_clipboard
    base_app._tip_for = tip_for
    base_app._build_prompts = quick_with_variation
    base_app._build_expert_prompt = expert_with_variation


def render_theme_fix() -> None:
    st.markdown(
        """
        <style>
        .dp-card {background: var(--secondary-background-color) !important; color: var(--text-color) !important;}
        .dp-footer {color: color-mix(in srgb, var(--text-color) 65%, transparent) !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )
