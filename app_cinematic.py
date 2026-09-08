import streamlit as st

import app as base_app
from cinematic_product import (
    CAMERA_MOVE_OPTIONS,
    HUMAN_PRESENCE_OPTIONS,
    INTERACTION_OPTIONS,
    LENS_OPTIONS,
    LIGHTING_OPTIONS as CINEMATIC_LIGHTING_OPTIONS,
    LOOK_OPTIONS,
    MODEL_OPTIONS,
    SHOT_OPTIONS,
    build_cinematic_product_prompt,
    build_product_plus_human_variant,
)


def _translate(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    translated, ok = base_app.translate_google(text, src="auto", dst="en")
    return translated if ok else text


def render_cinematic_product_video():
    st.markdown("---")
    st.markdown("## Cinematic Product Video (시네마틱 제품 영상)")
    st.caption(
        "제품을 단순히 움직이는 프롬프트가 아니라, 쇼트·렌즈·카메라 이동·조명·사람의 제품 사용까지 조합한 광고 영상 프롬프트를 만듭니다."
    )

    with st.expander("촬영 옵션 설정", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            product_kr = st.text_input(
                "제품 / Product",
                key="cin_product",
                placeholder="예: 검은색 프리미엄 스마트워치",
            )
            environment_kr = st.text_input(
                "배경 / Environment",
                key="cin_environment",
                placeholder="예: 현대적인 건축 공간, 따뜻한 저녁 조명",
            )
            shot = st.selectbox("Shot / 쇼트", list(SHOT_OPTIONS.keys()), key="cin_shot")
            camera_move = st.selectbox(
                "Camera Movement / 카메라 이동",
                list(CAMERA_MOVE_OPTIONS.keys()),
                key="cin_camera_move",
            )
            lens = st.selectbox("Lens / 렌즈", list(LENS_OPTIONS.keys()), key="cin_lens")
        with c2:
            lighting = st.selectbox(
                "Lighting / 조명",
                list(CINEMATIC_LIGHTING_OPTIONS.keys()),
                key="cin_lighting",
            )
            look = st.selectbox("Look / 광고 룩", list(LOOK_OPTIONS.keys()), key="cin_look")
            human = st.selectbox(
                "Human Presence / 사람 등장",
                list(HUMAN_PRESENCE_OPTIONS.keys()),
                key="cin_human",
            )
            interaction = st.selectbox(
                "Human Interaction / 제품과 사람의 행동",
                list(INTERACTION_OPTIONS.keys()),
                key="cin_interaction",
            )
            model = st.selectbox("Target Model / 대상 모델", MODEL_OPTIONS, key="cin_model")
            duration = st.slider("Duration / 길이(초)", 4, 15, 8, key="cin_duration")

        use_main_brand = st.checkbox("기존 Hangeul Design 브랜드명 사용", value=True, key="cin_use_brand")
        custom_brand = st.text_input(
            "별도 브랜드명(옵션)",
            key="cin_brand_custom",
            placeholder="비워두면 기존 브랜드 설정 사용",
        )

    generate = st.button("시네마틱 제품 영상 프롬프트 생성", type="primary", use_container_width=True)

    if generate:
        if not (product_kr or "").strip():
            st.warning("제품을 입력하세요.")
            return

        product_en = _translate(product_kr)
        environment_en = _translate(environment_kr)
        brand = (custom_brand or "").strip()
        if not brand and use_main_brand:
            brand = (st.session_state.get("brand") or "").strip()

        main_prompt = build_cinematic_product_prompt(
            product=product_en,
            environment=environment_en,
            shot=shot,
            camera_move=camera_move,
            lens=lens,
            lighting=lighting,
            look=look,
            human_presence=human,
            interaction=interaction,
            model=model,
            duration=duration,
            brand=brand,
        )
        human_variant = build_product_plus_human_variant(
            product=product_en,
            environment=environment_en,
            shot=shot if human != "없음 (Product Only)" else "오버숄더 (Over-the-Shoulder)",
            camera_move=camera_move,
            lens=lens,
            lighting=lighting,
            look=look,
            interaction=interaction,
            model=model,
            duration=duration,
            brand=brand,
        )

        st.session_state["cin_last_main"] = main_prompt
        st.session_state["cin_last_human"] = human_variant
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
            data=(
                "[CINEMATIC PRODUCT VIDEO]\n"
                + st.session_state["cin_last_main"]
                + "\n\n[PRODUCT + HUMAN VARIANT]\n"
                + st.session_state["cin_last_human"]
            ).encode("utf-8"),
            file_name="HangeulDesign_CinematicProductVideo.txt",
            mime="text/plain",
            use_container_width=True,
        )


def main():
    base_app.main()
    render_cinematic_product_video()


if __name__ == "__main__":
    main()
