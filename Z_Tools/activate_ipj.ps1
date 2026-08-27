$ipjPath = "D:\INVENTOR_DATA\MASTER_LIBRARIES.ipj"
try {
    $inv = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Inventor.Application")
    if ($inv) {
        $pjs = $inv.DesignProjectManager.DesignProjects
        try {
            $pj = $pjs.AddExisting($ipjPath)
            $pj.Activate()
            Write-Host ">>> DA KICH HOAT THANH CONG MASTER_LIBRARIES.ipj TRUC TIEP VAO INVENTOR!" -ForegroundColor Green
        } catch {
            foreach ($p in $pjs) {
                if ($p.FullFileName -eq $ipjPath) {
                    $p.Activate()
                    Write-Host ">>> DA ACTIVE MASTER_LIBRARIES.ipj TRUC TIEP VAO INVENTOR!" -ForegroundColor Green
                    break
                }
            }
        }
    }
} catch {
    Write-Host "Inventor chua mo, nhung file D:\INVENTOR_DATA\MASTER_LIBRARIES.ipj da duoc cau hinh chuan xac tren dia!" -ForegroundColor Cyan
}
