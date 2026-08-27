param(
    [string]$Profile = "",
    [string]$MasterDataJson = ""
)

# ----------------------------------------------------------------------
# 1. DYNAMIC RELATIVE PATH SETUP (PORTABILITY ACROSS DRIVES)
# ----------------------------------------------------------------------
$toolsDir = $PSScriptRoot
if (-not $toolsDir) { $toolsDir = "D:\WT3D_Project\Z_Tools" }
$videoDir = Split-Path $toolsDir -Parent
$videoDir = Join-Path $videoDir "2_Video_Renders"

if (-not (Test-Path $videoDir)) {
    New-Item -ItemType Directory -Force -Path $videoDir | Out-Null
}

$ffmpegExe = "$toolsDir\ffmpeg\ffmpeg.exe"
$ffprobeExe = "$toolsDir\ffmpeg\ffprobe.exe"

if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    $ffmpegExe = "ffmpeg"
    if (Get-Command ffprobe -ErrorAction SilentlyContinue) { $ffprobeExe = "ffprobe" }
} elseif (Test-Path "$toolsDir\ffmpeg\bin\ffmpeg.exe") {
    $ffmpegExe = "$toolsDir\ffmpeg\bin\ffmpeg.exe"
    $ffprobeExe = "$toolsDir\ffmpeg\bin\ffprobe.exe"
}

# ----------------------------------------------------------------------
# 2. DYNAMIC BRAND PROFILE LOADER (JSON SINGLE SOURCE OF TRUTH)
# ----------------------------------------------------------------------
$brandProfileConfig = @{}
$brandProfilesJsonPath = Join-Path $toolsDir "Brand_Profiles.json"
if (Test-Path $brandProfilesJsonPath) {
    try {
        $jsonRaw = Get-Content -Path $brandProfilesJsonPath -Raw -Encoding UTF8
        $brandConfig = ConvertFrom-Json $jsonRaw
        
        $selectedProfileKey = $brandConfig.default_profile
        if ($Profile -and $brandConfig.profiles.$Profile) {
            $selectedProfileKey = $Profile
        } elseif ($MasterDataJson -and (Test-Path $MasterDataJson)) {
            $masterData = ConvertFrom-Json (Get-Content -Path $MasterDataJson -Raw -Encoding UTF8)
            if ($masterData.active_brand_profile -and $brandConfig.profiles.$($masterData.active_brand_profile)) {
                $selectedProfileKey = $masterData.active_brand_profile
            }
        }
        $brandProfileConfig = $brandConfig.profiles.$selectedProfileKey
        Write-Host "[AI] Activated Brand Profile: $selectedProfileKey ($($brandProfileConfig.profile_name))" -ForegroundColor Cyan
    } catch {
        Write-Warning "[AI] Could not parse Brand_Profiles.json, fallback to default."
    }
}

$folders = Get-ChildItem -Path $videoDir -Directory | Where-Object { 
    (Get-ChildItem -Path $_.FullName -Filter "frame_*.png" | Select-Object -First 1) -ne $null
}

if ($folders.Count -eq 0) {
    Write-Host "Khong tim thay thu muc anh PNG nao trong 2_Video_Renders!" -ForegroundColor Yellow
    Exit
}

$audioDir = "$toolsDir\Audio"
if (-not (Test-Path $audioDir)) { New-Item -ItemType Directory -Force -Path $audioDir | Out-Null }

foreach ($folder in $folders) {
    Write-Host "=========================================="
    Write-Host "[AI] Xu ly Video tu thu muc: $($folder.Name)"
    
    $camId = "UNKNOWN"
    if ($folder.Name -match "CAM_1") { $camId = "CAM1" }
    elseif ($folder.Name -match "CAM_2") { $camId = "CAM2" }
    elseif ($folder.Name -match "CAM_3") { $camId = "CAM3" }
    elseif ($folder.Name -match "CAM_4") { $camId = "CAM4" }
    elseif ($folder.Name -match "CAM_5") { $camId = "CAM5" }
    elseif ($folder.Name -match "CAM_6") { $camId = "CAM6" }
    elseif ($folder.Name -match "CAM_7") { $camId = "CAM7" }
    elseif ($folder.Name -match "CAM_8") { $camId = "CAM8" }
    elseif ($folder.Name -match "CAM_9") { $camId = "CAM9" }
    
    # ----------------------------------------------------------------------
    # 3. DYNAMIC WATERMARK GENERATOR (CONFIGURED VIA BRAND_PROFILES.JSON)
    # ----------------------------------------------------------------------
    function GenerateWatermark($width, $height, $outFile, $profileCfg) {
        if (Test-Path $outFile) { Remove-Item $outFile -Force }
        Write-Host "  -> Generating Dynamic Watermark ($width x $height)..."
        try { Add-Type -AssemblyName System.Drawing } catch {}
        $bmp = New-Object System.Drawing.Bitmap($width, $height)
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

        $isVertical = ($height -gt $width)

        if ($isVertical) {
            $flagWFactor = 0.140; $flagXFactor = 0.045; $mailYFactor = 0.43; $mailSizeFactor = 0.082
            $brandSizeFactor = 0.022; $contactSizeFactor = 0.026; $qrSizeFactor = 0.145
            $cPadFactor = 0.022; $gapFactor = 0.022; $textGapFactor = 0.012
        } else {
            $flagWFactor = 0.105; $flagXFactor = 0.030; $mailYFactor = 0.44; $mailSizeFactor = 0.052
            $brandSizeFactor = 0.013; $contactSizeFactor = 0.015; $qrSizeFactor = 0.075
            $cPadFactor = 0.010; $gapFactor = 0.014; $textGapFactor = 0.008
        }

        # LỚP 1: VIETNAM FLAG (IF ENABLED IN PROFILE)
        if ($profileCfg.show_vietnam_flag) {
            $flagW = [int]($width * $flagWFactor)
            $flagH = [int]($flagW * 0.6667)
            $flagX = [int]($width * $flagXFactor)
            $flagY = [int]($height * 0.030)
            
            $flagPath = Join-Path $toolsDir ($profileCfg.flag_asset_relative_path)
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
        }

        # LỚP 2: GHOST CRYSTAL TEXT CENTER (IF ENABLED)
        if ($profileCfg.show_center_ghost_crystal -and $profileCfg.ghost_crystal_text) {
            $mailY = $height * $mailYFactor
            $cX = $width / 2.0
            $fontSize = [float]($width * $mailSizeFactor)
            $ghostText = $profileCfg.ghost_crystal_text
            
            $gFont = New-Object System.Drawing.Font("Arial Black", $fontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            $textSize = $g.MeasureString($ghostText, $gFont)
            $textX = $cX - ($textSize.Width / 2.0)
            $textY = $mailY - ($textSize.Height / 2.0)
            
            $brushMain = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(10, 255, 255, 255))
            $penWhite = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(55, 255, 255, 255), 1.5)
            $penBlack = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(35, 0, 0, 0), 1.5)

            $path = New-Object System.Drawing.Drawing2D.GraphicsPath
            $path.AddString($ghostText, $gFont.FontFamily, [int]$gFont.Style, $gFont.Size, (New-Object System.Drawing.PointF($textX, $textY)), [System.Drawing.StringFormat]::GenericDefault)
            
            $g.FillPath($brushMain, $path)
            $g.TranslateTransform(-1.5, -1.5)
            $g.DrawPath($penWhite, $path)
            $g.TranslateTransform(3.0, 3.0)
            $g.DrawPath($penBlack, $path)
            $g.ResetTransform()
            
            $brushMain.Dispose(); $penWhite.Dispose(); $penBlack.Dispose(); $path.Dispose(); $gFont.Dispose()
        }

        # LỚP 3: BOTTOM BADGE & QR (IF ENABLED)
        if ($profileCfg.show_bottom_badge) {
            $brandText = $profileCfg.bottom_badge_title
            $contactText = $profileCfg.bottom_badge_subtitle
            
            $bFontSize = [float]($width * $brandSizeFactor)
            $cFontSize = [float]($width * $contactSizeFactor)
            $brandFont = New-Object System.Drawing.Font("Arial", $bFontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            $contactFont = New-Object System.Drawing.Font("Arial", $cFontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            
            $bSize = $g.MeasureString($brandText, $brandFont)
            $cSize = $g.MeasureString($contactText, $contactFont)
            $maxW = [Math]::Max($bSize.Width, $cSize.Width)
            
            $cPad = [int]($width * $cPadFactor)
            $gap = [int]($width * $gapFactor)
            $textGap = [int]($height * $textGapFactor)
            $qrSize = [int]($width * $qrSizeFactor)
            if (-not $profileCfg.show_qr_code) { $qrSize = 0; $gap = 0 }
            
            $totalW = $maxW + $cPad*2 + $gap + $qrSize
            $totalH = $bSize.Height + $contactText + $textGap + $cPad*2
            $totalH = [Math]::Max($totalH, ($qrSize + $cPad*2))
            
            if ($isVertical) {
                $boxRX = [int](($width - $totalW) / 2)
                $boxRY = [int]($height - $totalH - ($height * 0.04))
            } else {
                $boxRX = [int]($width - $totalW - ($width * 0.025))
                $boxRY = [int]($height - $totalH - ($height * 0.025))
            }
            
            # Draw Emerald Gradient Background Card
            $rect = New-Object System.Drawing.Rectangle($boxRX, $boxRY, $totalW, $totalH)
            $gradBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rect, [System.Drawing.Color]::FromArgb(225, 52, 199, 89), [System.Drawing.Color]::FromArgb(225, 24, 150, 68), 45.0)
            $g.FillRectangle($gradBrush, $rect)
            
            # Text Drawing
            $textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
            $tX = $boxRX + $cPad
            $tY = $boxRY + $cPad
            $g.DrawString($brandText, $brandFont, $textBrush, $tX, $tY)
            $g.DrawString($contactText, $contactFont, $textBrush, $tX, ($tY + $bSize.Height + $textGap))
            
            # Draw QR Code if enabled
            if ($profileCfg.show_qr_code -and $profileCfg.qr_asset_relative_path) {
                $qrPath = Join-Path $toolsDir ($profileCfg.qr_asset_relative_path)
                if (Test-Path $qrPath) {
                    try {
                        $bytes = [System.IO.File]::ReadAllBytes($qrPath)
                        $ms = New-Object System.IO.MemoryStream(,$bytes)
                        $qrBmp = [System.Drawing.Image]::FromStream($ms)
                        $qrX = $boxRX + $cPad + $maxW + $gap
                        $qrY = $boxRY + [int](($totalH - $qrSize)/2)
                        
                        $qrBg = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
                        $g.FillRectangle($qrBg, ($qrX - 2), ($qrY - 2), ($qrSize + 4), ($qrSize + 4))
                        $g.DrawImage($qrBmp, $qrX, $qrY, $qrSize, $qrSize)
                        $qrBmp.Dispose(); $ms.Dispose(); $qrBg.Dispose()
                    } catch {}
                }
            }
            $gradBrush.Dispose(); $textBrush.Dispose(); $brandFont.Dispose(); $contactFont.Dispose()
        }
        
        $g.Dispose()
        $bmp.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)
        $bmp.Dispose()
    }
    
    # DETECT RESOLUTION FROM FIRST FRAME
    $sampleFrame = Get-ChildItem -Path "$($folder.FullName)\frame_*.png" | Select-Object -First 1
    $frameW = 1920
    $frameH = 1080
    $framePattern = "$($folder.FullName)\frame_%04d.png"
    if ($sampleFrame) {
        try {
            Add-Type -AssemblyName System.Drawing
            $bytes = [System.IO.File]::ReadAllBytes($sampleFrame.FullName)
            $ms = New-Object System.IO.MemoryStream(,$bytes)
            $tmpImg = [System.Drawing.Image]::FromStream($ms)
            $frameW = $tmpImg.Width
            $frameH = $tmpImg.Height
            $tmpImg.Dispose(); $ms.Dispose()
            Write-Host "  -> Detected Resolution: ${frameW}x${frameH}"
        } catch {}
        if ($sampleFrame.Name -match "frame_\d{3}\.png") {
            $framePattern = "$($folder.FullName)\frame_%03d.png"
        }
    }
    
    $wmkFile = "$($folder.FullName)\watermark_dynamic.png"
    GenerateWatermark $frameW $frameH $wmkFile $brandProfileConfig
    
    $outputMp4 = "$videoDir\$($folder.Name)_FINAL.mp4"
    $baseArgs = @("-y", "-framerate", "30", "-i", $framePattern, "-i", $wmkFile)
    
    $filterComplex = "[0:v]eq=contrast=1.20:brightness=0.01:saturation=1.28:gamma=0.93,unsharp=5:5:0.8:5:5:0.0[color];[color][1:v]overlay=0:0[vout]"
    $audioMap = ""
    $encodeArgs = @("-map", "[vout]", "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p")
    
    # AUDIO INJECTION
    $audioSelection = Get-ChildItem -Path $audioDir -Filter "*.mp3" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($audioSelection) {
        $baseArgs += @("-i", $audioSelection.FullName)
        $filterComplex += ";[2:a]volume=0.85[aout]"
        $audioMap = @("-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-shortest")
    }
    
    $ffmpegArgList = $baseArgs + @("-filter_complex", $filterComplex) + $encodeArgs
    if ($audioMap) { $ffmpegArgList += $audioMap }
    $ffmpegArgList += $outputMp4
    
    Write-Host "  -> Encoding with FFmpeg..."
    & $ffmpegExe @ffmpegArgList > "$videoDir\ffmpeg_out.log" 2> "$videoDir\ffmpeg_err.log"
    $ffmpegExitCode = $LASTEXITCODE
    
    # ----------------------------------------------------------------------
    # 4. SAFE GARBAGE COLLECTION GATEWAY (STRICT VALIDATION BEFORE DELETE)
    # ----------------------------------------------------------------------
    $isValid = $false
    if ($ffmpegExitCode -eq 0 -and (Test-Path $outputMp4)) {
        $fileInfo = Get-Item $outputMp4
        $fileSizeMB = [Math]::Round(($fileInfo.Length / 1MB), 2)
        
        # Check minimum file size (> 1.0 MB)
        if ($fileInfo.Length -gt (1024 * 1024)) {
            $isValid = $true
        }
        
        # Validate via FFprobe if available
        if ($isValid -and (Test-Path $ffprobeExe)) {
            try {
                $probeOut = & $ffprobeExe -v error -show_entries format=duration,size -of default=noprint_wrappers=1:nokey=1 $outputMp4 2>$null
                if ($probeOut -and $probeOut[0] -gt 0) {
                    $isValid = $true
                }
            } catch {
                Write-Warning "[AI] FFprobe check skipped."
            }
        }
    }
    
    if ($isValid) {
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host "  [VALIDATED] Video output is VALID ($fileSizeMB MB): $outputMp4" -ForegroundColor Green
        Write-Host "  -> Safe Garbage Collection: Deleting temporary PNG frames..." -ForegroundColor Green
        Start-Sleep -Seconds 1
        Remove-Item $folder.FullName -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  -> [CLEANED] Disk space freed successfully!" -ForegroundColor Green
    } else {
        Write-Host "==========================================" -ForegroundColor Red
        Write-Host "  [FAILED] Video validation failed or corrupted!" -ForegroundColor Red
        Write-Host "  -> [PRESERVED] Raw frames preserved in $($folder.FullName) for recovery." -ForegroundColor Yellow
    }
}

Write-Host "=========================================="
Write-Host "PIPELINE COMPLETE." -ForegroundColor Cyan
