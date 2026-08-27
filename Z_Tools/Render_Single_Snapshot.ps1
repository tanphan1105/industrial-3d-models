$toolsDir = "D:\WT3D_Project\Z_Tools"
$artifactDir = "C:\Users\ADMIN\.gemini\antigravity\brain\43aef838-7520-4e40-bcba-b8699ab024a8"
$outPhotoPath = "$artifactDir\actual_inventor_snapshot_test.png"

Write-Host "Connecting to active Inventor instance..."
try {
    $invApp = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Inventor.Application")
} catch {
    Write-Host "Could not connect to Inventor COM API."
    Exit
}

$doc = $invApp.ActiveDocument
if (-not $doc) {
    Write-Host "No active document found in Inventor!"
    Exit
}

Write-Host "Active Model:" $doc.DisplayName

$view = $invApp.ActiveView
$cam = $view.Camera

# Enforce Perspective & Hero 3/4 View
$cam.Perspective = $true
$cam.ViewOrientationType = [Inventor.ViewOrientationTypeEnum]::kIsoTopRightViewOrientation
$cam.Fit()
$cam.Apply()

# Save raw 4K bitmap snapshot
$rawImgPath = [System.IO.Path]::GetTempFileName() + ".png"
$w = 3840
$h = 2160
$cam.SaveAsBitmap($rawImgPath, $w, $h)

Write-Host "Raw snapshot saved to: $rawImgPath"

# Apply Multi-Layer Watermark Overlay using GDI+ System.Drawing
Add-Type -AssemblyName System.Drawing
$bmp = New-Object System.Drawing.Bitmap($rawImgPath)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

$isVertical = ($h -gt $w)

if ($isVertical) {
    $flagWFactor = 0.140; $flagXFactor = 0.045; $mailYFactor = 0.43; $mailSizeFactor = 0.082
    $brandSizeFactor = 0.022; $contactSizeFactor = 0.026; $qrSizeFactor = 0.145
    $cPadFactor = 0.022; $gapFactor = 0.022; $textGapFactor = 0.012
} else {
    $flagWFactor = 0.105; $flagXFactor = 0.030; $mailYFactor = 0.44; $mailSizeFactor = 0.052
    $brandSizeFactor = 0.013; $contactSizeFactor = 0.015; $qrSizeFactor = 0.075
    $cPadFactor = 0.010; $gapFactor = 0.014; $textGapFactor = 0.008
}

# 1. Vietnam Flag at Top-Left
$flagW = [int]($w * $flagWFactor)
$flagH = [int]($flagW * 0.6667)
$flagX = [int]($w * $flagXFactor)
$flagY = [int]($h * 0.030)

$flagPath = "$toolsDir\vietnam_flag.png"
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

# 2. Ghost Crystal Center Logo (@tanphan1105)
$state2 = $g.Save()
$mailY = $h * $mailYFactor
$cX = $w / 2.0
$g.TranslateTransform($cX, $mailY)
$mailText = "@tanphan1105"
$mailSize = [single][Math]::Max(12.0, ($w * $mailSizeFactor))
$mailFont = New-Object System.Drawing.Font("Arial Black", $mailSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$gp2 = New-Object System.Drawing.Drawing2D.GraphicsPath
$sf = New-Object System.Drawing.StringFormat
$sf.Alignment = [System.Drawing.StringAlignment]::Center
$sf.LineAlignment = [System.Drawing.StringAlignment]::Center
$gp2.AddString($mailText, $mailFont.FontFamily, [int]$mailFont.Style, $mailFont.Size, (New-Object System.Drawing.PointF(0, 0)), $sf)

$pThick2 = [Math]::Max(1, [int]($w * 0.0015))
$offsetPx = [Math]::Max(1, [int]($w * 0.0015))

# BÊN TỐI (Bottom-Right Shadow Edge)
$darkPen2 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(35, 0, 0, 0), $pThick2)
$g.TranslateTransform($offsetPx, $offsetPx)
$g.DrawPath($darkPen2, $gp2)
$g.TranslateTransform(-$offsetPx, -$offsetPx)

# BÊN SÁNG (Top-Left Highlight Edge)
$lightPen2 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(55, 255, 255, 255), $pThick2)
$g.TranslateTransform(-$offsetPx, -$offsetPx)
$g.DrawPath($lightPen2, $gp2)
$g.TranslateTransform($offsetPx, -$offsetPx)

# THÂN THỦY TINH CỰC MỜ (Ghost Translucent Core Fill - Alpha = 10)
$glassBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(10, 255, 255, 255))
$g.FillPath($glassBrush, $gp2)
$g.Restore($state2)

# 3. Green Card Badge (Diagonal Gradient Emerald)
$brandText = "WaterTreatment3D"
$brandSize = [single][Math]::Max(10.0, ($w * $brandSizeFactor))
$brandFont = New-Object System.Drawing.Font("Arial", $brandSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$contactText = "@tanphan1105 | Zalo: +84985267326"
$contactSize = [single][Math]::Max(10.0, ($w * $contactSizeFactor))
$contactFont = New-Object System.Drawing.Font("Arial", $contactSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)

$brandSz = $g.MeasureString($brandText, $brandFont)
$contactSz = $g.MeasureString($contactText, $contactFont)
$maxW = [Math]::Max($brandSz.Width, $contactSz.Width)

$qrSize = [int]($w * $qrSizeFactor)
$cPad = [int]($w * $cPadFactor)
$gap = [int]($w * $gapFactor)

$totalW = $maxW + $gap + $qrSize
$textBlockH = $brandSz.Height + $contactSz.Height + [int]($h * $textGapFactor)
$totalH = [Math]::Max($textBlockH, $qrSize)

if ($isVertical) {
    # Bố cục Căn Giữa Dưới Cùng cho Khung Dọc 9:16 (Shorts/Reels)
    $boxRX = ($w - ($totalW + $cPad*2)) / 2
    $boxRY = $h - $totalH - ($h * 0.035) - $cPad*2
} else {
    # Bố cục Góc Dưới Bên Phải cho Khung Ngang 16:9 (YouTube 4K)
    $boxRX = $w - $totalW - ($w * 0.025) - $cPad*2
    $boxRY = $h - $totalH - ($h * 0.035) - $cPad*2
}

$path = New-Object System.Drawing.Drawing2D.GraphicsPath
$r = [Math]::Max(6, [int]($w * 0.008))
$path.AddArc($boxRX, $boxRY, $r, $r, 180, 90)
$path.AddArc($boxRX + $totalW + $cPad*2 - $r, $boxRY, $r, $r, 270, 90)
$path.AddArc($boxRX + $totalW + $cPad*2 - $r, $boxRY + $totalH + $cPad*2 - $r, $r, $r, 0, 90)
$path.AddArc($boxRX, $boxRY + $totalH + $cPad*2 - $r, $r, $r, 90, 90)
$path.CloseAllFigures()

# DIAGONAL EMERALD GRADIENT (#34C759 -> #189644) WITH TRANSLUCENCY (Alpha 225 ~ 84%)
$rectF = New-Object System.Drawing.RectangleF($boxRX, $boxRY, ($totalW + $cPad*2), ($totalH + $cPad*2))
$c1 = [System.Drawing.Color]::FromArgb(225, 52, 199, 89)
$c2 = [System.Drawing.Color]::FromArgb(220, 24, 150, 68)
$gradBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rectF, $c1, $c2, 45.0)
$g.FillPath($gradBrush, $path)
$gradBrush.Dispose()

# THIN WHITE BORDER OUTLINE = 1PX
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(240, 255, 255, 255), 1)
$g.DrawPath($borderPen, $path)
$borderPen.Dispose()

$currY = $boxRY + $cPad + ($totalH - $textBlockH) / 2

# GAUSSIAN SOFT AMBIENT SHADOW
$sbShadow = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(110, 10, 40, 15))
$g.DrawString($brandText, $brandFont, $sbShadow, $boxRX + $cPad + 3, $currY + 3)

# CRISP WHITE TEXT WITH WHISPER-THIN 0.8PX OUTLINE
$mb1 = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
$g.DrawString($brandText, $brandFont, $mb1, $boxRX + $cPad, $currY)

$currY += $brandSz.Height + [int]($h * 0.004)
$g.DrawString($contactText, $contactFont, $sbShadow, $boxRX + $cPad + 3, $currY + 3)
$g.DrawString($contactText, $contactFont, $mb1, $boxRX + $cPad, $currY)

$sbShadow.Dispose(); $mb1.Dispose()

# OFFICIAL ZALO QR CODE ASSET
$qrPath = "$toolsDir\wt3d_qr_green.png"
if (Test-Path $qrPath) {
    try {
        $qrBmp = New-Object System.Drawing.Bitmap($qrPath)
        $qrX = $boxRX + $cPad + $maxW + $gap
        $qrY = $boxRY + $cPad + ($totalH - $qrSize)/2
        
        # White background padding for QR
        $qrBgPen = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
        $g.FillRectangle($qrBgPen, ($qrX - 4), ($qrY - 4), ($qrSize + 8), ($qrSize + 8))
        $qrBgPen.Dispose()

        $g.DrawImage($qrBmp, $qrX, $qrY, $qrSize, $qrSize)
        $qrBmp.Dispose()
    } catch {}
}

$bmp.Save($outPhotoPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bmp.Dispose()
Remove-Item $rawImgPath -Force

Write-Host "Successfully rendered actual snapshot to: $outPhotoPath"
