"""
WT3D WHIPCAM TIKTOK & CINEMATIC VIDEO EXPORTER
Automated 9:16 Vertical Video & 16:9 Landscape Exporter for Autodesk Inventor
Author: Phan Trong Tan (@tanphan1105)
"""

import os
import sys
import argparse
import subprocess
import glob
from PIL import Image, ImageDraw, ImageFont

def get_ffmpeg_exe():
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.exists(exe):
            return exe
    except Exception:
        pass
    
    # Fallback paths
    candidates = [
        r"D:\WT3D_Project\Z_Tools\ffmpeg\ffmpeg.exe",
        "ffmpeg"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return "ffmpeg"

def create_tiktok_overlay(width, height, model_name, shot_title, output_png):
    """
    Creates a high-end Glassmorphism Bento Card overlay for 9:16 TikTok / Reels / Shorts.
    Leaves the center (Y: 656 to 1264) crystal clear for the 3D model.
    """
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Fonts
    def load_font(font_names, size, bold=False):
        for fn in font_names:
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                continue
        return ImageFont.load_default()

    font_title = load_font(['arialbd.ttf', 'segoeuib.ttf', 'calibrib.ttf'], 36)
    font_sub = load_font(['arialbd.ttf', 'segoeuib.ttf'], 24)
    font_body = load_font(['arial.ttf', 'segoeui.ttf', 'calibri.ttf'], 20)
    font_brand = load_font(['arialbd.ttf', 'segoeuib.ttf'], 26)
    font_small = load_font(['arial.ttf', 'segoeui.ttf'], 17)

    # -------------------------------------------------------------
    # 1. TOP BENTO CARD (Y: 140 to 600)
    # -------------------------------------------------------------
    top_x1, top_y1, top_x2, top_y2 = 40, 150, width - 40, 600
    # Glassmorphism dark background with cyan border
    d.rounded_rectangle([top_x1, top_y1, top_x2, top_y2], radius=24, 
                        fill=(15, 23, 42, 230), outline=(56, 189, 248, 200), width=3)

    # Badge in top card
    d.rounded_rectangle([top_x1 + 30, top_y1 + 25, top_x1 + 340, top_y1 + 68], 
                        radius=12, fill=(14, 116, 144, 255))
    d.text((top_x1 + 45, top_y1 + 33), "AUTODESK INVENTOR 2025", fill=(255, 255, 255), font=font_small)

    # Main Project / Model Title
    display_model = model_name if model_name else "MÔ HÌNH KỸ THUẬT 3D CHUẨN WT3D"
    if len(display_model) > 35:
        display_model = display_model[:32] + "..."
    d.text((top_x1 + 30, top_y1 + 85), display_model, fill=(255, 255, 255), font=font_title)

    # Shot Subtitle
    display_shot = shot_title if shot_title else "CINEMATIC SHOWREEL"
    d.text((top_x1 + 30, top_y1 + 145), display_shot, fill=(56, 189, 248), font=font_sub)

    # Divider line
    d.line([top_x1 + 30, top_y1 + 195, top_x2 - 30, top_y1 + 195], fill=(51, 65, 85, 255), width=2)

    # Technical Specs Bullet Points
    d.text((top_x1 + 30, top_y1 + 215), "- Quỹ đạo chuyển động: Cubic Bézier C2 Quintic siêu mượt", fill=(203, 213, 225), font=font_body)
    d.text((top_x1 + 30, top_y1 + 255), "- Góc ống kính: Dynamic FOV (Tele 32 deg -> Wide 52 deg)", fill=(203, 213, 225), font=font_body)
    d.text((top_x1 + 30, top_y1 + 295), "- Lưu điểm vĩnh viễn: Dual Persistence (AttributeSets + Sidecar)", fill=(203, 213, 225), font=font_body)
    d.text((top_x1 + 30, top_y1 + 335), "- Trình diễn tự động hóa & Thiết kế giàn máy lọc nước", fill=(52, 211, 153), font=font_body)
    d.text((top_x1 + 30, top_y1 + 375), "- Độ phân giải: 1080x1920 (TikTok/Reels/Shorts 60 FPS)", fill=(147, 197, 253), font=font_small)

    # -------------------------------------------------------------
    # 2. BOTTOM BENTO CARD (Y: 1320 to 1640 - safe above TikTok captions)
    # -------------------------------------------------------------
    bot_x1, bot_y1, bot_x2, bot_y2 = 40, 1320, width - 40, 1630
    d.rounded_rectangle([bot_x1, bot_y1, bot_x2, bot_y2], radius=24, 
                        fill=(15, 23, 42, 230), outline=(34, 197, 94, 200), width=3)

    # Brand Ribbon Badge
    d.rounded_rectangle([bot_x1 + 30, bot_y1 + 25, bot_x1 + 420, bot_y1 + 75], 
                        radius=14, fill=(22, 101, 52, 255))
    d.text((bot_x1 + 45, bot_y1 + 34), "WT3D • WATER TREATMENT", fill=(255, 255, 255), font=font_brand)

    # Lead Engineer info
    d.text((bot_x1 + 30, bot_y1 + 95), "Lead Engineer & Designer: Phan Trọng Tấn (@tanphan1105)", fill=(255, 255, 255), font=font_sub)
    d.text((bot_x1 + 30, bot_y1 + 140), "Hotline/Zalo Kỹ thuật: 0985.267.326 | Portfolio: fab.com/sellers/Trong Tan Phan", fill=(203, 213, 225), font=font_body)
    d.text((bot_x1 + 30, bot_y1 + 180), "Hệ sinh thái thiết kế & dự toán cơ điện xử lý nước chuyên sâu", fill=(148, 163, 184), font=font_small)
    d.text((bot_x1 + 30, bot_y1 + 215), "Bản quyền thiết kế (c) Phan Trọng Tấn • All Rights Reserved", fill=(100, 116, 139), font=font_small)

    overlay.save(output_png)
    return output_png

def export_video(frames_dir, output_mp4, model_name="WT3D_Model", shot_title="WhipCam Cinematic", 
                 video_format="native_916", fps=30, audio_choice="auto", cleanup=False, open_folder=True):
    ffmpeg_exe = get_ffmpeg_exe()
    print(f"[WT3D Exporter] Using FFmpeg: {ffmpeg_exe}")
    
    # Check frames
    png_pattern = os.path.join(frames_dir, "frame_*.png")
    frames = sorted(glob.glob(png_pattern))
    if not frames:
        print(f"[WT3D Exporter] ERROR: No frames found in {frames_dir} matching {png_pattern}")
        return False
    
    total_frames = len(frames)
    duration_sec = total_frames / float(fps)
    print(f"[WT3D Exporter] Total frames: {total_frames} ({duration_sec:.2f}s at {fps} fps)")

    os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

    # Audio allocation
    audio_path = None
    if audio_choice != "none":
        audio_dir = r"D:\WT3D_Project\Z_Tools\Audio"
        if os.path.exists(audio_choice) and os.path.isfile(audio_choice):
            audio_path = audio_choice
        elif os.path.exists(audio_dir):
            shot_lower = shot_title.lower()
            if "cảnh 1" in shot_lower or "shot 01" in shot_lower or "fly-in" in shot_lower:
                candidate = os.path.join(audio_dir, "CAM1_Epic.mp3")
            elif "cảnh 2" in shot_lower or "shot 02" in shot_lower or "pull-back" in shot_lower:
                candidate = os.path.join(audio_dir, "CAM2_SciFi.mp3")
            elif "cảnh 3" in shot_lower or "shot 03" in shot_lower or "con lắc" in shot_lower:
                candidate = os.path.join(audio_dir, "CAM3_Phonk.mp3")
            elif "cảnh 4" in shot_lower or "shot 04" in shot_lower or "zoom" in shot_lower:
                candidate = os.path.join(audio_dir, "CAM4_Glitch.mp3")
            elif "cảnh 5" in shot_lower or "shot 05" in shot_lower or "orbit" in shot_lower:
                candidate = os.path.join(audio_dir, "CAM5_Apple.mp3")
            else:
                candidate = os.path.join(audio_dir, "CAM1_Epic.mp3")
            
            if os.path.exists(candidate):
                audio_path = candidate
                print(f"[WT3D Exporter] Allocated audio: {audio_path}")

    # Build FFmpeg command based on format
    input_pattern = os.path.join(frames_dir, "frame_%05d.png")
    
    if video_format == "tiktok_blur_916":
        # 1080x1920 with elegant blurred background and centered clean 3D model
        # NO heavy bento cards or text boxes blocking the view
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
            "[0:v]scale=1080:-2[fg];"
            "[bg][fg]overlay=0:(1920-overlay_h)/2[final]"
        )
        cmd = [
            ffmpeg_exe, "-y",
            "-framerate", str(fps),
            "-i", input_pattern
        ]
        if audio_path:
            cmd.extend(["-stream_loop", "-1", "-i", audio_path])
            cmd.extend([
                "-filter_complex", filter_complex,
                "-map", "[final]",
                "-map", "1:a",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest"
            ])
        else:
            cmd.extend([
                "-filter_complex", filter_complex,
                "-map", "[final]"
            ])
            
    elif video_format == "native_916":
        # Direct vertical frames (1080x1920) - 100% clean full-screen 3D
        cmd = [
            ffmpeg_exe, "-y",
            "-framerate", str(fps),
            "-i", input_pattern
        ]
        if audio_path:
            cmd.extend(["-stream_loop", "-1", "-i", audio_path])
            cmd.extend(["-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"])
            
    else: # widescreen_169 (1920x1080)
        cmd = [
            ffmpeg_exe, "-y",
            "-framerate", str(fps),
            "-i", input_pattern
        ]
        if audio_path:
            cmd.extend(["-stream_loop", "-1", "-i", audio_path])
            cmd.extend(["-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"])

    # Video encoding params
    cmd.extend([
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        output_mp4
    ])

    print("[WT3D Exporter] Running FFmpeg encoding...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[WT3D Exporter] FFmpeg ERROR:")
        print(res.stderr[-1000:])
        return False

    print(f"[WT3D Exporter] Video successfully exported to: {output_mp4}")
    print(f"[WT3D Exporter] File size: {os.path.getsize(output_mp4):,} bytes")

    # Cleanup temp frames if requested
    if cleanup:
        print("[WT3D Exporter] Cleaning up temporary frames...")
        for f in frames:
            try:
                os.remove(f)
            except Exception:
                pass
        overlay_tmp = os.path.join(frames_dir, "tiktok_overlay.png")
        if os.path.exists(overlay_tmp):
            try:
                os.remove(overlay_tmp)
            except Exception:
                pass

    if open_folder:
        try:
            # Highlight exported file in Explorer
            subprocess.run(f'explorer.exe /select,"{output_mp4}"', shell=True)
        except Exception:
            pass

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WT3D WhipCam Video Exporter")
    parser.add_argument("--frames-dir", required=True, help="Directory containing frame_XXXXX.png")
    parser.add_argument("--output-mp4", required=True, help="Path for output MP4 file")
    parser.add_argument("--model-name", default="Hệ Thống Xử Lý Nước WT3D", help="Model name for overlay")
    parser.add_argument("--shot-title", default="WhipCam Cinematic", help="Shot title")
    parser.add_argument("--format", default="native_916", choices=["tiktok_blur_916", "native_916", "widescreen_169"])
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    parser.add_argument("--audio", default="auto", help="Path to audio file or auto/none")
    parser.add_argument("--cleanup", action="store_true", help="Delete PNG frames after encode")
    parser.add_argument("--open-folder", action="store_true", help="Open folder after encode")

    args = parser.parse_args()
    ok = export_video(
        frames_dir=args.frames_dir,
        output_mp4=args.output_mp4,
        model_name=args.model_name,
        shot_title=args.shot_title,
        video_format=args.format,
        fps=args.fps,
        audio_choice=args.audio,
        cleanup=args.cleanup,
        open_folder=args.open_folder
    )
    sys.exit(0 if ok else 1)
