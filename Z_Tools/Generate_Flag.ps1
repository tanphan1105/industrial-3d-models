Add-Type -AssemblyName System.Drawing

function CreateVietnamFlag($w, $h, $outFile) {
    if (Test-Path $outFile) { Remove-Item $outFile -Force }
    $bmp = New-Object System.Drawing.Bitmap($w, $h)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    
    # Red background
    $g.Clear([System.Drawing.Color]::FromArgb(218, 37, 29))

    # Five-Pointed Gold Star (Subpixel precision)
    $cx = $w / 2.0
    $cy = $h / 2.0
    $rOuter = $h * 0.30
    $rInner = $rOuter * 0.381966

    $pts = New-Object 'System.Drawing.PointF[]' 10
    for ($i = 0; $i -lt 10; $i++) {
        $angle = ($i * 36 - 90) * [Math]::PI / 180.0
        $r = if ($i % 2 -eq 0) { $rOuter } else { $rInner }
        $px = $cx + $r * [Math]::Cos($angle)
        $py = $cy + $r * [Math]::Sin($angle)
        $pts[$i] = New-Object System.Drawing.PointF($px, $py)
    }

    $goldBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 0))
    $g.FillPolygon($goldBrush, $pts)

    # Gold Star Border (Anti-aliased gold stroke for silky smooth edges)
    $starPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 0), 2)
    $g.DrawPolygon($starPen, $pts)

    # White Outer Border Pen
    $borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 255, 255, 255), [Math]::Max(2, [int]($h * 0.025)))
    $g.DrawRectangle($borderPen, 0, 0, $w - 1, $h - 1)

    $bmp.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    $goldBrush.Dispose()
    $starPen.Dispose()
    $borderPen.Dispose()
}

$flagPath = "D:\WT3D_Project\Z_Tools\vietnam_flag.png"
CreateVietnamFlag 1200 800 $flagPath
Write-Host "Successfully generated 1200x800 Ultra-HD Vietnam Flag at: $flagPath"
