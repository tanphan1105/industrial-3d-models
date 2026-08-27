param(
    [Parameter(Mandatory=$true)]
    [string]$TargetFolder
)

$toolsDir = "d:\WT3D_Project\Z_Tools"
$ffmpegExe = "$toolsDir\ffmpeg\ffmpeg.exe"
$ffmpegZip = "$toolsDir\ffmpeg.zip"

# ==========================================
# 1. KIỂM TRA & TỰ ĐỘNG TẢI FFMPEG (Auto-Deploy)
# ==========================================
if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    # Ưu tiên FFmpeg hệ thống (đã cài đặt qua winget)
    $ffmpegExe = "ffmpeg"
} elseif (-not (Test-Path $ffmpegExe)) {
    Write-Host "[AI] Chưa có Lõi FFmpeg. Bắt đầu tự động lấy từ kho vũ khí..."
    New-Item -ItemType Directory -Force -Path "$toolsDir\ffmpeg" | Out-Null
    
    # Kéo công cụ mã nguồn mở xịn nhất về
    $url = "https://github.com/GyanD/codexffmpeg/releases/download/7.0.1/ffmpeg-7.0.1-essentials_build.zip"
    try {
        Invoke-WebRequest -Uri $url -OutFile $ffmpegZip -UseBasicParsing
        Expand-Archive -Path $ffmpegZip -DestinationPath "$toolsDir\ffmpeg_temp" -Force
        
        # Di chuyển cái file exe bé xíu ra cho nhẹ
        $extractedExe = Get-ChildItem -Path "$toolsDir\ffmpeg_temp" -Filter "ffmpeg.exe" -Recurse | Select-Object -First 1
        Move-Item -Path $extractedExe.FullName -Destination $ffmpegExe -Force
        
        # Dọn dẹp rác chiến trường
        Remove-Item -Path "$toolsDir\ffmpeg_temp" -Recurse -Force
        Remove-Item -Path $ffmpegZip -Force
    } catch {
        # Fallback offline ngầm
        Write-Host "Lỗi mạng khi tải lõi FFmpeg. Xin sếp kiểm tra Wifi!"
        Exit
    }
}

# ==========================================
# 2. BỘ TRỘN ÂM THANH NỐI TIẾP (TÌNH HUỐNG A)
# ==========================================
$audioDir = "$toolsDir\Audio"
if (-not (Test-Path $audioDir)) { New-Item -ItemType Directory -Force -Path $audioDir | Out-Null }

$audio1 = "$audioDir\1.mp3"
$audio2 = "$audioDir\2.mp3"

$hasAudio1 = (Test-Path $audio1)
$hasAudio2 = (Test-Path $audio2)

if ($hasAudio1 -and $hasAudio2) {
    Write-Host "[AI] Kich hoat Chuoi Am thanh Lien hoan (Tinh huong A): 1.mp3 -> 2.mp3"
    $audioMode = "ConcatDual"
}
if ($hasAudio1 -and (-not $hasAudio2)) {
    Write-Host "[AI] Kich hoat Am thanh Don: 1.mp3"
    $audioMode = "Single1"
}
if ((-not $hasAudio1) -and $hasAudio2) {
    Write-Host "[AI] Kich hoat Am thanh Don: 2.mp3"
    $audioMode = "Single2"
}
if ((-not $hasAudio1) -and (-not $hasAudio2)) {
    Write-Host "[AI] Khong tim thay 1.mp3 hoac 2.mp3. Khoa luong am thanh."
    $audioMode = "None"
}

# ==========================================
# 3. QUY TRÌNH WATERMARK & KẾT XUẤT (COMPILER)
# ==========================================
Write-Host "[AI] Đang nhào nặn phim tại: $TargetFolder"
$baseName = (Get-Item $TargetFolder).Name

# Bóc tách tên thật của Model từ tên folder (ví dụ TESLA_lay oz -> lay oz)
$modelName = $baseName
if ($baseName -match "^[A-Z]+_(.+)$") {
    $modelName = $matches[1]
}

$parentFolder = Split-Path $TargetFolder -Parent
$outputMp4 = "$parentFolder\${baseName}.mp4"

if (Test-Path $outputMp4) { Remove-Item $outputMp4 -Force }

$wmkFile = "$TargetFolder\watermark.png"

# ==========================================
# 3.5 BỘ MÁY ĐÚC TẠO WATERMARK (APPLE GREEN B2B STANDARD)
# Cơ chế phòng thủ: Nếu các khối iLogic chưa xuất watermark, PS sẽ tự thợ.
# Tự động gánh luôn cho tất cả Cinematic Styles chưa được nâng cấp.
# ==========================================
if (-not (Test-Path $wmkFile)) {
    Write-Host "[AI] Đang nung nóng Lớp Thủy Tinh Bản Quyền (Watermark Engine)..."
    Add-Type -AssemblyName System.Drawing
    $bmp = New-Object System.Drawing.Bitmap(1920, 1080)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    
    # Kính giữa tàng hình
    $state = $g.Save()
    $g.TranslateTransform(1920 / 2, 1080 / 2)
    $mailText = "trongtan.p@icloud.com"
    $mailFont = New-Object System.Drawing.Font("Arial", 60, [System.Drawing.FontStyle]::Bold)
    $gp = New-Object System.Drawing.Drawing2D.GraphicsPath
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $gp.AddString($mailText, $mailFont.FontFamily, $mailFont.Style, $mailFont.Size, (New-Object System.Drawing.PointF(0, 0)), $sf)
    $pThick = 2
    $darkPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(15, 0, 0, 0), $pThick)
    $g.TranslateTransform(2, 2)
    $g.DrawPath($darkPen, $gp)
    $g.TranslateTransform(-2, -2)
    $lightPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(25, 255, 255, 255), $pThick)
    $g.TranslateTransform(-2, -2)
    $g.DrawPath($lightPen, $gp)
    $g.TranslateTransform(2, 2)
    $g.Restore($state)
    
    # Hộp Xanh Lá
    $brandText = "WATER FILTER 3D DESIGN"
    $brandFont = New-Object System.Drawing.Font("Arial Narrow", 30, [System.Drawing.FontStyle]::Bold)
    $contactText = "trongtan.p@icloud.com | +84985267326"
    $contactFont = New-Object System.Drawing.Font("Arial Narrow", 20, [System.Drawing.FontStyle]::Bold)
    
    $brandSz = $g.MeasureString($brandText, $brandFont)
    $contactSz = $g.MeasureString($contactText, $contactFont)
    $maxW = [Math]::Max($brandSz.Width, $contactSz.Width)
    $qrSize = 100
    $cPad = 20
    $totalW = $maxW + 25 + $qrSize
    $textBlockH = $brandSz.Height + $contactSz.Height + 10
    $totalH = [Math]::Max($textBlockH, $qrSize)
    $boxRX = 1920 - $totalW - 40 - $cPad*2
    $boxRY = 1080 - $totalH - 40 - $cPad*2
    
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $r = 20
    $path.AddArc($boxRX, $boxRY, $r, $r, 180, 90)
    $path.AddArc($boxRX + $totalW + $cPad*2 - $r, $boxRY, $r, $r, 270, 90)
    $path.AddArc($boxRX + $totalW + $cPad*2 - $r, $boxRY + $totalH + $cPad*2 - $r, $r, $r, 0, 90)
    $path.AddArc($boxRX, $boxRY + $totalH + $cPad*2 - $r, $r, $r, 90, 90)
    $path.CloseAllFigures()
    
    $bgBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(235, 52, 199, 89))
    $g.FillPath($bgBrush, $path)
    $borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(180, 255, 255, 255), 2)
    $g.DrawPath($borderPen, $path)
    
    $currY = $boxRY + $cPad + ($totalH - $textBlockH) / 2
    Function DrawShadow($grp, $txt, $fnt, $x, $y, $alpha) {
        $sb = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(50, 0, 0, 0))
        $grp.DrawString($txt, $fnt, $sb, $x + 2, $y + 2)
        $sb.Dispose()
        $mb = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb($alpha, 255, 255, 255))
        $grp.DrawString($txt, $fnt, $mb, $x, $y)
        $mb.Dispose()
    }
    
    DrawShadow $g $brandText $brandFont ($boxRX + $cPad) $currY 255
    $currY += $brandSz.Height + 10
    DrawShadow $g $contactText $contactFont ($boxRX + $cPad) $currY 220
    
    $qrPath = [System.IO.Path]::GetTempPath() + "wt3d_qr_checkgreen_v1.png"
    if (-not (Test-Path $qrPath)) {
        try {
            Invoke-WebRequest -Uri 'https://api.qrserver.com/v1/create-qr-code/?size=300x300&margin=0&color=ffffff&bgcolor=34c759&data=https://zalo.me/84985267326' -OutFile $qrPath -UseBasicParsing -TimeoutSec 10
        } catch {}
    }
    if (Test-Path $qrPath) {
        $qrBmp = New-Object System.Drawing.Bitmap($qrPath)
        $g.DrawImage($qrBmp, ($boxRX + $cPad + $maxW + 25), ($boxRY + $cPad + ($totalH - $qrSize)/2), $qrSize, $qrSize)
        $qrBmp.Dispose()
    }
    
    $bmp.Save($wmkFile, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
}

# Lập trình Bộ lọc FFmpeg (Pipeline Render Đồng bộ 100% Ảnh Tĩnh)
$baseArgs = @("-y", "-framerate", "30", "-i", "$TargetFolder\frame_%03d.png", "-i", $wmkFile)
$encodeArgs = @("-map", "[vout]", "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p")

if ($audioMode -eq "ConcatDual") {
    $ffmpegArgList = $baseArgs + @("-i", $audio1, "-i", $audio2) + @("-filter_complex", "[2:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a1];[3:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a2];[a1][a2]concat=n=2:v=0:a=1[cat];[cat]apad[aout];[0:v][1:v]overlay=0:0[vout]") + $encodeArgs + @("-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-shortest", $outputMp4)
} elseif ($audioMode -eq "Single1") {
    $ffmpegArgList = $baseArgs + @("-i", $audio1) + @("-filter_complex", "[0:v][1:v]overlay=0:0[vout];[2:a]apad[aout]") + $encodeArgs + @("-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-shortest", $outputMp4)
} elseif ($audioMode -eq "Single2") {
    $ffmpegArgList = $baseArgs + @("-i", $audio2) + @("-filter_complex", "[0:v][1:v]overlay=0:0[vout];[2:a]apad[aout]") + $encodeArgs + @("-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-shortest", $outputMp4)
} else {
    $ffmpegArgList = $baseArgs + @("-filter_complex", "[0:v][1:v]overlay=0:0[vout]") + $encodeArgs + @($outputMp4)
}

Write-Host "Action! Đang đúc Video 4K + Đóng dấu Bản Quyền..."

# Gọi trực tiếp Lõi FFmpeg ngầm trong PowerShell, né tránh mọi lỗi Parser của Strings / CMD / Bat
& $ffmpegExe @ffmpegArgList

Write-Host "XONG! Tác phẩm xuất tại: $outputMp4"
Start-Process "explorer.exe" -ArgumentList "/select,`"$outputMp4`""
