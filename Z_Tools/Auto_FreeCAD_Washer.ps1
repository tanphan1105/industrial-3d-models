param(
    [string]$TargetFile
)

Write-Host "Bắt đầu tiến trình Washing File STEP bằng FreeCAD..."

# Define FreeCAD potential installation paths
$paths = @(
    "C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe",
    "C:\Program Files\FreeCAD 1.1.0\bin\FreeCADCmd.exe",
    "C:\Program Files\FreeCAD 0.21\bin\FreeCADCmd.exe",
    "C:\Program Files\FreeCAD 0.20\bin\FreeCADCmd.exe"
)

# Search for the wildcard versions just in case
$FreeCADPath = $null
foreach ($p in $paths) {
    if (Test-Path $p) {
        $FreeCADPath = $p
        break
    }
}

if (-not $FreeCADPath) {
    # Try generic wildcard search
    $wildcardPath = "C:\Program Files\FreeCAD*\bin\FreeCADCmd.exe"
    $resolved = Resolve-Path $wildcardPath -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($resolved) {
        $FreeCADPath = $resolved.Path
    }
}

if (-not $FreeCADPath) {
    Write-Host "❌ Lỗi: Không tìm thấy FreeCADCmd.exe. Vui lòng cài đặt FreeCAD."
    exit 1
}

# The Python engine script
$pyScript = "d:\WT3D_Project\Z_Tools\FreeCAD_Wash_STEP.py"

if (-not (Test-Path $TargetFile)) {
    Write-Host "❌ Lỗi: Không tìm thấy file STEP gốc tại: $TargetFile"
    exit 1
}

Write-Host "✅ Tìm thấy FreeCAD tại: $FreeCADPath"
Write-Host "🚿 Đang kích hoạt Headless Mode để rửa file: $($TargetFile)..."

# Run it silently
& $FreeCADPath $pyScript $TargetFile

Write-Host "Hoàn thành Washing File!"
