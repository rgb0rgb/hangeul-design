from __future__ import annotations

import streamlit as st

from prompt_compiler import apply_prompt_correction

SYMPTOMS = {
    "얼굴/손이 이상해요": "얼굴이 이상함",
    "한글/글자가 깨져요": "글자가 깨짐",
    "너무 어두워요": "너무 어두움",
    "제품이 원본과 달라요": "제품이 달라짐",
    "구도가 별로예요": "구도가 별로",
    "더 고급스럽게": "더 고급스럽게",
}

MESSAGE_KEY = "_hd_result_correction_message"


def _selected_plan():
    plans = st.session_state.get("plans") or []
    if not plans:
        return None
    selected_uid = st.session_state.get("selected_uid")
    if selected_uid:
        for plan in plans:
            if plan.get("uid") == selected_uid:
                return plan
    return plans[0]


def _render_pending_message() -> None:
    message = st.session_state.pop(MESSAGE_KEY, None)
    if not message:
        return
    level, text = message
    if level == "success":
        st.success(text)
    else:
        st.info(text)


def render_result_assistant() -> None:
    plan = _selected_plan()
    if not plan:
        return

    st.markdown("### 결과가 마음에 들지 않나요?")
    st.caption("문제를 고르면 현재 선택된 결과 프롬프트에 필요한 보정 지시를 자동으로 추가합니다.")
    _render_pending_message()
    symptom_label = st.selectbox("어떤 문제가 있나요?", list(SYMPTOMS.keys()), key="result_symptom")

    if st.button("보정 적용", use_container_width=True, key="apply_result_correction"):
        symptom = SYMPTOMS[symptom_label]
        before = plan.get("image_prompt", "")
        corrected_image = apply_prompt_correction(before, symptom)

        if corrected_image == before:
            st.info("이 보정은 이미 현재 프롬프트에 적용되어 있습니다.")
            return

        plan["image_prompt"] = corrected_image
        if symptom != "글자가 깨짐" and plan.get("video_prompt"):
            plan["video_prompt"] = apply_prompt_correction(plan["video_prompt"], symptom)
        plan["last_correction"] = symptom_label
        st.session_state[MESSAGE_KEY] = ("success", f"보정 적용 완료 · {symptom_label}")

        # render_main() appears before this assistant in the page. Rerun so the
        # corrected prompt and its copy control are rebuilt immediately from the
        # updated plan instead of remaining one interaction behind.
        st.rerun()
