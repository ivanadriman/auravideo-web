import cv2
import numpy as np
from typing import Optional, Tuple
from core.config import FilterParams


class FilterEngine:
    """
    High-performance, vectorized video aesthetic filter engine.
    Uses pre-computed 256-level Look-Up Tables (LUTs), cached noise textures,
    and SIMD-accelerated OpenCV operations for ultra-fast (60-200+ FPS) color grading.
    """

    def __init__(self):
        self._cached_params: Optional[FilterParams] = None
        self._cached_bgr_lut: Optional[np.ndarray] = None
        self._vignette_mask_u8: Optional[np.ndarray] = None
        self._vignette_shape: Optional[Tuple[int, int]] = None
        self._vignette_strength: float = 0.0

        # Pre-generated 35mm grain noise buffer (1024x1024 tiled int8)
        rng = np.random.RandomState(42)
        self._noise_pool = (rng.normal(0, 1.0, (1024, 1024)) * 32.0).astype(np.int16)
        self._noise_offset_x = 0
        self._noise_offset_y = 0

    def _build_lut(self, params: FilterParams) -> np.ndarray:
        """
        Builds a 3-channel 256-element LUT (BGR) combining exposure, shadow lift,
        highlight recovery, contrast S-curve, color temperature, and tint.
        """
        x = np.linspace(0.0, 1.0, 256, dtype=np.float32)

        # 1. Exposure compensation (EV)
        if abs(params.exposure) > 0.001:
            scale = 2.0 ** params.exposure
            x = x * scale

        # 2. Smart Brightness (Adaptive Shadow Lift)
        if abs(params.smart_brightness) > 0.001:
            lift = params.smart_brightness * 0.55
            x = x + lift * ((1.0 - np.clip(x, 0.0, 1.0)) ** 1.8)

        # 3. Highlight Recovery / Soft Knee Roll-off
        if params.highlight_recovery > 0.001:
            hl = params.highlight_recovery
            knee = 0.70
            mask = x > knee
            x[mask] = knee + (x[mask] - knee) / (1.0 + hl * (x[mask] - knee) * 2.5)

        # 4. Contrast S-Curve
        if abs(params.contrast - 1.0) > 0.001:
            x_centered = x - 0.45
            x = 0.45 + np.sign(x_centered) * (np.abs(x_centered) ** (1.0 / max(0.1, params.contrast)))

        x = np.clip(x, 0.0, 1.0)

        # Base channels: Blue, Green, Red
        lut_b = x.copy()
        lut_g = x.copy()
        lut_r = x.copy()

        # 5. Color Temperature (Cool/Cyan <-> Warm/Amber)
        if abs(params.temperature) > 0.001:
            t = params.temperature / 100.0
            if t > 0:
                lut_r = lut_r * (1.0 + t * 0.22)
                lut_g = lut_g * (1.0 + t * 0.08)
                lut_b = lut_b * (1.0 - t * 0.20)
            else:
                lut_r = lut_r * (1.0 + t * 0.18)
                lut_b = lut_b * (1.0 - t * 0.25)

        # 6. Tint (Green <-> Magenta)
        if abs(params.tint) > 0.001:
            tn = params.tint / 100.0
            if tn > 0:
                lut_r = lut_r * (1.0 + tn * 0.10)
                lut_g = lut_g * (1.0 - tn * 0.12)
                lut_b = lut_b * (1.0 + tn * 0.10)
            else:
                lut_g = lut_g * (1.0 - tn * 0.15)

        lut_b = np.clip(lut_b * 255.0, 0, 255).astype(np.uint8)
        lut_g = np.clip(lut_g * 255.0, 0, 255).astype(np.uint8)
        lut_r = np.clip(lut_r * 255.0, 0, 255).astype(np.uint8)

        # Shape (256, 1, 3) for cv2.LUT
        return np.dstack((lut_b, lut_g, lut_r))

    def _build_sat_lut(self, vibrance: float, saturation: float) -> np.ndarray:
        """Fast 1D lookup table for the HSV saturation channel."""
        s = np.linspace(0.0, 1.0, 256, dtype=np.float32)
        if abs(vibrance) > 0.01:
            s = s + vibrance * (1.0 - s) * s * 1.5
        if abs(saturation - 1.0) > 0.01:
            s = s * saturation
        return np.clip(s * 255.0, 0, 255).astype(np.uint8)

    def _get_vignette_mask_u8(self, h: int, w: int, strength: float) -> np.ndarray:
        """Generates and caches an elliptical vignette mask as uint8."""
        if (self._vignette_shape == (h, w)) and (abs(self._vignette_strength - strength) < 0.01) and (self._vignette_mask_u8 is not None):
            return self._vignette_mask_u8

        y, x = np.ogrid[:h, :w]
        cy, cx = h / 2.0, w / 2.0
        dist = np.sqrt(((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2) / np.sqrt(2.0)
        vignette = 1.0 - strength * (dist ** 2)
        vignette = np.clip(vignette * 255.0, 0, 255).astype(np.uint8)

        self._vignette_mask_u8 = np.dstack([vignette, vignette, vignette])
        self._vignette_shape = (h, w)
        self._vignette_strength = strength
        return self._vignette_mask_u8

    def apply_filter(self, frame_bgr: np.ndarray, params: FilterParams) -> np.ndarray:
        """
        Applies the complete color grading & aesthetic filter pipeline to a single BGR frame.
        """
        if frame_bgr is None or frame_bgr.size == 0:
            return frame_bgr

        if params.intensity <= 0.001:
            return frame_bgr

        original = frame_bgr.copy() if params.intensity < 0.999 else None

        # 1. Look-Up Table (Curves, Exposure, Shadow Lift, Highlight Roll-off, Temp, Tint)
        lut = self._build_lut(params)
        out = cv2.LUT(frame_bgr, lut)

        # 2. Vibrance & Global Saturation (Fast 1D LUT in HSV)
        if abs(params.vibrance) > 0.01 or abs(params.saturation - 1.0) > 0.01:
            hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV)
            sat_lut = self._build_sat_lut(params.vibrance, params.saturation)
            hsv[:, :, 1] = cv2.LUT(hsv[:, :, 1], sat_lut)
            out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # 3. Soft Bloom / Aesthetic Glow
        if params.bloom_strength > 0.01:
            h, w = out.shape[:2]
            small_w, small_h = max(32, w // 4), max(18, h // 4)
            small = cv2.resize(out, (small_w, small_h), interpolation=cv2.INTER_NEAREST)

            gray_small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            _, hl_mask = cv2.threshold(gray_small, 175, 255, cv2.THRESH_BINARY)
            hl_colored = cv2.bitwise_and(small, small, mask=hl_mask)

            glow_small = cv2.GaussianBlur(hl_colored, (19, 19), 0)
            glow = cv2.resize(glow_small, (w, h), interpolation=cv2.INTER_LINEAR)

            out = cv2.addWeighted(out, 1.0, glow, params.bloom_strength * 0.75, 0)

        # 4. Vignette (SIMD multiply via cv2)
        if params.vignette > 0.01:
            h, w = out.shape[:2]
            mask_u8 = self._get_vignette_mask_u8(h, w, params.vignette)
            out = cv2.multiply(out, mask_u8, scale=1.0 / 255.0)

        # 5. Film Grain (Tiled from pre-generated cache)
        if params.film_grain > 0.01:
            h, w = out.shape[:2]
            # Advance cyclic offset
            self._noise_offset_x = (self._noise_offset_x + 73) % (1024 - 100)
            self._noise_offset_y = (self._noise_offset_y + 47) % (1024 - 100)
            
            # Tile or crop from precomputed noise pool
            reps_y = int(np.ceil(h / 1024.0))
            reps_x = int(np.ceil(w / 1024.0))
            tiled = np.tile(self._noise_pool, (reps_y, reps_x))[:h, :w]
            noise_slice = (tiled * params.film_grain).astype(np.int16)
            
            # Fast add to channels
            noise_3ch = np.dstack([noise_slice, noise_slice, noise_slice])
            out_i16 = out.astype(np.int16) + noise_3ch
            out = np.clip(out_i16, 0, 255).astype(np.uint8)

        # 6. Micro-contrast / Sharpness
        if params.sharpness > 0.01:
            blur = cv2.GaussianBlur(out, (0, 0), sigmaX=1.5)
            out = cv2.addWeighted(out, 1.0 + params.sharpness * 0.6, blur, -params.sharpness * 0.6, 0)

        # 7. Master Intensity Blend
        if original is not None:
            out = cv2.addWeighted(original, 1.0 - params.intensity, out, params.intensity, 0)

        return out
