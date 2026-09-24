import json
import os
import shutil
import subprocess
import tempfile
from typing import Optional, Tuple, Dict, Any


def get_ffmpeg_binaries() -> Tuple[str, str]:
    """
    Locates ffmpeg and ffprobe from:
    1. System PATH
    2. Sibling project: ..\\Video Enhancer App\\bin
    3. Local project bin\\
    """
    # 1. System PATH
    sys_ffmpeg = shutil.which("ffmpeg")
    sys_ffprobe = shutil.which("ffprobe")
    if sys_ffmpeg and sys_ffprobe:
        return sys_ffmpeg, sys_ffprobe

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 2. Local bin/
    local_bin = os.path.join(base_dir, "bin")
    if os.path.exists(os.path.join(local_bin, "ffmpeg.exe")):
        return os.path.join(local_bin, "ffmpeg.exe"), os.path.join(local_bin, "ffprobe.exe")

    # 3. Check sibling Video Enhancer App bin/
    sibling_bin = os.path.abspath(os.path.join(base_dir, "..", "Video Enhancer App", "bin"))
    if os.path.exists(os.path.join(sibling_bin, "ffmpeg.exe")):
        return os.path.join(sibling_bin, "ffmpeg.exe"), os.path.join(sibling_bin, "ffprobe.exe")

    return "ffmpeg", "ffprobe"


def probe_video_metadata(video_path: str, ffprobe_bin: Optional[str] = None) -> Dict[str, Any]:
    """Extracts resolution, framerate, duration, and frame count."""
    if not ffprobe_bin:
        _, ffprobe_bin = get_ffmpeg_binaries()

    cmd = [
        ffprobe_bin,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,nb_frames,duration",
        "-show_entries", "format=duration",
        "-of", "json",
        video_path,
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    data = json.loads(res.stdout)
    stream = data["streams"][0]

    width = int(stream["width"])
    height = int(stream["height"])

    fps_parts = stream["r_frame_rate"].split("/")
    fps = float(fps_parts[0]) / float(fps_parts[1]) if len(fps_parts) == 2 and float(fps_parts[1]) != 0 else 30.0

    duration = float(stream.get("duration") or data.get("format", {}).get("duration", 0.0))

    nb_frames = stream.get("nb_frames")
    if nb_frames and nb_frames.isdigit() and int(nb_frames) > 0:
        total_frames = int(nb_frames)
    else:
        total_frames = max(1, int(round(duration * fps)))

    return {
        "width": width,
        "height": height,
        "fps": fps,
        "duration": duration,
        "total_frames": total_frames,
    }


def check_encoder_available(ffmpeg_bin: str, encoder: str = "h264_nvenc") -> bool:
    """Verifies whether an encoder (e.g. h264_nvenc) is available."""
    try:
        cmd = [
            ffmpeg_bin, "-v", "error", "-f", "lavfi", "-i", "nullsrc=s=64x64:d=0.1",
            "-c:v", encoder, "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0
    except Exception:
        return False


def extract_audio_lossless(video_path: str, ffmpeg_bin: str) -> Optional[str]:
    """Extracts audio stream into a temporary container without re-encoding."""
    # Check if video has an audio stream
    _, ffprobe_bin = get_ffmpeg_binaries()
    probe_cmd = [
        ffprobe_bin, "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=codec_type",
        "-of", "csv=p=0",
        video_path,
    ]
    probe_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if not probe_res.stdout.strip():
        return None

    temp_audio = tempfile.NamedTemporaryFile(suffix=".mkv", delete=False).name
    cmd = [
        ffmpeg_bin, "-y", "-v", "error",
        "-i", video_path,
        "-vn", "-c:a", "copy",
        "-map_metadata", "0",
        temp_audio,
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0 and os.path.exists(temp_audio) and os.path.getsize(temp_audio) > 0:
        return temp_audio

    if os.path.exists(temp_audio):
        os.remove(temp_audio)
    return None
