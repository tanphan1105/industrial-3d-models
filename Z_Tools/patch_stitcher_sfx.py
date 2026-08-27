import re

filepath = r"d:\WT3D_Project\Z_Tools\Auto_Stitch_Master.ps1"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"(?s)(\s*# Add Input \[2:a\] Main Music\r?\n\s+\$baseArgs \+= \@\(\"-stream_loop\", \"-1\", \"-i\", \$audioFile\)\r?\n\s+# Add Input \[3:a\] Synthetic Bass Drop SFX .*?)(?=\s*\$audioMap = \@\(\"-map\", \"\[aout\]\")"

new_block = """        # Add Input [2:a] Main Music
        $baseArgs += @("-stream_loop", "-1", "-i", $audioFile)
        
        $sfxDir = "$toolsDir\\Audio\\SFX"
        $sfxFile = Get-ChildItem -Path $sfxDir -Filter "*.wav" | Get-Random
        if ($sfxFile) {
            Write-Host "  -> B2B SFX Engine Injecting: $($sfxFile.Name)"
            $baseArgs += @("-i", $sfxFile.FullName)
        } else {
            Write-Host "  -> No WAV found, generating Lavfi Fallback Bass Drop"
            $baseArgs += @("-f", "lavfi", "-t", "3", "-i", "aevalsrc=exprs=0.8*sin(80*2*PI*t)*exp(-2*t)")
        }
        
        $vol = "1.0"
        if ($camId -eq "CAM5") { $vol = "0.40" }
        
        # Mix Main Audio and Sub-Bass Hook
        $filterComplex += ";[2:a]apad,volume=$vol`[main_a];[3:a]volume=1.0[sfx_a];[main_a][sfx_a]amix=inputs=2:duration=first:dropout_transition=3[aout]"
"""

if re.search(pattern, content):
    patched = re.sub(pattern, new_block.replace('\\', '\\\\'), content, count=1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(patched)
    print("Successfully patched SFX integration!")
else:
    print("FAILED to match block")
