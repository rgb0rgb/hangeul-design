import hashlib
from typing import Dict

import streamlit as st

REFERENCE_TYPES = ["jpg", "jpeg", "png", "bmp", "webp", "gif", "tif", "tiff"]

REFERENCE_MODES: Dict[str, str] = {
    "원본 정체성 유지 (추천)": (
        "Use the uploaded reference image as the primary identity reference. Preserve the visible subject/product identity, "
        "silhouette, proportions, colors, materials, distinctive details, and intentional branding. Do not redesign or replace "
        "the referenced subject unless the prompt explicitly requests a change."
    ),
    "원본 최대 유지": (
        "Preserve the uploaded reference image as faithfully as possible. Keep the original subject identity, geometry, color, "
        "materials, styling, and recognizable details. Change only the scene, camera, lighting, motion, or explicitly requested elements."
    ),
    "구도/배치 참고": (
        "Use the uploaded reference image mainly as a composition and spatial-layout reference. Preserve the important placement, "
        "relative scale, viewing direction, and visual hierarchy while allowing styling and environment changes requested by the prompt."
    ),
    "스타일/분위기 참고": (
        "Use the uploaded reference image mainly as a visual-style reference for palette, lighting, texture, material feel, and atmosphere. "
        "Do not copy unrelated objects from the reference unless they are required by the prompt."
    ),
}


def render_reference_image_uploader() -> None:
    st.markdown("## 참조 이미지 첨부")
    st.caption(
        "JPG, JPEG, PNG, BMP, WEBP, GIF, TIF/TIFF 이미지를 첨부할 수 있습니다. "
        "첨부 이미지는 Hangeul Design과 Cinematic Product Video의 프롬프트에 공통 참조로 반영됩니다."
    )

    uploaded = st.file_uploader(
        "참조 이미지",
        type=REFERENCE_TYPES,
        accept_multiple_files=False,
        key="hd_reference_upload",
        help="제품, 인물, 패키지, 공간 등 원본으로 유지하거나 참고할 이미지를 첨부합니다.",
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        st.selectbox(
            "이미지 적용 방식",
            list(REFERENCE_MODES.keys()),
            key="hd_reference_mode",
        )
    with c2:
        st.text_input(
            "참조 이미지 추가 지시(선택)",
            key="hd_reference_note",
            placeholder="예: 제품 모양과 색상은 그대로 유지하고 배경만 변경",
        )

    if uploaded is None:
        st.session_state.pop("hd_reference_meta", None)
        return

    data = uploaded.getvalue()
    digest = hashlib.sha256(data).hexdigest()[:12]
    st.session_state["hd_reference_meta"] = {
        "name": uploaded.name,
        "mime": uploaded.type or "image",
        "size": len(data),
        "sha": digest,
    }

    st.image(data, caption=f"참조 이미지: {uploaded.name}", use_container_width=True)
    st.success("참조 이미지가 활성화되었습니다. 아래 두 생성 프로그램에 공통 적용됩니다.")


def has_reference_image() -> bool:
    return bool(st.session_state.get("hd_reference_meta"))


def reference_status_text() -> str:
    meta = st.session_state.get("hd_reference_meta") or {}
    if not meta:
        return "참조 이미지 없음"
    return f"참조 이미지 활성: {meta.get('name', 'image')}"


def get_reference_directive() -> str:
    meta = st.session_state.get("hd_reference_meta") or {}
    if not meta:
        return ""

    mode = st.session_state.get("hd_reference_mode", "원본 정체성 유지 (추천)")
    mode_rule = REFERENCE_MODES.get(mode, REFERENCE_MODES["원본 정체성 유지 (추천)"])
    note = (st.session_state.get("hd_reference_note") or "").strip()

    parts = [
        "REFERENCE IMAGE CONTROL:",
        "An uploaded reference image is attached to this generation request and must be used together with this prompt.",
        mode_rule,
        "Maintain physically plausible geometry, contact, reflections, shadows, and temporal identity consistency when the reference subject appears in video.",
    ]
    if note:
        parts.append(f"User reference instruction: {note}.")
    return " ".join(parts)


def append_reference_to_prompt(prompt: str) -> str:
    directive = get_reference_directive()
    if not directive:
        return prompt
    return f"{prompt} {directive}".strip()
