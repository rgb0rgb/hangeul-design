import ast
import types
from pathlib import Path

import beginner_mode
import prompt_compiler
import runtime_quality

ROOT = Path(__file__).resolve().parents[1]


def test_python_sources_parse():
    for name in ["app.py", "app_reference.py", "app_cinematic.py", "cinematic_product.py", "reference_image.py", "runtime_quality.py", "launcher.py", "prompt_compiler.py", "beginner_mode.py"]:
        ast.parse((ROOT / name).read_text(encoding="utf-8"))


def test_beginner_shortform_auto_configuration():
    x = beginner_mode.recommend_settings("햄치즈 베이글 신메뉴", "릴스 / 틱톡 / 유튜브 쇼츠", "AI가 추천")
    assert x["aspect"] == "9:16"
    assert x["work_mode"] == "숏폼 영상 (Short-form Video)"


def test_beginner_hangul_intent_wins():
    x = beginner_mode.recommend_settings("한글 문구 중심 포스터", "포스터 / 인쇄물", "한글 문구 중심")
    assert x["work_mode"] == "한글 타이포그래피 (Hangul Typography)"
    assert x["prompt_engine"] == "전문가 모드"


def test_midjourney_compiler_uses_real_aspect_parameter():
    out = prompt_compiler.compile_image_prompt("premium product, exclude text, watermark, low resolution", "Midjourney", "9:16")
    assert "--ar 9:16" in out and "--no" in out


def test_expert_avoid_clause_is_extracted():
    src = "premium watch, controlled reflections, avoid unreadable random text, extra fingers, duplicated faces, warped product edges, watermark"
    out = prompt_compiler.compile_image_prompt(src, "Stable Diffusion / FLUX", "1:1")
    positive, negative = out.split("Negative prompt:", 1)
    assert "extra fingers" not in positive
    assert "duplicated faces" not in positive
    assert "extra fingers" in negative
    assert "duplicated faces" in negative


def test_reference_suffix_cannot_break_negative_extraction():
    src = "premium product, exclude text, watermark REFERENCE IMAGE CONTROL: preserve exact product identity"
    out = prompt_compiler.compile_image_prompt(src, "Midjourney", "4:5")
    assert "--no text watermark" in out
    assert "REFERENCE IMAGE CONTROL" in out


def test_sd_compiler_separates_negative_prompt():
    out = prompt_compiler.compile_image_prompt("premium product, exclude text, watermark", "Stable Diffusion / FLUX", "4:5")
    assert "Positive prompt:" in out and "Negative prompt:" in out and "Aspect ratio: 4:5" in out


def test_hangul_typography_does_not_apply_blanket_text_ban():
    out = prompt_compiler.compile_image_prompt("Hangul poster, exclude text, letters, watermark, broken typography", "Midjourney", "3:2", allow_text=True, hangul_text="한글 디자인")
    low = out.lower()
    assert "--no text" not in low
    assert "--no letters" not in low
    assert "broken-typography" in low
    assert '"한글 디자인"' in out


def test_general_compiler_keeps_prose_not_mj_parameters():
    out = prompt_compiler.compile_image_prompt("premium product, exclude watermark", "ChatGPT / Gemini", "16:9")
    assert "Output aspect ratio: 16:9" in out and "--ar" not in out


def test_video_compiler_applies_aspect_and_model_guidance():
    out = prompt_compiler.compile_video_prompt("cinematic video prompt, aspect ratio: 1:1, stable subject", "Kling", "9:16")
    assert "Frame aspect ratio: 9:16" in out
    assert "Target Kling" in out
    assert "aspect ratio: 1:1" not in out


def test_symptom_correction_preserves_midjourney_parameters_at_end():
    out = prompt_compiler.apply_prompt_correction("premium watch --ar 4:5 --no watermark", "제품이 달라짐")
    assert "preserve the exact product identity" in out
    assert out.endswith("--ar 4:5 --no watermark")


def test_variant_axes_are_materially_distinct():
    assert len(runtime_quality.VARIANT_AXES) >= 6
    assert len(set(runtime_quality.VARIANT_AXES)) == len(runtime_quality.VARIANT_AXES)


def test_variant_respects_explicit_camera_and_lighting():
    axis = runtime_quality.VARIANT_AXES[1]
    text = runtime_quality.build_variant_direction(2, axis, "Neon", "Top View", True, False)
    assert "composition variation:" in text
    assert "lighting variation:" not in text
    assert "camera variation:" not in text
    assert "palette variation:" not in text


def _fake_app():
    def quick(*args, **kwargs): return "IMAGE", "VIDEO", "3D"
    def expert(*args, **kwargs): return "IMAGE", "VIDEO", "3D", "BLUEPRINT"
    return types.SimpleNamespace(_build_prompts=quick, _build_expert_prompt=expert, _tip_for=lambda preset: "tip", FAV_FILE="favorites.json", _fav_id=lambda: "1")


def test_install_is_idempotent_and_originals_are_captured_once():
    app = _fake_app()
    original_quick = app._build_prompts
    original_expert = app._build_expert_prompt
    runtime_quality.install(app)
    first_quick = app._build_prompts
    first_expert = app._build_expert_prompt
    assert app._hd_original_build_prompts is original_quick
    assert app._hd_original_build_expert_prompt is original_expert
    runtime_quality.install(app)
    assert app._build_prompts is first_quick
    assert app._build_expert_prompt is first_expert
    assert app._hd_original_build_prompts is original_quick
    assert app._hd_original_build_expert_prompt is original_expert


def test_repeated_generation_has_exactly_one_variant_prefix():
    app = _fake_app()
    runtime_quality.install(app)
    runtime_quality.reset_variant_counter()
    first = app._build_prompts(subject_en="watch", preset="매출형", work_mode="제품", lighting="AI 자동", camera="AI 자동")[0]
    second = app._build_prompts(subject_en="watch", preset="매출형", work_mode="제품", lighting="AI 자동", camera="AI 자동")[0]
    assert first.count("Variant ") == 1
    assert second.count("Variant ") == 1
    assert first != second


def test_minimum_streamlit_version_is_155():
    req = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert "streamlit>=1.55,<2.0" in req


def test_license_is_noncommercial_personal_use():
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "personal, non-commercial" in text
    assert "Commercial Use Prohibited" in text
