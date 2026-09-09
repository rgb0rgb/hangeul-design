# Changelog

## 1.2.0 - in development

- Added three-question beginner auto-configuration for subject, destination, and desired visual feel.
- Added target image compiler for ChatGPT/Gemini, Midjourney, and Stable Diffusion/FLUX.
- Added main video prompt compiler for General, Veo, Sora, Runway, and Kling.
- Added direct aspect-ratio selection and tool-specific aspect output.
- Fixed expert `avoid ...` negative clauses so real expert negatives are moved into Midjourney/SD negative controls instead of falling back to generic defaults.
- Made negative extraction independent of reference-image directives by compiling before reference instructions are appended.
- Fixed Hangul typography conflict with blanket text/letter exclusions while retaining useful malformed-text constraints.
- Added visible Hangul rendering warning and reliable post-overlay guidance.
- Unified beginner/compiler controls across the 8504 and 8505 entry points.
- Added regression tests for expert negatives, reference suffixes, video aspect/model guidance, correction preservation, and one-time runtime wrapper capture.
- Documented `stop.bat`, `stop_cinematic.bat`, ports, compiler workflow, and reference-image handoff.

## 1.1.0 - 2026-09

- Added Cinematic Product Video prompt generation with shot, movement, lens, lighting, human presence, and interaction controls.
- Added shared JPG/PNG/BMP/WEBP/GIF/TIF/TIFF reference-image workflow.
- Added Personal Non-Commercial License for free personal use; commercial use requires permission.
- Fixed favorites/template application timing under Streamlit session state.
- Fixed expert custom-style propagation.
- Raised the supported Streamlit minimum to 1.55.
- Made the runtime quality layer idempotent so Streamlit reruns cannot stack prompt wrappers.
- Changed prompt variants to respect explicit camera, lighting, and palette selections; automatic axes vary only when applicable.
- Added regression tests and CI AppTest coverage.
- Fixed frozen launcher recursion by using the project virtual-environment Python.
- Separated Hangeul Design (8504) and Cinematic (8505) ports.

## 1.0.0

- Created Hangeul Design as a separate project from the original DesignPD folder.
- Added Hangul-focused presets, work modes, and image styles.
- Added expert prompt engine with concept spine, exact Hangul copy, HEX palette, continuity, and detail-density controls.
- Added image, video, 3D, and structure output tabs.
- Added local favorites/templates and report export.
- Added Windows `run.bat` and executable launcher build script.
