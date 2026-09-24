import os
import sys
import tempfile
import streamlit as st
import numpy as np
import cv2

# Add web_deployment directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import FilterParams, PRESET_DEFINITIONS
from core.filter_engine import FilterEngine
from video_service import process_single_frame, render_filtered_video

# Page configuration
st.set_page_config(
    page_title="AuraVideo Studio — Online Color Suite",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling for dark aesthetic studio
st.markdown(
    """
    <style>
    .main { background-color: #0b0f19; }
    h1, h2, h3 { color: #00d2ff !important; font-family: 'Segoe UI', sans-serif; }
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #00d2ff 100%);
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #38bdf8 100%);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def get_engine():
    return FilterEngine()

engine = get_engine()

# Header
st.title("🎬 AuraVideo Studio — Aesthetic Video Color Suite")
st.caption("Professional color grading, shadow illumination & aesthetic styling in your browser.")

# Sidebar: Preset & Adjustments
st.sidebar.header("🎨 Step 1: Select Preset & Fine-Tune")

preset_names = list(PRESET_DEFINITIONS.keys())
default_preset_idx = preset_names.index("Warm Intimate Bedroom") if "Warm Intimate Bedroom" in preset_names else 0

selected_preset = st.sidebar.selectbox(
    "Choose Aesthetic Look (36 Presets)",
    preset_names,
    index=default_preset_idx,
)

preset_data = PRESET_DEFINITIONS.get(selected_preset, {}).get("params", {})
preset_desc = PRESET_DEFINITIONS.get(selected_preset, {}).get("description", "")
st.sidebar.info(f"**{selected_preset}**\n\n{preset_desc}")

master_intensity = st.sidebar.slider(
    "Master Look Strength",
    min_value=0.0,
    max_value=1.0,
    value=1.0,
    step=0.05,
)

with st.sidebar.expander("☀️ Light & Tone Adjustments", expanded=True):
    val_exp = float(preset_data.get("exposure", 0.0))
    val_sb = float(preset_data.get("smart_brightness", 0.25))
    val_hl = float(preset_data.get("highlight_recovery", 0.20))
    val_contrast = float(preset_data.get("contrast", 1.10))

    exposure = st.slider("Exposure (EV)", -2.0, 2.0, val_exp, 0.05)
    smart_brightness = st.slider("Smart Brightness (Shadow Lift)", 0.0, 1.0, val_sb, 0.02)
    highlight_recovery = st.slider("Highlight Recovery / Knee", 0.0, 1.0, val_hl, 0.02)
    contrast = st.slider("Contrast Filmic S-Curve", 0.5, 2.0, val_contrast, 0.02)

with st.sidebar.expander("🎨 Color Balance & Vibrance", expanded=True):
    val_temp = float(preset_data.get("temperature", 8.0))
    val_tint = float(preset_data.get("tint", 2.0))
    val_vib = float(preset_data.get("vibrance", 0.25))
    val_sat = float(preset_data.get("saturation", 1.05))

    temperature = st.slider("Temperature (Cool ↔ Warm)", -100.0, 100.0, val_temp, 1.0)
    tint = st.slider("Tint (Green ↔ Magenta)", -100.0, 100.0, val_tint, 1.0)
    vibrance = st.slider("Vibrance (Skin-Safe Boost)", -1.0, 1.0, val_vib, 0.02)
    saturation = st.slider("Global Saturation", 0.0, 2.0, val_sat, 0.02)

with st.sidebar.expander("✨ Atmosphere FX & Micro-Contrast", expanded=False):
    val_bloom = float(preset_data.get("bloom_strength", 0.18))
    val_grain = float(preset_data.get("film_grain", 0.0))
    val_vignette = float(preset_data.get("vignette", 0.10))
    val_sharp = float(preset_data.get("sharpness", 0.20))

    bloom_strength = st.slider("Soft Bloom / Glow", 0.0, 1.0, val_bloom, 0.02)
    film_grain = st.slider("35mm Film Grain", 0.0, 1.0, val_grain, 0.02)
    vignette = st.slider("Cinematic Vignette", 0.0, 1.0, val_vignette, 0.02)
    sharpness = st.slider("Clarity / Edge Sharpness", 0.0, 2.0, val_sharp, 0.02)

with st.sidebar.expander("⚙️ Export Encoding Quality", expanded=False):
    crf = st.slider("Quality CRF (12 Lossless - 30 Compressed)", 12, 30, 18, 1)

params = FilterParams(
    preset_name=selected_preset,
    intensity=master_intensity,
    exposure=exposure,
    smart_brightness=smart_brightness,
    highlight_recovery=highlight_recovery,
    contrast=contrast,
    temperature=temperature,
    tint=tint,
    vibrance=vibrance,
    saturation=saturation,
    bloom_strength=bloom_strength,
    film_grain=film_grain,
    vignette=vignette,
    sharpness=sharpness,
    crf=crf,
)

# Main area: Video Upload & Interactive Live Viewport
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader("📹 Step 2: Upload Video")
    uploaded_file = st.file_uploader(
        "Upload MP4, MOV, or MKV video",
        type=["mp4", "mov", "mkv", "avi", "webm"],
    )

if uploaded_file is not None:
    # Save uploaded file to temp path
    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, f"input_{uploaded_file.name}")
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    # Get video duration for preview scrubbing
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / max(1.0, fps)
    cap.release()

    with col_right:
        st.subheader("🔍 Step 3: Interactive Live Preview")
        preview_sec = st.slider(
            "Scrub Frame Timestamp (Seconds)",
            min_value=0.0,
            max_value=max(1.0, float(int(duration_sec))),
            value=min(2.0, duration_sec),
            step=0.5,
        )

    # Render Side-by-Side Single-Frame Preview
    try:
        orig_rgb, filtered_rgb = process_single_frame(
            input_path, params, timestamp_sec=preview_sec, engine=engine
        )

        st.markdown("### 👁️ Before / After Frame Comparison")
        prev_col1, prev_col2 = st.columns(2)
        with prev_col1:
            st.image(orig_rgb, caption=f"Original (Frame at {preview_sec:.1f}s)", use_container_width=True)
        with prev_col2:
            st.image(filtered_rgb, caption=f"Graded with '{selected_preset}'", use_container_width=True)
    except Exception as e:
        st.error(f"Preview rendering error: {e}")

    # Full Video Render Section
    st.markdown("---")
    st.subheader("⚡ Step 4: Render & Download Full Video")
    st.write("Streams frames through zero-disk RAM with full lossless audio pass-through.")

    if st.button("🚀 Render Full Video with Audio", use_container_width=True):
        progress_bar = st.progress(0.0)
        status_text = st.empty()

        def on_progress(pct, desc):
            progress_bar.progress(pct)
            status_text.text(desc)

        output_path = os.path.join(temp_dir, f"graded_{uploaded_file.name}")

        try:
            render_filtered_video(
                input_path,
                output_path,
                params,
                progress_callback=on_progress,
                engine=engine,
            )
            st.success("🎉 Video rendering complete!")

            with open(output_path, "rb") as out_file:
                video_bytes = out_file.read()

            st.download_button(
                label="📥 Download Filtered Video",
                data=video_bytes,
                file_name=f"AuraVideo_{selected_preset.replace(' ', '_')}_{uploaded_file.name}",
                mime="video/mp4",
                use_container_width=True,
            )
        except Exception as err:
            st.error(f"Render failed: {err}")
else:
    st.info("👆 Upload any video file above to start grading frames and exporting!")
