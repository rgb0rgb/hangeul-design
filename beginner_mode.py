from __future__ import annotations

from typing import Dict

import streamlit as st

DESTINATIONS = [
    "인스타그램 피드",
    "릴스 / 틱톡 / 유튜브 쇼츠",
    "유튜브 썸네일",
    "블로그 / 쇼핑몰 상세",
    "포스터 / 인쇄물",
    "웹 / 프레젠테이션",
]

VISUAL_GOALS = [
    "AI가 추천",
    "실제 사진처럼",
    "고급 광고처럼",
    "감성적으로",
    "강렬하게",
    "일러스트 / 캐릭터",
    "한글 문구 중심",
]


def recommend_settings(subject: str, destination: str, visual_goal: str) -> Dict[str, object]:
    """Infer a useful first-attempt configuration from three beginner answers."""
    s = (subject or "").strip().lower()

    result: Dict[str, object] = {
        "preset": "매출형",
        "work_mode": "SNS 홍보 (Social)",
        "image_style": "하이퍼리얼 제품사진",
        "lighting": "AI 자동",
        "camera": "AI 자동",
        "aspect": "1:1 (기본)",
        "prompt_engine": "빠른 모드",
        "pop3d": False,
        "count": 3,
    }

    if destination == "인스타그램 피드":
        result.update(work_mode="SNS 홍보 (Social)", aspect="4:5")
    elif destination == "릴스 / 틱톡 / 유튜브 쇼츠":
        result.update(preset="숏폼 바이럴", work_mode="숏폼 영상 (Short-form Video)", aspect="9:16")
    elif destination == "유튜브 썸네일":
        result.update(work_mode="썸네일 (Thumbnail)", aspect="16:9", image_style="강렬/임팩트")
    elif destination == "블로그 / 쇼핑몰 상세":
        result.update(preset="제품 상세형", work_mode="제품 상세컷 (Product Detail)", aspect="4:5")
    elif destination == "포스터 / 인쇄물":
        result.update(work_mode="포스터 (Poster)", aspect="3:2")
    elif destination == "웹 / 프레젠테이션":
        result.update(work_mode="브랜드 키비주얼 (Brand Key Visual)", aspect="16:9")

    if any(k in s for k in ("한글", "글자", "문구", "타이포", "간판")):
        result.update(preset="한글 디자인", work_mode="한글 타이포그래피 (Hangul Typography)", image_style="한글 모던 그래픽", prompt_engine="전문가 모드")
    elif any(k in s for k in ("캐릭터", "마스코트", "웹툰", "만화")):
        result.update(preset="캐릭터 IP형", work_mode="캐릭터/IP (Character IP)", image_style="친근/귀여움/치비 캐릭터", pop3d=True)
    elif any(k in s for k in ("인테리어", "공간", "매장", "카페 내부", "사무실")):
        result.update(work_mode="공간/인테리어 (Space)", image_style="프리미엄 미니멀")
    elif any(k in s for k in ("로고", "브랜드 로고")):
        result.update(work_mode="로고 (Logo)", image_style="프리미엄 미니멀", prompt_engine="전문가 모드")
    elif any(k in s for k in ("패키지", "포장", "박스", "용기")):
        result.update(work_mode="패키지 디자인 (Package)", image_style="브랜드 에디토리얼", prompt_engine="전문가 모드")

    if visual_goal == "실제 사진처럼":
        result.update(image_style="하이퍼리얼 제품사진", lighting="Studio")
    elif visual_goal == "고급 광고처럼":
        result.update(image_style="시네마틱 광고", lighting="Cinematic")
    elif visual_goal == "감성적으로":
        result.update(preset="감성형", image_style="프리미엄 미니멀", lighting="Natural")
    elif visual_goal == "강렬하게":
        result.update(preset="매출형", image_style="강렬/임팩트", lighting="Hard")
    elif visual_goal == "일러스트 / 캐릭터":
        result.update(work_mode="일러스트 (Art)", image_style="친근/귀여움/치비 캐릭터")
    elif visual_goal == "한글 문구 중심":
        result.update(preset="한글 디자인", work_mode="한글 타이포그래피 (Hangul Typography)", image_style="한글 모던 그래픽", prompt_engine="전문가 모드")

    return result


def apply_recommendation(settings: Dict[str, object], subject: str) -> None:
    for key, value in settings.items():
        st.session_state[key] = value
    st.session_state["subject"] = (subject or "").strip()
    if st.session_state.get("prompt_engine") == "전문가 모드" and not st.session_state.get("expert_subject"):
        st.session_state["expert_subject"] = (subject or "").strip()


def render_beginner_panel() -> None:
    # IMPORTANT: render this panel before base_app.render_sidebar(). The Apply button
    # writes widget-backed session-state keys; Streamlit forbids mutating those keys
    # after the corresponding sidebar widgets have already been instantiated.
    st.markdown("## 초보자 자동 설정")
    st.caption("세 가지만 답하면 작업 모드·스타일·화면비·조명 등을 먼저 추천합니다. 아래 세부 설정에서 언제든 바꿀 수 있습니다.")
    with st.container(border=True):
        subject = st.text_input(
            "1. 무엇을 만들거나 홍보하려고 하나요?",
            key="beginner_subject",
            placeholder="예: 햄치즈 베이글 신메뉴, 미용실 할인 행사, 한글 포스터",
        )
        c1, c2 = st.columns(2)
        with c1:
            destination = st.selectbox("2. 어디에 사용할 건가요?", DESTINATIONS, key="beginner_destination")
        with c2:
            visual_goal = st.selectbox("3. 어떤 느낌을 원하나요?", VISUAL_GOALS, key="beginner_visual_goal")
        if st.button("AI가 세부 설정 자동 결정", type="primary", use_container_width=True, key="beginner_apply"):
            if not (subject or "").strip():
                st.warning("무엇을 만들지 한 줄만 입력하세요.")
            else:
                settings = recommend_settings(subject, destination, visual_goal)
                apply_recommendation(settings, subject)
                st.success(f"자동 설정 완료 · {settings['work_mode']} · {settings['image_style']} · {settings['aspect']}")
