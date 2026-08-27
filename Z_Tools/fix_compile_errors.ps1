$file = 'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
$lines = Get-Content $file -Encoding UTF8

$out = @()
$addedSharedVars = $false
$fixCount1 = 0
$fixCount2 = 0

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]

    # ================================================================
    # FIX 1: Khai bao curR va theta truoc Select Case shotType
    # ================================================================
    if ($line -match "^\s+Select Case shotType\s*$" -and -not $addedSharedVars) {
        $out += "        ' --- Bien dung chung (tranh loi Dim hides variable) ---"
        $out += "        Dim curR As Double = 0"
        $out += "        Dim theta As Double = 0"
        $addedSharedVars = $true
    }

    # ================================================================
    # FIX 1b: Trong cac Case, xoa "Dim curR As Double" va "Dim theta As Double"
    # Chi bo Dim, giu lai phan assignment
    # ================================================================
    
    # Pattern: "    Dim curR As Double = something"  ->  "    curR = something"
    if ($line -match '(\s+)Dim (curR|theta) As Double(\s*=.*)') {
        $indent  = $matches[1]
        $varName = $matches[2]
        $rest    = $matches[3]
        $line = "$indent$varName$rest"
        $fixCount1++
    }
    # Pattern: "    Dim curR As Double" (khong co assignment) -> remove line (da khai bao o tren)
    elseif ($line -match '^\s+Dim (curR|theta) As Double\s*$') {
        # Bo qua dong nay
        $fixCount1++
        continue
    }

    # ================================================================
    # FIX 2: Thay VisualStyleEnum bang DisplayModeEnum (compile safe)
    # kHiddenLineVisualStyle -> kWireframeRendering (wireframe, hien thi ket cau)
    # kShadedWithEdgesVisualStyle -> kShadedWithEdgesRendering
    # ================================================================
    if ($line -match 'VisualStyleEnum') {
        $line = $line -replace 'oView\.VisualStyle\s*=\s*VisualStyleEnum\.kHiddenLineVisualStyle', 'oView.DisplayMode = DisplayModeEnum.kWireframeRendering'
        $line = $line -replace 'oView\.VisualStyle\s*=\s*VisualStyleEnum\.kShadedWithEdgesVisualStyle', 'oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering'
        $fixCount2++
    }

    $out += $line
}

$out | Set-Content $file -Encoding UTF8
Write-Host "DONE!"
Write-Host "  Fix curR/theta Dim removed: $fixCount1 lines"
Write-Host "  Fix VisualStyleEnum:        $fixCount2 lines"
Write-Host "  Total lines: $($out.Count)"
