import streamlit as st

import app as base_app
import runtime_quality
from beginner_mode import render_beginner_panel
from prompt_compiler import TARGET_IMAGE_MODELS, TARGET_VIDEO_MODELS, compile_image_prompt, compile_video_prompt
from reference_image import append_reference_to_prompt, render_reference_image_uploader


runtime_quality.install(base_app)
_original_build_prompts = base_app._build_prompts
_original_build_expert_prompt = base_app._build_expert_prompt


def _allow_hangul_text() -> bool:
    return "한글 타이포그래피" in st.session_state.get("work_mode", "") or bool((st.session_state.get("hangul_text", "") or "").strip())


def _compile_image(image_prompt: str) -> str:
    return compile_image_prompt(
        image_prompt,
        target_model=st.session_state.get("target_image_model", TARGET_IMAGE_MODELS[0]),
        aspect=st.session_state.get("aspect", "1:1"),
        allow_text=_allow_hangul_text(),
        hangul_text=st.session_state.get("hangul_text", ""),
    )


def _compile_video(video_prompt: str) -> str:
    return compile_video_prompt(
        video_prompt,
        target_model=st.session_state.get("target_video_model", TARGET_VIDEO_MODELS[0]),
        aspect=st.session_state.get("aspect", "1:1"),
    )


def _build_prompts_with_reference(*args, **kwargs):
    image_prompt, video_prompt, d3_prompt = _original_build_prompts(*args, **kwargs)
    # Compile before appending reference directives so negative extraction cannot
    # depend on whether a reference image is active.
    return append_reference_to_prompt(_compile_image(image_prompt)), append_reference_to_prompt(_compile_video(video_prompt)), append_reference_to_prompt(d3_prompt)


def _build_expert_with_reference(*args, **kwargs):
    image_prompt, video_prompt, d3_prompt, blueprint = _original_build_expert_prompt(*args, **kwargs)
    directive_applied = append_reference_to_prompt("")
    if directive_applied:
        blueprint += "\nReference image: attached reference is active; preserve/apply it according to the selected reference mode."
    return append_reference_to_prompt(_compile_image(image_prompt)), append_reference_to_prompt(_compile_video(video_prompt)), append_reference_to_prompt(d3_prompt), blueprint


def install_reference_hooks():
    base_app._build_prompts = _build_prompts_with_reference
    base_app._build_expert_prompt = _build_expert_with_reference


def render_generator_panel():
    st.markdown("## 생성 AI 설정")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("이미지 생성 AI", TARGET_IMAGE_MODELS, key="target_image_model")
    with c2:
        st.selectbox("영상 생성 AI", TARGET_VIDEO_MODELS, key="target_video_model")
    with c3:
        st.selectbox("화면비", base_app.ASPECT_OPTIONS, key="aspect")
    st.caption("이미지·영상 프롬프트를 선택한 생성 AI와 화면비에 맞게 자동 변환합니다.")
    if _allow_hangul_text():
        st.warning("한글 글자는 생성 모델에 따라 깨질 수 있습니다. 정확한 문구가 중요하면 글자 없는 배경/제품 이미지를 먼저 만든 뒤 Canva·미리캔버스 등에서 정확한 한글을 얹는 방법이 가장 안정적입니다.")


def render_reference_panel():
    st.markdown("---")
    render_reference_image_uploader()
    st.caption("참조 이미지를 사용했다면 생성 AI에서도 이 프롬프트와 같은 이미지를 함께 첨부하세요.")


def main():
    base_app._ss_init()
    runtime_quality.apply_pending_favorite(base_app)
    runtime_quality.reset_variant_counter()
    install_reference_hooks()
    runtime_quality.render_theme_fix()
    render_beginner_panel()
    render_generator_panel()
    render_reference_panel()
    base_app.render_sidebar()
    base_app.render_main()


if __name__ == "__main__":
    main()
