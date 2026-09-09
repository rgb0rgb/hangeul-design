import streamlit as st

import app as base_app
from reference_image import append_reference_to_prompt, render_reference_image_uploader


_original_build_prompts = base_app._build_prompts
_original_build_expert_prompt = base_app._build_expert_prompt


def _build_prompts_with_reference(*args, **kwargs):
    image_prompt, video_prompt, d3_prompt = _original_build_prompts(*args, **kwargs)
    return (
        append_reference_to_prompt(image_prompt),
        append_reference_to_prompt(video_prompt),
        append_reference_to_prompt(d3_prompt),
    )


def _build_expert_with_reference(*args, **kwargs):
    image_prompt, video_prompt, d3_prompt, blueprint = _original_build_expert_prompt(*args, **kwargs)
    directive_applied = append_reference_to_prompt("")
    if directive_applied:
        blueprint = blueprint + "\nReference image: attached reference is active; preserve/apply it according to the selected reference mode."
    return (
        append_reference_to_prompt(image_prompt),
        append_reference_to_prompt(video_prompt),
        append_reference_to_prompt(d3_prompt),
        blueprint,
    )


def install_reference_hooks():
    base_app._build_prompts = _build_prompts_with_reference
    base_app._build_expert_prompt = _build_expert_with_reference


def render_reference_panel():
    st.markdown("---")
    render_reference_image_uploader()
    st.caption("이미지를 첨부한 뒤 아래 Hangeul Design에서 기획안을 생성하면 이미지·영상·3D 프롬프트에 참조 이미지 제어문이 자동 적용됩니다.")


def main():
    install_reference_hooks()
    render_reference_panel()
    base_app.main()


if __name__ == "__main__":
    main()
