param([string]$targetDir = "d:\WT3D_Project\1_Exports_Batch")

# =====================================================================
# AUTO SEO EXIF BURNER v5.0 - Night Crawler Pipeline
# FIX v5: Xử lý ảnh 4K không bị crash GDI+ - dùng MemoryStream riêng
# Engine: System.Drawing PropertyItem (EXIF Tags chuẩn Windows)
# Kết quả: Windows Explorer Properties -> Details hiển thị đầy đủ
# =====================================================================

Add-Type -AssemblyName System.Drawing

$title     = "Industrial 3D CAD Model - B2B Engineering Asset"
$author    = "TANPHAN STUDIO - trongtan.p@icloud.com"
$copyright = "Copyright 2026 TANPHAN STUDIO. All rights reserved. trongtan.p@icloud.com"
$comment   = "High fidelity industrial 3D asset. Download CAD files: cgtrader.com/designers/tanphan1105 | fab.com/sellers/Trong Tan Phan"
$subject   = "Industrial 3D Model, CAD, Water Treatment, STEP, FBX, TANPHAN STUDIO"

function Set-ImageMetadata {
    param([string]$srcPath)

    $finalPath = [System.IO.Path]::ChangeExtension($srcPath, ".jpg")
    $tmpFinal  = $finalPath + ".exif_tmp"

    try {
        # Bước 1: Load PNG qua MemoryStream (tránh file lock)
        $rawBytes = [System.IO.File]::ReadAllBytes($srcPath)
        $ms = New-Object System.IO.MemoryStream($rawBytes, 0, $rawBytes.Length)
        $bmp = New-Object System.Drawing.Bitmap($ms)

        # Bước 2: Lấy JPEG encoder
        $jpegEncoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() |
                       Where-Object { $_.MimeType -eq "image/jpeg" } |
                       Select-Object -First 1
        $encParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
        $encParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter(
            [System.Drawing.Imaging.Encoder]::Quality, [long]95)

        # Bước 3: Save JPEG ra file tạm (giải phóng RAM ngay)
        $bmp.Save($tmpFinal, $jpegEncoder, $encParams)
        $bmp.Dispose()
        $ms.Dispose()
        $rawBytes = $null
        [GC]::Collect()

        # Bước 4: Load lại JPEG tạm, inject EXIF bằng Reflection
        $jpegBytes = [System.IO.File]::ReadAllBytes($tmpFinal)
        $ms2 = New-Object System.IO.MemoryStream($jpegBytes, 0, $jpegBytes.Length)
        $jpegBmp = New-Object System.Drawing.Bitmap($ms2)

        $piType = [System.Drawing.Imaging.PropertyItem]
        $ctor = $piType.GetConstructor(
            [System.Reflection.BindingFlags]::NonPublic -bor [System.Reflection.BindingFlags]::Instance,
            $null, @(), $null)

        # XPTitle (Unicode) - 40091
        $pi = $ctor.Invoke($null)
        $pi.Id = 40091; $pi.Type = 1
        $pi.Value = [System.Text.Encoding]::Unicode.GetBytes($title + "`0")
        $pi.Len = $pi.Value.Length
        $jpegBmp.SetPropertyItem($pi)

        # XPAuthor (Unicode) - 40093
        $pi = $ctor.Invoke($null)
        $pi.Id = 40093; $pi.Type = 1
        $pi.Value = [System.Text.Encoding]::Unicode.GetBytes($author + "`0")
        $pi.Len = $pi.Value.Length
        $jpegBmp.SetPropertyItem($pi)

        # XPComment (Unicode) - 40092
        $pi = $ctor.Invoke($null)
        $pi.Id = 40092; $pi.Type = 1
        $pi.Value = [System.Text.Encoding]::Unicode.GetBytes($comment + "`0")
        $pi.Len = $pi.Value.Length
        $jpegBmp.SetPropertyItem($pi)

        # Copyright ASCII - 33432
        $pi = $ctor.Invoke($null)
        $pi.Id = 33432; $pi.Type = 2
        $pi.Value = [System.Text.Encoding]::ASCII.GetBytes($copyright + "`0")
        $pi.Len = $pi.Value.Length
        $jpegBmp.SetPropertyItem($pi)

        # Artist ASCII - 315
        $pi = $ctor.Invoke($null)
        $pi.Id = 315; $pi.Type = 2
        $pi.Value = [System.Text.Encoding]::ASCII.GetBytes($author + "`0")
        $pi.Len = $pi.Value.Length
        $jpegBmp.SetPropertyItem($pi)

        # ImageDescription ASCII - 270
        $pi = $ctor.Invoke($null)
        $pi.Id = 270; $pi.Type = 2
        $pi.Value = [System.Text.Encoding]::ASCII.GetBytes($subject + "`0")
        $pi.Len = $pi.Value.Length
        $jpegBmp.SetPropertyItem($pi)

        # Bước 5: Save JPEG cuối với EXIF
        $ms3 = New-Object System.IO.MemoryStream
        $jpegBmp.Save($ms3, $jpegEncoder, $encParams)
        $jpegBmp.Dispose()
        $ms2.Dispose()
        $jpegBytes = $null
        [GC]::Collect()

        # Bước 6: Ghi ra file, xóa PNG gốc
        [System.IO.File]::WriteAllBytes($finalPath + ".final2", $ms3.ToArray())
        $ms3.Dispose()

        Remove-Item $tmpFinal -Force -ErrorAction SilentlyContinue
        Remove-Item $finalPath -Force -ErrorAction SilentlyContinue
        Rename-Item ($finalPath + ".final2") $finalPath -Force

        if ($srcPath -ne $finalPath -and (Test-Path $srcPath)) {
            Remove-Item $srcPath -Force -ErrorAction SilentlyContinue
        }

        return $true
    }
    catch {
        Remove-Item $tmpFinal -Force -ErrorAction SilentlyContinue
        Remove-Item ($finalPath + ".final2") -Force -ErrorAction SilentlyContinue
        Write-Host "     ERROR: $_" -ForegroundColor Red
        return $false
    }
}

# === Main ===
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Night-Crawler EXIF Burner v5.0 (4K Fix)" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Target: $targetDir" -ForegroundColor Gray

$files = Get-ChildItem -Path $targetDir -Include *.png, *.jpg, *.jpeg -Recurse -ErrorAction SilentlyContinue |
         Where-Object { $_.Name -notlike "temp_*" }

if ($null -eq $files -or @($files).Count -eq 0) {
    Write-Host "Khong tim thay anh nao." -ForegroundColor Yellow; exit 0
}

$ok = 0; $fail = 0
foreach ($file in $files) {
    Write-Host "  -> $($file.Name)" -NoNewline
    $result = Set-ImageMetadata -srcPath $file.FullName
    if ($result) { Write-Host " [OK]" -ForegroundColor Green; $ok++ }
    else         { Write-Host " [FAIL]" -ForegroundColor Red; $fail++ }
}

Write-Host ""
Write-Host "XONG: $ok OK | $fail loi" -ForegroundColor Cyan
Write-Host "Kiểm tra: Chuột phải JPG -> Properties -> Details -> Title / Authors / Copyright" -ForegroundColor Yellow
