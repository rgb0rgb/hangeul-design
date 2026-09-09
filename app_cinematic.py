import streamlit as st

import app as base_app
import runtime_quality
from beginner_mode import render_beginner_panel
from cinematic_product import (
    CAMERA_MOVE_OPTIONS, HUMAN_PRESENCE_OPTIONS, INTERACTION_OPTIONS, LENS_OPTIONS,
    LIGHTING_OPTIONS as CINEMATIC_LIGHTING_OPTIONS, LOOK_OPTIONS, MODEL_OPTIONS,
    SHOT_OPTIONS, build_cinematic_product_prompt, build_product_plus_human_variant,
)
from prompt_compiler import TARGET_IMAGE_MODELS, TARGET_VIDEO_MODELS, compile_image_prompt, compile_video_prompt
from reference_image import append_reference_to_prompt, has_reference_image, reference_status_text, render_reference_image_uploader

runtime_quality.install(base_app)
_original_build_prompts = base_app._build_prompts
_original_build_expert_prompt = base_app._build_expert_prompt


def _allow_hangul_text() -> bool:
    return "한글 타이포그래피" in st.session_state.get("work_mode", "") or bool((st.session_state.get("hangul_text", "") or "").strip())


def _compile_image(prompt: str) -> str:
    return compile_image_prompt(
        prompt,
        st.session_state.get("target_image_model", TARGET_IMAGE_MODELS[0]),
        st.session_state.get("aspect", "1:1"),
        _allow_hangul_text(),
        st.session_state.get("hangul_text", ""),
    )


def _compile_video(prompt: str) -> str:
    return compile_video_prompt(
        prompt,
        st.session_state.get("target_video_model", TARGET_VIDEO_MODELS[0]),
        st.session_state.get("aspect", "1:1"),
    )


def _build_prompts_with_reference(*args, **kwargs):
    image_prompt, video_prompt, d3_prompt = _original_build_prompts(*args, **kwargs)
    return (
        append_reference_to_prompt(_compile_image(image_prompt)),
        append_reference_to_prompt(_compile_video(video_prompt)),
        append_reference_to_prompt(d3_prompt),
    )


def _build_expert_with_reference(*args, **kwargs):
    image_prompt, video_prompt, d3_prompt, blueprint = _original_build_expert_prompt(*args, **kwargs)
    if has_reference_image():
        blueprint += "\nReference image: attached reference is active; preserve/apply it according to the selected reference mode."
    return (
        append_reference_to_prompt(_compile_image(image_prompt)),
        append_reference_to_prompt(_compile_video(video_prompt)),
        append_reference_to_prompt(d3_prompt),
        blueprint,
    )


def _install_reference_hooks():
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
    if _allow_hangul_text():
        st.warning("한글 글자는 생성 모델에 따라 깨질 수 있습니다. 정확한 문구가 중요하면 글자 없는 이미지를 먼저 생성한 뒤 Canva·미리캔버스 등에서 한글을 얹는 방법이 가장 안정적입니다.")


def _translate(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    translated, ok = base_app.translate_google(text, src="auto", dst="en")
    return translated if ok else text


def render_cinematic_product_video():
    st.markdown("## 시네마틱 디자인")
    st.caption("쇼트·렌즈·카메라 이동·조명·사람의 제품 사용까지 조합한 전문 광고 영상 프롬프트를 만듭니다.")
    if has_reference_image():
        st.info(reference_status_text() + " · 생성 AI에서도 같은 참조 이미지를 프롬프트와 함께 첨부하세요.")

    with st.expander("촬영 옵션 설정", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            product_kr = st.text_input("제품 / Product", key="cin_product", placeholder="예: 검은색 프리미엄 스마트워치")
            environment_kr = st.text_input("배경 / Environment", key="cin_environment", placeholder="예: 현대적인 건축 공간, 따뜻한 저녁 조명")
            shot = st.selectbox("Shot / 쇼트", list(SHOT_OPTIONS.keys()), key="cin_shot")
            camera_move = st.selectbox("Camera Movement / 카메라 이동", list(CAMERA_MOVE_OPTIONS.keys()), key="cin_camera_move")
            lens = st.selectbox("Lens / 렌즈", list(LENS_OPTIONS.keys()), key="cin_lens")
        with c2:
            lighting = st.selectbox("Lighting / 조명", list(CINEMATIC_LIGHTING_OPTIONS.keys()), key="cin_lighting")
            look = st.selectbox("Look / 광고 룩", list(LOOK_OPTIONS.keys()), key="cin_look")
            human = st.selectbox("Human Presence / 사람 등장", list(HUMAN_PRESENCE_OPTIONS.keys()), key="cin_human")
            interaction = st.selectbox("Human Interaction / 제품과 사람의 행동", list(INTERACTION_OPTIONS.keys()), key="cin_interaction")
            model = st.selectbox("Target Model / 대상 모델", MODEL_OPTIONS, key="cin_model")
            duration = st.slider("Duration / 길이(초)", 4, 15, 8, key="cin_duration")
        use_main_brand = st.checkbox("한글 디자인의 브랜드명 사용", value=True, key="cin_use_brand")
        custom_brand = st.text_input("별도 브랜드명(옵션)", key="cin_brand_custom", placeholder="비워두면 한글 디자인 브랜드 설정 사용")

    generate = st.button("시네마틱 제품 영상 프롬프트 생성", type="primary", use_container_width=True)
    if generate:
        if not (product_kr or "").strip() and not has_reference_image():
            st.warning("제품을 입력하거나 참조 이미지를 첨부하세요.")
            return
        product_en = _translate(product_kr) if (product_kr or "").strip() else "the primary product shown in the uploaded reference image"
        environment_en = _translate(environment_kr)
        brand = (custom_brand or "").strip()
        if not brand and use_main_brand:
            brand = (st.session_state.get("brand") or "").strip()
        main_prompt = build_cinematic_product_prompt(
            product=product_en, environment=environment_en, shot=shot, camera_move=camera_move,
            lens=lens, lighting=lighting, look=look, human_presence=human, interaction=interaction,
            model=model, duration=duration, brand=brand,
        )
        human_variant = build_product_plus_human_variant(
            product=product_en, environment=environment_en,
            shot=shot if human != "없음 (Product Only)" else "오버숄더 (Over-the-Shoulder)",
            camera_move=camera_move, lens=lens, lighting=lighting, look=look,
            interaction=interaction, model=model, duration=duration, brand=brand,
        )
        st.session_state["cin_last_main"] = append_reference_to_prompt(main_prompt)
        st.session_state["cin_last_human"] = append_reference_to_prompt(human_variant)
        st.session_state["cin_product_en"] = product_en

    if st.session_state.get("cin_last_main"):
        st.markdown(f"**Product EN:** {st.session_state.get('cin_product_en', '')}")
        t1, t2 = st.tabs(["선택 설정 프롬프트", "제품 + 사람 자동 버전"])
        with t1:
            st.code(st.session_state["cin_last_main"], language="text")
            base_app._clipboard_button("복사", st.session_state["cin_last_main"], key="copy_cinematic_main")
        with t2:
            st.code(st.session_state["cin_last_human"], language="text")
            base_app._clipboard_button("복사", st.session_state["cin_last_human"], key="copy_cinematic_human")
        st.download_button(
            "두 프롬프트 TXT 저장",
            data=("[CINEMATIC PRODUCT VIDEO]\n" + st.session_state["cin_last_main"] + "\n\n[PRODUCT + HUMAN VARIANT]\n" + st.session_state["cin_last_human"]).encode("utf-8"),
            file_name="HangeulDesign_CinematicProductVideo.txt",
            mime="text/plain",
            use_container_width=True,
        )


def main():
    base_app._ss_init()
    runtime_quality.apply_pending_favorite(base_app)
    runtime_quality.reset_variant_counter()
    _install_reference_hooks()
    runtime_quality.render_theme_fix()

    # Shared controls stay in one sidebar while the two products switch from the top tabs.
    base_app.render_sidebar()
    with st.sidebar.expander("참조 이미지", expanded=False):
        render_reference_image_uploader()
        st.caption("참조 이미지를 사용했다면 실제 생성 AI에서도 같은 이미지를 프롬프트와 함께 첨부하세요.")

    tab_hangeul, tab_cinematic = st.tabs(["한글 디자인", "시네마틱 디자인"])

    with tab_hangeul:
        render_beginner_panel()
        render_generator_panel()
        base_app.render_main()

    with tab_cinematic:
        render_cinematic_product_video()


if __name__ == "__main__":
    main()
