import re
import codecs

def indent(text, spaces=0):
    return "\n".join(" "*spaces + line for line in text.split("\n"))

def get_cam_1():
    scenes = [
        # Cut 1: High Angle Whip Pan (60f)
        ("High Angle Whip Pan", 60, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = 1 - (1-t)**3
    Dim R = max_dim * (1.8 - 0.5 * e)
    Dim ang = Math.PI * 0.25 + e * Math.PI
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.8, cz + R*Math.Sin(ang)) """),
        # Cut 2: Macro Push-in (50f)
        ("Macro Push-in", 50, "Shaded", "0.45", """
    Dim t = i / fMax : Dim e = t * t
    Dim R = max_dim * (1.2 - 0.7 * e)
    oCam.Eye = tg.CreatePoint(cx + R, cy + dy*0.2, cz) """),
        # Cut 3: Macro Pull-out Wireframe (50f)
        ("Wireframe Pull-out", 50, "Wireframe", "0.55", """
    Dim t = i / fMax : Dim e = 1 - (1-t)**2
    Dim R = max_dim * (0.3 + 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx - R, cy + dy*0.1, cz + R) """),
        # Cut 4: Dutch Angle Slide (60f)
        ("Dutch Angle Slide", 60, "Shaded", "0.65", """
    Dim t = i / fMax : Dim e = t * t * (3 - 2*t)
    Dim R = max_dim * 1.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(Math.PI*1.2), cy + dy*0.3, cz + R*Math.Sin(Math.PI*1.2) + max_dim*e)
    Dim tilt = Math.Sin(t * Math.PI) * 0.2
    oCam.UpVector = tg.CreateUnitVector(tilt, 1, 0) """),
        # Cut 5: Top-down spiral (70f)
        ("Top-down Spiral", 70, "Shaded", "0.7", """
    Dim t = i / fMax : Dim e = 1 - (1-t)**4
    Dim R = max_dim * (1.0 - 0.8 * e)
    Dim ang = e * Math.PI * 2
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), rb.MaxPoint.Y + max_dim*(1.5 - 1.2*e), cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz) """),
        # Cut 6: Worm Eye Flyby (60f)
        ("Worm Eye Flyby", 60, "Shaded", "0.8", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 0.5
    oCam.Eye = tg.CreatePoint(cx - max_dim + 2*max_dim*e, minY - dy*0.1, cz + R)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.3, cz) """),
        # Cut 7: X-Ray Sweep (50f)
        ("X-Ray Sweep", 50, "Wireframe", "0.6", """
    Dim t = i / fMax : Dim e = t**3
    Dim R = max_dim * 1.1
    Dim ang = Math.PI * 0.5 + Math.PI * e
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.5, cz + R*Math.Sin(ang)) """),
        # Cut 8: Hero Orbit Reveal (80f)
        ("Hero Orbit Reveal", 80, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = 1 - (1-t)**3
    Dim R = max_dim * (0.8 + 1.2 * e)
    Dim ang = Math.PI * 1.5 - e * Math.PI * 0.4
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.1 + dy*0.2*e, cz + R*Math.Sin(ang)) """)
    ]
    return generate_code(scenes, 1920, 1080)

def get_cam_3(): # SHORTS 9:16 (10 scenes)
    scenes = [
        ("Sky Drop", 45, "Shaded", "0.85", """
    Dim t = i / fMax : Dim e = 1 - (1-t)**3
    Dim R = max_dim * (2.2 - 1.2 * e)
    Dim ang = Math.PI * 0.25
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), rb.MaxPoint.Y + max_dim*(1.5 - 1.0*e), cz + R*Math.Sin(ang)) """),
        ("Macro Strike", 40, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = t * t * (3 - 2*t)
    Dim R = max_dim * (1.2 - 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx - R, cy + dy*0.1, cz + R*0.5) """),
        ("Whip Pan Wireframe", 45, "Wireframe", "0.7", """
    Dim t = i / fMax : Dim e = t * t
    Dim R = max_dim * 0.8
    Dim ang = Math.PI + e * Math.PI * 0.8
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.3, cz + R*Math.Sin(ang)) """),
        ("Reverse Dolly", 45, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = 1 - (1-t)**2
    Dim R = max_dim * (0.4 + 1.2 * e)
    oCam.Eye = tg.CreatePoint(cx, cy + dy*0.2, cz - R) """),
        ("Kamikaze", 45, "Shaded", "0.9", """
    Dim t = i / fMax : Dim e = t**3
    Dim R = max_dim * (1.5 - 1.0 * e)
    Dim ang = Math.PI * 1.75
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), rb.MaxPoint.Y - dy*e, cz + R*Math.Sin(ang)) """),
        ("Dutch Sweep", 45, "Shaded", "0.8", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 0.9
    Dim ang = Math.PI * 0.5 + e * Math.PI * 0.4
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy, cz + R*Math.Sin(ang))
    Dim tilt = Math.Sin(e * Math.PI) * 0.25
    oCam.UpVector = tg.CreateUnitVector(tilt, 1, 0) """),
        ("Micro Zoom Wireframe", 45, "Wireframe", "0.5", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * (0.8 - 0.4 * e)
    oCam.Eye = tg.CreatePoint(cx + R, cy + dy*0.4, cz) """),
        ("Extreme Punch", 40, "Shaded", "0.75", """
    Dim t = i / fMax : Dim e = t**4
    Dim R = max_dim * (1.1 - 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx, cy - dy*0.1 + dy*0.5*e, cz + R) """),
        ("Quick Orbit", 50, "Shaded", "0.65", """
    Dim t = i / fMax : Dim e = 1 - (1-t)**3
    Dim R = max_dim * 1.3
    Dim ang = Math.PI * 0.1 + e * Math.PI * 0.6
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.2, cz + R*Math.Sin(ang)) """),
        ("Launch Out", 50, "Shaded", "0.55", """
    Dim t = i / fMax : Dim e = t * t * (3 - 2*t)
    Dim R = max_dim * (0.5 + 1.8 * e)
    Dim ang = Math.PI * 0.7 - e * Math.PI * 0.2
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.3 + dy*0.5*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz) """)
    ]
    return generate_code(scenes, 1080, 1920)

def generate_code(scenes, w, h):
    lines = [
        "Dim orgDispMode = oView.DisplayMode",
        "Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try",
        "oCam.Perspective = True"
    ]
    
    for idx, (name, frames, mode, persp, logic) in enumerate(scenes, 1):
        lines.append(f"\n' === SCENE {idx}: {name} ({frames}f) ===")
        if mode == "Wireframe":
            lines.append("Try : oView.DisplayMode = DisplayModeEnum.kWireframeNoHiddenEdges : oView.Update() : Catch : End Try")
        else:
            lines.append("Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try")
            
        lines.append(f"oCam.PerspectiveAngle = {persp}")
        lines.append(f"Dim fMax{idx} = {frames}")
        lines.append(f"For i = 1 To fMax{idx}")
        lines.append(f"    Dim fMax = fMax{idx}.0")
        
        # Replace ** with math.pow
        logic = re.sub(r'([a-zA-Z0-9_\-\.\(\)\s]+)\*\*([0-9\.]+)', r'Math.Pow(\1, \2)', logic)
        for l in logic.strip().split('\n'):
            lines.append("    " + l.strip())
            
        if "oCam.Target =" not in logic:
            lines.append("    oCam.Target = tg.CreatePoint(cx, cy, cz)")
        if "oCam.UpVector =" not in logic:
            lines.append("    oCam.UpVector = tg.CreateUnitVector(0, 1, 0)")
            
        lines.append("    oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()")
        lines.append(f'    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", {w}, {h}) : frameCount += 1')
        lines.append('    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera')
        lines.append("Next")
        
    lines.append("\nTry : oView.DisplayMode = orgDispMode : Catch : End Try")
    return "\n".join(lines)

def patch_file(filepath, scenes_func, w, h):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()

    new_content = scenes_func()
    
    # We will replace from "Dim orgDispMode =" down to "RestoreCamera"
    # Actually, the file might currently have "Dim orgDispMode = ..." because we already patched it
    # We regex from the first "Dim orgDispMode =" down to "RestoreCamera:"
    
    pattern = r"(?s)(Dim orgDispMode = oView\.DisplayMode\r?\nTry : oView\.DisplayMode = DisplayModeEnum\.kShadedWithEdgesRendering : oView\.Update\(\) : Catch : End Try\r?\noCam\.Perspective = True).*?(?=\r?\n\s*RestoreCamera:)"
    
    m = re.search(pattern, content)
    if m:
        content = content[:m.start()] + new_content + content[m.end():]
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"FAILED to find target block in {filepath}")

import glob
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_1_YT_CinematicWalkthrough.iLogicVb", get_cam_1, 1920, 1080)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_2_YT_TechnicalXRay.iLogicVb", get_cam_1, 1920, 1080)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_3_SHORTS_Supercar_V1.iLogicVb", get_cam_3, 1080, 1920)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_4_SHORTS_Supercar_V2.iLogicVb", get_cam_3, 1080, 1920)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_5_SHORTS_MacroFocus.iLogicVb", get_cam_3, 1080, 1920)

