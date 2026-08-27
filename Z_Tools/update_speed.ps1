$file = "d:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb"
$text = Get-Content $file -Raw

# Hàm thay thế số frame cho 1 Case cụ thể
function Set-Speed ($caseName, $oldFrame, $newFrame) {
    # Tìm đoạn Case "$caseName"... For i As Integer = 1 To $oldFrame... i / $oldFrame.0
    $pattern = '(?s)(Case "' + $caseName + '".*?For i As Integer = 1 To )' + $oldFrame + '(.*?i / )' + $oldFrame + '\.0'
    $replacement = '${1}' + $newFrame + '${2}' + $newFrame + '.0'
    $global:text = [regex]::Replace($global:text, $pattern, $replacement, "IgnoreCase")
}

# TĂNG TỐC KỊCH LIỆT các shot toàn cảnh / lia máy
Set-Speed "Extents_Pullback_Reveal" 60 25
Set-Speed "Crane_Descent" 45 20
Set-Speed "Low_Tracking_Sneak" 45 20
Set-Speed "Tension_Zoom" 30 15
Set-Speed "Top_Down_God_Eye" 30 15
Set-Speed "Monument_Lift" 60 25
Set-Speed "Axis_Reveal" 45 20
Set-Speed "Worm_Eye_Whip" 15 10
Set-Speed "Blueprint_Hologram_Scan" 45 25
Set-Speed "Tesla_Speed_Ramp" 45 35
Set-Speed "FPV_Drone_Dive" 40 20
Set-Speed "Turn_Around_Majestic" 60 25
Set-Speed "Flowline_Track" 60 25
Set-Speed "Energy_Path_Reveal" 45 20
Set-Speed "Extreme_Tilt_Up" 40 20

# KHỰNG LẠI (GIỮ/TĂNG THỜI GIAN) các shot siêu cận / chi tiết
Set-Speed "Macro_Surface_Glide" 30 45
Set-Speed "Detail_Spin_Focus" 45 60
Set-Speed "Slow_Macro_Creep" 40 60
Set-Speed "Micro_Focus_Snap" 12 18
Set-Speed "Flash_Cut_Detail" 10 15
Set-Speed "Material_Kiss" 20 30

$text | Set-Content $file
