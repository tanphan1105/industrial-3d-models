#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WT3D SUPERCAR CINEMATIC POST-FX ENGINE (STAGE 2)
=============================================================================
Vectorized Directional Whip Blur + Radial Zoom Blur + 60 FPS FFmpeg Encoding
Lead Engineer: Phan Trong Tan (@tanphan1105) - WaterTreatment3D
=============================================================================
"""

import os
import sys
import argparse
import subprocess
import glob
import csv
import math
import numpy as np
from PIL import Image

def apply_directional_whip_blur(im_arr, angle_deg, distance, num_steps=9):
    """Vectorized linear motion blur along specified screen angle."""
    if distance < 2:
        return im_arr
    h, w, c = im_arr.shape
    rad = math.radians(angle_deg)
    dx = distance * math.cos(rad)
    dy = distance * math.sin(rad)
    
    accum = np.zeros_like(im_arr, dtype=np.float32)
    total_w = 0.0
    offsets = np.linspace(-0.5, 0.5, num_steps)
    
    for off in offsets:
        ox = int(round(off * dx))
        oy = int(round(off * dy))
        shifted = np.roll(im_arr, shift=(oy, ox), axis=(0, 1))
        wt = 1.0 - abs(off) * 0.75
        accum += shifted * wt
        total_w += wt
        
    return np.clip(accum / total_w, 0, 255).astype(np.uint8)

def apply_radial_zoom_blur(image, center=None, intensity=0.10, num_steps=8):
    """Center-burst radial zoom blur radiating from hero optical center."""
    if intensity < 0.01:
        return image
    w, h = image.size
    if center is None:
        cx, cy = w // 2, h // 2
    else:
        cx, cy = center
        
    im_arr = np.array(image, dtype=np.float32)
    accum = np.zeros_like(im_arr)
    total_w = 0.0
    
    for i in range(num_steps):
        scale = 1.0 + intensity * (i / max(1, num_steps - 1))
        wt = 1.0 - (i / num_steps) * 0.5
        nw = int(w * scale)
        nh = int(h * scale)
        scaled = image.resize((nw, nh), Image.Resampling.BILINEAR)
        left = (nw - w) // 2
        top = (nh - h) // 2
        cropped = scaled.crop((left, top, left + w, top + h))
        accum += np.array(cropped, dtype=np.float32) * wt
        total_w += wt
        
    return Image.fromarray(np.clip(accum / total_w, 0, 255).astype(np.uint8))

def apply_chromatic_aberration(im_arr, shift_pixels=2):
    """Subtle lens dispersion for high-speed supercar rush."""
    if shift_pixels < 1:
        return im_arr
    r = np.roll(im_arr[:, :, 0], shift=shift_pixels, axis=1)
    g = im_arr[:, :, 1]
    b = np.roll(im_arr[:, :, 2], shift=-shift_pixels, axis=1)
    return np.stack([r, g, b], axis=2)

def process_frames(input_dir, fps=60):
    telemetry_file = os.path.join(input_dir, "WT3D_Supercar_Telemetry.csv")
    frame_files = sorted(glob.glob(os.path.join(input_dir, "WT3D_Frame_*.png")))
    
    if not frame_files:
        print(f"Error: No WT3D_Frame_*.png files found in {input_dir}")
        return False
        
    print(f"Found {len(frame_files)} frames. Reading telemetry...")
    telemetry = {}
    if os.path.exists(telemetry_file):
        with open(telemetry_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    f_num = int(row["Frame"])
                    telemetry[f_num] = {
                        "Time": float(row["Time"]),
                        "ShotIndex": int(row["ShotIndex"]),
                        "ShotName": row["ShotName"],
                        "IsCut": int(row["IsCut"]),
                        "CutProg": float(row["CutProg"]),
                        "Speed": float(row["Speed"]),
                        "RollDeg": float(row["RollDeg"]),
                        "FOV": float(row["FOV"])
                    }
                except Exception as e:
                    pass

    processed_dir = os.path.join(input_dir, "post_processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    total = len(frame_files)
    print("Executing Stage 2 Post-FX Pipeline...")
    
    for idx, f_path in enumerate(frame_files):
        f_num = idx + 1
        meta = telemetry.get(f_num, {})
        is_cut = meta.get("IsCut", 0) == 1
        cut_prog = meta.get("CutProg", 0.0)
        speed = meta.get("Speed", 0.0)
        roll = meta.get("RollDeg", 0.0)
        
        img = Image.open(f_path).convert("RGB")
        im_arr = np.array(img, dtype=np.uint8)
        
        # 1. Whip Blur Cut Transition Window
        if is_cut:
            whip_factor = max(0.0, 1.0 - abs(cut_prog))
            dist = int(10 + 35 * whip_factor)
            angle = 25.0 + roll * 1.5
            im_arr = apply_directional_whip_blur(im_arr, angle, dist, num_steps=9)
            
            # Radial burst
            temp_img = Image.fromarray(im_arr)
            temp_img = apply_radial_zoom_blur(temp_img, intensity=0.12 * whip_factor, num_steps=8)
            im_arr = np.array(temp_img, dtype=np.uint8)
            
            # Chromatic edge shift
            if whip_factor > 0.4:
                im_arr = apply_chromatic_aberration(im_arr, shift_pixels=2)
                
        # 2. Hyper-Speed Apex Burst Window (Shot 6 Beat Drop around 6.13s - 7.03s)
        elif speed > 280.0:
            speed_factor = min(1.0, (speed - 280.0) / 100.0)
            temp_img = Image.fromarray(im_arr)
            temp_img = apply_radial_zoom_blur(temp_img, intensity=0.08 * speed_factor, num_steps=6)
            im_arr = np.array(temp_img, dtype=np.uint8)
            im_arr = apply_chromatic_aberration(im_arr, shift_pixels=1)

        # 3. The Frozen Hero Hold (Shot 4: 3.60s -> 5.53s) - Subtle Optical Tension
        elif meta.get("ShotIndex") == 4:
            temp_img = Image.fromarray(im_arr)
            temp_img = apply_radial_zoom_blur(temp_img, intensity=0.035, num_steps=5)
            im_arr = np.array(temp_img, dtype=np.uint8)

        out_name = f"WT3D_Post_{f_num:04d}.png"
        out_path = os.path.join(processed_dir, out_name)
        Image.fromarray(im_arr).save(out_path, format="PNG")
        
        if f_num % 60 == 0 or f_num == total:
            print(f"  [Post-FX] Processed {f_num}/{total} frames ({(f_num/total)*100:.1f}%)")

    return True

def encode_mp4(input_dir, fps=60, audio_path=None, output_name="WT3D_Supercar_Edit_60FPS.mp4"):
    ffmpeg_exe = "ffmpeg.exe"
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        candidate_ffmpeg = [
            r"C:\Users\PHAN TRONG TAN\AppData\Roaming\Python\Python312\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe",
            r"C:\ProgramData\chocolatey\bin\ffmpeg.exe",
            "ffmpeg.exe"
        ]
        for cf in candidate_ffmpeg:
            if os.path.exists(cf):
                ffmpeg_exe = cf
                break
        
    post_dir = os.path.join(input_dir, "post_processed")
    input_pattern = os.path.join(post_dir, "WT3D_Post_%04d.png")
    output_mp4 = os.path.join(input_dir, output_name)
    
    if audio_path is None or not os.path.exists(audio_path):
        candidate_audio = [
            r"D:\WT3D_Project\Z_Tools\Audio\CAM3_Phonk.mp3",
            r"D:\WT3D_Project\industrial-3d-models\Z_Tools\Audio\CAM3_Phonk.mp3",
            r"D:\WT3D_Project\industrial-3d-models\04_AUDIO_STUDIO\02_Processed_Shorts_Audio\CAM3_Phonk.mp3",
            r"D:\WT3D_Project\Z_Tools\CAM3_Phonk.mp3"
        ]
        for ca in candidate_audio:
            if os.path.exists(ca):
                audio_path = ca
                break

    audio_cmd = []
    if audio_path and os.path.exists(audio_path):
        print(f"Muxing audio track: {audio_path}")
        audio_cmd = ["-i", audio_path, "-c:a", "aac", "-b:a", "192k", "-shortest"]
        
    cmd = [
        ffmpeg_exe, "-y",
        "-framerate", str(fps),
        "-i", input_pattern
    ] + audio_cmd + [
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_mp4
    ]
    
    print("Running FFmpeg 60 FPS Master Encoding...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg Error:", res.stderr)
        return False
        
    print(f"Master MP4 generated successfully: {output_mp4}")
    
    # Cleanup post_processed png frames
    try:
        for f in glob.glob(os.path.join(post_dir, "WT3D_Post_*.png")):
            os.remove(f)
        os.rmdir(post_dir)
    except Exception:
        pass
        
    try:
        subprocess.Popen(["explorer.exe", f"/select,{output_mp4}"])
    except Exception:
        pass
        
    return True

def main():
    parser = argparse.ArgumentParser(description="WT3D Supercar Cinematic Post-FX Engine")
    parser.add_argument("--input-dir", required=True, help="Directory containing rendered frames and telemetry")
    parser.add_argument("--fps", type=int, default=60, help="Output framerate (default: 60)")
    parser.add_argument("--audio", default=None, help="Audio file path")
    parser.add_argument("--output", default="WT3D_Supercar_Edit_60FPS.mp4", help="Output MP4 filename")
    
    args = parser.parse_args()
    if not os.path.exists(args.input_dir):
        print(f"Error: Directory {args.input_dir} does not exist.")
        sys.exit(1)
        
    success = process_frames(args.input_dir, fps=args.fps)
    if success:
        encode_mp4(args.input_dir, fps=args.fps, audio_path=args.audio, output_name=args.output)
    else:
        print("Post-FX processing failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
