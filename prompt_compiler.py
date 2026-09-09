from __future__ import annotations

import re
from typing import Tuple

TARGET_IMAGE_MODELS = [
    "ChatGPT / Gemini",
    "Midjourney",
    "Stable Diffusion / FLUX",
]

TARGET_VIDEO_MODELS = [
    "General / ChatGPT / Gemini",
    "Veo",
    "Sora",
    "Runway",
    "Kling",
]


def normalize_aspect(aspect: str) -> str:
    value = (aspect or "1:1").split()[0].strip()
    return value if re.fullmatch(r"\d+:\d+", value) else "1:1"


def _split_exclusions(prompt: str) -> Tuple[str, list[str]]:
    """Extract the final avoid/exclude clause and preserve reference control as positive guidance."""
    text = (prompt or "").strip()
    if not text:
        return "", []

    reference = ""
    ref_pos = text.find("REFERENCE IMAGE CONTROL:")
    if ref_pos >= 0:
        reference = text[ref_pos:].strip()
        text = text[:ref_pos].rstrip(" ,.\n")

    matches = list(re.finditer(r"(?:^|[,.]\s+|\s+)(exclude|avoid)\s*:?[ ]*", text, flags=re.I))
    if not matches:
        body = text
        if reference:
            body = f"{body} {reference}".strip()
        return body, []

    marker = matches[-1]
    raw = text[marker.end():].strip(" ,.\n")
    items = [x.strip(" ,.;") for x in raw.split(",") if x.strip(" ,.;")]
    body = text[:marker.start()].strip(" ,.\n")
    if reference:
        body = f"{body} {reference}".strip()
    return body, items


def _clean_text_negatives(items: list[str], allow_text: bool) -> list[str]:
    if not allow_text:
        return items
    blanket = {"text", "letters", "letter", "typography", "all text", "readable text"}
    return [item for item in items if item.lower().strip() not in blanket]


def compile_image_prompt(prompt: str, target_model: str, aspect: str, allow_text: bool = False, hangul_text: str = "") -> str:
    body, negatives = _split_exclusions(prompt)
    negatives = _clean_text_negatives(negatives, allow_text)
    ratio = normalize_aspect(aspect)

    if allow_text:
        exact = (hangul_text or "").strip()
        if exact:
            body += (
                f' Preserve this exact Korean text as a primary design element: "{exact}". '
                "Keep Hangul glyph structure, spacing, and readability accurate. Do not invent additional copy."
            )
        else:
            body += " Hangul typography is intentional; do not remove Korean lettering or treat it as an artifact."

    model = target_model or TARGET_IMAGE_MODELS[0]
    if model == "Midjourney":
        no_items = negatives or ["watermark", "signature", "random logos", "low resolution", "muddy details"]
        no_clause = " --no " + " ".join(x.replace(" ", "-") for x in no_items)
        return f"{body} --ar {ratio}{no_clause}".strip()
    if model == "Stable Diffusion / FLUX":
        neg = ", ".join(negatives) if negatives else "watermark, signature, random logos, low resolution, muddy details"
        return f"Positive prompt:\n{body}\n\nNegative prompt:\n{neg}\n\nAspect ratio: {ratio}"
    if negatives:
        body += " Avoid: " + ", ".join(negatives) + "."
    body += f" Output aspect ratio: {ratio}."
    return body.strip()


def compile_video_prompt(prompt: str, target_model: str, aspect: str) -> str:
    """Adapt the main video prompt without inventing vendor-specific unsupported flags."""
    ratio = normalize_aspect(aspect)
    body = re.sub(r"\baspect ratio\s*:\s*\d+:\d+\b[,]?", "", prompt or "", flags=re.I)
    body = re.sub(r"\s{2,}", " ", body).strip(" ,")
    model = target_model or TARGET_VIDEO_MODELS[0]
    notes = {
        "Veo": "Target Veo. Prioritize coherent physical motion, camera continuity, and stable subject identity across frames.",
        "Sora": "Target Sora. Describe the scene temporally with clear subject motion, camera behavior, and continuity.",
        "Runway": "Target Runway. Keep motion direction explicit, visually concise, and suitable for image-to-video or text-to-video generation.",
        "Kling": "Target Kling. Emphasize stable geometry, realistic movement, product or character consistency, and clear camera motion.",
        "General / ChatGPT / Gemini": "Use as a general video-generation instruction with explicit scene, motion, and continuity.",
    }
    return f"{body} Frame aspect ratio: {ratio}. {notes[model]}".strip()


CORRECTIONS = {
    "얼굴이 이상함": "Correction: natural facial anatomy, symmetric eyes, realistic skin structure, correct hands and fingers, no duplicated facial features.",
    "글자가 깨짐": "Correction: keep only intended copy; remove random characters; preserve accurate Hangul glyph structure, spacing, and legibility.",
    "너무 어두움": "Correction: raise key and fill exposure, preserve highlight detail, maintain readable midtones, avoid crushed blacks.",
    "제품이 달라짐": "Correction: preserve the exact product identity, silhouette, proportions, colors, materials, logo placement, and distinctive details.",
    "구도가 별로": "Correction: simplify the composition, strengthen one clear focal point, improve hierarchy and negative space, keep the subject immediately readable.",
    "더 고급스럽게": "Correction: refine materials, lighting, reflections, spacing, and art direction for a restrained premium commercial finish without visual clutter.",
}


def apply_prompt_correction(prompt: str, symptom: str) -> str:
    """Apply one symptom correction while preserving terminal model parameters."""
    addition = CORRECTIONS.get(symptom)
    if not addition:
        return prompt
    text = (prompt or "").strip()
    if addition in text:
        return text
    if "Positive prompt:\n" in text and "\n\nNegative prompt:" in text:
        positive, rest = text.split("\n\nNegative prompt:", 1)
        return f"{positive}\n{addition}\n\nNegative prompt:{rest}"
    param = re.search(r"\s(--ar\s+\d+:\d+.*)$", text)
    if param:
        return f"{text[:param.start()].rstrip()} {addition} {param.group(1)}"
    aspect = re.search(r"\s(Output aspect ratio:|Frame aspect ratio:)\s*\d+:\d+\.?", text, flags=re.I)
    if aspect:
        return f"{text[:aspect.start()].rstrip()} {addition}{text[aspect.start():]}"
    return f"{text} {addition}".strip()
