# ==============================================================================
# WT3D VERSION MANAGER - Quản Lý Phiên Bản Script iLogic
# ==============================================================================

$TargetFile  = "D:\WT3D_Project\Z_Tools\WT3D_Engineering_Projection_Engine.iLogicVb"
$VersionDir  = "D:\WT3D_Project\Z_Tools\_VERSIONS"

if (-not (Test-Path $VersionDir)) { New-Item -ItemType Directory -Path $VersionDir | Out-Null }

function Show-Menu {
    Clear-Host
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host "  WT3D VERSION MANAGER - Phuc Hoi Phien Ban iLogic"       -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host "  [1]  SNAPSHOT - Luu phien ban hien tai"                  -ForegroundColor Green
    Write-Host "  [2]  LIST     - Liet ke tat ca phien ban"                -ForegroundColor Yellow
    Write-Host "  [3]  RESTORE  - Phuc hoi phien ban cu"                   -ForegroundColor Red
    Write-Host "  [4]  DIFF     - So sanh 2 phien ban"                     -ForegroundColor Magenta
    Write-Host "  [Q]  THOAT"                                              -ForegroundColor Gray
    Write-Host ""
}

function Save-Snapshot {
    $label = Read-Host "  Nhan ten mo ta phien ban (VD: DIM_OK_locked)"
    $ts    = Get-Date -Format "yyyyMMdd_HHmmss"
    $safe  = $label -replace '[^\w]', '_'
    $dest  = Join-Path $VersionDir "v_${ts}_${safe}.iLogicVb"
    Copy-Item $TargetFile $dest
    Write-Host "  OK Da luu: $dest" -ForegroundColor Green
    Pause
}

function List-Snapshots {
    $files = Get-ChildItem $VersionDir -Filter "*.iLogicVb" | Sort-Object Name
    if ($files.Count -eq 0) {
        Write-Host "  Chua co phien ban nao duoc luu." -ForegroundColor Yellow
    } else {
        Write-Host "  ID   Thoi gian              Ten phien ban" -ForegroundColor Cyan
        $i = 1
        foreach ($f in $files) {
            $size = "{0,5} KB" -f [math]::Round($f.Length / 1024, 0)
            Write-Host ("  [{0,2}]  {1}  {2}  ({3})" -f $i, $f.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss"), $f.BaseName, $size)
            $i++
        }
    }
    Pause
}

function Restore-Snapshot {
    $files = Get-ChildItem $VersionDir -Filter "*.iLogicVb" | Sort-Object Name
    if ($files.Count -eq 0) { Write-Host "  Chua co phien ban nao." -ForegroundColor Yellow; Pause; return }
    $i = 1
    foreach ($f in $files) {
        Write-Host ("  [{0,2}]  {1}  {2}" -f $i, $f.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss"), $f.BaseName) -ForegroundColor Yellow
        $i++
    }
    $choice = Read-Host "  Nhap ID phien ban muon phuc hoi"
    if ([string]::IsNullOrEmpty($choice)) { return }
    $idx = [int]$choice - 1
    $selected = $files[$idx]
    # Auto backup truoc khi ghi de
    $bak = Join-Path $VersionDir "v_$(Get-Date -Format 'yyyyMMdd_HHmmss')_AUTO_BACKUP.iLogicVb"
    Copy-Item $TargetFile $bak
    Write-Host "  Backup hien tai: $bak" -ForegroundColor DarkGray
    Copy-Item $selected.FullName $TargetFile -Force
    Write-Host "  OK Da phuc hoi: $($selected.BaseName)" -ForegroundColor Green
    Write-Host "  Vao Inventor -> iLogic -> Reload de ap dung." -ForegroundColor Cyan
    Pause
}

function Diff-Snapshots {
    $files = Get-ChildItem $VersionDir -Filter "*.iLogicVb" | Sort-Object Name
    if ($files.Count -lt 2) { Write-Host "  Can it nhat 2 phien ban." -ForegroundColor Yellow; Pause; return }
    for ($i = 0; $i -lt $files.Count; $i++) {
        Write-Host ("  [{0,2}]  {1}" -f ($i+1), $files[$i].BaseName) -ForegroundColor Yellow
    }
    $a = [int](Read-Host "  ID phien ban A") - 1
    $b = [int](Read-Host "  ID phien ban B") - 1
    $diff = Compare-Object (Get-Content $files[$a].FullName) (Get-Content $files[$b].FullName)
    if ($diff) {
        foreach ($d in $diff) {
            if ($d.SideIndicator -eq "<=") { Write-Host ("  - " + $d.InputObject) -ForegroundColor Red }
            else { Write-Host ("  + " + $d.InputObject) -ForegroundColor Green }
        }
    } else { Write-Host "  Hai phien ban giong het nhau." -ForegroundColor Green }
    Pause
}

do {
    Show-Menu
    $key = Read-Host "  Chon"
    switch ($key.ToUpper()) {
        "1" { Save-Snapshot }
        "2" { List-Snapshots }
        "3" { Restore-Snapshot }
        "4" { Diff-Snapshots }
    }
} while ($key.ToUpper() -ne "Q")
