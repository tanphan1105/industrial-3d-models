import re
import codecs

def get_cam_1():
    scenes = [
        # Cut 1: High Angle Whip Pan (60f) -> Front sweep
        ("High Angle Whip Pan", 60, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (1.8 - 0.5 * e)
    Dim ang = Math.PI * 0.1 + e * Math.PI * 0.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy, cz + R*Math.Sin(ang)) 
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)"""),
        # Cut 2: Macro Push-in (50f) -> Front right
        ("Macro Push-in", 50, "Shaded", "0.45", """
    Dim t = i / fMax : Dim e = t * t
    Dim R = max_dim * (1.5 - 0.7 * e)
    oCam.Eye = tg.CreatePoint(cx + R*0.5, cy - dy*0.1, cz + R) 
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.15, cz)"""),
        # Cut 3: Macro Pull-out Wireframe (50f) -> Front left
        ("Wireframe Pull-out", 50, "Wireframe", "0.55", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * (0.5 + 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx - R*0.5, cy - dy*0.1, cz + R) 
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)"""),
        # Cut 4: Straight Dolly Slide (60f) -> No Dutch Tilt
        ("Straight Slide", 60, "Shaded", "0.65", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 1.5
    oCam.Eye = tg.CreatePoint(cx - R*0.5 + R*1.0*e, cy - dy*0.1, cz + R*0.8)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)"""),
        # Cut 5: Drop Hero (70f) -> Front
        ("Drop Hero", 70, "Shaded", "0.7", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 4.0)
    Dim R = max_dim * (1.2 - 0.5 * e)
    Dim ang = Math.PI * 0.3 + e * Math.PI * 0.15
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.6*(1.0-e), cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz) """),
        # Cut 6: Worm Eye Flyby (60f) -> Slide front floor
        ("Worm Eye Flyby", 60, "Shaded", "0.8", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 0.8
    oCam.Eye = tg.CreatePoint(cx - max_dim*0.8 + 1.6*max_dim*e, minY, cz + R)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.3, cz) """),
        # Cut 7: X-Ray Sweep (50f) -> Front left to center
        ("X-Ray Sweep", 50, "Wireframe", "0.6", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 3.0)
    Dim R = max_dim * 1.1
    Dim ang = Math.PI * 0.8 - Math.PI * 0.4 * e
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.1, cz + R*Math.Sin(ang)) 
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.25, cz)"""),
        # Cut 8: Hero Orbit Reveal (80f) -> Front right to center
        ("Hero Orbit Reveal", 80, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (0.8 + 1.2 * e)
    Dim ang = Math.PI * 0.1 + e * Math.PI * 0.3
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.15 + dy*0.1*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.15, cz) """)
    ]
    return generate_code(scenes, 1920, 1080)

def get_cam_3(): # SHORTS 9:16 (10 scenes)
    scenes = [
        ("Sky Drop", 45, "Shaded", "0.85", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (2.2 - 0.8 * e)
    Dim ang = Math.PI * 0.35 + e * Math.PI * 0.1
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.8*(1.0-e), cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz) """),
        ("Macro Strike", 40, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * (1.5 - 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx + R*0.3, cy - dy*0.1, cz + R)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz) """),
        ("Whip Pan Wireframe", 45, "Wireframe", "0.7", """
    Dim t = i / fMax : Dim e = t * t
    Dim R = max_dim * 1.0
    Dim ang = Math.PI * 0.1 + e * Math.PI * 0.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.05, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.25, cz) """),
        ("Reverse Dolly", 45, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * (0.6 + 1.2 * e)
    oCam.Eye = tg.CreatePoint(cx - R*0.2, cy - dy*0.15, cz + R)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.15, cz) """),
        ("Kamikaze", 45, "Shaded", "0.9", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 3.0)
    Dim R = max_dim * (1.8 - 1.0 * e)
    Dim ang = Math.PI * 0.45 + e * 0.1 * Math.PI
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.6*(1.0-e) - dy*0.1, cz + R*Math.Sin(ang)) 
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)"""),
        ("Worm Sweep", 45, "Shaded", "0.8", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 1.1
    Dim ang = Math.PI * 0.75 - e * Math.PI * 0.4
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.2, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.3, cz) """),
        ("Micro Zoom Wireframe", 45, "Wireframe", "0.5", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * (0.9 - 0.4 * e)
    oCam.Eye = tg.CreatePoint(cx + R*0.5, cy - dy*0.1, cz + R*0.8)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz) """),
        ("Extreme Punch", 40, "Shaded", "0.75", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 4.0)
    Dim R = max_dim * (1.2 - 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx - R*0.1, cy - dy*0.2 + dy*0.1*e, cz + R)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz) """),
        ("Quick Orbit", 50, "Shaded", "0.65", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * 1.3
    Dim ang = Math.PI * 0.2 + e * Math.PI * 0.4
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.1, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.25, cz) """),
        ("Launch Out", 50, "Shaded", "0.55", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * (0.7 + 1.8 * e)
    Dim ang = Math.PI * 0.6 - e * Math.PI * 0.2
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.1, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.25, cz) """)
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
        lines.append(f"Dim fMax{idx} As Integer = {frames}")
        lines.append(f"For i = 1 To fMax{idx}")
        lines.append(f"    Dim fMax As Double = CDbl(fMax{idx})")
        
        for l in logic.strip().split('\n'):
            lines.append("    " + l.strip())
            
        if "oCam.Target =" not in logic:
            lines.append("    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)")
            
        # Clean UpVector without tilt
        lines.append("    oCam.UpVector = tg.CreateUnitVector(0, 1, 0)")
            
        lines.append("    oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()")
        lines.append(f'    oCam.SaveAsBitmap(saveFolder & "\\frame_" & frameCount.ToString("0000") & ".png", {w}, {h}) : frameCount += 1')
        lines.append('    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera')
        lines.append("Next")
        
    lines.append("\nTry : oView.DisplayMode = orgDispMode : Catch : End Try")
    return "\n".join(lines)

def patch_file(filepath, scenes_func):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()

    new_content = scenes_func()
    
    pattern = r"(?s)(Dim orgDispMode = oView\.DisplayMode\r?\nTry : oView\.DisplayMode = DisplayModeEnum\.kShadedWithEdgesRendering : oView\.Update\(\) : Catch : End Try\r?\noCam\.Perspective = True).*?(?=\r?\n\s*RestoreCamera:)"
    
    m = re.search(pattern, content)
    if m:
        content = content[:m.start()] + new_content + content[m.end():]
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"FAILED to find target block in {filepath}")

patch_file(r"d:\WT3D_Project\Z_Tools\CAM_1_YT_CinematicWalkthrough.iLogicVb", get_cam_1)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_2_YT_TechnicalXRay.iLogicVb", get_cam_1)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_3_SHORTS_Supercar_V1.iLogicVb", get_cam_3)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_4_SHORTS_Supercar_V2.iLogicVb", get_cam_3)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_5_SHORTS_MacroFocus.iLogicVb", get_cam_3)
