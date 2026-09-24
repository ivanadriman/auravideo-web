from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class FilterParams:
    # Preset
    preset_name: str = "Bright & Pretty"
    intensity: float = 1.0  # Master blend: 0.0 (original) -> 1.0 (full effect)

    # Light & Tone
    exposure: float = 0.0           # -2.0 to +2.0 EV
    smart_brightness: float = 0.25  # 0.0 to 1.0 (adaptive shadow lift)
    highlight_recovery: float = 0.2 # 0.0 to 1.0 (prevents white clipping)
    contrast: float = 1.10          # 0.5 to 2.0 (filmic S-curve)

    # Color & Balance
    temperature: float = 8.0        # -100 to +100 (Cool/Cyan <-> Warm/Amber)
    tint: float = 2.0               # -100 to +100 (Green <-> Magenta)
    vibrance: float = 0.25          # -1.0 to +1.0 (skin-safe saturation boost)
    saturation: float = 1.05        # 0.0 to 2.0 (global saturation)

    # Atmosphere & Effects
    bloom_strength: float = 0.18    # 0.0 to 1.0 (soft romantic glow)
    film_grain: float = 0.0         # 0.0 to 1.0 (analog 35mm grain)
    vignette: float = 0.10          # 0.0 to 1.0 (lens edge falloff)
    sharpness: float = 0.20         # 0.0 to 2.0 (crisp edge micro-contrast)

    # Output / Export settings
    codec: str = "Auto (NVENC / x264)"
    crf: int = 18
    encoder_preset: str = "p4 - Medium"

    def copy(self) -> 'FilterParams':
        return FilterParams(**self.__dict__)


# =========================================================================
# Curated Preset Definitions (Categorized & Expert-Tuned)
# =========================================================================
PRESET_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    # ---------------------------------------------------------------------
    # 0. Low-Light & Intimate Indoor (Tailored for Ambient Bedroom / Evening)
    # ---------------------------------------------------------------------
    "Warm Intimate Bedroom": {
        "label": "Warm Intimate Bedroom",
        "badge": "🕯️ Warm Intimate",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Tailored for low-light & bedroom footage: lifts underexposed shadows without digital noise blowout, warms skin tones, and softens ambient light with gentle aesthetic glow.",
        "params": {
            "exposure": 0.35, "smart_brightness": 0.55, "highlight_recovery": 0.45, "contrast": 1.05,
            "temperature": 16.0, "tint": 6.0, "vibrance": 0.32, "saturation": 1.08,
            "bloom_strength": 0.18, "film_grain": 0.0, "vignette": 0.08, "sharpness": 0.30,
        }
    },
    "Midnight Clarity": {
        "label": "Midnight Clarity",
        "badge": "💎 Midnight Clean",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "De-muddies dark indoor scenes: aggressive shadow recovery, balanced neutral whites, and crisp micro-contrast clarity while protecting bedding and skin highlights.",
        "params": {
            "exposure": 0.40, "smart_brightness": 0.62, "highlight_recovery": 0.42, "contrast": 1.10,
            "temperature": -2.0, "tint": 4.0, "vibrance": 0.25, "saturation": 1.04,
            "bloom_strength": 0.12, "film_grain": 0.0, "vignette": 0.06, "sharpness": 0.42,
        }
    },
    "Golden Candlelight": {
        "label": "Golden Candlelight",
        "badge": "🍯 Honey Glow",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Luminous amber and honey midtones for evening indoor footage: illuminates shadowed bodies with radiant golden warmth and velvety contrast.",
        "params": {
            "exposure": 0.28, "smart_brightness": 0.48, "highlight_recovery": 0.40, "contrast": 1.12,
            "temperature": 28.0, "tint": 10.0, "vibrance": 0.38, "saturation": 1.14,
            "bloom_strength": 0.22, "film_grain": 0.04, "vignette": 0.12, "sharpness": 0.25,
        }
    },
    "Soft Velvet Boudoir": {
        "label": "Soft Velvet Boudoir",
        "badge": "🍷 Velvet Boudoir",
        "category": "Cinema",
        "recommended": False,
        "description": "Atmospheric boudoir aesthetic: lifted smoky blacks, subtle rose-tinted diffusion, and filmic soft roll-off for private indoor moments.",
        "params": {
            "exposure": 0.25, "smart_brightness": 0.58, "highlight_recovery": 0.50, "contrast": 0.98,
            "temperature": 8.0, "tint": 14.0, "vibrance": 0.20, "saturation": 0.96,
            "bloom_strength": 0.26, "film_grain": 0.05, "vignette": 0.10, "sharpness": 0.20,
        }
    },
    # ---------------------------------------------------------------------
    # 0b. Bright & High-Clarity Indoor (Radiant Detail without Clipping)
    # ---------------------------------------------------------------------
    "Radiant Clean Clarity": {
        "label": "Radiant Clean Clarity",
        "badge": "☀️ Radiant Clean",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Transforms dark, murky scenes into bright, clean, vivid footage: high shadow boost with deep S-curve contrast, crisp micro-edge detail, and soft highlight protection.",
        "params": {
            "exposure": 0.38, "smart_brightness": 0.62, "highlight_recovery": 0.55, "contrast": 1.24,
            "temperature": 8.0, "tint": 4.0, "vibrance": 0.36, "saturation": 1.12,
            "bloom_strength": 0.08, "film_grain": 0.0, "vignette": 0.04, "sharpness": 0.48,
        }
    },
    "Golden Sunlit Warmth": {
        "label": "Golden Sunlit Warmth",
        "badge": "🌅 Sunlit Warmth",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Bright, sun-drenched illumination for underexposed rooms: rich amber midtone brilliance, rich contrast, and luminous skin glow without digital clipping.",
        "params": {
            "exposure": 0.32, "smart_brightness": 0.58, "highlight_recovery": 0.52, "contrast": 1.28,
            "temperature": 24.0, "tint": 8.0, "vibrance": 0.42, "saturation": 1.16,
            "bloom_strength": 0.12, "film_grain": 0.0, "vignette": 0.08, "sharpness": 0.42,
        }
    },
    "High-Key Studio Glow": {
        "label": "High-Key Studio Glow",
        "badge": "💡 Studio Glow",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Luminous high-key aesthetic: lifts shadows aggressively with a gentle porcelain bloom, soft highlight knee, and rosy skin warmth for high-end look.",
        "params": {
            "exposure": 0.45, "smart_brightness": 0.65, "highlight_recovery": 0.68, "contrast": 1.18,
            "temperature": 4.0, "tint": 6.0, "vibrance": 0.28, "saturation": 1.06,
            "bloom_strength": 0.18, "film_grain": 0.0, "vignette": 0.04, "sharpness": 0.38,
        }
    },
    "Crisp Vivid Brilliance": {
        "label": "Crisp Vivid Brilliance",
        "badge": "⚡ Vivid Brilliance",
        "category": "Social & Beauty",
        "recommended": False,
        "description": "Maximum visual punch & de-fogging: punchy contrast, sharp texture definition, and rich color saturation that brings out hidden room details.",
        "params": {
            "exposure": 0.35, "smart_brightness": 0.56, "highlight_recovery": 0.50, "contrast": 1.32,
            "temperature": -2.0, "tint": 2.0, "vibrance": 0.48, "saturation": 1.22,
            "bloom_strength": 0.06, "film_grain": 0.0, "vignette": 0.05, "sharpness": 0.55,
        }
    },

    # ---------------------------------------------------------------------
    # 1. Clean & Beauty / Social Media (Instagram, TikTok, Reels)
    # ---------------------------------------------------------------------
    "Bright & Pretty": {
        "label": "Bright & Pretty",
        "badge": "✨ Clean Glow",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Recommended: Lifts dark shadows naturally, protects skin tones, adds a soft aesthetic bloom and crisp clarity.",
        "params": {
            "exposure": 0.15, "smart_brightness": 0.38, "highlight_recovery": 0.32, "contrast": 1.08,
            "temperature": 10.0, "tint": 4.0, "vibrance": 0.30, "saturation": 1.06,
            "bloom_strength": 0.22, "film_grain": 0.0, "vignette": 0.08, "sharpness": 0.25,
        }
    },
    "Soft Porcelain (K-Beauty)": {
        "label": "Soft Porcelain (K-Beauty)",
        "badge": "🌸 K-Beauty Clean",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Milky, luminous skin tones with lifted highlights, clean desaturated shadows, and a gentle aesthetic glow.",
        "params": {
            "exposure": 0.22, "smart_brightness": 0.42, "highlight_recovery": 0.40, "contrast": 1.02,
            "temperature": 2.0, "tint": 8.0, "vibrance": 0.12, "saturation": 0.94,
            "bloom_strength": 0.30, "film_grain": 0.0, "vignette": 0.05, "sharpness": 0.15,
        }
    },
    "Latte Girl / Warm Vanilla": {
        "label": "Latte Girl / Warm Vanilla",
        "badge": "☕ Vanilla Latte",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Trending warm cozy aesthetic: creamy beige tones, rich caramel midtones, and soft sun-kissed warmth.",
        "params": {
            "exposure": 0.10, "smart_brightness": 0.30, "highlight_recovery": 0.28, "contrast": 1.06,
            "temperature": 26.0, "tint": 8.0, "vibrance": 0.22, "saturation": 1.04,
            "bloom_strength": 0.20, "film_grain": 0.06, "vignette": 0.12, "sharpness": 0.18,
        }
    },
    "Golden Hour Radiance": {
        "label": "Golden Hour Radiance",
        "badge": "🌅 Golden Hour",
        "category": "Social & Beauty",
        "recommended": True,
        "description": "Warm, luminous late-afternoon sunlight with glowing amber highlights and gentle cinematic contrast.",
        "params": {
            "exposure": 0.12, "smart_brightness": 0.25, "highlight_recovery": 0.35, "contrast": 1.12,
            "temperature": 38.0, "tint": 10.0, "vibrance": 0.35, "saturation": 1.14,
            "bloom_strength": 0.26, "film_grain": 0.05, "vignette": 0.18, "sharpness": 0.18,
        }
    },
    "Y2K Digicam Flash": {
        "label": "Y2K Digicam Flash",
        "badge": "📸 Y2K Digicam",
        "category": "Social & Beauty",
        "recommended": False,
        "description": "Early 2000s direct flash snapshot look: punchy primary colors, crisp digital contrast, and cool flash highlights.",
        "params": {
            "exposure": 0.18, "smart_brightness": 0.10, "highlight_recovery": 0.15, "contrast": 1.28,
            "temperature": -8.0, "tint": 6.0, "vibrance": 0.35, "saturation": 1.20,
            "bloom_strength": 0.25, "film_grain": 0.12, "vignette": 0.06, "sharpness": 0.40,
        }
    },
    "Pastel Dream Bloom": {
        "label": "Pastel Dream Bloom",
        "badge": "🍬 Pastel Dream",
        "category": "Social & Beauty",
        "recommended": False,
        "description": "Lifted blacks, soft light diffusion, and gentle cotton-candy pastel tonality for music videos and aesthetics.",
        "params": {
            "exposure": 0.18, "smart_brightness": 0.45, "highlight_recovery": 0.40, "contrast": 0.95,
            "temperature": 5.0, "tint": 15.0, "vibrance": 0.15, "saturation": 0.92,
            "bloom_strength": 0.40, "film_grain": 0.08, "vignette": 0.05, "sharpness": 0.08,
        }
    },
    "Matcha & Sage Minimal": {
        "label": "Matcha & Sage Minimal",
        "badge": "🍵 Matcha Clean",
        "category": "Social & Beauty",
        "recommended": False,
        "description": "Modern minimalist aesthetic: desaturated greens, clean muted tones, crisp lighting, and quiet elegance.",
        "params": {
            "exposure": 0.08, "smart_brightness": 0.22, "highlight_recovery": 0.30, "contrast": 1.05,
            "temperature": -10.0, "tint": -12.0, "vibrance": -0.10, "saturation": 0.88,
            "bloom_strength": 0.12, "film_grain": 0.04, "vignette": 0.10, "sharpness": 0.25,
        }
    },
    "Vivid Pop Feed Stopper": {
        "label": "Vivid Pop Feed Stopper",
        "badge": "⚡ Vivid Pop",
        "category": "Social & Beauty",
        "recommended": False,
        "description": "High dynamic vibrance, rich color separation, deep contrast, and punchy clarity that stops scrollers.",
        "params": {
            "exposure": 0.05, "smart_brightness": 0.20, "highlight_recovery": 0.25, "contrast": 1.22,
            "temperature": 4.0, "tint": 0.0, "vibrance": 0.45, "saturation": 1.25,
            "bloom_strength": 0.10, "film_grain": 0.0, "vignette": 0.12, "sharpness": 0.45,
        }
    },

    # ---------------------------------------------------------------------
    # 2. Cinema & Film Director Looks
    # ---------------------------------------------------------------------
    "Cinematic Teal & Orange": {
        "label": "Cinematic Teal & Orange",
        "badge": "🎬 Hollywood Teal",
        "category": "Cinema",
        "recommended": True,
        "description": "The blockbuster staple: warm glowing skin tones complemented by deep teal shadows and rich contrast.",
        "params": {
            "exposure": 0.0, "smart_brightness": 0.10, "highlight_recovery": 0.25, "contrast": 1.28,
            "temperature": 24.0, "tint": -6.0, "vibrance": 0.28, "saturation": 1.15,
            "bloom_strength": 0.12, "film_grain": 0.12, "vignette": 0.22, "sharpness": 0.35,
        }
    },
    "Wong Kar-wai (Neon Romance)": {
        "label": "Wong Kar-wai (Neon Romance)",
        "badge": "🏮 Neon Romance",
        "category": "Cinema",
        "recommended": True,
        "description": "In The Mood For Love aesthetic: lush warm greens, romantic amber highlights, nostalgic moody shadows.",
        "params": {
            "exposure": -0.05, "smart_brightness": 0.15, "highlight_recovery": 0.30, "contrast": 1.24,
            "temperature": 18.0, "tint": -16.0, "vibrance": 0.32, "saturation": 1.18,
            "bloom_strength": 0.32, "film_grain": 0.22, "vignette": 0.28, "sharpness": 0.20,
        }
    },
    "Bleach Bypass (Gritty War)": {
        "label": "Bleach Bypass (Gritty War)",
        "badge": "🛡️ Bleach Bypass",
        "category": "Cinema",
        "recommended": False,
        "description": "Classic silver-retention film processing: extreme contrast, desaturated cold colors, and gritty intense textures.",
        "params": {
            "exposure": 0.0, "smart_brightness": -0.15, "highlight_recovery": 0.35, "contrast": 1.45,
            "temperature": -12.0, "tint": -4.0, "vibrance": -0.40, "saturation": 0.65,
            "bloom_strength": 0.05, "film_grain": 0.25, "vignette": 0.32, "sharpness": 0.50,
        }
    },
    "Fincher Mood (Matrix Green)": {
        "label": "Fincher Mood (Matrix Green)",
        "badge": "🟢 Fincher Green",
        "category": "Cinema",
        "recommended": False,
        "description": "David Fincher / Matrix psychological thriller vibe: atmospheric olive-green cast with deep inky blacks.",
        "params": {
            "exposure": -0.12, "smart_brightness": 0.05, "highlight_recovery": 0.30, "contrast": 1.30,
            "temperature": -10.0, "tint": -22.0, "vibrance": 0.10, "saturation": 0.95,
            "bloom_strength": 0.14, "film_grain": 0.18, "vignette": 0.30, "sharpness": 0.35,
        }
    },
    "Wes Anderson (Storybook)": {
        "label": "Wes Anderson (Storybook)",
        "badge": "🎨 Wes Storybook",
        "category": "Cinema",
        "recommended": False,
        "description": "Whimsical storybook palette: warm pastel yellows, salmon-peach highlights, lifted shadows, and gentle nostalgia.",
        "params": {
            "exposure": 0.14, "smart_brightness": 0.32, "highlight_recovery": 0.25, "contrast": 1.04,
            "temperature": 32.0, "tint": 12.0, "vibrance": 0.28, "saturation": 1.10,
            "bloom_strength": 0.18, "film_grain": 0.10, "vignette": 0.12, "sharpness": 0.20,
        }
    },
    "Gotham Dark Knight": {
        "label": "Gotham Dark Knight",
        "badge": "🦇 Gotham Dark",
        "category": "Cinema",
        "recommended": False,
        "description": "Christopher Nolan brooding superhero look: desaturated steel blues, cold shadows, and sharp architectural edges.",
        "params": {
            "exposure": -0.15, "smart_brightness": -0.08, "highlight_recovery": 0.35, "contrast": 1.35,
            "temperature": -25.0, "tint": 0.0, "vibrance": -0.20, "saturation": 0.78,
            "bloom_strength": 0.08, "film_grain": 0.18, "vignette": 0.35, "sharpness": 0.42,
        }
    },
    "Film Noir / Silver Screen": {
        "label": "Film Noir / Silver Screen",
        "badge": "🎩 Classic Noir",
        "category": "Cinema",
        "recommended": False,
        "description": "Timeless 1940s black and white cinema: rich deep blacks, glowing silver highlights, and authentic medium grain.",
        "params": {
            "exposure": 0.0, "smart_brightness": 0.05, "highlight_recovery": 0.35, "contrast": 1.40,
            "temperature": 0.0, "tint": 0.0, "vibrance": -1.0, "saturation": 0.0,
            "bloom_strength": 0.18, "film_grain": 0.25, "vignette": 0.35, "sharpness": 0.30,
        }
    },

    # ---------------------------------------------------------------------
    # 3. Vintage Cameras & Analog Film Stocks
    # ---------------------------------------------------------------------
    "Kodak Portra 400": {
        "label": "Kodak Portra 400",
        "badge": "🎞️ Portra 400",
        "category": "Vintage & Film",
        "recommended": True,
        "description": "The legendary portrait film: natural warm skin tones, soft pastel highlights, organic fine grain, and subtle contrast.",
        "params": {
            "exposure": 0.08, "smart_brightness": 0.25, "highlight_recovery": 0.28, "contrast": 1.10,
            "temperature": 16.0, "tint": 4.0, "vibrance": 0.15, "saturation": 1.02,
            "bloom_strength": 0.14, "film_grain": 0.20, "vignette": 0.15, "sharpness": 0.22,
        }
    },
    "CineStill 800T (Halation)": {
        "label": "CineStill 800T (Halation)",
        "badge": "🌃 CineStill 800T",
        "category": "Vintage & Film",
        "recommended": True,
        "description": "Tungsten balanced movie stock: cool blue shadows paired with red/amber halation bloom around street lamps and neon.",
        "params": {
            "exposure": 0.02, "smart_brightness": 0.15, "highlight_recovery": 0.20, "contrast": 1.25,
            "temperature": -18.0, "tint": 8.0, "vibrance": 0.30, "saturation": 1.12,
            "bloom_strength": 0.35, "film_grain": 0.25, "vignette": 0.25, "sharpness": 0.25,
        }
    },
    "Fujifilm Superia 1600": {
        "label": "Fujifilm Superia 1600",
        "badge": "📷 Fuji Superia",
        "category": "Vintage & Film",
        "recommended": False,
        "description": "Moody street photography film: vivid crisp greens, cool cyan shadows, vibrant red pops, and gritty organic grain.",
        "params": {
            "exposure": 0.0, "smart_brightness": 0.10, "highlight_recovery": 0.20, "contrast": 1.20,
            "temperature": -8.0, "tint": -10.0, "vibrance": 0.25, "saturation": 1.08,
            "bloom_strength": 0.10, "film_grain": 0.32, "vignette": 0.22, "sharpness": 0.30,
        }
    },
    "Kodachrome 64 Vintage": {
        "label": "Kodachrome 64 Vintage",
        "badge": "📼 Kodachrome 64",
        "category": "Vintage & Film",
        "recommended": False,
        "description": "1970s National Geographic color transparency: deep saturated reds and yellows, rich nostalgic contrast.",
        "params": {
            "exposure": 0.05, "smart_brightness": 0.12, "highlight_recovery": 0.22, "contrast": 1.24,
            "temperature": 22.0, "tint": -4.0, "vibrance": 0.35, "saturation": 1.18,
            "bloom_strength": 0.12, "film_grain": 0.22, "vignette": 0.26, "sharpness": 0.28,
        }
    },
    "Polaroid 600 Instant": {
        "label": "Polaroid 600 Instant",
        "badge": "📦 Polaroid 600",
        "category": "Vintage & Film",
        "recommended": False,
        "description": "Classic instant camera: lifted creamy matte blacks, warm retro color cast, soft edges, and analog nostalgia.",
        "params": {
            "exposure": 0.12, "smart_brightness": 0.35, "highlight_recovery": 0.30, "contrast": 1.02,
            "temperature": 20.0, "tint": 6.0, "vibrance": 0.05, "saturation": 0.94,
            "bloom_strength": 0.25, "film_grain": 0.22, "vignette": 0.32, "sharpness": 0.10,
        }
    },
    "VHS 1980s Camcorder": {
        "label": "VHS 1980s Camcorder",
        "badge": "📹 VHS Tape",
        "category": "Vintage & Film",
        "recommended": False,
        "description": "Retro magnetic tape look: warm greenish-cyan color balance, lifted darks, soft analog glow, and tape character.",
        "params": {
            "exposure": 0.10, "smart_brightness": 0.28, "highlight_recovery": 0.22, "contrast": 1.12,
            "temperature": -4.0, "tint": -15.0, "vibrance": 0.18, "saturation": 1.08,
            "bloom_strength": 0.28, "film_grain": 0.26, "vignette": 0.18, "sharpness": 0.12,
        }
    },
    "Super 8mm Home Movie": {
        "label": "Super 8mm Home Movie",
        "badge": "🎞️ Super 8mm",
        "category": "Vintage & Film",
        "recommended": False,
        "description": "Sun-bleached 1960s home movie reel: golden-sepia warmth, heavy organic film grain, soft focus, and heavy vignette.",
        "params": {
            "exposure": 0.15, "smart_brightness": 0.32, "highlight_recovery": 0.25, "contrast": 1.15,
            "temperature": 42.0, "tint": 12.0, "vibrance": -0.05, "saturation": 0.95,
            "bloom_strength": 0.30, "film_grain": 0.40, "vignette": 0.38, "sharpness": 0.08,
        }
    },

    # ---------------------------------------------------------------------
    # 4. Stylized & Atmospheric FX
    # ---------------------------------------------------------------------
    "Cyberpunk Neo Tokyo": {
        "label": "Cyberpunk Neo Tokyo",
        "badge": "⚡ Cyberpunk",
        "category": "Stylized & FX",
        "recommended": True,
        "description": "High contrast night-city vibe with electric magentas, cyan shadows, glowing neon bloom, and crisp details.",
        "params": {
            "exposure": -0.05, "smart_brightness": 0.08, "highlight_recovery": 0.15, "contrast": 1.34,
            "temperature": -28.0, "tint": 28.0, "vibrance": 0.50, "saturation": 1.35,
            "bloom_strength": 0.35, "film_grain": 0.14, "vignette": 0.25, "sharpness": 0.35,
        }
    },
    "Midnight Blue Hour": {
        "label": "Midnight Blue Hour",
        "badge": "🌌 Blue Hour",
        "category": "Stylized & FX",
        "recommended": False,
        "description": "Atmospheric evening twilights: deep indigo sky, cold shadows, contrasted with warm glowing architectural windows.",
        "params": {
            "exposure": -0.10, "smart_brightness": 0.05, "highlight_recovery": 0.28, "contrast": 1.25,
            "temperature": -42.0, "tint": 8.0, "vibrance": 0.30, "saturation": 1.15,
            "bloom_strength": 0.22, "film_grain": 0.15, "vignette": 0.28, "sharpness": 0.30,
        }
    },
    "Pacific Northwest (Moody Pine)": {
        "label": "Pacific Northwest (Moody Pine)",
        "badge": "🌲 Moody Pine",
        "category": "Stylized & FX",
        "recommended": False,
        "description": "Muted evergreen look: deep rich pine greens, desaturated warm tones, foggy shadow lift, and quiet forest mood.",
        "params": {
            "exposure": -0.05, "smart_brightness": 0.18, "highlight_recovery": 0.32, "contrast": 1.15,
            "temperature": -15.0, "tint": -18.0, "vibrance": 0.05, "saturation": 0.85,
            "bloom_strength": 0.18, "film_grain": 0.12, "vignette": 0.22, "sharpness": 0.35,
        }
    },
    "Autumn Amber Warmth": {
        "label": "Autumn Amber Warmth",
        "badge": "🍂 Autumn Amber",
        "category": "Stylized & FX",
        "recommended": False,
        "description": "Cozy autumn palette: boosted rustic reds and golds, warm amber highlights, and rich earthy contrast.",
        "params": {
            "exposure": 0.08, "smart_brightness": 0.24, "highlight_recovery": 0.26, "contrast": 1.14,
            "temperature": 34.0, "tint": 6.0, "vibrance": 0.38, "saturation": 1.16,
            "bloom_strength": 0.20, "film_grain": 0.08, "vignette": 0.16, "sharpness": 0.25,
        }
    },
    "Sepia Western Dust": {
        "label": "Sepia Western Dust",
        "badge": "🏜️ Western Dust",
        "category": "Stylized & FX",
        "recommended": False,
        "description": "Sun-drenched frontier look: dry ochre tones, bleached desert highlights, warm brown shadows, and film grain.",
        "params": {
            "exposure": 0.10, "smart_brightness": 0.20, "highlight_recovery": 0.22, "contrast": 1.18,
            "temperature": 45.0, "tint": 0.0, "vibrance": -0.20, "saturation": 0.82,
            "bloom_strength": 0.15, "film_grain": 0.28, "vignette": 0.35, "sharpness": 0.25,
        }
    },
    "Original (Flat / Raw)": {
        "label": "Original (Flat / Raw)",
        "badge": "⚪ Neutral Raw",
        "category": "All",
        "recommended": False,
        "description": "Clean, unadjusted raw camera footage with zero alteration.",
        "params": {
            "exposure": 0.0, "smart_brightness": 0.0, "highlight_recovery": 0.0, "contrast": 1.0,
            "temperature": 0.0, "tint": 0.0, "vibrance": 0.0, "saturation": 1.0,
            "bloom_strength": 0.0, "film_grain": 0.0, "vignette": 0.0, "sharpness": 0.0,
        }
    }
}
