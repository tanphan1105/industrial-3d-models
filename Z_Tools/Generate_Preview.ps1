Add-Type -AssemblyName System.Drawing

$previewPath = "C:\Users\ADMIN\.gemini\antigravity\brain\43aef838-7520-4e40-bcba-b8699ab024a8\watermark_preview_confirmation.png"
$toolsDir = "D:\WT3D_Project\Z_Tools"

$w = 1080
$h = 1920
$bmp = New-Object System.Drawing.Bitmap($w, $h)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

# 1. Background: Dark Metallic Industrial Gradient (Simulating 4K 3D Render)
$rect = New-Object System.Drawing.Rectangle(0, 0, $w, $h)
$bgBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rect, 
    [System.Drawing.Color]::FromArgb(255, 12, 18, 26), 
    [System.Drawing.Color]::FromArgb(255, 32, 42, 56), 
    45.0)
$g.FillRectangle($bgBrush, $rect)

# Draw 3D Grid lines
$penGrid = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(30, 255, 255, 255), 2)
for ($x = 0; $x -lt $w; $x += 120) { $g.DrawLine($penGrid, $x, 0, $x, $h) }
for ($y = 0; $y -lt $h; $y += 120) { $g.DrawLine($penGrid, 0, $y, $w, $y) }

# Draw 3D Equipment Mockup (RO Filtration Skid)
$machPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(100, 52, 199, 89), 4)
$g.DrawRectangle($machPen, 180, 420, 720, 1100)
$g.DrawEllipse($machPen, 240, 480, 280, 980)
$g.DrawEllipse($machPen, 560, 480, 280, 980)

# ----------------------------------------------------------------------
# LỚP 1: LÁ CỜ VIỆT NAM (GÓC TRÊN TRÁI TOP-LEFT)
# ----------------------------------------------------------------------
$flagW = [int]($w * 0.10)  # 108px wide
$flagH = [int]($flagW * 0.6667) # 72px high
$flagX = [int]($w * 0.04) # 43px offset
$flagY = [int]($h * 0.035) # 67px offset

$flagPath = "$toolsDir\vietnam_flag.png"
if (Test-Path $flagPath) {
    try {
        $flagImg = [System.Drawing.Image]::FromFile($flagPath)
        $g.DrawImage($flagImg, $flagX, $flagY, $flagW, $flagH)
        $flagImg.Dispose()
    } catch {}
}

# ----------------------------------------------------------------------
# LỚP 2: BẢN QUYỀN THỦY TINH CHÍNH GIỮA MÀN HÌNH (@tanphan1105 TO KHỔNG LỒ)
# ----------------------------------------------------------------------
$state2 = $g.Save()
$g.TranslateTransform($w / 2, $h * 0.46)
$mailText = "@tanphan1105"
$mailFont = New-Object System.Drawing.Font("Arial Black", 75, [System.Drawing.FontStyle]::Bold)
$gp2 = New-Object System.Drawing.Drawing2D.GraphicsPath
$sf = New-Object System.Drawing.StringFormat
$sf.Alignment = [System.Drawing.StringAlignment]::Center
$sf.LineAlignment = [System.Drawing.StringAlignment]::Center
$gp2.AddString($mailText, $mailFont.FontFamily, $mailFont.Style, $mailFont.Size, (New-Object System.Drawing.PointF(0, 0)), $sf)

$pThick2 = 5
$darkPen2 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(45, 0, 0, 0), $pThick2)
$g.TranslateTransform(4, 4)
$g.DrawPath($darkPen2, $gp2)
$g.TranslateTransform(-4, -4)
$lightPen2 = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(70, 255, 255, 255), $pThick2)
$g.TranslateTransform(-4, -4)
$g.DrawPath($lightPen2, $gp2)
$g.Restore($state2)

# ----------------------------------------------------------------------
# LỚP 3: THẺ GREEN CARD LOGO (WaterTreatment3D + @tanphan1105 SIÊU TO + QR)
# ----------------------------------------------------------------------
$brandText = "WaterTreatment3D"
$brandFont = New-Object System.Drawing.Font("Arial Narrow", 40, [System.Drawing.FontStyle]::Bold)

# HÀNG DƯỚI TO NỔI BẬT THEO YÊU CẦU NGHỆ SĨ
$contactText = "@tanphan1105 | Zalo: +84985267326"
$contactFont = New-Object System.Drawing.Font("Arial", 46, [System.Drawing.FontStyle]::Bold)

$brandSz = $g.MeasureString($brandText, $brandFont)
$contactSz = $g.MeasureString($contactText, $contactFont)
$maxW = [Math]::Max($brandSz.Width, $contactSz.Width)
$qrSize = 160
$cPad = 32
$totalW = $maxW + 40 + $qrSize
$textBlockH = $brandSz.Height + $contactSz.Height + 16
$totalH = [Math]::Max($textBlockH, $qrSize)

$boxRX = ($w - ($totalW + $cPad*2)) / 2
$boxRY = $h - $totalH - ($h * 0.04) - $cPad*2

$path = New-Object System.Drawing.Drawing2D.GraphicsPath
$r = 26
$path.AddArc($boxRX, $boxRY, $r, $r, 180, 90)
$path.AddArc($boxRX + $totalW + $cPad*2 - $r, $boxRY, $r, $r, 270, 90)
$path.AddArc($boxRX + $totalW + $cPad*2 - $r, $boxRY + $totalH + $cPad*2 - $r, $r, $r, 0, 90)
$path.AddArc($boxRX, $boxRY + $totalH + $cPad*2 - $r, $r, $r, 90, 90)
$path.CloseAllFigures()

$cardBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(240, 52, 199, 89))
$g.FillPath($cardBrush, $path)
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 255, 255, 255), 3)
$g.DrawPath($borderPen, $path)

$currY = $boxRY + $cPad + ($totalH - $textBlockH) / 2

# Draw Brand Header
$sb1 = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(60, 0, 0, 0))
$mb1 = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
$g.DrawString($brandText, $brandFont, $sb1, $boxRX + $cPad + 2, $currY + 2)
$g.DrawString($brandText, $brandFont, $mb1, $boxRX + $cPad, $currY)

# Draw Bottom Line (HUGE & BOLD)
$currY += $brandSz.Height + 8
$mb2 = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
$g.DrawString($contactText, $contactFont, $sb1, $boxRX + $cPad + 3, $currY + 3)
$g.DrawString($contactText, $contactFont, $mb2, $boxRX + $cPad, $currY)

# Draw QR Code on the right side
$qrPath = "$toolsDir\wt3d_qr_green.png"
if (-not (Test-Path $qrPath)) { $qrPath = [System.IO.Path]::GetTempPath() + "wt3d_qr_green.png" }
if (Test-Path $qrPath) {
    try {
        $qrBmp = New-Object System.Drawing.Bitmap($qrPath)
        $g.DrawImage($qrBmp, ($boxRX + $cPad + $maxW + 40), ($boxRY + $cPad + ($totalH - $qrSize)/2), $qrSize, $qrSize)
        $qrBmp.Dispose()
    } catch {}
}

$bmp.Save($previewPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bmp.Dispose()
Write-Host "Successfully rendered updated preview image to: $previewPath"
