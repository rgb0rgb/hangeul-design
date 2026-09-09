# Changelog

## 1.1.0 - 2026-09

- Added Cinematic Product Video prompt generation with shot, movement, lens, lighting, human presence, and interaction controls.
- Added shared JPG/PNG/BMP/WEBP/GIF/TIF/TIFF reference-image workflow.
- Added Personal Non-Commercial License for free personal use; commercial use requires permission.
- Fixed favorites/template application timing under Streamlit session state.
- Fixed expert custom-style propagation.
- Raised the supported Streamlit minimum to 1.55.
- Made the runtime quality layer idempotent so Streamlit reruns cannot stack prompt wrappers.
- Changed prompt variants to respect explicit camera, lighting, and palette selections; automatic axes vary only when applicable.
- Added regression tests for repeated generation, wrapper idempotence, variant conflicts, and minimum dependency declaration.
- Added CI jobs for Streamlit 1.55 minimum and supported-latest, with two consecutive AppTest runs.
- Fixed frozen launcher recursion by using the project virtual-environment Python.
- Separated Hangeul Design (8504) and Cinematic (8505) ports and delayed browser launch until Streamlit health is ready.
- Hardened clipboard JavaScript encoding and translation caching.

## 1.0.0

- Created Hangeul Design as a separate project from the original DesignPD folder.
- Added Hangul-focused presets, work modes, and image styles.
- Added expert prompt engine with concept spine, exact Hangul copy, HEX palette, continuity, and detail-density controls.
- Added sidebar help popovers for presets, engines, work modes, styles, and expert fields.
- Added image, video, 3D, and structure output tabs.
- Added local favorites/templates and report export.
- Added Windows `run.bat` and executable launcher build script.
