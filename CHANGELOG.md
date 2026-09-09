# Changelog

## 1.2.0 - in development

- Added three-question beginner auto-configuration for subject, destination, and desired visual feel.
- Made beginner auto-configuration render-order independent with a pending-settings queue and rerun application step.
- Added target image compiler for ChatGPT/Gemini, Midjourney, and Stable Diffusion/FLUX.
- Added main video prompt compiler for General, Veo, Sora, Runway, and Kling.
- Added direct aspect-ratio selection and tool-specific aspect output.
- Fixed expert `avoid ...` negative clauses so real expert negatives are moved into Midjourney/SD negative controls instead of falling back to generic defaults.
- Made reference-image directives compatible with negative extraction and ensured Midjourney `--ar` / `--no` parameters remain at the end of the final prompt.
- Fixed Hangul typography conflict with blanket text/letter exclusions while retaining useful malformed-text constraints.
- Added visible Hangul rendering warning and reliable post-overlay guidance.
- Unified Hangeul Design and Cinematic Design into one Streamlit application on port 8504 with top-level tabs.
- Removed the obsolete secondary `app_reference.py`, `run_cinematic.bat`, and `stop_cinematic.bat` entry paths.
- Updated the launcher to start the unified `app_cinematic.py` entry point.
- Added regression tests for expert negatives, reference suffixes, video aspect/model guidance, correction preservation, one-time runtime wrapper capture, repeated reruns, and beginner-button state application.
- CI tests both the declared minimum Streamlit version and the supported dependency set, including real beginner-button interaction through AppTest.

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
- Separated Hangeul Design (8504) and Cinematic (8505) ports. This architecture was superseded by the unified v1.2 application.

## 1.0.0

- Created Hangeul Design as a separate project from the original DesignPD folder.
- Added Hangul-focused presets, work modes, and image styles.
- Added expert prompt engine with concept spine, exact Hangul copy, HEX palette, continuity, and detail-density controls.
- Added image, video, 3D, and structure output tabs.
- Added local favorites/templates and report export.
- Added Windows `run.bat` and executable launcher build script.
