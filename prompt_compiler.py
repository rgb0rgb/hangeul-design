from __future__ import annotations

import re
from typing import Tuple

TARGET_IMAGE_MODELS = [
    "ChatGPT / Gemini",
    "Midjourney",
    "Stable Diffusion / FLUX",
]


def normalize_aspect(aspect: str) -> str:
    value = (aspect or "1:1").split()[0].strip()
    return value if re.fullmatch(r"\d+:\d+", value) else "1:1"


def _split_exclusions(prompt: str) -> Tuple[str, list[str]]:
    text = (prompt or "").strip()
    m = re.search(r"(?:^|[,.]\s*)exclude\s+([^.]*)\.?\s*$", text, flags=re.I)
    if not m:
        return text, []
    raw = m.group(1)
    items = [x.strip(" ,") for x in raw.split(",") if x.strip(" ,")]
    body = (text[: m.start()] + text[m.end() :]).strip(" ,.")
    return body, items


def _clean_text_negatives(items: list[str], allow_text: bool) -> list[str]:
    if not allow_text:
        return items
    blocked = ("text", "letter", "typography", "broken typography")
    return [item for item in items if not any(word in item.lower() for word in blocked)]


def compile_image_prompt(
    prompt: str,
    target_model: str,
    aspect: str,
    allow_text: bool = False,
    hangul_text: str = "",
) -> str:
    """Compile one generic Hangeul Design image prompt for the selected generator."""
    body, negatives = _split_exclusions(prompt)
    negatives = _clean_text_negatives(negatives, allow_text)
    ratio = normalize_aspect(aspect)

    if allow_text:
        exact = (hangul_text or "").strip()
        if exact:
            body += f' Preserve this exact Korean text as a primary design element: "{exact}". Keep Hangul glyph structure, spacing, and readability accurate.'
        else:
            body += " Hangul typography is intentional; do not remove Korean lettering or treat it as an artifact."

    model = target_model or TARGET_IMAGE_MODELS[0]

    if model == "Midjourney":
        no_items = negatives or ["watermark", "signature", "random logos", "low resolution", "muddy details"]
        no_clause = " --no " + " ".join(x.replace(" ", "-") for x in no_items)
        return f"{body} --ar {ratio}{no_clause}".strip()

    if model == "Stable Diffusion / FLUX":
        neg = ", ".join(negatives) if negatives else "watermark, signature, random logos, low resolution, muddy details"
        return f"Positive prompt:\n{body}\n\nNegative prompt:\n{neg}\n\nAspect ratio: {ratio}"

    if negatives:
        body += " Avoid: " + ", ".join(negatives) + "."
    body += f" Output aspect ratio: {ratio}."
    return body.strip()
