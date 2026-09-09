import ast
import types
from pathlib import Path

import runtime_quality


ROOT = Path(__file__).resolve().parents[1]


def test_python_sources_parse():
    for name in ["app.py", "app_reference.py", "app_cinematic.py", "cinematic_product.py", "reference_image.py", "runtime_quality.py", "launcher.py"]:
        ast.parse((ROOT / name).read_text(encoding="utf-8"))


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
    assert "35mm" not in text
    assert "hard side light" not in text


def test_auto_axes_receive_real_variation():
    axis = runtime_quality.VARIANT_AXES[2]
    text = runtime_quality.build_variant_direction(3, axis, "AI 자동", "AI 자동", False, False)
    assert "lighting variation:" in text
    assert "camera variation:" in text
    assert "palette variation:" in text


def _fake_app():
    def quick(*args, **kwargs):
        return "IMAGE", "VIDEO", "3D"

    def expert(*args, **kwargs):
        return "IMAGE", "VIDEO", "3D", "BLUEPRINT"

    return types.SimpleNamespace(
        _build_prompts=quick,
        _build_expert_prompt=expert,
        _tip_for=lambda preset: "tip",
        FAV_FILE="favorites.json",
        _fav_id=lambda: "1",
    )


def test_install_is_idempotent_and_does_not_stack_wrappers():
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
