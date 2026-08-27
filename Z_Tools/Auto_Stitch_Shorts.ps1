param(
    [Parameter(Mandatory=$false)]
    [string]$TargetFolder = "",
    [string]$Profile = "",
    [string]$MasterDataJson = ""
)

# ----------------------------------------------------------------------
# 1. DYNAMIC RELATIVE PATH SETUP
# ----------------------------------------------------------------------
$toolsDir = $PSScriptRoot
if (-not $toolsDir) { $toolsDir = "D:\WT3D_Project\Z_Tools" }
$videoDir = Split-Path $toolsDir -Parent
$videoDir = Join-Path $videoDir "2_Video_Renders"

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
# 2. DYNAMIC BRAND PROFILE LOADER
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
        Write-Warning "[AI] Could not parse Brand_Profiles.json."
    }
}

$foldersToProcess = @()
if ($TargetFolder -and (Test-Path $TargetFolder)) {
    $foldersToProcess += (Get-Item $TargetFolder)
} else {
    $foldersToProcess = Get-ChildItem -Path $videoDir -Directory | Where-Object { 
        (Get-ChildItem -Path $_.FullName -Filter "frame_*.png" | Select-Object -First 1) -ne $null
    }
}

if ($foldersToProcess.Count -eq 0) {
    Write-Host "Khong tim thay frame PNG nao de xu ly!" -ForegroundColor Yellow
    Exit
}

$audioDir = "$toolsDir\Audio"

foreach ($folder in $foldersToProcess) {
    Write-Host "=========================================="
    Write-Host "[AI] Processing 9:16 Shorts Video from: $($folder.Name)"
    
    # DETECT RESOLUTION
    $sampleFrame = Get-ChildItem -Path "$($folder.FullName)\frame_*.png" | Select-Object -First 1
    $frameW = 1080
    $frameH = 1920
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
            Write-Host "  -> Resolution: ${frameW}x${frameH}"
        } catch {}
        if ($sampleFrame.Name -match "frame_\d{3}\.png") {
            $framePattern = "$($folder.FullName)\frame_%03d.png"
        }
    }
    
    # WATERMARK GENERATOR
    function GenerateWatermark($width, $height, $outFile, $profileCfg) {
        if (Test-Path $outFile) { Remove-Item $outFile -Force }
        try { Add-Type -AssemblyName System.Drawing } catch {}
        $bmp = New-Object System.Drawing.Bitmap($width, $height)
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

        # LỚP 1: VIETNAM FLAG
        if ($profileCfg.show_vietnam_flag -and $profileCfg.flag_asset_relative_path) {
            $flagW = [int]($width * 0.140)
            $flagH = [int]($flagW * 0.6667)
            $flagX = [int]($width * 0.045)
            $flagY = [int]($height * 0.030)
            $flagPath = Join-Path $toolsDir ($profileCfg.flag_asset_relative_path)
            if (Test-Path $flagPath) {
                try {
                    $bytes = [System.IO.File]::ReadAllBytes($flagPath)
                    $ms = New-Object System.IO.MemoryStream(,$bytes)
                    $flagImg = [System.Drawing.Image]::FromStream($ms)
                    $g.DrawImage($flagImg, $flagX, $flagY, $flagW, $flagH)
                    $flagImg.Dispose(); $ms.Dispose()
                } catch {}
            }
        }

        # LỚP 2: GHOST CRYSTAL TEXT CENTER
        if ($profileCfg.show_center_ghost_crystal -and $profileCfg.ghost_crystal_text) {
            $mailY = $height * 0.43
            $cX = $width / 2.0
            $fontSize = [float]($width * 0.082)
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

        # LỚP 3: BOTTOM BADGE CARD 9:16 (FULL 90% WIDTH CENTERED)
        if ($profileCfg.show_bottom_badge) {
            $brandText = $profileCfg.bottom_badge_title
            $contactText = $profileCfg.bottom_badge_subtitle
            
            $bFontSize = [float]($width * 0.024)
            $cFontSize = [float]($width * 0.028)
            $brandFont = New-Object System.Drawing.Font("Arial", $bFontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            $contactFont = New-Object System.Drawing.Font("Arial", $cFontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            
            $bSize = $g.MeasureString($brandText, $brandFont)
            $cSize = $g.MeasureString($contactText, $contactFont)
            $maxW = [Math]::Max($bSize.Width, $cSize.Width)
            
            $cPad = [int]($width * 0.025)
            $gap = [int]($width * 0.022)
            $textGap = [int]($height * 0.010)
            $qrSize = [int]($width * 0.145)
            if (-not $profileCfg.show_qr_code) { $qrSize = 0; $gap = 0 }
            
            $totalW = $maxW + $cPad*2 + $gap + $qrSize
            $totalH = $bSize.Height + $contactText + $textGap + $cPad*2
            $totalH = [Math]::Max($totalH, ($qrSize + $cPad*2))
            
            $boxRX = [int](($width - $totalW) / 2)
            $boxRY = [int]($height - $totalH - ($height * 0.045))
            
            $rect = New-Object System.Drawing.Rectangle($boxRX, $boxRY, $totalW, $totalH)
            $gradBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rect, [System.Drawing.Color]::FromArgb(225, 52, 199, 89), [System.Drawing.Color]::FromArgb(225, 24, 150, 68), 45.0)
            $g.FillRectangle($gradBrush, $rect)
            
            $textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
            $tX = $boxRX + $cPad
            $tY = $boxRY + $cPad
            $g.DrawString($brandText, $brandFont, $textBrush, $tX, $tY)
            $g.DrawString($contactText, $contactFont, $textBrush, $tX, ($tY + $bSize.Height + $textGap))
            
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
    
    $wmkFile = "$($folder.FullName)\watermark_dynamic_shorts.png"
    GenerateWatermark $frameW $frameH $wmkFile $brandProfileConfig
    
    $outputMp4 = "$videoDir\$($folder.Name)_SHORTS_FINAL.mp4"
    $baseArgs = @("-y", "-framerate", "30", "-i", $framePattern, "-i", $wmkFile)
    $filterComplex = "[0:v]eq=contrast=1.22:brightness=0.01:saturation=1.30:gamma=0.92,unsharp=5:5:0.8:5:5:0.0[color];[color][1:v]overlay=0:0[vout]"
    $audioMap = ""
    $encodeArgs = @("-map", "[vout]", "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p")
    
    $audioSelection = Get-ChildItem -Path $audioDir -Filter "*Shorts*.mp3" -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $audioSelection) {
        $audioSelection = Get-ChildItem -Path $audioDir -Filter "*.mp3" -ErrorAction SilentlyContinue | Select-Object -First 1
    }
    if ($audioSelection) {
        $baseArgs += @("-i", $audioSelection.FullName)
        $filterComplex += ";[2:a]volume=0.90[aout]"
        $audioMap = @("-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-shortest")
    }
    
    $ffmpegArgList = $baseArgs + @("-filter_complex", $filterComplex) + $encodeArgs
    if ($audioMap) { $ffmpegArgList += $audioMap }
    $ffmpegArgList += $outputMp4
    
    Write-Host "  -> Encoding 9:16 Shorts with FFmpeg..."
    & $ffmpegExe @ffmpegArgList > "$videoDir\ffmpeg_shorts_out.log" 2> "$videoDir\ffmpeg_shorts_err.log"
    $ffmpegExitCode = $LASTEXITCODE
    
    # SAFE GARBAGE COLLECTION GATE
    $isValid = $false
    if ($ffmpegExitCode -eq 0 -and (Test-Path $outputMp4)) {
        $fileInfo = Get-Item $outputMp4
        $fileSizeMB = [Math]::Round(($fileInfo.Length / 1MB), 2)
        if ($fileInfo.Length -gt (1024 * 1024)) {
            $isValid = $true
        }
    }
    
    if ($isValid) {
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host "  [VALIDATED] Shorts output is VALID ($fileSizeMB MB): $outputMp4" -ForegroundColor Green
        Write-Host "  -> Safe Garbage Collection: Deleting temporary PNG frames..." -ForegroundColor Green
        Start-Sleep -Seconds 1
        Remove-Item $folder.FullName -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  -> [CLEANED] Disk space freed successfully!" -ForegroundColor Green
    } else {
        Write-Host "==========================================" -ForegroundColor Red
        Write-Host "  [FAILED] Video validation failed or corrupted!" -ForegroundColor Red
        Write-Host "  -> [PRESERVED] Raw frames preserved in $($folder.FullName)." -ForegroundColor Yellow
    }
}

Write-Host "=========================================="
Write-Host "SHORTS PIPELINE COMPLETE." -ForegroundColor Cyan
