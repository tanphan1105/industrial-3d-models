import re

filepath = r"d:\WT3D_Project\Z_Tools\Auto_Stitch_Master.ps1"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the old block
old_block = """    $filterComplex = "[0:v][1:v]overlay=0:0[vout]"
    $audioMap = ""
    $encodeArgs = @("-map", "[vout]", "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-metadata", "title=B2B Cinematic Engineering Asset", "-metadata", "artist=TANPHAN STUDIO", "-metadata", "copyright=Copyright 2026 TANPHAN STUDIO. trongtan.p@icloud.com. All rights reserved.", "-metadata", "comment=Download 3D CAD files: cgtrader.com/designers/tanphan1105 | fab.com/sellers/Trong Tan Phan")
    
    $audioSelection = $null
    if ($camId -match "CAM3|CAM4|CAM5") {
        $audioSelection = Get-ChildItem -Path $audioDir -Filter "*Shorts*.mp3" | Select-Object -First 1
    } else {
        $audioSelection = Get-ChildItem -Path $audioDir -Filter "*Horizontal*.mp3" | Select-Object -First 1
    }
    if (-not $audioSelection) {
        $audioSelection = Get-ChildItem -Path $audioDir -Filter "*.mp3" | Get-Random
    }
    if ($audioSelection) {
        $audioFile = $audioSelection.FullName
        Write-Host "  -> Tm th?y d? li?u Audio: $($audioSelection.Name)"
        $baseArgs += @("-stream_loop", "-1", "-i", $audioFile)
        
        if ($camId -eq "CAM5") {
            $filterComplex += ";[2:a]apad,volume=0.40[aout]" 
        } else {
            $filterComplex += ";[2:a]apad[aout]"
        }
        $audioMap = @("-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-shortest")
    } else {"""

# If there is character encoding mismatch in Write-Host, we use regex
pattern = r'(?s)(    \$filterComplex = "\[0:v\]\[1:v\]overlay=0:0\[vout\]".*?\$audioMap = \@\("-map", "\[aout\]", "-c:a", "aac", "-b:a", "192k", "-shortest"\)\r?\n\s+\} else \{)'

new_block = """    # --- B2B CAPCUT FEATURES ---
    $hookText = "ENGINEERING 3D REVIEW"
    if ($camId -match "CAM2") { $hookText = "TECHNICAL X-RAY SCAN" }
    elseif ($camId -match "CAM5") { $hookText = "MACRO INSPECTION" }
    
    $fontSize = "80"
    if ($camId -match "CAM3|CAM4|CAM5") { $fontSize = "130" }
    
    $drawtext = "drawtext=text='$hookText':fontfile='C\\:/Windows/Fonts/arialbd.ttf':fontcolor=white:fontsize=$fontSize:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,2.5)':shadowcolor=black:shadowx=5:shadowy=5"
    
    $filterComplex = "[0:v]eq=contrast=1.15:saturation=1.3:gamma=0.95[color];[color][1:v]overlay=0:0[wm];[wm]$drawtext`[vout]"
    $audioMap = ""
    $encodeArgs = @("-map", "[vout]", "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-metadata", "title=B2B Cinematic Engineering Asset", "-metadata", "artist=TANPHAN STUDIO", "-metadata", "copyright=Copyright 2026 TANPHAN STUDIO. trongtan.p@icloud.com. All rights reserved.", "-metadata", "comment=Download 3D CAD files: cgtrader.com/designers/tanphan1105 | fab.com/sellers/Trong Tan Phan")
    
    $audioSelection = $null
    if ($camId -match "CAM3|CAM4|CAM5") {
        $audioSelection = Get-ChildItem -Path $audioDir -Filter "*Shorts*.mp3" | Select-Object -First 1
    } else {
        $audioSelection = Get-ChildItem -Path $audioDir -Filter "*Horizontal*.mp3" | Select-Object -First 1
    }
    if (-not $audioSelection) {
        $audioSelection = Get-ChildItem -Path $audioDir -Filter "*.mp3" | Get-Random
    }
    if ($audioSelection) {
        $audioFile = $audioSelection.FullName
        Write-Host "  -> Tìm thấy dữ liệu Audio: $($audioSelection.Name)"
        
        # Add Input [2:a] Main Music
        $baseArgs += @("-stream_loop", "-1", "-i", $audioFile)
        # Add Input [3:a] Synthetic Bass Drop SFX (Duration 3s, sweeping sine wave)
        $baseArgs += @("-f", "lavfi", "-t", "3", "-i", "aevalsrc=exprs=0.8*sin(80*2*PI*t)*exp(-2*t)")
        
        $vol = "1.0"
        if ($camId -eq "CAM5") { $vol = "0.40" }
        
        # Mix Main Audio and Sub-Bass Hook
        $filterComplex += ";[2:a]apad,volume=$vol`[main_a];[3:a]volume=1.0[bass_a];[main_a][bass_a]amix=inputs=2:duration=first:dropout_transition=3[aout]"
        
        $audioMap = @("-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-shortest")
    } else {"""

if re.search(pattern, content):
    patched = re.sub(pattern, new_block.replace('\\', '\\\\'), content, count=1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(patched)
    print("Successfully patched Auto_Stitch_Master.ps1 with CapCut features!")
else:
    print("FAILED to match block in Auto_Stitch_Master.ps1")
