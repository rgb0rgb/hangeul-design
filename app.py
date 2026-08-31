# app.py - Hangeul Design (Streamlit UI, no license) - v1.0
# Added:
# - Favorites/Templates (save/reuse in 1 click) persisted to local JSON
# - Prompt Intensity slider (Conservative <-> Creative) controls variation
# - Online translation via Google (unofficial endpoint). Fallback if fails.
# - Expert prompt engine inspired by measured prompt-structure practices:
#   subject spine, identity/detail anchors, scene layers, lighting, palette, camera, and negative controls.

import os
import json
import time
import uuid
import random
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Tuple

import streamlit as st
import streamlit.components.v1 as components

APP_NAME = "Hangeul Design"
APP_PORT = "8504"

st.set_page_config(page_title=APP_NAME, layout="wide")

CSS = """
<style>
.block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; }
.sidebar-h { font-size: 0.95rem; font-weight: 700; margin: 0.75rem 0 0.25rem 0; }
.dp-card {
  border: 1px solid rgba(49, 51, 63, 0.15);
  border-radius: 18px;
  padding: 16px;
  background: white;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.dp-tip { color: rgba(37, 99, 235, 0.95); font-size: 0.9rem; }
.dp-chip {
  display:inline-block; padding: 2px 10px; border-radius: 999px;
  border: 1px solid rgba(49, 51, 63, 0.15); font-size: 0.75rem; margin-left: 8px;
}
.dp-hr { border: 0; height: 1px; background: rgba(49, 51, 63, 0.12); margin: 12px 0; }
.dp-footer {
  margin-top: 24px;
  padding-top: 10px;
  border-top: 1px solid rgba(49,51,63,0.12);
  color: rgba(49,51,63,0.6);
  font-size: 0.85rem;
  text-align: center;
}
.small-muted { color: rgba(49,51,63,0.65); font-size: 0.82rem; }
section[data-testid="stSidebar"] div[data-testid="stPopover"] button {
  min-width: 54px;
  white-space: nowrap;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PRESETS = [
    "한글 디자인",
    "매출형",
    "감성형",
    "트렌드",
    "브랜드 일관성",
    "숏폼 바이럴",
    "시네마 영상형",
    "제품 상세형",
    "캐릭터 IP형",
    "화보 전문가형",
]

WORK_MODES = [
    "제품 (Product)",
    "제품 상세컷 (Product Detail)",
    "SNS 홍보 (Social)",
    "숏폼 영상 (Short-form Video)",
    "광고 캠페인 (Ad Campaign)",
    "로고 (Logo)",
    "브랜드 키비주얼 (Brand Key Visual)",
    "패키지 디자인 (Package)",
    "캐릭터/IP (Character IP)",
    "AI 모델/착장 (AI Model)",
    "공간/인테리어 (Space)",
    "일러스트 (Art)",
    "포스터 (Poster)",
    "썸네일 (Thumbnail)",
    "영상 콘티 (Storyboard)",
    "한글 타이포그래피 (Hangul Typography)",
    "화보 세트 (Editorial Set)",
]

STYLE_OPTIONS = [
    "프리미엄 미니멀",
    "고급/프리미엄",
    "강렬/임팩트",
    "하이퍼리얼 제품사진",
    "시네마틱 광고",
    "브랜드 에디토리얼",
    "AI 인플루언서 룩북",
    "퓨처 럭셔리",
    "클레이/토이 3D",
    "픽사풍 3D 캐릭터",
    "레트로 퓨처리즘",
    "키네틱 타이포 배경",
    "패션 매거진",
    "K-뷰티 글로우",
    "테크웨어 사이버",
    "네온 누아르",
    "한글 모던 그래픽",
    "전통 한글 포스터",
    "K-에디토리얼 화보",
    "생활 스냅 화보",
    "친근/귀여움/치비 캐릭터",
    "한국민화 웹툰",
    "스티커 사진",
    "드라미틱 레트로 애니",
    "아이소메트릭 3D",
    "직접입력",
]

LIGHTING_OPTIONS = ["AI 자동", "Hard", "Soft", "Neon", "Studio", "Natural", "Golden Hour", "Cinematic", "Beauty Softbox"]
CAMERA_OPTIONS = ["AI 자동", "정면", "탑뷰", "로우앵글", "와이드", "클로즈업", "매크로", "핸드헬드", "드론샷"]
ASPECT_OPTIONS = ["1:1 (기본)", "16:9", "9:16", "4:5", "3:2", "21:9"]
LANG_OPTIONS = ["English"]

PRESET_DEFAULTS = {
    "한글 디자인": dict(work_mode="한글 타이포그래피 (Hangul Typography)", style="한글 모던 그래픽", pop3d=False),
    "매출형": dict(work_mode="제품 (Product)", style="강렬/임팩트", pop3d=False),
    "감성형": dict(work_mode="SNS 홍보 (Social)", style="프리미엄 미니멀", pop3d=False),
    "트렌드": dict(work_mode="SNS 홍보 (Social)", style="드라미틱 레트로 애니", pop3d=True),
    "브랜드 일관성": dict(work_mode="브랜드 키비주얼 (Brand Key Visual)", style="브랜드 에디토리얼", pop3d=False),
    "숏폼 바이럴": dict(work_mode="숏폼 영상 (Short-form Video)", style="키네틱 타이포 배경", pop3d=True),
    "시네마 영상형": dict(work_mode="영상 콘티 (Storyboard)", style="시네마틱 광고", pop3d=False),
    "제품 상세형": dict(work_mode="제품 상세컷 (Product Detail)", style="하이퍼리얼 제품사진", pop3d=False),
    "캐릭터 IP형": dict(work_mode="캐릭터/IP (Character IP)", style="픽사풍 3D 캐릭터", pop3d=True),
    "화보 전문가형": dict(work_mode="화보 세트 (Editorial Set)", style="K-에디토리얼 화보", pop3d=False),
}

STYLE_PHRASE = {
    "프리미엄 미니멀": "premium minimal, clean composition, refined high-end look, elegant negative space",
    "고급/프리미엄": "luxury, premium look, high-end finish, refined details, sophisticated aesthetic",
    "강렬/임팩트": "bold visual style, strong contrast, impactful composition",
    "하이퍼리얼 제품사진": "hyper-real product photography, physically plausible materials, accurate reflections, premium studio setup",
    "시네마틱 광고": "cinematic commercial look, anamorphic feel, controlled contrast, premium campaign lighting",
    "브랜드 에디토리얼": "brand editorial visual system, consistent color language, refined layout thinking, campaign-ready art direction",
    "AI 인플루언서 룩북": "AI influencer lookbook, natural posing, fashion campaign framing, realistic skin and fabric detail",
    "퓨처 럭셔리": "future luxury, sleek materials, subtle metallic accents, advanced premium design language",
    "클레이/토이 3D": "clay toy 3D, tactile handmade texture, soft rounded forms, playful collectible look",
    "픽사풍 3D 캐릭터": "stylized 3D animated character, expressive face, appealing proportions, cinematic family-friendly lighting",
    "레트로 퓨처리즘": "retro futurism, analog sci-fi mood, chrome details, nostalgic future palette",
    "키네틱 타이포 배경": "kinetic typography background without readable text, motion-graphic energy, bold shapes, rhythmic layout",
    "패션 매거진": "fashion magazine editorial, high-end styling, elegant pose direction, glossy print aesthetic",
    "K-뷰티 글로우": "K-beauty glow, luminous skin-safe lighting, soft highlights, clean cosmetic advertising aesthetic",
    "테크웨어 사이버": "techwear cyber aesthetic, functional details, dark utility fabrics, futuristic urban styling",
    "네온 누아르": "neon noir, cinematic night lighting, wet reflections, dramatic atmosphere",
    "한글 모던 그래픽": "modern Hangul graphic design, Korean letterform-led composition, clean grid, refined spacing",
    "전통 한글 포스터": "traditional Korean Hangul poster, calligraphic rhythm, hanji texture, contemporary museum-grade layout",
    "K-에디토리얼 화보": "K-editorial fashion photography, refined Korean commercial art direction, polished styling, realistic detail",
    "생활 스냅 화보": "everyday editorial snapshot, lived-in Korean scene, natural candid mood, rich small details",
    "친근/귀여움/치비 캐릭터": "friendly cute chibi character style, rounded shapes, charming expression",
    "한국민화 웹툰": "Korean minhwa-inspired webtoon style, traditional motifs, modern line art",
    "스티커 사진": "sticker-photo look, cutout edges, playful layout, glossy finish",
    "드라미틱 레트로 애니": "dramatic retro anime, 80s-90s vibe, bold shading, nostalgic color palette",
    "아이소메트릭 3D": "isometric 3D, clean geometry, soft ambient occlusion, crisp edges",
}

WORKMODE_PHRASE = {
    "제품 (Product)": "product hero shot",
    "제품 상세컷 (Product Detail)": "product macro detail shot, texture and material emphasis",
    "SNS 홍보 (Social)": "social media promo creative",
    "숏폼 영상 (Short-form Video)": "short-form vertical video concept, hook-first composition",
    "광고 캠페인 (Ad Campaign)": "integrated advertising campaign key visual",
    "로고 (Logo)": "logo concept",
    "브랜드 키비주얼 (Brand Key Visual)": "brand key visual system",
    "패키지 디자인 (Package)": "package design concept and product packaging visual",
    "캐릭터/IP (Character IP)": "character IP concept sheet",
    "AI 모델/착장 (AI Model)": "AI model fashion and styling shot",
    "공간/인테리어 (Space)": "spatial design and interior visualization",
    "일러스트 (Art)": "illustration artwork",
    "포스터 (Poster)": "poster design",
    "썸네일 (Thumbnail)": "thumbnail design",
    "영상 콘티 (Storyboard)": "cinematic storyboard frame",
    "한글 타이포그래피 (Hangul Typography)": "Hangul typography-led design concept",
    "화보 세트 (Editorial Set)": "editorial image set concept with consistent subject and styling",
}

PRESET_PHRASE = {
    "한글 디자인": "Hangul-first design, Korean visual identity, readable letterform priority, balanced modern layout",
    "매출형": "conversion-focused framing, product clarity, strong focal point, buyer psychology oriented",
    "감성형": "emotional tone, gentle atmosphere, warm storytelling, trust-building mood",
    "트렌드": "trend-forward aesthetics, bold art direction, modern palette, shareable hook",
    "브랜드 일관성": "brand consistency first, reusable campaign system, coherent colors, repeatable visual grammar",
    "숏폼 바이럴": "first-second hook, scroll-stopping composition, punchy visual rhythm, platform-native vertical framing",
    "시네마 영상형": "cinematic sequencing, clear shot direction, premium filmic mood, motion-ready composition",
    "제품 상세형": "material accuracy, tactile close-up detail, clean product information hierarchy, premium e-commerce usability",
    "캐릭터 IP형": "character consistency, memorable silhouette, expression sheet thinking, merchandise-ready appeal",
    "화보 전문가형": "expert editorial prompt structure, strong subject identity, wardrobe detail, scene specificity, camera realism",
}

PRESET_TAGS = {
    "매출형": "Sales",
    "감성형": "Mood",
    "트렌드": "Trend",
    "브랜드 일관성": "Brand",
    "숏폼 바이럴": "Viral",
    "시네마 영상형": "Cinema",
    "제품 상세형": "Detail",
    "캐릭터 IP형": "IP",
    "한글 디자인": "Hangul",
    "화보 전문가형": "Expert",
}

VIDEO_MOTION_PHRASE = {
    "제품 (Product)": "slow push-in, controlled product reveal, subtle turntable motion",
    "제품 상세컷 (Product Detail)": "macro glide, rack focus, material highlight sweep",
    "SNS 홍보 (Social)": "fast clean cuts, energetic reveal, social-first pacing",
    "숏폼 영상 (Short-form Video)": "0.5-second hook, snap zoom, match cuts, loopable ending",
    "광고 캠페인 (Ad Campaign)": "premium campaign pacing, hero reveal, smooth transition beats",
    "로고 (Logo)": "minimal logo reveal motion without readable text artifacts",
    "브랜드 키비주얼 (Brand Key Visual)": "parallax brand scene, gentle camera drift, reusable campaign motion",
    "패키지 디자인 (Package)": "package rotation, label-safe reveal, shelf-impact framing",
    "캐릭터/IP (Character IP)": "character idle motion, expressive gesture, clean silhouette reveal",
    "AI 모델/착장 (AI Model)": "runway walk beat, natural pose shift, fabric motion",
    "공간/인테리어 (Space)": "slow dolly through space, depth reveal, natural light movement",
    "일러스트 (Art)": "layered parallax, brush texture reveal, subtle atmospheric motion",
    "포스터 (Poster)": "poster-to-motion transition, depth separation, graphic reveal",
    "썸네일 (Thumbnail)": "fast focal punch-in, attention-grabbing reveal, clear subject hold",
    "영상 콘티 (Storyboard)": "shot-by-shot cinematic motion, clear camera direction, continuity-ready staging",
    "한글 타이포그래피 (Hangul Typography)": "subtle kinetic layout reveal, letterform depth, clean graphic motion",
    "화보 세트 (Editorial Set)": "editorial camera rhythm, consistent model identity, pose variation, smooth set continuity",
}

QUALITY_PHRASE = (
    "2026-generation ready, reference-friendly structure, coherent subject identity, "
    "consistent materials, controlled artifacts, high fidelity"
)

NEGATIVE_IMAGE_PHRASE = (
    "exclude text, watermark, letters, broken typography, signature, deformed hands, duplicate limbs, "
    "distorted face, low resolution, muddy details, random logos"
)

EXPERT_NEGATIVE_PHRASE = (
    "avoid generic stock-photo look, plastic skin, incoherent anatomy, unreadable random text, "
    "extra fingers, duplicated faces, warped product edges, over-smoothed texture, watermark"
)

DEFAULT_PALETTES = [
    ("ink black", "#111111"),
    ("warm ivory", "#F4EDE0"),
    ("porcelain white", "#FAFAF7"),
    ("deep jade", "#0E5B4F"),
    ("hanbok red", "#B8202E"),
    ("soft sky blue", "#9EC7D8"),
    ("brushed gold", "#B9975B"),
    ("charcoal gray", "#33363A"),
]

APP_GUIDE = {
    "개요": "왼쪽 메뉴에서 프리셋, 엔진, 작업 모드, 스타일을 고른 뒤 중앙의 주제 입력창에 만들고 싶은 내용을 적습니다. 결과는 구조, 이미지, 영상, 3D 탭으로 나뉘어 생성됩니다.",
    "추천 순서": "1. 빠른 프리셋 선택\n2. 프롬프트 엔진 선택\n3. 작업 모드와 이미지 스타일 선택\n4. 전문가 모드라면 컨셉 스파인, 한글 문구, 팔레트 보강\n5. 주제 입력 후 기획안 생성",
    "빠른 모드": "짧고 빠른 프롬프트가 필요할 때 사용합니다. 선택한 프리셋, 작업 모드, 스타일, 조명, 카메라를 한 문장형 프롬프트로 조합합니다.",
    "전문가 모드": "품질과 일관성이 중요한 작업에 사용합니다. 주제의 핵심 의도, 주체의 특징, 배경, 색상, 카메라, 금지 요소를 구조적으로 넣어 더 긴 프롬프트를 만듭니다.",
}

PRESET_HELP = {
    "한글 디자인": "한글 글자 형태, 한국적 색감, 포스터나 그래픽 레이아웃을 중심으로 결과를 만듭니다. 한글 문구가 중요한 배너, 포스터, 브랜드 시안에 적합합니다.",
    "매출형": "제품이 눈에 잘 띄고 구매 욕구가 생기도록 강한 초점, 대비, 명확한 구도를 우선합니다. 쇼핑몰 대표 이미지, 광고 소재, 상세페이지 첫 화면에 적합합니다.",
    "감성형": "따뜻한 분위기, 부드러운 조명, 스토리텔링을 강조합니다. 카페, 라이프스타일, 브랜드 무드 이미지, SNS 감성 콘텐츠에 적합합니다.",
    "트렌드": "최신 시각 트렌드, 강한 색감, 공유하기 좋은 후킹 이미지를 만듭니다. SNS 업로드용 이미지나 젊은 타깃 캠페인에 적합합니다.",
    "브랜드 일관성": "여러 장을 만들 때 색상, 소재, 톤앤매너가 흔들리지 않도록 구성합니다. 브랜드 캠페인, 시리즈 이미지, 룩북에 적합합니다.",
    "숏폼 바이럴": "처음 1초에 시선을 잡는 강한 장면, 빠른 움직임, 세로형 구도를 우선합니다. 릴스, 쇼츠, 틱톡용 영상 프롬프트에 적합합니다.",
    "시네마 영상형": "영화 같은 조명, 카메라 움직임, 장면 흐름을 강조합니다. 영상 콘티, 광고 영상, 무드 필름용 프롬프트에 적합합니다.",
    "제품 상세형": "재질, 질감, 반사, 접사 디테일을 강조합니다. 제품 상세컷, 소재 설명, 고급 제품 사진에 적합합니다.",
    "캐릭터 IP형": "캐릭터의 실루엣, 표정, 의상, 굿즈화 가능성을 강조합니다. 캐릭터 개발, 마스코트, 스티커, IP 시리즈에 적합합니다.",
    "화보 전문가형": "인물, 의상, 장소, 조명, 카메라를 세밀하게 구성합니다. 패션 화보, 인물 룩북, 광고 화보 스타일에 적합합니다.",
}

ENGINE_HELP = {
    "전문가 모드": "긴 프롬프트를 구조적으로 만듭니다. 컨셉 스파인, 주체 특징, 배경 레이어, 색상 팔레트, 카메라, 조명, 금지 요소를 모두 반영합니다.",
    "빠른 모드": "짧은 프롬프트를 빠르게 만듭니다. 상세 입력이 부담스러울 때 적합하고, 간단한 이미지 시안이나 초안 생성에 좋습니다.",
}

WORK_MODE_HELP = {
    "제품 (Product)": "제품 하나를 주인공으로 세워 대표 이미지를 만듭니다. 쇼핑몰 썸네일, 광고 배너, 제품 히어로컷에 적합합니다.",
    "제품 상세컷 (Product Detail)": "표면, 재질, 질감, 작은 부품을 접사처럼 강조합니다. 상세페이지의 소재 설명 이미지에 적합합니다.",
    "SNS 홍보 (Social)": "SNS에서 빠르게 눈에 띄는 홍보 이미지를 만듭니다. 카드뉴스, 피드 이미지, 이벤트 홍보에 적합합니다.",
    "숏폼 영상 (Short-form Video)": "세로 영상, 빠른 후킹 장면, 루프 가능한 움직임을 중심으로 구성합니다.",
    "광고 캠페인 (Ad Campaign)": "제품이나 브랜드를 하나의 캠페인 키비주얼처럼 보이게 만듭니다.",
    "로고 (Logo)": "로고 컨셉을 만들기 위한 방향성 프롬프트입니다. 최종 로고 파일이 아니라 아이디어 시안용입니다.",
    "브랜드 키비주얼 (Brand Key Visual)": "브랜드를 대표하는 메인 이미지 시스템을 만듭니다. 웹 첫 화면, 캠페인 대표컷에 적합합니다.",
    "패키지 디자인 (Package)": "상자, 병, 라벨, 파우치 등 패키지 시안을 만듭니다. 실제 인쇄 문구는 후작업이 필요할 수 있습니다.",
    "캐릭터/IP (Character IP)": "반복 사용 가능한 캐릭터의 외형과 성격을 잡습니다.",
    "AI 모델/착장 (AI Model)": "모델, 의상, 포즈, 스타일링이 중요한 패션 또는 뷰티 컷에 적합합니다.",
    "공간/인테리어 (Space)": "매장, 전시, 실내 공간, 배경 세트를 구성합니다.",
    "일러스트 (Art)": "사진보다 그림, 아트워크, 삽화 느낌을 원할 때 사용합니다.",
    "포스터 (Poster)": "행사, 전시, 브랜드 포스터처럼 한 장의 완성된 그래픽을 목표로 합니다.",
    "썸네일 (Thumbnail)": "작은 화면에서도 잘 보이는 강한 초점과 대비를 만듭니다.",
    "영상 콘티 (Storyboard)": "영상의 한 장면처럼 카메라, 조명, 구도를 잡습니다.",
    "한글 타이포그래피 (Hangul Typography)": "한글 글자 모양과 배치를 중심으로 그래픽을 만듭니다. 글자 정확도는 생성 모델 성능에 따라 달라집니다.",
    "화보 세트 (Editorial Set)": "같은 인물, 같은 분위기, 같은 팔레트로 여러 장의 화보를 만들 때 적합합니다.",
}

STYLE_HELP = {
    "프리미엄 미니멀": "불필요한 장식을 줄이고 여백, 정돈된 구도, 고급스러운 단순함을 강조합니다.",
    "고급/프리미엄": "고가 제품처럼 보이도록 소재, 조명, 마감감, 세련된 분위기를 강조합니다.",
    "강렬/임팩트": "강한 대비와 선명한 초점으로 첫눈에 들어오는 이미지를 만듭니다.",
    "하이퍼리얼 제품사진": "실제 촬영처럼 보이는 제품 질감, 반사, 그림자, 스튜디오 조명을 강조합니다.",
    "시네마틱 광고": "영화 광고처럼 깊은 조명, 렌즈감, 고급스러운 화면 분위기를 만듭니다.",
    "브랜드 에디토리얼": "브랜드 화보나 매거진처럼 일관된 색감과 편집 디자인 감각을 강조합니다.",
    "AI 인플루언서 룩북": "가상의 모델, 자연스러운 포즈, 의상 디테일을 중심으로 룩북 이미지를 만듭니다.",
    "퓨처 럭셔리": "미래적인 소재와 고급스러운 금속감, 매끈한 디자인 언어를 결합합니다.",
    "클레이/토이 3D": "점토 장난감이나 피규어처럼 부드럽고 귀여운 3D 질감을 만듭니다.",
    "픽사풍 3D 캐릭터": "표정이 살아 있는 가족 친화형 3D 애니메이션 캐릭터 느낌입니다.",
    "레트로 퓨처리즘": "복고적 미래감, 크롬, 오래된 SF 포스터 같은 분위기를 냅니다.",
    "키네틱 타이포 배경": "움직이는 그래픽과 글자 배치 느낌을 배경으로 사용합니다. 실제 읽히는 문구보다는 에너지 있는 배치를 목표로 합니다.",
    "패션 매거진": "잡지 화보 같은 포즈, 스타일링, 광택 있는 편집 이미지를 만듭니다.",
    "K-뷰티 글로우": "깨끗한 피부광, 부드러운 하이라이트, 화장품 광고 같은 이미지를 만듭니다.",
    "테크웨어 사이버": "기능성 의상, 도시적 미래감, 어두운 사이버 스타일을 강조합니다.",
    "네온 누아르": "밤거리, 네온 반사, 영화적 어둠과 강한 색을 결합합니다.",
    "한글 모던 그래픽": "현대적인 한글 글자 배치, 그리드, 여백, 한국적 그래픽 감각을 강조합니다.",
    "전통 한글 포스터": "한지 질감, 붓글씨 리듬, 전통 색감과 현대 포스터 구성을 결합합니다.",
    "K-에디토리얼 화보": "한국 상업 화보처럼 세련된 인물, 의상, 장소, 조명을 구성합니다.",
    "생활 스냅 화보": "일상 장면을 자연스럽고 감성적인 화보처럼 만듭니다.",
    "친근/귀여움/치비 캐릭터": "작고 둥근 캐릭터, 귀여운 표정, 친근한 인상을 만듭니다.",
    "한국민화 웹툰": "민화의 소재와 색감을 현대 웹툰 선화 느낌으로 바꿉니다.",
    "스티커 사진": "오려 붙인 듯한 컷아웃, 광택, 장난스러운 배치를 만듭니다.",
    "드라미틱 레트로 애니": "80~90년대 애니메이션 같은 강한 명암과 감성을 만듭니다.",
    "아이소메트릭 3D": "비스듬한 위에서 보는 3D 도식, 공간, 제품 설명 이미지에 적합합니다.",
    "직접입력": "목록에 없는 스타일을 직접 영어 또는 한국어로 입력합니다. 원하는 작가명보다 구도, 질감, 조명, 색감을 쓰는 편이 안정적입니다.",
}

FIELD_HELP = {
    "생성 개수": "한 번에 만들 기획안 수입니다. 여러 결과를 비교하려면 3개 이상이 좋고, 빠른 확인만 할 때는 1개가 적합합니다.",
    "조명": "이미지의 분위기와 품질을 크게 좌우합니다. 제품은 Studio, 감성 이미지는 Natural 또는 Golden Hour, 뷰티는 Beauty Softbox가 적합합니다.",
    "카메라 앵글": "피사체를 어느 시점에서 볼지 정합니다. 제품은 정면/클로즈업/매크로, 공간은 와이드/드론샷, 영상은 핸드헬드가 유용합니다.",
    "브랜드명": "브랜드 이름이나 프로젝트명을 넣으면 프롬프트 안에서 정체성 유지 규칙으로 사용합니다. 실제 로고나 정확한 문구 생성은 별도 후작업이 필요할 수 있습니다.",
    "3D Pop-out": "대상이 화면 밖으로 튀어나오는 입체감을 주는 옵션입니다. 캐릭터, 썸네일, 숏폼 후킹 장면에 효과적입니다.",
    "컨셉 스파인": "작업 전체를 관통하는 한 문장짜리 핵심 의도입니다. 예를 들어 '비 오는 을지로 골목의 한글 간판 감성'처럼 결과가 흔들리지 않게 잡아주는 중심 문장입니다.",
    "정확한 한글 문구": "이미지 안에 넣고 싶은 한글 문구입니다. 예: '한글 디자인'. 다만 이미지 생성 모델은 글자를 틀릴 수 있으므로, 최종 포스터 문구는 편집 프로그램에서 다시 넣는 것이 안전합니다.",
    "색상/HEX 팔레트": "결과 전체에 반복할 색상 규칙입니다. 예: ink black #111111, ivory #F4EDE0. 비워두면 앱이 한글 디자인에 맞는 기본 팔레트를 자동으로 고릅니다.",
    "세트 일관성 유지": "여러 장 생성 시 색상, 소재, 인물/제품 정체성이 비슷하게 유지되도록 합니다. 룩북, 브랜드 캠페인, 시리즈 이미지에 필요합니다.",
    "디테일 밀도": "프롬프트의 상세함 정도입니다. 낮으면 간결하고 안정적이며, 높으면 더 풍부하지만 결과가 복잡해질 수 있습니다.",
    "프롬프트 강도": "창의적 변형의 강도입니다. 낮으면 안정적이고, 높으면 트렌드 키워드와 실험적 표현이 더 들어갑니다.",
    "구글 번역": "한국어 주제를 영어로 변환해서 프롬프트에 넣습니다. 비공식 번역 방식이므로 실패하면 원문을 그대로 사용합니다.",
    "즐겨찾기/템플릿": "마음에 드는 프리셋 조합과 결과 프롬프트를 저장하고 다시 불러오는 기능입니다.",
    "히스토리": "이번 실행 중 생성한 결과를 다시 선택하는 영역입니다. 전체 삭제를 누르면 화면 기록만 지워집니다.",
}

def _data_dir() -> str:
    d = os.path.join(os.path.expanduser("~"), ".hangeul_design")
    os.makedirs(d, exist_ok=True)
    return d

FAV_FILE = os.path.join(_data_dir(), "favorites.json")

def _load_favorites() -> List[Dict[str, Any]]:
    try:
        if os.path.exists(FAV_FILE):
            with open(FAV_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []

def _save_favorites(items: List[Dict[str, Any]]) -> None:
    try:
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    except Exception:
        return

def _uid() -> str:
    return uuid.uuid4().hex

def _ts_label() -> str:
    return time.strftime("%m-%d %H:%M:%S")

def _aspect_phrase(aspect: str) -> str:
    return aspect.split(" ")[0].strip()

def _palette_phrase(custom_palette: str) -> str:
    custom_palette = (custom_palette or "").strip()
    if custom_palette:
        return custom_palette
    picked = random.sample(DEFAULT_PALETTES, k=6)
    names = ", ".join([name for name, _ in picked])
    hexes = ", ".join([hex_code for _, hex_code in picked])
    return f"{names}. HEX palette: [{hexes}]"

def _detail_density_phrase(density: int) -> str:
    density = max(0, min(100, int(density)))
    if density < 35:
        return "clean concise details, no over-description, practical production prompt"
    if density < 70:
        return "rich but controlled details, specific materials, clear setting, refined styling"
    return "dense expert-level description, layered styling, tactile materials, precise background traces, strong art direction"

def _hangul_copy_phrase(hangul_text: str) -> str:
    hangul_text = (hangul_text or "").strip()
    if not hangul_text:
        return "If typography is used, prioritize correct Hangul structure and avoid random unreadable letters."
    return (
        f"Use the exact Hangul text '{hangul_text}' only if the target model supports exact text rendering; "
        "otherwise treat it as a layout reference and keep letterforms clean."
    )

def _build_expert_prompt(
    subject_en: str,
    preset: str,
    work_mode: str,
    style: str,
    lighting: str,
    camera: str,
    aspect: str,
    brand: str,
    pop3d: bool,
    intensity: int,
    expert_subject: str,
    hangul_text: str,
    palette: str,
    continuity: bool,
    detail_density: int,
) -> Tuple[str, str, str, str]:
    subject_en = (subject_en or "").strip()
    expert_subject = (expert_subject or "").strip()
    brand = (brand or "").strip()

    mode_phrase = WORKMODE_PHRASE.get(work_mode, work_mode)
    style_phrase = STYLE_PHRASE.get(style, style)
    preset_phrase = PRESET_PHRASE.get(preset, PRESET_PHRASE["한글 디자인"])
    palette_phrase = _palette_phrase(palette)
    density_phrase = _detail_density_phrase(detail_density)
    motion_phrase = VIDEO_MOTION_PHRASE.get(work_mode, "controlled motion with stable subject identity")
    aspect_phrase = _aspect_phrase(aspect)
    cam_phrase = _camera_phrase(camera)
    lighting_phrase = "lighting: auto, plausible source, consistent shadows" if lighting == "AI 자동" else f"lighting: {lighting}, direction and shadow behavior clearly defined"
    continuity_phrase = "same subject identity, same outfit/material rules, same color palette across the whole set" if continuity else "allow each result to vary while keeping the concept recognizable"
    hangul_phrase = _hangul_copy_phrase(hangul_text)
    variation = _pick_variations(intensity, preset)

    blueprint = "\n".join([
        f"Engine: 전문가 모드",
        f"Concept spine: {expert_subject or subject_en}",
        f"Preset: {preset}",
        f"Mode: {work_mode}",
        f"Style: {style}",
        f"Continuity: {continuity_phrase}",
        f"Palette: {palette_phrase}",
        f"Detail density: {detail_density}",
    ])

    blocks = [
        f"Create a {mode_phrase} for subject: {subject_en}.",
        f"Concept spine: {expert_subject or subject_en}; every visual decision must support this one idea.",
        f"Brand rule: {brand}, keep identity coherent and non-generic." if brand else "Brand rule: no fake brand marks or random logos.",
        f"Style direction: {style_phrase}; {preset_phrase}.",
        f"Subject/detail anchors: define a clear silhouette, material behavior, surface texture, scale, and focal hierarchy; {density_phrase}.",
        f"Scene design: use a specific place, foreground detail, mid-ground action, background depth, and small lived-in traces that fit the concept.",
        f"Lighting: {lighting_phrase}.",
        f"Palette: {palette_phrase}; repeat the main color in at least three visual elements for coherence.",
        f"Camera and composition: {cam_phrase}, aspect ratio {aspect_phrase}, strong focal point, production-ready framing.",
        f"Hangul/text control: {hangul_phrase}",
        f"Continuity control: {continuity_phrase}.",
        QUALITY_PHRASE,
    ]
    if variation:
        blocks.append(f"Creative variation: {variation}.")
    if pop3d:
        blocks.append("3D pop-out depth is allowed: layered parallax, tactile shadows, subject breaking the frame.")
    blocks.append(EXPERT_NEGATIVE_PHRASE)

    image_prompt = " ".join([x for x in blocks if x])
    video_prompt = (
        "Video generation prompt. "
        + image_prompt.replace(EXPERT_NEGATIVE_PHRASE, "avoid flicker, unstable identity, morphing face, jitter, random text, watermark")
        + f" Motion plan: {motion_phrase}. Duration: 5-8 seconds. Keep temporal consistency and a loopable ending when useful."
    )
    d3_prompt = (
        "3D/design visualization prompt. "
        + image_prompt
        + " Convert the concept into clean geometry, readable material separation, front/back silhouette clarity, usable lighting, and render-safe proportions."
    )
    return image_prompt, video_prompt, d3_prompt, blueprint

def _camera_phrase(cam: str) -> str:
    m = {
        "AI 자동": "camera: auto",
        "정면": "front view",
        "탑뷰": "top-down view",
        "로우앵글": "low angle",
        "와이드": "wide shot",
        "클로즈업": "close-up",
        "매크로": "macro lens close-up",
        "핸드헬드": "natural handheld camera",
        "드론샷": "drone-style overhead establishing shot",
    }
    return m.get(cam, cam)

def _tip_for(preset: str) -> str:
    tips = {
        "매출형": "Tip: Strong contrast keeps attention longer and supports conversion intent.",
        "감성형": "Tip: Warm tones and soft lighting increase trust and emotional resonance.",
        "트렌드": "Tip: Use 1-2 trend keywords precisely, not many.",
        "브랜드 일관성": "Tip: Repeat color, material, and framing rules across every prompt.",
        "숏폼 바이럴": "Tip: Put the visual hook in the first clause so video models prioritize it.",
        "시네마 영상형": "Tip: Camera movement and continuity cues matter more than extra style words.",
        "제품 상세형": "Tip: Name materials, reflections, and macro details for better product realism.",
        "캐릭터 IP형": "Tip: Keep silhouette, costume, and expression rules stable across generations.",
    }
    return tips.get(preset, tips["트렌드"])

def _clipboard_button(label: str, text: str, key: str):
    safe = (text or "").replace("\\", "\\\\").replace("`", "\\`")
    html = f"""
    <div style="margin-top:6px;">
      <button id="{key}" style="border:1px solid rgba(49,51,63,0.18);border-radius:10px;padding:8px 10px;background:white;cursor:pointer;">{label}</button>
      <span id="{key}_msg" style="margin-left:8px;color:rgba(49,51,63,0.7);font-size:12px;"></span>
    </div>
    <script>
      const btn = document.getElementById("{key}");
      const msg = document.getElementById("{key}_msg");
      btn.addEventListener("click", async () => {{
        try {{
          await navigator.clipboard.writeText(`{safe}`);
          msg.textContent = "Copied";
          setTimeout(()=>msg.textContent="", 1200);
        }} catch(e) {{
          msg.textContent = "Copy failed";
          setTimeout(()=>msg.textContent="", 2000);
        }}
      }});
    </script>
    """
    components.html(html, height=46)

def _export_report(plans: List[Dict[str, Any]]) -> str:
    lines = [f"{APP_NAME} Report", "=" * 40]
    for i, p in enumerate(plans, 1):
        lines.append(f"[{i}] {p['title']}")
        lines.append(f"- keyword: {p['subject']}")
        lines.append(f"- subject_en: {p.get('subject_en','')}")
        lines.append(f"- preset: {p['preset']}")
        lines.append(f"- mode: {p['work_mode']}")
        lines.append(f"- style: {p['style']}")
        lines.append(f"- lighting: {p['lighting']}")
        lines.append(f"- camera: {p['camera']}")
        lines.append(f"- aspect: {p['aspect']}")
        if p.get("brand"):
            lines.append(f"- brand: {p['brand']}")
        lines.append(f"- intensity: {p.get('intensity', 50)}")
        lines.append(f"- engine: {p.get('prompt_engine', '빠른 모드')}")
        if p.get("prompt_blueprint"):
            lines.append("")
            lines.append("[STRUCTURE]")
            lines.append(p["prompt_blueprint"])
        lines.append(f"- tip: {p['tip']}")
        lines.append("")
        lines.append("[IMAGE]")
        lines.append(p["image_prompt"])
        lines.append("")
        lines.append("[VIDEO]")
        lines.append(p["video_prompt"])
        lines.append("")
        lines.append("[3D]")
        lines.append(p["d3_prompt"])
        lines.append("-" * 40)
    return "\n".join(lines)

def translate_google(text: str, src: str = "auto", dst: str = "en") -> Tuple[str, bool]:
    t = (text or "").strip()
    if not t:
        return "", True
    try:
        q = urllib.parse.quote(t)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={dst}&dt=t&q={q}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
        data = json.loads(raw)
        out = "".join([seg[0] for seg in data[0] if seg and isinstance(seg, list) and len(seg) > 0])
        out = (out or "").strip()
        return (out if out else t), bool(out)
    except Exception:
        return t, False

def _maybe_translate_subject(subject: str) -> Tuple[str, bool]:
    if not st.session_state.get("use_google_translate", True):
        return subject, True
    return translate_google(subject, src="auto", dst="en")

CREATIVE_ADJ = [
    "unexpected micro-details", "playful surreal twist", "bold art direction", "inventive material choice",
    "cinematic atmosphere", "stylized texture language", "graphic silhouette emphasis", "dynamic negative space",
]
CONSERVATIVE_ADJ = [
    "clean composition", "balanced framing", "realistic materials", "studio clarity", "consistent lighting",
]
TREND_KWS = [
    "neo-retro", "hyperpop aesthetic", "Y2K", "memphis revival", "soft brutalism", "holographic accents",
    "AI editorial", "micro-cinematic realism", "collectible toy render", "K-culture premium",
    "mixed-media collage", "analog-film texture",
]

def _intensity_pack(intensity: int) -> Dict[str, Any]:
    intensity = max(0, min(100, int(intensity)))
    extra_n = 0 if intensity < 15 else (1 if intensity < 45 else (2 if intensity < 75 else 3))
    trend_n = 0 if intensity < 60 else (1 if intensity < 85 else 2)
    return {"extra_n": extra_n, "trend_n": trend_n}

def _pick_variations(intensity: int, preset: str) -> str:
    pack = _intensity_pack(intensity)
    parts = []
    if pack["extra_n"] > 0:
        pool = CREATIVE_ADJ if intensity >= 50 else (CREATIVE_ADJ + CONSERVATIVE_ADJ)
        parts.extend(random.sample(pool, k=min(pack["extra_n"], len(pool))))
    if pack["trend_n"] > 0 and preset in ["트렌드", "숏폼 바이럴", "시네마 영상형"]:
        parts.extend(random.sample(TREND_KWS, k=min(pack["trend_n"], len(TREND_KWS))))
    return ", ".join(parts)

def _build_prompts(
    subject_en: str,
    preset: str,
    work_mode: str,
    style: str,
    lighting: str,
    camera: str,
    aspect: str,
    brand: str,
    pop3d: bool,
    intensity: int,
) -> Tuple[str, str, str]:
    subject_en = (subject_en or "").strip()
    brand = (brand or "").strip()

    mode_phrase = WORKMODE_PHRASE.get(work_mode, work_mode)
    if style == "직접입력":
        style_phrase = (st.session_state.get("style_custom") or "").strip() or "creative art direction, clean composition"
    else:
        style_phrase = STYLE_PHRASE.get(style, style)

    lighting_phrase = "lighting: auto" if lighting == "AI 자동" else f"lighting: {lighting}"
    cam_phrase = _camera_phrase(camera)
    aspect_phrase = _aspect_phrase(aspect)
    preset_phrase = PRESET_PHRASE.get(preset, PRESET_PHRASE["트렌드"])
    motion_phrase = VIDEO_MOTION_PHRASE.get(work_mode, "smooth camera movement, clear subject reveal")

    variation = _pick_variations(intensity, preset)
    if variation:
        variation = f"creative variation: {variation}"

    base = [
        f"{mode_phrase}, subject: {subject_en}",
        f"style: {style_phrase}",
        "language: English",
        lighting_phrase,
        cam_phrase,
        f"aspect ratio: {aspect_phrase}",
        preset_phrase,
        QUALITY_PHRASE,
    ]

    if brand:
        base.insert(1, f"brand (English): {brand}, keep brand identity coherent and non-generic")

    if variation:
        base.append(variation)

    if intensity >= 70:
        base.append("allow stylistic experimentation, surprising but coherent design choices")
    else:
        base.append("keep coherent and practical")

    if work_mode in ["로고 (Logo)", "패키지 디자인 (Package)", "브랜드 키비주얼 (Brand Key Visual)"]:
        base.append("avoid generating final readable copy unless the target model supports exact typography")

    base.append("high quality, creative details, tasteful composition, production-ready output")
    base.append(NEGATIVE_IMAGE_PHRASE)

    image_prompt = ", ".join([x for x in base if x])

    video_prompt = (
        "cinematic video prompt, "
        + image_prompt.replace(NEGATIVE_IMAGE_PHRASE, "exclude on-screen text, watermark, flicker, morphing faces, jitter, unstable hands")
        + f", motion: {motion_phrase}, stable subject identity across frames, temporal consistency, 5-8 seconds"
    )

    pop = ""
    if pop3d:
        pop_strength = "strong" if intensity >= 60 else "moderate"
        pop = (
            f"pop-out 3D ({pop_strength}), strong depth separation, subject breaking the frame, "
            "layered parallax, dynamic shadowing, tactile materials, rim highlights, "
        )
    d3_prompt = (
        f"3D render, {pop}"
        + image_prompt.replace(
            "high quality, creative details, tasteful composition",
            "high poly, clean topology, realistic materials, studio-grade render, crisp AO, clean reflections",
        )
        + ", model-ready proportions, clear front silhouette, usable material separation"
    )

    return image_prompt, video_prompt, d3_prompt

def _ss_init():
    st.session_state.setdefault("preset", "한글 디자인")
    st.session_state.setdefault("work_mode", PRESET_DEFAULTS["한글 디자인"]["work_mode"])
    st.session_state.setdefault("image_style", PRESET_DEFAULTS["한글 디자인"]["style"])
    st.session_state.setdefault("pop3d", PRESET_DEFAULTS["한글 디자인"]["pop3d"])

    st.session_state.setdefault("count", 3)
    st.session_state.setdefault("lighting", "AI 자동")
    st.session_state.setdefault("camera", "AI 자동")
    st.session_state.setdefault("brand", "")
    st.session_state.setdefault("aspect", "1:1 (기본)")
    st.session_state.setdefault("lang", "English")
    st.session_state.setdefault("lab_on", False)

    st.session_state.setdefault("subject", "")
    st.session_state.setdefault("plans", [])
    st.session_state.setdefault("last_batch_uids", [])
    st.session_state.setdefault("selected_uid", None)
    st.session_state.setdefault("style_custom", "")

    st.session_state.setdefault("intensity", 55)
    st.session_state.setdefault("use_google_translate", True)
    st.session_state.setdefault("prompt_engine", "전문가 모드")
    st.session_state.setdefault("expert_subject", "")
    st.session_state.setdefault("hangul_text", "")
    st.session_state.setdefault("palette", "")
    st.session_state.setdefault("continuity", True)
    st.session_state.setdefault("detail_density", 72)

    st.session_state.setdefault("favorites", _load_favorites())

def _apply_preset_defaults(preset: str):
    d = PRESET_DEFAULTS.get(preset)
    if not d:
        return
    st.session_state.work_mode = d["work_mode"]
    st.session_state.image_style = d["style"]
    st.session_state.pop3d = d["pop3d"]

def _on_preset_change():
    _apply_preset_defaults(st.session_state.preset)

def _fav_id() -> str:
    return uuid.uuid4().hex[:10]

def _save_current_as_favorite(plan: Dict[str, Any]):
    favs = list(st.session_state.favorites or [])
    item = {
        "id": _fav_id(),
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
    st.session_state.favorites = favs
    _save_favorites(favs)
    st.toast("즐겨찾기에 저장됨", icon="✅")

def _apply_favorite(item: Dict[str, Any]):
    st.session_state.preset = item.get("preset", st.session_state.preset)
    _apply_preset_defaults(st.session_state.preset)
    st.session_state.work_mode = item.get("work_mode", st.session_state.work_mode)
    st.session_state.image_style = item.get("style", st.session_state.image_style)
    st.session_state.lighting = item.get("lighting", st.session_state.lighting)
    st.session_state.camera = item.get("camera", st.session_state.camera)
    st.session_state.aspect = item.get("aspect", st.session_state.aspect)
    st.session_state.pop3d = bool(item.get("pop3d", st.session_state.pop3d))
    st.session_state.intensity = int(item.get("intensity", st.session_state.intensity))
    st.session_state.brand = item.get("brand", st.session_state.brand)
    st.session_state.prompt_engine = item.get("prompt_engine", st.session_state.prompt_engine)
    st.session_state.expert_subject = item.get("expert_subject", st.session_state.expert_subject)
    st.session_state.hangul_text = item.get("hangul_text", st.session_state.hangul_text)
    st.session_state.palette = item.get("palette", st.session_state.palette)
    st.session_state.continuity = bool(item.get("continuity", st.session_state.continuity))
    st.session_state.detail_density = int(item.get("detail_density", st.session_state.detail_density))
    st.toast("템플릿 적용됨", icon="⭐")

def _delete_favorite(fid: str):
    favs = [x for x in (st.session_state.favorites or []) if x.get("id") != fid]
    st.session_state.favorites = favs
    _save_favorites(favs)
    st.toast("삭제됨", icon="🗑️")

def _safe_key(text: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in text).strip("_")[:80]

def _help_popover(title: str, selected: str = "", help_map: Dict[str, str] | None = None, general: str = ""):
    with st.popover("설명", width="content", key=f"help_{_safe_key(title + selected)}"):
        st.markdown(f"#### {title}")
        if general:
            st.markdown(general)
        if selected and help_map:
            st.markdown(f"**현재 선택: {selected}**")
            st.write(help_map.get(selected, "선택한 항목에 대한 설명이 아직 없습니다."))
        if help_map:
            with st.expander("전체 항목 설명"):
                for name, desc in help_map.items():
                    st.markdown(f"**{name}**")
                    st.write(desc)

def _sidebar_section(title: str, help_title: str, selected: str = "", help_map: Dict[str, str] | None = None, general: str = ""):
    c1, c2 = st.sidebar.columns([0.74, 0.26])
    with c1:
        st.markdown(f'<div class="sidebar-h">{title}</div>', unsafe_allow_html=True)
    with c2:
        _help_popover(help_title, selected=selected, help_map=help_map, general=general)

def _sidebar_help_line(label: str, help_text: str):
    c1, c2 = st.sidebar.columns([0.74, 0.26])
    with c1:
        st.markdown(f'<div class="sidebar-h">{label}</div>', unsafe_allow_html=True)
    with c2:
        _help_popover(label, general=help_text)

def render_sidebar():
    st.sidebar.markdown(f"### {APP_NAME}")
    with st.sidebar.popover("사용 설명서", use_container_width=True):
        st.markdown("#### 전체 사용 순서")
        st.write(APP_GUIDE["개요"])
        st.markdown(APP_GUIDE["추천 순서"].replace("\n", "  \n"))
        st.markdown("#### 모드 선택 기준")
        st.write(APP_GUIDE["전문가 모드"])
        st.write(APP_GUIDE["빠른 모드"])

    _sidebar_section(
        "빠른 프리셋",
        "빠른 프리셋 설명",
        selected=st.session_state.get("preset", "한글 디자인"),
        help_map=PRESET_HELP,
        general="프리셋은 작업 목적을 빠르게 정하는 시작점입니다. 프리셋을 바꾸면 추천 작업 모드, 이미지 스타일, 3D 옵션이 함께 바뀝니다.",
    )
    st.sidebar.selectbox(
        "프리셋",
        PRESETS,
        label_visibility="collapsed",
        key="preset",
        on_change=_on_preset_change,
    )

    _sidebar_section(
        "기본 설정",
        "기본 설정 설명",
        general="프롬프트 엔진은 문장 생성 방식, 작업 모드는 결과물의 용도, 이미지 스타일은 시각 표현 방식을 정합니다.",
    )
    _sidebar_section(
        "프롬프트 엔진",
        "프롬프트 엔진 설명",
        selected=st.session_state.get("prompt_engine", "전문가 모드"),
        help_map=ENGINE_HELP,
    )
    st.sidebar.selectbox("프롬프트 엔진", ["전문가 모드", "빠른 모드"], key="prompt_engine", label_visibility="collapsed")
    _sidebar_section(
        "작업 모드",
        "작업 모드 설명",
        selected=st.session_state.get("work_mode", WORK_MODES[0]),
        help_map=WORK_MODE_HELP,
    )
    st.sidebar.selectbox("작업 모드", WORK_MODES, key="work_mode", label_visibility="collapsed")
    _sidebar_section(
        "이미지 스타일",
        "이미지 스타일 설명",
        selected=st.session_state.get("image_style", STYLE_OPTIONS[0]),
        help_map=STYLE_HELP,
    )
    st.sidebar.selectbox("이미지 스타일", STYLE_OPTIONS, key="image_style", label_visibility="collapsed")
    if st.session_state.image_style == "직접입력":
        st.sidebar.text_input("스타일 직접입력", key="style_custom", placeholder="예: ultra clean magazine layout, pastel cyberpunk ...")
    _sidebar_help_line("3D Pop-out", FIELD_HELP["3D Pop-out"])
    st.sidebar.toggle("3D Pop-out", key="pop3d")

    _sidebar_section("상세 옵션", "상세 옵션 설명", general="생성 개수, 조명, 카메라, 브랜드명을 조정해 결과물의 안정성과 방향성을 세부 조정합니다.")
    _sidebar_help_line("생성 개수", FIELD_HELP["생성 개수"])
    st.sidebar.slider("생성 개수", min_value=1, max_value=8, key="count", label_visibility="collapsed")
    _sidebar_help_line("조명", FIELD_HELP["조명"])
    st.sidebar.selectbox("조명", LIGHTING_OPTIONS, key="lighting", label_visibility="collapsed")
    _sidebar_help_line("카메라 앵글", FIELD_HELP["카메라 앵글"])
    st.sidebar.selectbox("카메라 앵글", CAMERA_OPTIONS, key="camera", label_visibility="collapsed")
    _sidebar_help_line("브랜드명(옵션)", FIELD_HELP["브랜드명"])
    st.sidebar.text_input("브랜드명(옵션)", key="brand", placeholder="영어로 작성", label_visibility="collapsed")

    if st.session_state.prompt_engine == "전문가 모드":
        _sidebar_section(
            "전문가 구조",
            "전문가 구조 설명",
            general="전문가 구조는 프롬프트를 더 길고 안정적으로 만드는 추가 입력 영역입니다. 반드시 모두 채울 필요는 없지만, 중요한 작업일수록 채우는 편이 좋습니다.",
        )
        _sidebar_help_line("컨셉 스파인", FIELD_HELP["컨셉 스파인"])
        st.sidebar.text_area("컨셉 스파인", key="expert_subject", height=86, placeholder="예: 비 오는 을지로 골목의 한글 간판 감성", label_visibility="collapsed")
        _sidebar_help_line("정확한 한글 문구(옵션)", FIELD_HELP["정확한 한글 문구"])
        st.sidebar.text_input("정확한 한글 문구(옵션)", key="hangul_text", placeholder="예: 한글 디자인", label_visibility="collapsed")
        _sidebar_help_line("색상/HEX 팔레트(옵션)", FIELD_HELP["색상/HEX 팔레트"])
        st.sidebar.text_area("색상/HEX 팔레트(옵션)", key="palette", height=72, placeholder="예: ink black #111111, ivory #F4EDE0, jade #0E5B4F", label_visibility="collapsed")
        _sidebar_help_line("세트 일관성 유지", FIELD_HELP["세트 일관성 유지"])
        st.sidebar.toggle("세트 일관성 유지", key="continuity")
        _sidebar_help_line("디테일 밀도", FIELD_HELP["디테일 밀도"])
        st.sidebar.slider("디테일 밀도", 0, 100, key="detail_density", label_visibility="collapsed")

    _sidebar_section("프롬프트 튜닝", "프롬프트 튜닝 설명", general="프롬프트의 창의성, 변형 정도, 번역 여부를 조정합니다.")
    _sidebar_help_line("프롬프트 강도", FIELD_HELP["프롬프트 강도"])
    st.sidebar.slider("프롬프트 강도", 0, 100, key="intensity", label_visibility="collapsed")
    _sidebar_help_line("구글 번역", FIELD_HELP["구글 번역"])
    st.sidebar.toggle("구글 번역(주제 자동 영어 변환)", key="use_google_translate")
    st.sidebar.caption("주의: 비공식 구글 번역 엔드포인트 사용(확실하지 않음). 실패 시 원문 유지")

    _sidebar_section("즐겨찾기/템플릿", "즐겨찾기/템플릿 설명", general=FIELD_HELP["즐겨찾기/템플릿"])
    favs = st.session_state.favorites or []
    if favs:
        options = [f"{x['name']}  ({x['created']})" for x in favs]
        idx = st.sidebar.selectbox("저장된 템플릿", list(range(len(options))), format_func=lambda i: options[i], key="fav_idx")
        item = favs[int(idx)]
        c1, c2 = st.sidebar.columns(2)
        with c1:
            if st.button("적용", use_container_width=True, key="fav_apply"):
                _apply_favorite(item)
                st.rerun()
        with c2:
            if st.button("삭제", use_container_width=True, key="fav_del"):
                _delete_favorite(item["id"])
                st.rerun()
    else:
        st.sidebar.caption("저장된 템플릿 없음")

    _sidebar_section("히스토리", "히스토리 설명", general=FIELD_HELP["히스토리"])
    c1, c2 = st.sidebar.columns(2)
    with c1:
        st.button("최근 배치", use_container_width=True)
    with c2:
        if st.button("전체 삭제", use_container_width=True):
            st.session_state.plans = []
            st.session_state.last_batch_uids = []
            st.session_state.selected_uid = None

    if st.session_state.plans:
        for p in st.session_state.plans[:20]:
            label = f"{p.get('label','')} | {(p.get('subject','')[:16])}"
            if st.sidebar.button(label, key=f"h_{p['uid']}", use_container_width=True):
                st.session_state.selected_uid = p["uid"]

def render_main():
    st.markdown('<div class="dp-card">', unsafe_allow_html=True)
    st.markdown("## Hangeul Design 시작하기")
    st.caption("한국어 주제에서 이미지/영상/3D 프롬프트와 전문가 구조를 생성합니다.")

    c1, c2 = st.columns([5, 1.3])
    with c1:
        st.text_input("주제", key="subject", label_visibility="collapsed", placeholder="비 오는 을지로 골목의 한글 간판")
        st.markdown("<div class='small-muted'>주제 한글 입력 시, 번역 ON이면 자동 영어 변환 후 생성합니다.</div>", unsafe_allow_html=True)
    with c2:
        gen = st.button("기획안 생성", type="primary", use_container_width=True)

    c3, c4 = st.columns([1, 1])
    with c3:
        st.markdown("**생성 결과**")
    with c4:
        report = _export_report(st.session_state.plans) if st.session_state.plans else ""
        st.download_button(
            "리포트 저장",
            data=report.encode("utf-8"),
            file_name="HangeulDesign_report.txt",
            mime="text/plain",
            use_container_width=True,
            disabled=(not bool(report)),
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if gen:
        subject = (st.session_state.subject or "").strip()
        if not subject:
            st.warning("주제를 입력하세요.")
        else:
            subject_en, ok = _maybe_translate_subject(subject)
            if not ok:
                st.info("구글 번역 실패(확실하지 않음). 원문 주제를 그대로 사용합니다.")

            preset = st.session_state.preset
            tip = _tip_for(preset)
            work_mode = st.session_state.work_mode
            style = st.session_state.image_style
            lighting = st.session_state.lighting
            camera = st.session_state.camera
            aspect = st.session_state.aspect
            brand = st.session_state.brand
            pop3d = bool(st.session_state.pop3d)
            intensity = int(st.session_state.intensity)
            prompt_engine = st.session_state.prompt_engine
            prompt_blueprint = ""
            active_palette = st.session_state.get("palette", "")
            if prompt_engine == "전문가 모드" and bool(st.session_state.get("continuity", True)) and not active_palette.strip():
                active_palette = _palette_phrase("")

            new_items = []
            batch_uids = []
            for i in range(int(st.session_state.count)):
                uid = _uid()
                batch_uids.append(uid)
                title = f"[{preset}] {work_mode} 기획안 {i+1}"
                if prompt_engine == "전문가 모드":
                    img, vid, d3, prompt_blueprint = _build_expert_prompt(
                        subject_en=subject_en,
                        preset=preset,
                        work_mode=work_mode,
                        style=style,
                        lighting=lighting,
                        camera=camera,
                        aspect=aspect,
                        brand=brand,
                        pop3d=pop3d,
                        intensity=intensity,
                        expert_subject=st.session_state.expert_subject,
                        hangul_text=st.session_state.hangul_text,
                        palette=active_palette,
                        continuity=bool(st.session_state.continuity),
                        detail_density=int(st.session_state.detail_density),
                    )
                else:
                    img, vid, d3 = _build_prompts(
                        subject_en=subject_en,
                        preset=preset,
                        work_mode=work_mode,
                        style=style,
                        lighting=lighting,
                        camera=camera,
                        aspect=aspect,
                        brand=brand,
                        pop3d=pop3d,
                        intensity=intensity,
                    )
                    prompt_blueprint = "Engine: 빠른 모드\nStructure: preset + work mode + style + lighting + camera + quality controls"
                new_items.append({
                    "uid": uid,
                    "label": _ts_label(),
                    "title": title,
                    "subject": subject,
                    "subject_en": subject_en,
                    "preset": preset,
                    "work_mode": work_mode,
                    "style": style if style != "직접입력" else (st.session_state.style_custom or "custom"),
                    "lighting": lighting,
                    "camera": camera,
                    "aspect": aspect,
                    "brand": brand,
                    "pop3d": pop3d,
                    "intensity": intensity,
                    "prompt_engine": prompt_engine,
                    "expert_subject": st.session_state.get("expert_subject", ""),
                    "hangul_text": st.session_state.get("hangul_text", ""),
                    "palette": active_palette,
                    "continuity": bool(st.session_state.get("continuity", True)),
                    "detail_density": int(st.session_state.get("detail_density", 72)),
                    "prompt_blueprint": prompt_blueprint,
                    "tip": tip,
                    "image_prompt": img,
                    "video_prompt": vid,
                    "d3_prompt": d3,
                })
                time.sleep(0.002)

            st.session_state.plans = new_items + st.session_state.plans
            st.session_state.last_batch_uids = batch_uids
            st.session_state.selected_uid = batch_uids[0]

    selected = None
    if st.session_state.selected_uid:
        for p in st.session_state.plans:
            if p.get("uid") == st.session_state.selected_uid:
                selected = p
                break
    if selected is None and st.session_state.plans:
        selected = st.session_state.plans[0]

    if selected:
        st.markdown('<div class="dp-card">', unsafe_allow_html=True)
        top1, top2 = st.columns([4, 1])
        with top1:
            st.markdown("### 생성 결과")
            st.markdown(
                f"<div class='small-muted'>Subject EN: <b>{selected.get('subject_en','')}</b> &nbsp;|&nbsp; Intensity: {selected.get('intensity', 50)}</div>",
                unsafe_allow_html=True,
            )
        with top2:
            if st.button("⭐ 즐겨찾기 저장", use_container_width=True, key="save_fav"):
                _save_current_as_favorite(selected)

        tabs = st.tabs(["구조", "이미지", "영상", "3D"])
        with tabs[0]:
            st.code(selected.get("prompt_blueprint", ""), language="text")
            _clipboard_button("복사", selected.get("prompt_blueprint", ""), key="copy_sel_struct")
        with tabs[1]:
            st.code(selected["image_prompt"], language="text")
            _clipboard_button("복사", selected["image_prompt"], key="copy_sel_img")
        with tabs[2]:
            st.code(selected["video_prompt"], language="text")
            _clipboard_button("복사", selected["video_prompt"], key="copy_sel_vid")
        with tabs[3]:
            st.code(selected["d3_prompt"], language="text")
            _clipboard_button("복사", selected["d3_prompt"], key="copy_sel_3d")
        st.markdown("</div>", unsafe_allow_html=True)

    # latest batch only
    cards: List[Dict[str, Any]] = []
    if st.session_state.last_batch_uids:
        uidset = set(st.session_state.last_batch_uids)
        cards = [p for p in st.session_state.plans if p.get("uid") in uidset]
    else:
        cards = st.session_state.plans[: int(st.session_state.count)]

    for p in cards:
        st.markdown('<div class="dp-card">', unsafe_allow_html=True)
        tag = PRESET_TAGS.get(p["preset"], "Plan")
        st.markdown(f"### {p['title']} <span class='dp-chip'>{tag}</span>", unsafe_allow_html=True)
        st.markdown(f"- 키워드: **{p['subject']}**  \n- 스타일: **{p['style']}**  \n- 엔진: **{p.get('prompt_engine', '빠른 모드')}**", unsafe_allow_html=True)
        st.markdown(f"<div class='dp-tip'>{p['tip']}</div>", unsafe_allow_html=True)
        st.markdown("<div class='dp-hr'></div>", unsafe_allow_html=True)

        tabs = st.tabs(["구조", "이미지", "영상", "3D"])
        with tabs[0]:
            st.code(p.get("prompt_blueprint", ""), language="text")
            _clipboard_button("복사", p.get("prompt_blueprint", ""), key=f"copy_{p['uid']}_struct")
        with tabs[1]:
            st.code(p["image_prompt"], language="text")
            _clipboard_button("복사", p["image_prompt"], key=f"copy_{p['uid']}_img")
        with tabs[2]:
            st.code(p["video_prompt"], language="text")
            _clipboard_button("복사", p["video_prompt"], key=f"copy_{p['uid']}_vid")
        with tabs[3]:
            st.code(p["d3_prompt"], language="text")
            _clipboard_button("복사", p["d3_prompt"], key=f"copy_{p['uid']}_3d")

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("이 결과 선택", key=f"sel_{p['uid']}", use_container_width=True):
                st.session_state.selected_uid = p["uid"]
                st.rerun()
        with c2:
            if st.button("⭐ 저장", key=f"fav_{p['uid']}", use_container_width=True):
                _save_current_as_favorite(p)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='dp-footer'>"
        "Hangeul Design &nbsp;|&nbsp; Contact: tigersin@kakao.com &nbsp;|&nbsp; Copyright © Jeon Youngshin. All rights reserved."
        "</div>",
        unsafe_allow_html=True,
    )

def main():
    _ss_init()
    render_sidebar()
    render_main()

if __name__ == "__main__":
    main()
