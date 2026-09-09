import streamlit as st

import app as base_app
import runtime_quality
from prompt_compiler import TARGET_IMAGE_MODELS, compile_image_prompt
from reference_image import append_reference_to_prompt, render_reference_image_uploader


runtime_quality.install(base_app)
_original_build_prompts = base_app._build_prompts
_original_build_expert_prompt = base_app._build_expert_prompt


def _compile_image(image_prompt: str) -> str:
    work_mode = st.session_state.get("work_mode", "")
    hangul_text = st.session_state.get("hangul_text", "")
    allow_text = "한글 타이포그래피" in work_mode or bool((hangul_text or "").strip())
    return compile_image_prompt(
        image_prompt,
        target_model=st.session_state.get("target_image_model", TARGET_IMAGE_MODELS[0]),
        aspect=st.session_state.get("aspect", "1:1"),
        allow_text=allow_text,
        hangul_text=hangul_text,
    )


def _build_prompts_with_reference(*args, **kwargs):
    image_prompt, video_prompt, d3_prompt = _original_build_prompts(*args, **kwargs)
    image_prompt = append_reference_to_prompt(image_prompt)
    return _compile_image(image_prompt), append_reference_to_prompt(video_prompt), append_reference_to_prompt(d3_prompt)


def _build_expert_with_reference(*args, **kwargs):
    image_prompt, video_prompt, d3_prompt, blueprint = _original_build_expert_prompt(*args, **kwargs)
    directive_applied = append_reference_to_prompt("")
    if directive_applied:
        blueprint += "\nReference image: attached reference is active; preserve/apply it according to the selected reference mode."
    image_prompt = append_reference_to_prompt(image_prompt)
    return _compile_image(image_prompt), append_reference_to_prompt(video_prompt), append_reference_to_prompt(d3_prompt), blueprint


def install_reference_hooks():
    base_app._build_prompts = _build_prompts_with_reference
    base_app._build_expert_prompt = _build_expert_with_reference


def render_target_model_panel():
    st.markdown("## 1. 사용할 이미지 AI 선택")
    st.selectbox(
        "대상 이미지 생성 도구",
        TARGET_IMAGE_MODELS,
        key="target_image_model",
        help="선택한 도구에 맞게 화면비와 네거티브 프롬프트 형식을 자동 변환합니다.",
    )
    st.caption("같은 기획 내용이라도 Midjourney, Stable Diffusion/FLUX, ChatGPT/Gemini에 맞는 형식으로 자동 변환됩니다.")


def render_reference_panel():
    st.markdown("---")
    render_reference_image_uploader()
    st.caption("이미지를 첨부한 뒤 아래 Hangeul Design에서 기획안을 생성하면 이미지·영상·3D 프롬프트에 참조 이미지 제어문이 자동 적용됩니다.")


def main():
    base_app._ss_init()
    runtime_quality.apply_pending_favorite(base_app)
    runtime_quality.reset_variant_counter()
    install_reference_hooks()
    runtime_quality.render_theme_fix()
    render_target_model_panel()
    render_reference_panel()
    base_app.render_sidebar()
    base_app.render_main()


if __name__ == "__main__":
    main()
