import re
import codecs

def generate_code(scenes, w, h):
    lines = [
        "Dim orgDispMode = oView.DisplayMode",
        "Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try",
        "oCam.Perspective = True"
    ]
    
    for idx, (name, frames, mode, logic) in enumerate(scenes, 1):
        lines.append(f"\n' === SCENE {idx}: {name} ({frames}f) ===")
        if mode == "Wireframe":
            lines.append("Try : oView.DisplayMode = DisplayModeEnum.kWireframeNoHiddenEdges : oView.Update() : Catch : End Try")
        else:
            lines.append("Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try")
            
        lines.append(f"Dim fMax{idx} As Integer = {frames}")
        lines.append(f"For i = 1 To fMax{idx}")
        lines.append(f"    Dim fMax As Double = CDbl(fMax{idx})")
        
        for l in logic.strip().split('\n'):
            lines.append("    " + l.strip())
            
        if "oCam.UpVector =" not in logic:
            lines.append("    oCam.UpVector = tg.CreateUnitVector(0, 1, 0)")
            
        lines.append("    oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()")
        lines.append(f'    oCam.SaveAsBitmap(saveFolder & "\\frame_" & frameCount.ToString("0000") & ".png", {w}, {h}) : frameCount += 1')
        lines.append('    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera')
        lines.append("Next")
        
    lines.append("\nTry : oView.DisplayMode = orgDispMode : Catch : End Try")
    return "\n".join(lines)


# -------------------------------------------------------------------------
# CAM 1: CINEMATIC WALKTHROUGH (Maxskills Smooth Continuous)
def get_cam_1():
    scenes = [
        ("Maxskills ISO Dive", 100, "Shaded", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim sEyeX = cx + max_dim*1.2 : Dim sEyeY = rb.MaxPoint.Y + max_dim : Dim sEyeZ = cz + max_dim*1.2
    Dim eEyeX = cx + max_dim*0.8 : Dim eEyeY = cy - dy*0.1 : Dim eEyeZ = cz + max_dim*0.8
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, sEyeY + (eEyeY - sEyeY)*e, sEyeZ + (eEyeZ - sEyeZ)*e)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.4*(1.0-e), cz)
    oCam.PerspectiveAngle = 0.5 + 0.3 * e """),
        
        ("Maxskills Deep Sweep", 100, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim sEyeX = cx + max_dim*0.8 : Dim sEyeY = cy - dy*0.1 : Dim sEyeZ = cz + max_dim*0.8
    Dim eEyeX = cx - max_dim*0.8 : Dim eEyeY = cy - dy*0.1 : Dim eEyeZ = cz + max_dim*0.5
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, sEyeY + (eEyeY - sEyeY)*e, sEyeZ + (eEyeZ - sEyeZ)*e)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 0.8 - 0.2 * e """),

        ("Wireframe X-Ray Reveal", 80, "Wireframe", """
    Dim t = i / fMax : Dim e = t * t
    Dim sEyeX = cx - max_dim*0.8 : Dim sEyeY = cy - dy*0.1 : Dim sEyeZ = cz + max_dim*0.5
    Dim eEyeX = cx : Dim eEyeY = cy + dy*0.3 : Dim eEyeZ = cz + max_dim*1.2
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, sEyeY + (eEyeY - sEyeY)*e, sEyeZ + (eEyeZ - sEyeZ)*e)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 0.6 + 0.2 * e """),

        ("Dolly Zoom Hero", 100, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim sEyeX = cx : Dim sEyeY = cy + dy*0.3 : Dim sEyeZ = cz + max_dim*1.2
    Dim eEyeX = cx + max_dim*0.5 : Dim eEyeY = rb.MaxPoint.Y + max_dim*0.5 : Dim eEyeZ = cz + max_dim*1.5
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, sEyeY + (eEyeY - sEyeY)*e, sEyeZ + (eEyeZ - sEyeZ)*e)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.8 - 0.4 * e """)
    ]
    return generate_code(scenes, 1920, 1080)


# -------------------------------------------------------------------------
# CAM 2: TECHNICAL X-RAY (Orthogonal paths, strict wireframe/shaded toggles)
def get_cam_2():
    scenes = [
        ("Tech Ortho Slide X", 90, "Wireframe", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim sEyeX = cx + max_dim : Dim sEyeZ = cz + max_dim*0.5
    Dim eEyeX = cx - max_dim : Dim eEyeZ = cz + max_dim*0.5
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, cy, sEyeZ)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.5 """),
        
        ("Tech Inspection Zoom", 80, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim sEyeX = cx - max_dim : Dim sEyeZ = cz + max_dim*0.5
    Dim eEyeX = cx - max_dim*0.2 : Dim eEyeZ = cz + max_dim*0.8
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, cy + dy*0.2*e, sEyeZ + (eEyeZ - sEyeZ)*e)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.5 + 0.3 * e """),

        ("Tech Ortho Slide Y", 90, "Wireframe", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim sEyeX = cx - max_dim*0.2 : Dim sEyeZ = cz + max_dim*0.8
    oCam.Eye = tg.CreatePoint(sEyeX, cy + dy*0.2 + max_dim*(0.8*e), sEyeZ)
    oCam.Target = tg.CreatePoint(cx, cy + max_dim*(0.4*e), cz)
    oCam.PerspectiveAngle = 0.8 """),

        ("Solid Review", 120, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim sEyeX = cx - max_dim*0.2 : Dim sEyeY = cy + dy*0.2 + max_dim*0.8
    Dim eEyeX = cx + max_dim : Dim eEyeY = cy - dy*0.1
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, sEyeY + (eEyeY - sEyeY)*e, cz + max_dim*0.8 + max_dim*0.4*e)
    oCam.Target = tg.CreatePoint(cx, cy + max_dim*0.4*(1.0-e), cz)
    oCam.PerspectiveAngle = 0.8 - 0.3 * e """)
    ]
    return generate_code(scenes, 1920, 1080)


# -------------------------------------------------------------------------
# CAM 3: SHORTS SUPERCAR V1 (Maxskills Aggressive Predator)
def get_cam_3():
    scenes = [
        ("Dolly Zoom Punch", 70, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    oCam.Eye = tg.CreatePoint(cx + max_dim*(1.0 - 0.6*e), cy - dy*0.1, cz + max_dim*(1.0 - 0.6*e))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 0.5 + 0.6 * e """),
        
        ("Whip Reverse Dolly", 60, "Wireframe", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    oCam.Eye = tg.CreatePoint(cx + max_dim*0.4, cy - dy*0.1, cz + max_dim*0.4 + max_dim*1.2*e)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 1.1 - 0.6 * e """),

        ("Kamikaze Orbit", 70, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    Dim ang = Math.PI * 0.2 + e * Math.PI * 0.6
    Dim R = max_dim * (1.6 - 0.8*e)
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), rb.MaxPoint.Y - dy*1.5*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 0.8 """),

        ("Worm Eye Slide", 70, "Shaded", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim sEyeX = cx - max_dim*0.4 : Dim eEyeX = cx + max_dim*0.8
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, minY - dy*0.1, cz + max_dim*(0.8 + 0.4*e))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.3, cz)
    oCam.PerspectiveAngle = 0.9 """),

        ("Wireframe Blast", 60, "Wireframe", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 4.0)
    oCam.Eye = tg.CreatePoint(cx + max_dim*0.8, minY - dy*0.1 + max_dim*1.0*e, cz + max_dim*1.2)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 0.9 - 0.4 * e """),

        ("Center Launch Strike", 70, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 3.0)
    oCam.Eye = tg.CreatePoint(cx, cy + max_dim - max_dim*1.1*e, cz + max_dim*(1.2 - 0.8*e))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 0.5 + 0.4 * e """)
    ]
    return generate_code(scenes, 1080, 1920)

# -------------------------------------------------------------------------
# CAM 4: SHORTS SUPERCAR V2 (Tracking & Lateral Slides)
def get_cam_4():
    scenes = [
        ("Long Right Slide", 80, "Shaded", """
    Dim t = i / fMax : Dim e = t
    oCam.Eye = tg.CreatePoint(cx + max_dim*0.8, cy + dy*0.2, cz + max_dim - max_dim*0.8*e)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.7 """),

        ("Long Left Slide", 80, "Wireframe", """
    Dim t = i / fMax : Dim e = t
    oCam.Eye = tg.CreatePoint(cx - max_dim*0.8, cy, cz + max_dim*0.2 + max_dim*0.8*e)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.1, cz)
    oCam.PerspectiveAngle = 0.7 """),

        ("Diagonal Front Slide", 80, "Shaded", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim sEyeX = cx - max_dim*0.5 : Dim eEyeX = cx + max_dim*0.5
    oCam.Eye = tg.CreatePoint(sEyeX + (eEyeX - sEyeX)*e, cy - dy*0.1, cz + max_dim)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.1, cz)
    oCam.PerspectiveAngle = 0.6 """),

        ("Ground Right Slide", 80, "Shaded", """
    Dim t = i / fMax : Dim e = t
    oCam.Eye = tg.CreatePoint(cx + max_dim*0.5 + max_dim*0.5*e, minY, cz + max_dim)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 0.8 """),

        ("Pullout Tracking", 80, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    oCam.Eye = tg.CreatePoint(cx + max_dim - max_dim*1.2*e, cy + dy*0.2*e, cz + max_dim + max_dim*0.5*e)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.8 - 0.3 * e """)
    ]
    return generate_code(scenes, 1080, 1920)


# -------------------------------------------------------------------------
# CAM 5: SHORTS MACRO FOCUS (High Zoom, tight radius)
def get_cam_5():
    scenes = [
        ("Macro Center Drift", 80, "Shaded", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    oCam.Eye = tg.CreatePoint(cx - max_dim*0.1*e, cy, cz + max_dim*0.5)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.35 """),

        ("Macro Extreme Push", 70, "Wireframe", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    oCam.Eye = tg.CreatePoint(cx - max_dim*0.1, cy + dy*0.1*e, cz + max_dim*(0.5 - 0.2*e))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.35 + 0.1 * e """),

        ("Macro Detail Left", 70, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    oCam.Eye = tg.CreatePoint(cx - max_dim*0.3, cy - dy*0.1, cz + max_dim*0.4 + max_dim*0.2*e)
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.1, cz)
    oCam.PerspectiveAngle = 0.45 """),

        ("Macro Detail Right", 70, "Shaded", """
    Dim t = i / fMax : Dim e = t
    oCam.Eye = tg.CreatePoint(cx + max_dim*0.3, cy - dy*0.1 + dy*0.2*e, cz + max_dim*0.6)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.4 """),

        ("Macro Solid Review", 110, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    oCam.Eye = tg.CreatePoint(cx + max_dim*0.3 - max_dim*0.6*e, cy + dy*0.1, cz + max_dim*0.6 + max_dim*0.5*e)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.4 + 0.3 * e """)
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
