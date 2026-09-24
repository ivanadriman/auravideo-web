import os
import subprocess
import tempfile
import time
from typing import Optional, Callable
import cv2
import numpy as np

from core.config import FilterParams
from core.filter_engine import FilterEngine
from core.ffmpeg_utils import (
    get_ffmpeg_binaries,
    probe_video_metadata,
    check_encoder_available,
    extract_audio_lossless,
)


def process_single_frame(
    video_path: str,
    params: FilterParams,
    timestamp_sec: float = 1.0,
    engine: Optional[FilterEngine] = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extracts a frame at timestamp_sec and applies the aesthetic filter pipeline.
    Returns (orig_rgb, filtered_rgb) as uint8 NumPy arrays.
    """
    if engine is None:
        engine = FilterEngine()

    # 1. Attempt standard OpenCV VideoCapture
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frame = min(max(0, total_frames - 1), max(0, int(timestamp_sec * fps)))

    frame_bgr = None
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ret, read_frame = cap.read()
        if ret and read_frame is not None and read_frame.size > 0:
            frame_bgr = read_frame
        cap.release()

    # 2. Robust FFmpeg fallback (essential for Linux headless cloud where OpenCV has no native codecs)
    if frame_bgr is None:
        ffmpeg_bin, _ = get_ffmpeg_binaries()
        cmd = [
            ffmpeg_bin,
            "-ss", str(max(0.0, float(timestamp_sec))),
            "-i", video_path,
            "-vframes", "1",
            "-f", "image2pipe",
            "-vcodec", "png",
            "-",
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0 and len(res.stdout) > 0:
            img_arr = np.frombuffer(res.stdout, dtype=np.uint8)
            frame_bgr = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

    if frame_bgr is None or frame_bgr.size == 0:
        raise ValueError(
            f"Cannot extract frame from: {os.path.basename(video_path)} at {timestamp_sec}s. "
            "The video format may be unreadable or corrupt."
        )

    filtered_bgr = engine.apply_filter(frame_bgr, params)

    orig_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    filtered_rgb = cv2.cvtColor(filtered_bgr, cv2.COLOR_BGR2RGB)
    return orig_rgb, filtered_rgb


def render_filtered_video(
    input_path: str,
    output_path: str,
    params: FilterParams,
    progress_callback: Optional[Callable[[float, str], None]] = None,
    engine: Optional[FilterEngine] = None,
) -> str:
    """
    In-memory zero-disk video processing pipeline for web deployment.
    Uses FFmpeg pipe streaming with lossless audio pass-through.
    """
    if engine is None:
        engine = FilterEngine()

    ffmpeg_bin, ffprobe_bin = get_ffmpeg_binaries()
    meta = probe_video_metadata(input_path, ffprobe_bin)
    w = meta["width"]
    h = meta["height"]
    fps = meta["fps"]
    total_frames = meta["total_frames"]

    if progress_callback:
        progress_callback(0.05, f"Extracting audio track ({w}x{h} @ {fps:.1f} FPS)...")

    # 1. Audio stream extraction
    temp_audio = extract_audio_lossless(input_path, ffmpeg_bin)
    raw_output_video = (
        tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        if temp_audio
        else output_path
    )

    # 2. Select encoder
    nvenc_available = check_encoder_available(ffmpeg_bin, "h264_nvenc")
    encoder = "h264_nvenc" if nvenc_available else "libx264"
    preset_val = "p4" if nvenc_available else "medium"
    quality_args = ["-cq:v", str(params.crf)] if nvenc_available else ["-crf", str(params.crf)]

    reader_proc = None
    writer_proc = None

    try:
        if progress_callback:
            progress_callback(0.10, f"Initializing {encoder} encoding pipeline...")

        # 3. Reader Subprocess
        reader_proc = subprocess.Popen(
            [
                ffmpeg_bin, "-v", "error",
                "-i", input_path,
                "-an",
                "-f", "rawvideo",
                "-pix_fmt", "bgr24",
                "-",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=10 ** 8,
        )

        # 4. Writer Subprocess
        writer_cmd = [
            ffmpeg_bin, "-y", "-v", "error",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{w}x{h}",
            "-pix_fmt", "bgr24",
            "-r", str(fps),
            "-i", "-",
            "-c:v", encoder,
            "-preset", preset_val,
            *quality_args,
            "-pix_fmt", "yuv420p",
            raw_output_video,
        ]
        writer_proc = subprocess.Popen(
            writer_cmd,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=10 ** 8,
        )

        # 5. Frame Loop
        frame_size = w * h * 3
        current_frame = 0
        start_time = time.time()

        while True:
            raw_bytes = reader_proc.stdout.read(frame_size)
            if not raw_bytes or len(raw_bytes) < frame_size:
                break

            frame_bgr = np.frombuffer(raw_bytes, dtype=np.uint8).reshape((h, w, 3))
            filtered_bgr = engine.apply_filter(frame_bgr, params)
            writer_proc.stdin.write(filtered_bgr.tobytes())
            current_frame += 1

            if current_frame % 20 == 0 or current_frame == total_frames:
                pct = 0.10 + 0.80 * (current_frame / max(1, total_frames))
                elapsed = time.time() - start_time
                cur_fps = current_frame / max(0.001, elapsed)
                if progress_callback:
                    progress_callback(pct, f"Rendering frame {current_frame}/{total_frames} ({cur_fps:.1f} FPS)...")

        if writer_proc.stdin:
            writer_proc.stdin.close()
        reader_proc.wait()
        writer_proc.wait()

        # 6. Audio Remux
        if temp_audio and os.path.exists(temp_audio):
            if progress_callback:
                progress_callback(0.95, "Finalizing container with audio muxing...")
            mux_cmd = [
                ffmpeg_bin, "-y", "-v", "error",
                "-i", raw_output_video,
                "-i", temp_audio,
                "-c:v", "copy",
                "-c:a", "copy",
                "-map", "0:v:0",
                "-map", "1:a?",
                "-shortest",
                output_path,
            ]
            res = subprocess.run(mux_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                raise RuntimeError(f"FFmpeg muxing failed: {res.stderr.decode('utf-8', errors='ignore')}")

        if progress_callback:
            progress_callback(1.0, "Export completed successfully!")

        return output_path

    finally:
        # Cleanup temp video & audio
        if temp_audio and os.path.exists(temp_audio):
            try:
                os.remove(temp_audio)
            except OSError:
                pass
        if temp_audio and raw_output_video and os.path.exists(raw_output_video) and raw_output_video != output_path:
            try:
                os.remove(raw_output_video)
            except OSError:
                pass
