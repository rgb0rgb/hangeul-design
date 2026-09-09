import ast
from pathlib import Path

import runtime_quality


ROOT = Path(__file__).resolve().parents[1]


def test_python_sources_parse():
    for name in ["app.py", "app_reference.py", "app_cinematic.py", "cinematic_product.py", "reference_image.py", "runtime_quality.py", "launcher.py"]:
        ast.parse((ROOT / name).read_text(encoding="utf-8"))


def test_variant_axes_are_materially_distinct():
    assert len(runtime_quality.VARIANT_AXES) >= 6
    assert len(set(runtime_quality.VARIANT_AXES)) == len(runtime_quality.VARIANT_AXES)
    compositions = {x[0] for x in runtime_quality.VARIANT_AXES}
    lights = {x[1] for x in runtime_quality.VARIANT_AXES}
    cameras = {x[2] for x in runtime_quality.VARIANT_AXES}
    palettes = {x[3] for x in runtime_quality.VARIANT_AXES}
    assert len(compositions) >= 6
    assert len(lights) >= 6
    assert len(cameras) >= 6
    assert len(palettes) >= 6


def test_license_is_noncommercial_personal_use():
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "personal, non-commercial" in text
    assert "Commercial Use Prohibited" in text
