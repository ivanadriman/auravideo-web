import os
import sys
import tempfile
import gradio as gr
import numpy as np

# Ensure local directory is on import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import FilterParams, PRESET_DEFINITIONS
from core.filter_engine import FilterEngine
from video_service import process_single_frame, render_filtered_video

engine = FilterEngine()

# Prepare preset categories and names
PRESET_NAMES = list(PRESET_DEFINITIONS.keys())
DEFAULT_PRESET = "Warm Intimate Bedroom"


def get_params_for_preset(preset_name: str, intensity: float) -> tuple:
    """Returns slider values when a preset is chosen."""
    p_dict = PRESET_DEFINITIONS.get(preset_name, {}).get("params", {})
    return (
        round(p_dict.get("exposure", 0.0), 2),
        round(p_dict.get("smart_brightness", 0.25), 2),
        round(p_dict.get("highlight_recovery", 0.20), 2),
        round(p_dict.get("contrast", 1.10), 2),
        round(p_dict.get("temperature", 8.0), 1),
        round(p_dict.get("tint", 2.0), 1),
        round(p_dict.get("vibrance", 0.25), 2),
        round(p_dict.get("saturation", 1.05), 2),
        round(p_dict.get("bloom_strength", 0.18), 2),
        round(p_dict.get("film_grain", 0.0), 2),
        round(p_dict.get("vignette", 0.10), 2),
        round(p_dict.get("sharpness", 0.20), 2),
    )


def preview_frame(
    video_file,
    preset_name,
    intensity,
    exposure,
    smart_brightness,
    highlight_recovery,
    contrast,
    temperature,
    tint,
    vibrance,
    saturation,
    bloom_strength,
    film_grain,
    vignette,
    sharpness,
    timestamp_sec,
):
    """Generates before/after comparison frames."""
    if video_file is None:
        return None, None, "⚠️ Please upload a video file first."

    params = FilterParams(
        preset_name=preset_name,
        intensity=float(intensity),
        exposure=float(exposure),
        smart_brightness=float(smart_brightness),
        highlight_recovery=float(highlight_recovery),
        contrast=float(contrast),
        temperature=float(temperature),
        tint=float(tint),
        vibrance=float(vibrance),
        saturation=float(saturation),
        bloom_strength=float(bloom_strength),
        film_grain=float(film_grain),
        vignette=float(vignette),
        sharpness=float(sharpness),
    )

    try:
        orig_rgb, filtered_rgb = process_single_frame(
            video_file, params, timestamp_sec=float(timestamp_sec), engine=engine
        )
        msg = f"✨ Preview updated at {timestamp_sec:.1f}s | Preset: {preset_name} (Intensity: {int(intensity*100)}%)"
        return orig_rgb, filtered_rgb, msg
    except Exception as e:
        return None, None, f"❌ Error: {str(e)}"


def process_video_full(
    video_file,
    preset_name,
    intensity,
    exposure,
    smart_brightness,
    highlight_recovery,
    contrast,
    temperature,
    tint,
    vibrance,
    saturation,
    bloom_strength,
    film_grain,
    vignette,
    sharpness,
    crf_val,
    progress=gr.Progress(track_tqdm=True),
):
    """Processes and exports the entire video with audio pass-through."""
    if video_file is None:
        return None, "⚠️ Please upload a video file first."

    params = FilterParams(
        preset_name=preset_name,
        intensity=float(intensity),
        exposure=float(exposure),
        smart_brightness=float(smart_brightness),
        highlight_recovery=float(highlight_recovery),
        contrast=float(contrast),
        temperature=float(temperature),
        tint=float(tint),
        vibrance=float(vibrance),
        saturation=float(saturation),
        bloom_strength=float(bloom_strength),
        film_grain=float(film_grain),
        vignette=float(vignette),
        sharpness=float(sharpness),
        crf=int(crf_val),
    )

    out_temp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name

    def on_progress(pct, text):
        progress(pct, desc=text)

    try:
        render_filtered_video(video_file, out_temp, params, progress_callback=on_progress, engine=engine)
        return out_temp, "🎉 Video processing complete! Download your video below."
    except Exception as e:
        return None, f"❌ Processing failed: {str(e)}"


# Build the Gradio Interface
custom_css = """
.gradio-container { max-width: 1300px !important; }
#title-header { text-align: center; margin-bottom: 8px; }
#status-box { font-weight: 600; color: #00d2ff; }
"""

with gr.Blocks(title="AuraVideo Studio — Online Suite", theme=gr.themes.Soft(primary_hue="cyan"), css=custom_css) as app:
    gr.Markdown(
        """
        # 🎬 AuraVideo Studio — Instant Aesthetic Video Color Suite
        ### Professional real-time color grading, shadow illumination & aesthetic styling in your browser.
        """,
        elem_id="title-header",
    )

    with gr.Row():
        # LEFT COLUMN: Video I/O & Interactive Viewport
        with gr.Column(scale=6):
            input_video = gr.Video(label="📹 Step 1: Upload Source Video (MP4 / MKV / MOV)")

            gr.Markdown("### 🔍 Live Single-Frame Preview")
            timestamp_slider = gr.Slider(
                label="Preview Frame Timestamp (seconds)",
                minimum=0.0,
                maximum=60.0,
                value=2.0,
                step=0.5,
            )

            with gr.Row():
                preview_orig = gr.Image(label="Original Frame", type="numpy")
                preview_filtered = gr.Image(label="Filtered Aesthetic Result", type="numpy")

            btn_preview = gr.Button("🔄 Refresh Live Preview Frame", variant="secondary")

            gr.Markdown("---")
            gr.Markdown("### ⚡ Step 3: Render & Export Full Video")
            btn_export = gr.Button("🚀 Process Full Video with Audio", variant="primary", size="lg")
            export_status = gr.Markdown("Ready to process.", elem_id="status-box")
            output_video = gr.Video(label="📥 Download Filtered Video")

        # RIGHT COLUMN: Presets & Lightroom Fine-Tuning
        with gr.Column(scale=5):
            gr.Markdown("### 🎨 Step 2: Choose Preset & Fine-Tune")

            preset_dropdown = gr.Dropdown(
                label="⭐ Select Aesthetic Preset (36 Curated Looks)",
                choices=PRESET_NAMES,
                value=DEFAULT_PRESET,
            )

            master_intensity = gr.Slider(
                label="Master Look Strength", minimum=0.0, maximum=1.0, value=1.0, step=0.05
            )

            with gr.Accordion("☀️ Light & Tone Adjustments", open=True):
                slider_exp = gr.Slider(label="Exposure Compensation (EV)", minimum=-2.0, maximum=2.0, value=0.35, step=0.05)
                slider_sb = gr.Slider(label="Smart Brightness (Shadow Lift)", minimum=0.0, maximum=1.0, value=0.55, step=0.02)
                slider_hl = gr.Slider(label="Highlight Recovery / Roll-Off", minimum=0.0, maximum=1.0, value=0.45, step=0.02)
                slider_contrast = gr.Slider(label="Contrast Filmic S-Curve", minimum=0.5, maximum=2.0, value=1.05, step=0.02)

            with gr.Accordion("🎨 Color Balance & Vibrance", open=True):
                slider_temp = gr.Slider(label="Temperature (Cool ↔ Warm)", minimum=-100.0, maximum=100.0, value=16.0, step=1.0)
                slider_tint = gr.Slider(label="Tint (Green ↔ Magenta)", minimum=-100.0, maximum=100.0, value=6.0, step=1.0)
                slider_vib = gr.Slider(label="Vibrance (Skin-Safe Boost)", minimum=-1.0, maximum=1.0, value=0.32, step=0.02)
                slider_sat = gr.Slider(label="Global Saturation", minimum=0.0, maximum=2.0, value=1.08, step=0.02)

            with gr.Accordion("✨ Atmospheric FX & Sharpness", open=False):
                slider_bloom = gr.Slider(label="Soft Aesthetic Bloom / Glow", minimum=0.0, maximum=1.0, value=0.18, step=0.02)
                slider_grain = gr.Slider(label="35mm Analog Film Grain", minimum=0.0, maximum=1.0, value=0.0, step=0.02)
                slider_vignette = gr.Slider(label="Cinematic Vignette Falloff", minimum=0.0, maximum=1.0, value=0.08, step=0.02)
                slider_sharp = gr.Slider(label="Clarity / Edge Sharpness", minimum=0.0, maximum=2.0, value=0.30, step=0.02)

            with gr.Accordion("⚙️ Export Quality Settings", open=False):
                slider_crf = gr.Slider(
                    label="Quality CRF (Lower = Higher Quality)",
                    minimum=12,
                    maximum=30,
                    value=18,
                    step=1,
                )

    # Wire up preset changes to automatically update sliders
    all_sliders = [
        slider_exp,
        slider_sb,
        slider_hl,
        slider_contrast,
        slider_temp,
        slider_tint,
        slider_vib,
        slider_sat,
        slider_bloom,
        slider_grain,
        slider_vignette,
        slider_sharp,
    ]

    preset_dropdown.change(
        fn=get_params_for_preset,
        inputs=[preset_dropdown, master_intensity],
        outputs=all_sliders,
    )

    # Wire preview button
    preview_inputs = [
        input_video,
        preset_dropdown,
        master_intensity,
        slider_exp,
        slider_sb,
        slider_hl,
        slider_contrast,
        slider_temp,
        slider_tint,
        slider_vib,
        slider_sat,
        slider_bloom,
        slider_grain,
        slider_vignette,
        slider_sharp,
        timestamp_slider,
    ]

    btn_preview.click(
        fn=preview_frame,
        inputs=preview_inputs,
        outputs=[preview_orig, preview_filtered, export_status],
    )

    # Auto-refresh preview on timestamp slider release
    timestamp_slider.release(
        fn=preview_frame,
        inputs=preview_inputs,
        outputs=[preview_orig, preview_filtered, export_status],
    )

    # Wire full video render
    render_inputs = [
        input_video,
        preset_dropdown,
        master_intensity,
        slider_exp,
        slider_sb,
        slider_hl,
        slider_contrast,
        slider_temp,
        slider_tint,
        slider_vib,
        slider_sat,
        slider_bloom,
        slider_grain,
        slider_vignette,
        slider_sharp,
        slider_crf,
    ]

    btn_export.click(
        fn=process_video_full,
        inputs=render_inputs,
        outputs=[output_video, export_status],
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
