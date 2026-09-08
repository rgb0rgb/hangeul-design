from __future__ import annotations

from typing import Dict

# Hangeul Design cinematic product-video engine.
# The vocabulary follows general filmmaking practice (shot size, lens, camera movement,
# lighting, composition, temporal consistency) and does not copy third-party prompt text.

SHOT_OPTIONS: Dict[str, str] = {
    "AI 자동 (Auto)": "commercial hero framing chosen to best reveal the product",
    "히어로 샷 (Hero Shot)": "hero shot with the product as the unmistakable focal point",
    "클로즈업 (Close-Up)": "tight close-up emphasizing product form and surface detail",
    "익스트림 클로즈업 (Extreme Close-Up)": "extreme close-up revealing micro texture and material detail",
    "매크로 (Macro)": "macro product shot with shallow depth of field and tactile material detail",
    "아이레벨 (Eye Level)": "eye-level framing with a natural premium commercial perspective",
    "로우앵글 (Low Angle)": "low-angle hero framing that makes the product feel powerful and premium",
    "하이앵글 (High Angle)": "controlled high-angle composition that clearly shows product layout and interaction",
    "탑뷰 (Top View)": "top-down composition with clean graphic product placement",
    "오버숄더 (Over-the-Shoulder)": "over-the-shoulder framing showing a person naturally using the product",
    "POV": "first-person POV focused on believable product interaction",
    "와이드 환경 샷 (Wide Environment)": "wide environmental shot establishing lifestyle context while keeping the product readable",
}

CAMERA_MOVE_OPTIONS: Dict[str, str] = {
    "AI 자동 (Auto)": "one restrained camera move selected for clarity",
    "고정 (Locked)": "locked-off camera with no camera movement",
    "슬로우 돌리 인 (Slow Dolly-In)": "slow, precise dolly-in toward the product",
    "슬로우 돌리 아웃 (Slow Dolly-Out)": "slow dolly-out revealing the surrounding environment",
    "사이드 트래킹 (Side Tracking)": "smooth lateral tracking move with controlled parallax",
    "오빗 (Orbit)": "gentle partial orbit around the product, keeping geometry stable",
    "슬라이더 (Slider)": "short cinematic slider move across the product",
    "틸트 리빌 (Tilt Reveal)": "measured tilt reveal from detail to complete product form",
    "푸시인 + 랙포커스 (Push-In + Rack Focus)": "slow push-in with one deliberate rack-focus transition",
    "핸드헬드 라이프스타일 (Handheld Lifestyle)": "subtle natural handheld movement appropriate for a lifestyle commercial",
}

LENS_OPTIONS: Dict[str, str] = {
    "AI 자동 (Auto)": "cinematic commercial lens chosen for natural perspective",
    "24mm Wide": "24mm wide-angle lens, controlled distortion",
    "35mm": "35mm cinematic lens, immersive environmental perspective",
    "50mm": "50mm lens, natural perspective and balanced depth",
    "75mm": "75mm portrait-commercial lens with refined compression",
    "85mm": "85mm lens with premium compression and shallow depth of field",
    "100mm Macro": "100mm macro lens for precise product details",
    "Anamorphic": "anamorphic lens character with restrained horizontal flare and cinematic depth",
}

LIGHTING_OPTIONS: Dict[str, str] = {
    "AI 자동 (Auto)": "motivated premium commercial lighting with consistent shadows and reflections",
    "소프트 스튜디오 (Soft Studio)": "large soft key light, gentle fill, controlled product reflections",
    "하드 스튜디오 (Hard Studio)": "hard directional key light with crisp sculptural shadows",
    "림 라이트 (Rim Light)": "controlled rim lighting separating the product from the background",
    "윈도우 라이트 (Window Light)": "natural directional window light with soft falloff",
    "골든아워 (Golden Hour)": "warm golden-hour side light with realistic environmental bounce",
    "블루아워 (Blue Hour)": "cool blue-hour ambience with selective warm practical lights",
    "네온 (Neon)": "controlled neon accents and reflective highlights without obscuring product identity",
    "뷰티 소프트박스 (Beauty Softbox)": "beauty softbox lighting with clean skin tones and polished product highlights",
}

HUMAN_PRESENCE_OPTIONS: Dict[str, str] = {
    "없음 (Product Only)": "no person present; keep the product as the sole hero",
    "손만 (Hand Only)": "show only natural human hands interacting with the product",
    "상반신 (Upper Body)": "show a natural upper-body lifestyle model interacting with the product",
    "전신 모델 (Full Model)": "show a full human model naturally integrated into the product scene",
    "라이프스타일 모델 (Lifestyle Model)": "show a believable lifestyle model in a natural real-world context",
    "전문가/직업인 (Professional)": "show a believable professional whose role naturally supports product use",
}

INTERACTION_OPTIONS: Dict[str, str] = {
    "자동 (Auto)": "perform one simple, believable interaction appropriate to the product",
    "들고 있기 (Holding)": "hold the product naturally with anatomically correct hand contact",
    "착용 (Wearing)": "wear the product naturally with realistic fit, fabric or skin contact",
    "사용 (Using)": "use the product in one clear, believable action",
    "열기 (Opening)": "open the product or package with clear cause-and-effect motion",
    "언박싱 (Unboxing)": "perform a clean premium unboxing action while preserving package geometry",
    "마시기 (Drinking)": "drink naturally from the product with correct hand and mouth contact",
    "바르기 (Applying)": "apply the product naturally with accurate hand-to-face or hand-to-body contact",
    "시연 (Demonstrating)": "demonstrate one key product function with restrained purposeful movement",
    "걷기 + 제품 (Walking With Product)": "walk naturally while carrying or wearing the product; keep the product readable",
}

LOOK_OPTIONS: Dict[str, str] = {
    "프리미엄 광고 (Premium Commercial)": "premium global commercial aesthetic, refined art direction, restrained luxury",
    "럭셔리 (Luxury)": "luxury campaign aesthetic, elegant contrast, premium materials and finish",
    "테크 (Technology)": "clean advanced technology commercial, precise highlights, modern architectural styling",
    "K-뷰티 (K-Beauty)": "clean K-beauty advertising aesthetic, luminous skin, soft polished highlights",
    "패션 에디토리얼 (Fashion Editorial)": "high-end fashion editorial direction with confident composition",
    "라이프스타일 (Lifestyle)": "natural aspirational lifestyle commercial with believable lived-in detail",
    "푸드 광고 (Food Commercial)": "appetizing food-commercial styling, tactile texture, controlled steam and highlights",
    "미니멀 (Minimal)": "minimal premium set design with deliberate negative space",
    "시네마틱 드라마 (Cinematic Drama)": "cinematic dramatic mood with motivated lighting and controlled contrast",
}

MODEL_OPTIONS = ["General", "Veo", "Sora", "Runway", "Kling"]


def _model_note(model: str, duration: int) -> str:
    model = (model or "General").strip()
    if model == "Veo":
        return f"Target: Veo. Keep the shot executable as one coherent {duration}-second clip with one primary camera intention."
    if model == "Sora":
        return f"Target: Sora. Keep spatial continuity and subject identity stable across the {duration}-second shot."
    if model == "Runway":
        return f"Target: Runway. Prioritize a clear start frame, one camera path, and a clean final hero frame across {duration} seconds."
    if model == "Kling":
        return f"Target: Kling. Keep motion physically plausible, controlled, and temporally stable for {duration} seconds."
    return f"Technology-agnostic video prompt for a coherent {duration}-second commercial shot."


def build_cinematic_product_prompt(
    product: str,
    environment: str = "",
    shot: str = "AI 자동 (Auto)",
    camera_move: str = "AI 자동 (Auto)",
    lens: str = "AI 자동 (Auto)",
    lighting: str = "AI 자동 (Auto)",
    look: str = "프리미엄 광고 (Premium Commercial)",
    human_presence: str = "없음 (Product Only)",
    interaction: str = "자동 (Auto)",
    model: str = "General",
    duration: int = 8,
    brand: str = "",
) -> str:
    product = (product or "").strip()
    environment = (environment or "").strip()
    brand = (brand or "").strip()

    shot_phrase = SHOT_OPTIONS.get(shot, shot)
    move_phrase = CAMERA_MOVE_OPTIONS.get(camera_move, camera_move)
    lens_phrase = LENS_OPTIONS.get(lens, lens)
    lighting_phrase = LIGHTING_OPTIONS.get(lighting, lighting)
    look_phrase = LOOK_OPTIONS.get(look, look)
    human_phrase = HUMAN_PRESENCE_OPTIONS.get(human_presence, human_presence)
    interaction_phrase = INTERACTION_OPTIONS.get(interaction, interaction)

    scene = environment or "a visually coherent premium environment appropriate to the product"
    brand_rule = (
        f"Preserve the brand identity '{brand}' and do not invent alternate logos or packaging." if brand
        else "Do not invent random logos, labels, or unreadable typography."
    )

    return " ".join([
        f"Cinematic product commercial featuring {product}.",
        f"Scene: {scene}.",
        f"Shot design: {shot_phrase}.",
        f"Camera movement: {move_phrase}; use only this primary movement and avoid conflicting camera instructions.",
        f"Lens: {lens_phrase}.",
        f"Lighting: {lighting_phrase}.",
        f"Art direction: {look_phrase}.",
        f"Human presence: {human_phrase}.",
        f"Human-product interaction: {interaction_phrase}.",
        "Product fidelity: preserve exact product silhouette, proportions, materials, surface finish, color, packaging geometry, and readable visual identity across every frame.",
        "Contact realism: hands, fingers, clothing, skin, and the product must make physically believable contact without intersections, floating objects, extra fingers, or warped geometry.",
        "Motion discipline: one primary product action, at most one secondary beat, stable temporal continuity, realistic inertia, controlled reflections, and no sudden scene changes.",
        "Composition: clear foreground-midground-background separation, purposeful negative space, realistic depth of field, and a clean final product-readable frame.",
        brand_rule,
        _model_note(model, int(duration)),
        "Avoid flicker, identity drift, duplicate products, morphing objects, unstable hands, warped faces, random text, watermarks, camera jitter, abrupt zooms, and conflicting motion.",
    ])


def build_product_plus_human_variant(
    product: str,
    environment: str = "",
    shot: str = "오버숄더 (Over-the-Shoulder)",
    camera_move: str = "슬로우 돌리 인 (Slow Dolly-In)",
    lens: str = "85mm",
    lighting: str = "소프트 스튜디오 (Soft Studio)",
    look: str = "프리미엄 광고 (Premium Commercial)",
    interaction: str = "사용 (Using)",
    model: str = "General",
    duration: int = 8,
    brand: str = "",
) -> str:
    return build_cinematic_product_prompt(
        product=product,
        environment=environment,
        shot=shot,
        camera_move=camera_move,
        lens=lens,
        lighting=lighting,
        look=look,
        human_presence="라이프스타일 모델 (Lifestyle Model)",
        interaction=interaction,
        model=model,
        duration=duration,
        brand=brand,
    )
