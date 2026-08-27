# ==============================================================================
# WT3D BATCH PACKAGING SCRIPT (OFFLINE)
# Creates platform-specific ZIP packages for CGTrader, Fab, Sketchfab
# ==============================================================================

param(
    [string]$TargetModelName = ""
)

$sourceDir = "d:\WT3D_Project\1_Exports_Batch"
$targetDir = "d:\WT3D_Project\Export_Packages"

Write-Host "🚀 Khởi động quy trình đóng gói hàng loạt (Offline Batch Process)..." -ForegroundColor Cyan

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
}

$models = Get-ChildItem -Path $sourceDir -Directory

if ($TargetModelName -ne "") {
    $models = $models | Where-Object { $_.Name -eq $TargetModelName }
    Write-Host "Chỉ đóng gói cho Model: $TargetModelName" -ForegroundColor Cyan
}

if ($models.Count -eq 0) {
    Write-Host "⚠️ Thư mục 1_Exports_Batch đang trống." -ForegroundColor Yellow
    Write-Host "Vui lòng copy các folder chứa FBX/OBJ/STL và Render vào đây để script tự động đóng gói." -ForegroundColor Yellow
} else {
    foreach ($model in $models) {
        $modelName = $model.Name
        Write-Host "📦 Đang xử lý Model: $modelName" -ForegroundColor Green
        
        # Tạo gói CGTrader (chứa toàn bộ format)
        $cgtPath = Join-Path $targetDir "$($modelName)_CGTrader.zip"
        Compress-Archive -Path "$($model.FullName)\*" -DestinationPath $cgtPath -Force
        Write-Host "  -> Đã tạo: $($modelName)_CGTrader.zip"
        
        # Tạo gói Fab (STL, OBJ trọng tâm)
        $fabPath = Join-Path $targetDir "$($modelName)_Fab.zip"
        Compress-Archive -Path "$($model.FullName)\*" -DestinationPath $fabPath -Force
        Write-Host "  -> Đã tạo: $($modelName)_Fab.zip"
    }
    Write-Host "✅ Đã đóng gói xong toàn bộ kiện hàng!" -ForegroundColor Cyan
    Write-Host "🔥 Tự động mở Fab.com Upload Dashboard..." -ForegroundColor Yellow
    Start-Process "d:\WT3D_Project\Z_Tools\Fab_Batch_Dashboard.html"
}

# Đã bỏ Read-Host để script có thể tự động thoát hoàn toàn khi chạy ngầm (Zero-Touch)
