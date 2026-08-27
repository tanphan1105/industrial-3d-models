param(
    [Parameter(Mandatory=$true)]
    [string]$TargetFolder
)

$toolsDir = "d:\WT3D_Project\Z_Tools"
$ffmpegExe = "$toolsDir\ffmpeg\ffmpeg.exe"

# ==========================================
# 1. CHECK & AUTO-DEPLOY FFMPEG
# ==========================================
if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    $ffmpegExe = "ffmpeg"
} elseif (-not (Test-Path $ffmpegExe)) {
    Write-Host "[AI] FFmpeg not found. Auto-downloading..."
    New-Item -ItemType Directory -Force -Path "$toolsDir\ffmpeg" | Out-Null
    
    $url = "https://github.com/GyanD/codexffmpeg/releases/download/7.0.1/ffmpeg-7.0.1-essentials_build.zip"
    try {
        $zipFile = "$toolsDir\ffmpeg_download.zip"
        Invoke-WebRequest -Uri $url -OutFile $zipFile -UseBasicParsing
        Expand-Archive -Path $zipFile -DestinationPath "$toolsDir\ffmpeg_unpack" -Force
        
        $extractedExe = Get-ChildItem -Path "$toolsDir\ffmpeg_unpack" -Filter "ffmpeg.exe" -Recurse | Select-Object -First 1
        Move-Item -Path $extractedExe.FullName -Destination $ffmpegExe -Force
        
        Remove-Item -Path "$toolsDir\ffmpeg_unpack" -Recurse -Force
        Remove-Item -Path $zipFile -Force
    } catch {
        Write-Host "Network error downloading FFmpeg. Check internet!"
        Exit
    }
}

# ==========================================
# 2. AUDIO CHAIN SETUP (SMART MUSIC ALLOCATION)
# ==========================================
$audioDir = "$toolsDir\Audio"
if (-not (Test-Path $audioDir)) { New-Item -ItemType Directory -Force -Path $audioDir | Out-Null }

$assignedAudio = ""

if ($TargetFolder -match "NIGHTCRAWLER_V43") {
    $assignedAudio = "$audioDir\CAM2_SciFi.mp3"
    Write-Host "[AI] Detected v4.3 B2B Commercial -> Using Tech/SciFi Music"
} elseif ($TargetFolder -match "SHORTS_MAXSKILLS_") {
    $assignedAudio = "$audioDir\CAM3_Phonk.mp3"
    Write-Host "[AI] Detected v4.3 Tension Shorts -> Using Phonk Music"
} elseif ($TargetFolder -match "MAXSKILLS_SHORTS_") {
    $assignedAudio = "$audioDir\CAM4_Glitch.mp3"
    Write-Host "[AI] Detected 9:16 Deep Core -> Using Hyper Glitch Music"
} elseif ($TargetFolder -match "MAXSKILLS") {
    $assignedAudio = "$audioDir\CAM1_Epic.mp3"
    Write-Host "[AI] Detected v4.1 Cinematic Masterpiece -> Using Epic Cinematic Music"
} else {
    $assignedAudio = "$audioDir\1.mp3"
    Write-Host "[AI] Unknown engine -> Fallback to 1.mp3"
}

$hasAudio = (Test-Path $assignedAudio)

$audioMode = "None"
if ($hasAudio) {
    Write-Host "[AI] Audio Mode: Smart Single ($assignedAudio)"
    $audioMode = "SmartSingle"
} else {
    Write-Host "[AI] No matching audio files found. Silent video mode."
}

# ==========================================
# 3. WATERMARK & COMPILE PIPELINE
# ==========================================
Write-Host "[AI] Processing video at: $TargetFolder"
$baseName = (Get-Item $TargetFolder).Name
$parentFolder = Split-Path $TargetFolder -Parent
$actualModelName = Split-Path $parentFolder -Leaf

$modelName = $actualModelName
if ($actualModelName -match "^[A-Z]+_(.+)$") {
    $modelName = $matches[1]
}

# Fix edge case where the TargetFolder is already in 2_Video_Renders (v4.3 Shorts case)
if ($actualModelName -match "Video_Renders") {
    # Extract model name directly from TargetFolder
    if ($baseName -match "SHORTS_MAXSKILLS_(.+)") {
        $modelName = $matches[1]
        $parentFolder = "d:\WT3D_Project\1_Exports_Batch\$modelName"
    } else {
        $modelName = "Unknown_Model"
    }
}

$outputMp4 = "$parentFolder\${baseName}.mp4"

if (Test-Path $outputMp4) { Remove-Item $outputMp4 -Force }

$wmkFile = "$TargetFolder\watermark.png"
if (Test-Path $wmkFile) { Remove-Item $wmkFile -Force }

# ==========================================
# 3.5 WATERMARK GENERATOR (LOCKED MASTER SPECIFICATION)
# ==========================================
Write-Host "[AI] Generating Fresh QHD Watermark overlay..."
Add-Type -AssemblyName System.Drawing
    $width = 2560
    $height = 1440
    $isVertical = $false
    
    $bmp = New-Object System.Drawing.Bitmap($width, $height)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

    # ----------------------------------------------------------------------
    # LỚP 1: LÁ CỜ VIỆT NAM (GÓC TRÊN BÊN TRÁI)
    # ----------------------------------------------------------------------
    $flagW = [int]($width * 0.105)
    $flagH = [int]($flagW * 0.6667)
    $flagX = [int]($width * 0.030)
    $flagY = [int]($height * 0.030)
    
    $flagPath = "$toolsDir\vietnam_flag.png"
    if (-not (Test-Path $flagPath)) {
        $flagPath = [System.IO.Path]::GetTempPath() + "vietnam_flag.png"
    }
    if (Test-Path $flagPath) {
        try {
            $bytes = [System.IO.File]::ReadAllBytes($flagPath)
            $ms = New-Object System.IO.MemoryStream(,$bytes)
            $flagImg = [System.Drawing.Image]::FromStream($ms)
            $g.DrawImage($flagImg, $flagX, $flagY, $flagW, $flagH)
            $flagImg.Dispose()
            $ms.Dispose()
        } catch {}
    }

    # ----------------------------------------------------------------------
    # LỚP 2: BẢN QUYỀN THỦY TINH KHÓI CHÍNH GIỮA MÀN HÌNH (@tanphan1105)
    # ----------------------------------------------------------------------
    $state2 = $g.Save()
    $mailY = $height * 0.44
    $cX = $width / 2.0
    $g.TranslateTransform($cX, $mailY)
    $mailText = "@tanphan1105"
    $mailSize = [int]($width * 0.052)
    $mailFont = New-Object System.Drawing.Font("Arial Black", $mailSize, [System.Drawing.FontStyle]::Bold)
    $gp2 = New-Object System.Drawing.Drawing2D.GraphicsPath
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $gp2.AddString($mailText, $mailFont.FontFamily, $mailFont.Style, $mailFont.Size, (New-Object System.Drawing.PointF(0, 0)), $sf)
    
    $pThick2 = [Math]::Max(1, [int]($width * 0.0015))
    $offsetPx = [Math]::Max(1, [int]($width * 0.0015))
    
    # BÊN TỐI (Bottom-Right Shadow Edge) - Alpha = 25
    $darkPen2 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(25, 0, 0, 0), $pThick2)
    $g.TranslateTransform($offsetPx, $offsetPx)
    $g.DrawPath($darkPen2, $gp2)
    $g.TranslateTransform(-$offsetPx, -$offsetPx)
    
    # BÊN SÁNG (Top-Left Highlight Edge) - Alpha = 45
    $lightPen2 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(45, 255, 255, 255), $pThick2)
    $g.TranslateTransform(-$offsetPx, -$offsetPx)
    $g.DrawPath($lightPen2, $gp2)
    $g.TranslateTransform($offsetPx, $offsetPx)
    
    # THÂN THỦY TINH CỰC MỜ (Ghost Translucent Core Fill - Alpha = 6)
    $glassBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(6, 255, 255, 255))
    $g.FillPath($glassBrush, $gp2)
    $g.Restore($state2)
    
    # ----------------------------------------------------------------------
    # LỚP 3: THẺ GREEN CARD LOGO DIAGONAL GRADIENT HIGH CONTRAST (WaterTreatment3D + @tanphan1105 + QR)
    # ----------------------------------------------------------------------
    $brandText = "WaterTreatment3D"
    $brandSize = [int]($width * 0.014)
    $brandFont = New-Object System.Drawing.Font("Arial", $brandSize, [System.Drawing.FontStyle]::Bold)
    $contactText = "@tanphan1105 | Zalo: +84.985.267.326"
    $contactSize = [int]($width * 0.021)
    $contactFont = New-Object System.Drawing.Font("Arial", $contactSize, [System.Drawing.FontStyle]::Bold)
    
    $brandSz = $g.MeasureString($brandText, $brandFont)
    $contactSz = $g.MeasureString($contactText, $contactFont)
    $maxW = [Math]::Max($brandSz.Width, $contactSz.Width)
    $textBlockH = $brandSz.Height + $contactSz.Height + [int]($height * 0.008)
    
    $qrSize = [int]($width * 0.092)
    $qrBoxPad = [int]($width * 0.004)
    $qrBoxSize = $qrSize + $qrBoxPad * 2
    
    $cPadX = [int]($width * 0.018)
    $cPadY = [int]($height * 0.014)
    
    # Khung xanh thu hẹp chiều cao ôm sát chữ
    $ribbonH = $textBlockH + $cPadY * 2
    $ribbonW = $maxW + $cPadX * 2 + [int]($qrBoxSize / 2) + [int]($width * 0.010)
    
    $marginR = [int]($width * 0.025)
    $marginB = [int]($height * 0.035)
    
    $qrY = $height - $marginB - $qrBoxSize
    $ribbonY = $qrY + [int](($qrBoxSize - $ribbonH) / 2)
    
    $ribbonX = $width - $marginR - $ribbonW - [int]($qrBoxSize / 2)
    $qrX = $ribbonX + $ribbonW - [int]($qrBoxSize / 2)
    
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $r = [Math]::Max(6, [int]($width * 0.006))
    $path.AddArc($ribbonX, $ribbonY, $r, $r, 180, 90)
    $path.AddArc($ribbonX + $ribbonW - $r, $ribbonY, $r, $r, 270, 90)
    $path.AddArc($ribbonX + $ribbonW - $r, $ribbonY + $ribbonH - $r, $r, $r, 0, 90)
    $path.AddArc($ribbonX, $ribbonY + $ribbonH - $r, $r, $r, 90, 90)
    $path.CloseAllFigures()
    
    # DIAGONAL EMERALD GRADIENT (#34C759 -> #189644) WITH TRANSLUCENCY (Alpha 225 ~ 84%)
    $rectF = New-Object System.Drawing.RectangleF($ribbonX, $ribbonY, $ribbonW, $ribbonH)
    $c1 = [System.Drawing.Color]::FromArgb(225, 52, 199, 89)
    $c2 = [System.Drawing.Color]::FromArgb(220, 24, 150, 68)
    $gradBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rectF, $c1, $c2, 45.0)
    $g.FillPath($gradBrush, $path)
    $gradBrush.Dispose()

    # THIN WHITE BORDER OUTLINE = 1PX
    $borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(240, 255, 255, 255), 1)
    $g.DrawPath($borderPen, $path)
    $borderPen.Dispose()
    
    $currY = $ribbonY + $cPadY
    
    # GAUSSIAN SOFT AMBIENT SHADOW
    $sbShadow = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(110, 10, 40, 15))
    $g.DrawString($brandText, $brandFont, $sbShadow, $ribbonX + $cPadX + 2, $currY + 2)
    
    # CRISP WHITE TEXT WITH WHISPER-THIN 0.8PX OUTLINE
    $mb1 = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
    $g.DrawString($brandText, $brandFont, $mb1, $ribbonX + $cPadX, $currY)
    
    $currY += $brandSz.Height + [int]($height * 0.008)
    $g.DrawString($contactText, $contactFont, $sbShadow, $ribbonX + $cPadX + 2, $currY + 2)
    $g.DrawString($contactText, $contactFont, $mb1, $ribbonX + $cPadX, $currY)
    
    $sbShadow.Dispose(); $mb1.Dispose()

    # OFFICIAL ZALO QR CODE ASSET (POP-OUT TALLER THAN GREEN RIBBON)
    $qrPath = "$toolsDir\wt3d_qr_green.png"
    if (Test-Path $qrPath) {
        try {
            $bytes = [System.IO.File]::ReadAllBytes($qrPath)
            $ms = New-Object System.IO.MemoryStream(,$bytes)
            $qrBmp = [System.Drawing.Image]::FromStream($ms)
            
            # White background box with rounded corners and emerald border
            $qrPathBox = New-Object System.Drawing.Drawing2D.GraphicsPath
            $qrR = 8
            $qrPathBox.AddArc($qrX, $qrY, $qrR, $qrR, 180, 90)
            $qrPathBox.AddArc($qrX + $qrBoxSize - $qrR, $qrY, $qrR, $qrR, 270, 90)
            $qrPathBox.AddArc($qrX + $qrBoxSize - $qrR, $qrY + $qrBoxSize - $qrR, $qrR, $qrR, 0, 90)
            $qrPathBox.AddArc($qrX, $qrY + $qrBoxSize - $qrR, $qrR, $qrR, 90, 90)
            $qrPathBox.CloseAllFigures()
            
            $qrBgBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
            $g.FillPath($qrBgBrush, $qrPathBox)
            $qrBorderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(230, 52, 199, 89), 2)
            $g.DrawPath($qrBorderPen, $qrPathBox)
            
            $g.DrawImage($qrBmp, ($qrX + $qrBoxPad), ($qrY + $qrBoxPad), $qrSize, $qrSize)
            
            $qrBgBrush.Dispose(); $qrBorderPen.Dispose(); $qrPathBox.Dispose()
            $qrBmp.Dispose()
            $ms.Dispose()
        } catch {}
    }
    
    $g.Dispose()
    $bmp.Save($wmkFile, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()

# FFmpeg Pipeline
$baseArgs = @("-y", "-framerate", "30", "-i", "$TargetFolder\frame_%03d.png", "-i", $wmkFile)
$encodeArgs = @("-map", "[vout]", "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p", "-metadata", "title=Industrial Engineering Asset - $actualModelName", "-metadata", "artist=TANPHAN", "-metadata", "copyright=CGTrader B2B Commercial License", "-metadata", "description=Engineered and rendered via Master Blaster Pipeline")

if ($audioMode -eq "SmartSingle") {
    $audioFilter = "[2:a]apad[aout]"
    $ffmpegArgList = $baseArgs + @("-stream_loop", "-1", "-i", $assignedAudio) + @("-filter_complex", "[0:v][1:v]overlay=0:0[vout];$audioFilter") + $encodeArgs + @("-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-shortest", $outputMp4)
} else {
    $ffmpegArgList = $baseArgs + @("-filter_complex", "[0:v][1:v]overlay=0:0[vout]") + $encodeArgs + @($outputMp4)
}

Write-Host "[AI] Stitching video with FFmpeg..."

& $ffmpegExe @ffmpegArgList

Write-Host "[AI] DONE! Output: $outputMp4"

# ==========================================
# DELIVER TO VIDEO REPO & MODEL SUBFOLDER 03_Video_Renders
# ==========================================
$VideoRepo = "d:\WT3D_Project\2_Video_Renders"
if (-not (Test-Path $VideoRepo)) { New-Item -ItemType Directory -Force -Path $VideoRepo }

$camName = "UNKNOWN_CAM"
if ($TargetFolder -match "MAXSKILLS$") {
    $camName = "_CAM_1_FINAL"
} elseif ($TargetFolder -match "NIGHTCRAWLER_V43") {
    $camName = "_CAM_2_FINAL"
} elseif ($TargetFolder -match "SHORTS_MAXSKILLS_") {
    $camName = "_CAM_3_FINAL"
} elseif ($TargetFolder -match "MAXSKILLS_SHORTS_") {
    $camName = "_CAM_4_FINAL"
}

# Optimize model name for SEO (replace spaces with hyphens)
$seoModelName = $modelName -replace ' ', '-'
$finalDelivery = "$VideoRepo\${seoModelName}${camName}.mp4"

# Fallback: if somehow file conflicts, append ticks
if (Test-Path $finalDelivery) {
    Remove-Item $finalDelivery -Force -ErrorAction SilentlyContinue 
    if (Test-Path $finalDelivery) {
        $finalDelivery = "$VideoRepo\${seoModelName}${camName}_$([DateTime]::Now.Ticks).mp4"
    }
}

Copy-Item -Path $outputMp4 -Destination $finalDelivery -Force -ErrorAction SilentlyContinue

# AUTOMATICALLY DELIVER TO 03_Video_Renders SUBFOLDER IN MODEL DIRECTORY
$subVidRepo = "$parentFolder\03_Video_Renders"
if (-not (Test-Path $subVidRepo)) { New-Item -ItemType Directory -Force -Path $subVidRepo | Out-Null }
Copy-Item -Path $outputMp4 -Destination "$subVidRepo\$(Split-Path $outputMp4 -Leaf)" -Force -ErrorAction SilentlyContinue
if (Test-Path $finalDelivery) {
    Copy-Item -Path $finalDelivery -Destination "$subVidRepo\$(Split-Path $finalDelivery -Leaf)" -Force -ErrorAction SilentlyContinue
}

Copy-Item $outputMp4 -Destination $finalDelivery -Force
Write-Host "[AI] Copied to repo: $finalDelivery"

# ==========================================
# DISK VACUUM: DELETE INTERMEDIATE PNG FRAMES
# ==========================================
if (Test-Path $outputMp4) {
    Write-Host "[AI] Cleaning up intermediate files to free disk space..."
    Remove-Item $outputMp4 -Force -ErrorAction SilentlyContinue
    Remove-Item $TargetFolder -Recurse -Force -ErrorAction SilentlyContinue
}
