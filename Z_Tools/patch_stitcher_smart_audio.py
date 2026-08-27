import re

filepath = r"d:\WT3D_Project\Z_Tools\Auto_Stitch_Master.ps1"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"(?s)(\s*\$sfxDir = \"\$toolsDir\\Audio\\SFX\"\r?\n\s+\$sfxFile = Get-ChildItem -Path \$sfxDir -Filter \"\*\.wav\" \| Get-Random)(?=\r?\n\s+if \(\$sfxFile\))"

new_block = """        $sfxDir = "$toolsDir\\Audio\\SFX"
        
        # --- B2B AI DIRECTOR: SMART AUDIO MAPPING ---
        $sfxFileName = "1_Cinematic_Bass_Drop.wav" 
        if ($camId -eq "CAM2") { $sfxFileName = "2_Robotic_Glitch_Whoosh.wav" }
        elseif ($camId -eq "CAM3") { $sfxFileName = "3_Metal_Impact_Riser.wav" }
        elseif ($camId -eq "CAM4") { $sfxFileName = "4_Pure_Cinematic_Whoosh.wav" }
        elseif ($camId -eq "CAM5") { $sfxFileName = "2_Robotic_Glitch_Whoosh.wav" }
        
        $sfxFile = Get-Item "$sfxDir\\$sfxFileName" -ErrorAction SilentlyContinue"""

if re.search(pattern, content):
    patched = re.sub(pattern, new_block.replace('\\', '\\\\'), content, count=1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(patched)
    print("Successfully mapped Smart SFX logic in Auto_Stitch_Master.ps1")
else:
    print("FAILED to match block")
