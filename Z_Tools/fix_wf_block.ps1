$file = 'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
$lines = Get-Content $file -Encoding UTF8

$out = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    # Fix 1: Line ~621 - missing Case "Material_Kiss"
    # Pattern: comment line with garbled text + next line is "For i As Integer = 1 To 30" without a Case above
    if ($line -match "K.{1,5} CH B.{1,5}N KH.{1,5}I G.{1,5} N/LINH" -or $line -match "KICH BAN KHOI GO N") {
        $out += "            ' -------------------------------------------------------------"
        $out += "            ' KICH BAN KHOI GON/LINH KIEN (COMPACT / CONTROL COMPONENT)"
        $out += "            ' -------------------------------------------------------------"
        $out += '            Case "Material_Kiss" ' + "' Dao luot ap sat miet cac ngam may"
        $i++ # skip the bad comment line, next line should be the For loop
        $out += $lines[$i] # add "---" separator
        continue
    }
    
    # Fix 2: Line ~656 - bad merged content in wfInt For loop
    if ($line -match "wfInt = 33538 OrEl\s+Try") {
        $out += "                        If wfInt = 33538 OrElse wfInt = 33539 Then Continue For"
        $out += "                        Try"
        $out += "                            oView.DisplayMode = CType(wfInt, DisplayModeEnum)"
        $out += "                            If CInt(oView.DisplayMode) <> 33539 Then"
        $out += "                                wfModeSet = True"
        $out += '                                Try : System.IO.File.WriteAllText("d:\WT3D_Project\Z_Tools\wf_mode_found.txt", "WireframeHiddenEdge mode = " & wfInt.ToString()) : Catch : End Try'
        $out += "                                Exit For"
        $out += "                            End If"
        $out += "                        Catch : End Try"
        $out += "                    Next"
        $out += "                End If"
        # Skip until orbit loop
        while ($i + 1 -lt $lines.Count -and $lines[$i+1] -notmatch "For i As Integer = 1 To 60") {
            $i++
        }
        continue
    }
    
    $out += $line
}

$out | Set-Content $file -Encoding UTF8
Write-Host "Done! Total lines: $($out.Count)"
