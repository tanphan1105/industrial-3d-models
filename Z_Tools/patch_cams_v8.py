import re
import codecs

# COMMON GENERATOR FUNCTION
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
            
        lines.append("    oCam.UpVector = tg.CreateUnitVector(0, 1, 0)")
        lines.append("    oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()")
        lines.append(f'    oCam.SaveAsBitmap(saveFolder & "\\frame_" & frameCount.ToString("0000") & ".png", {w}, {h}) : frameCount += 1')
        lines.append('    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera')
        lines.append("Next")
        
    lines.append("\nTry : oView.DisplayMode = orgDispMode : Catch : End Try")
    return "\n".join(lines)


# -------------------------------------------------------------------------
# CAM 1: CINEMATIC WALKTHROUGH (16:9 | 8 Scenes | Grand, Slow-to-Fast, Sweeping)
def get_cam_1():
    scenes = [
        ("Cinematic Sweep", 70, "Shaded", "0.55", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (1.6 - 0.4 * e)
    Dim ang = Math.PI * 0.1 + e * Math.PI * 0.7
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.3, cz + R*Math.Sin(ang)) """),
        ("Left-Side Tracking", 60, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 1.2
    oCam.Eye = tg.CreatePoint(cx - R, cy + dy*0.2, cz + max_dim*0.5 - max_dim*1.0*e)"""),
        ("Mid-Air Wireframe Flash", 40, "Wireframe", "0.65", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * (0.8 + 0.5 * e)
    oCam.Eye = tg.CreatePoint(cx + R*0.5, cy + dy*0.5, cz + R)"""),
        ("Hero Low-Angle Rise", 70, "Shaded", "0.7", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 4.0)
    Dim R = max_dim * 1.5
    oCam.Eye = tg.CreatePoint(cx, cy - dy*0.2 + dy*0.6*e, cz + R)"""),
        ("Right-Side Slide", 60, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 1.3
    oCam.Eye = tg.CreatePoint(cx + R, cy, cz - max_dim*0.5 + max_dim*1.0*e)"""),
        ("Top-Down Reveal", 60, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    Dim R = max_dim * 0.8
    oCam.Eye = tg.CreatePoint(cx + R*e, rb.MaxPoint.Y + max_dim*(1.0 - 0.5*e), cz + R)
    oCam.Target = tg.CreatePoint(cx, cy, cz) """),
        ("Internal X-Ray", 50, "Wireframe", "0.45", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * (0.6 - 0.3 * e)
    oCam.Eye = tg.CreatePoint(cx - R, cy, cz + R)"""),
        ("Grand Pull-out Orbit", 70, "Shaded", "0.55", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (0.8 + 1.2 * e)
    Dim ang = Math.PI * 0.7 - e * Math.PI * 0.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy, cz + R*Math.Sin(ang))""")
    ]
    return generate_code(scenes, 1920, 1080)


# -------------------------------------------------------------------------
# CAM 2: TECHNICAL X-RAY (16:9 | 8 Scenes | Heavy Wireframe, Orthogonal paths)
def get_cam_2():
    scenes = [
        ("Tech Analysis Strike", 50, "Wireframe", "0.5", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (1.5 - 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx + R, cy + dy*0.1, cz + R)"""),
        ("Blueprint Sweep", 70, "Wireframe", "0.4", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 1.5
    Dim ang = Math.PI * 0.9 - e * Math.PI * 0.8
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy, cz + R*Math.Sin(ang))"""),
        ("Solid Check", 40, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    Dim R = max_dim * 1.2
    oCam.Eye = tg.CreatePoint(cx, cy - dy*0.1, cz + R - max_dim*0.3*e)"""),
        ("Internal Component Shift", 60, "Wireframe", "0.7", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 0.5
    oCam.Eye = tg.CreatePoint(cx - R + R*2.0*e, cy + dy*0.2, cz + R)"""),
        ("Top-Down Engineering", 70, "Wireframe", "0.5", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * 0.8
    oCam.Eye = tg.CreatePoint(cx, rb.MaxPoint.Y + max_dim*(0.5 + 0.5*e), cz + R - R*e)
    oCam.Target = tg.CreatePoint(cx, cy, cz)"""),
        ("Lateral Scan", 60, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 1.1
    oCam.Eye = tg.CreatePoint(cx + R, cy + dy*0.4 - dy*0.6*e, cz + R*0.5)"""),
        ("Deep Structure Push", 50, "Wireframe", "0.8", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 3.0)
    Dim R = max_dim * (0.8 - 0.4 * e)
    oCam.Eye = tg.CreatePoint(cx - R, cy, cz + R)"""),
        ("Final Solid Overview", 80, "Shaded", "0.45", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (0.5 + 1.2 * e)
    Dim ang = Math.PI * 0.3 + e * Math.PI * 0.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.2, cz + R*Math.Sin(ang))""")
    ]
    return generate_code(scenes, 1920, 1080)


# -------------------------------------------------------------------------
# CAM 3: SHORTS SUPERCAR V1 (9:16 | 10 Scenes | FPV Drone, Wild, Dropping)
def get_cam_3():
    scenes = [
        ("FPV Sky Drop", 45, "Shaded", "0.85", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (2.0 - 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx + R*0.5, rb.MaxPoint.Y + max_dim*(1.2 - 1.0*e), cz + R*0.8)"""),
        ("Whip Left", 40, "Wireframe", "0.7", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 1.0
    Dim ang = Math.PI * 0.1 + e * Math.PI * 0.4
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy, cz + R*Math.Sin(ang))"""),
        ("Ground Rush", 45, "Shaded", "0.9", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    oCam.Eye = tg.CreatePoint(cx, minY - dy*0.1 + dy*0.5*e, cz + max_dim*(1.5 - 0.8*e))"""),
        ("Right Bank Glide", 45, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * (0.8 + 0.4 * e)
    oCam.Eye = tg.CreatePoint(cx + R, cy + dy*0.1, cz + max_dim*0.2*e)"""),
        ("Macro Strike Center", 45, "Wireframe", "0.8", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 3.0)
    Dim R = max_dim * (1.2 - 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx - R*0.2, cy - dy*0.1, cz + R)"""),
        ("Orbit Rush", 45, "Shaded", "0.7", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 0.9
    Dim ang = Math.PI * 0.7 - e * Math.PI * 0.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.1, cz + R*Math.Sin(ang))"""),
        ("Drop from Top-Right", 45, "Shaded", "0.65", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * 0.8
    oCam.Eye = tg.CreatePoint(cx + R, rb.MaxPoint.Y - dy*0.8*e, cz + R)"""),
        ("Front-Left Kamikaze", 40, "Wireframe", "0.85", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    Dim R = max_dim * (1.4 - 0.8 * e)
    oCam.Eye = tg.CreatePoint(cx - R, cy, cz + R*0.8)"""),
        ("Close Sweep", 50, "Shaded", "0.7", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * 0.6
    Dim ang = Math.PI * 0.2 + e * Math.PI * 0.6
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.1, cz + R*Math.Sin(ang))"""),
        ("Boom Launch", 50, "Shaded", "0.55", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * (0.6 + 1.4 * e)
    oCam.Eye = tg.CreatePoint(cx, cy + dy*0.3*e, cz + R)""")
    ]
    return generate_code(scenes, 1080, 1920)


# -------------------------------------------------------------------------
# CAM 4: SHORTS SUPERCAR V2 (9:16 | 10 Scenes | Tracking, Sliding, Lateral)
def get_cam_4():
    scenes = [
        ("Front Lateral Slide", 45, "Shaded", "0.65", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 1.1
    oCam.Eye = tg.CreatePoint(cx - R + R*2.0*e, cy, cz + R*0.8)"""),
        ("Mid Zoom Lock", 40, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (1.0 - 0.4 * e)
    oCam.Eye = tg.CreatePoint(cx + R*0.5, cy - dy*0.1, cz + R)"""),
        ("Rising Tracking", 45, "Wireframe", "0.7", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * 1.3
    oCam.Eye = tg.CreatePoint(cx - R*0.8, minY + dy*0.8*e, cz + R*0.5)"""),
        ("Right Side Speed", 45, "Shaded", "0.6", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 0.9
    oCam.Eye = tg.CreatePoint(cx + R, cy, cz + max_dim*0.8 - max_dim*1.6*e)"""),
        ("Left Side Speed", 45, "Wireframe", "0.6", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 0.9
    oCam.Eye = tg.CreatePoint(cx - R, cy, cz - max_dim*0.8 + max_dim*1.6*e)"""),
        ("Diagonal Push", 45, "Shaded", "0.75", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    Dim R = max_dim * (1.5 - 0.7*e)
    oCam.Eye = tg.CreatePoint(cx + R*0.7, cy + dy*0.2, cz + R*0.7)"""),
        ("Diagonal Reverse", 45, "Shaded", "0.7", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * (0.8 + 0.6*e)
    oCam.Eye = tg.CreatePoint(cx - R*0.7, cy - dy*0.1, cz + R*0.7)"""),
        ("High Slider", 40, "Wireframe", "0.55", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 1.2
    oCam.Eye = tg.CreatePoint(cx + R*0.8 - R*1.6*e, rb.MaxPoint.Y + max_dim*0.2, cz + R*0.6)"""),
        ("Ground Slider", 50, "Shaded", "0.8", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 1.0
    oCam.Eye = tg.CreatePoint(cx - R*0.8 + R*1.6*e, minY - dy*0.2, cz + R*0.8)"""),
        ("Reverse Pull Out", 50, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (0.6 + 1.2 * e)
    oCam.Eye = tg.CreatePoint(cx, cy, cz + R)""")
    ]
    return generate_code(scenes, 1080, 1920)


# -------------------------------------------------------------------------
# CAM 5: SHORTS MACRO FOCUS (9:16 | 10 Scenes | Extreme Close-Up, Very Slow Panning, Tight Depth)
def get_cam_5():
    scenes = [
        ("Macro Front Push", 45, "Shaded", "0.35", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * (0.6 - 0.3 * e)
    oCam.Eye = tg.CreatePoint(cx, cy - dy*0.1, cz + R)"""),
        ("Macro Left Texture", 40, "Wireframe", "0.4", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 0.4
    oCam.Eye = tg.CreatePoint(cx - R, cy, cz + max_dim*0.4 - max_dim*0.2*e)"""),
        ("Macro Right Check", 45, "Shaded", "0.35", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 0.4
    oCam.Eye = tg.CreatePoint(cx + R, cy, cz + max_dim*0.2 + max_dim*0.2*e)"""),
        ("Macro Base Scan", 45, "Shaded", "0.45", """
    Dim t = i / fMax : Dim e = t * t
    Dim R = max_dim * 0.5
    oCam.Eye = tg.CreatePoint(cx - R*0.5 + R*1.0*e, minY, cz + R*0.8)"""),
        ("Macro Top Hub", 45, "Wireframe", "0.4", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim R = max_dim * 0.4
    oCam.Eye = tg.CreatePoint(cx, rb.MaxPoint.Y + max_dim*0.1, cz + R - max_dim*0.2*e)"""),
        ("Tight Shift Right", 45, "Shaded", "0.3", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 0.35
    oCam.Eye = tg.CreatePoint(cx + R, cy - dy*0.2 + dy*0.2*e, cz + R)"""),
        ("Tight Shift Left", 45, "Wireframe", "0.3", """
    Dim t = i / fMax : Dim e = t
    Dim R = max_dim * 0.35
    oCam.Eye = tg.CreatePoint(cx - R, cy + dy*0.1 - dy*0.2*e, cz + R)"""),
        ("Core Explosion", 40, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 3.0)
    Dim R = max_dim * (0.8 - 0.5 * e)
    oCam.Eye = tg.CreatePoint(cx, cy, cz + R)"""),
        ("Surface Wipe", 50, "Shaded", "0.4", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim R = max_dim * 0.5
    oCam.Eye = tg.CreatePoint(cx + R*0.8 - R*1.6*e, cy + dy*0.1, cz + R)"""),
        ("Macro Fade Out", 50, "Shaded", "0.5", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim R = max_dim * (0.4 + 1.0 * e)
    oCam.Eye = tg.CreatePoint(cx, cy, cz + R)""")
    ]
    return generate_code(scenes, 1080, 1920)

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
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_2_YT_TechnicalXRay.iLogicVb", get_cam_2)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_3_SHORTS_Supercar_V1.iLogicVb", get_cam_3)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_4_SHORTS_Supercar_V2.iLogicVb", get_cam_4)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_5_SHORTS_MacroFocus.iLogicVb", get_cam_5)
