import re
import codecs

def generate_code(scenes, w, h):
    lines = [
        "Dim isAborted As Boolean = False",
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
            
        if "oCam.UpVector =" not in logic and "ViewOrientationType" not in logic:
            lines.append("    oCam.UpVector = tg.CreateUnitVector(0, 1, 0)")
            
        lines.append("    oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()")
        lines.append(f'    oCam.SaveAsBitmap(saveFolder & "\\frame_" & frameCount.ToString("0000") & ".png", {w}, {h}) : frameCount += 1')
        lines.append('    ThisApplication.UserInterfaceManager.DoEvents()')
        lines.append('    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then : isAborted = True : GoTo AbortCamera : End If')
        lines.append("Next")
        
    lines.append("\nGoTo NormalCompletion")
    lines.append("AbortCamera:")
    lines.append("    MessageBox.Show(\"🛑 HỦY RENDER THÀNH CÔNG! Đã dừng việc chụp ảnh và xuất FFmpeg.\", \"Ngắt Khẩn Cấp B2B\")")
    lines.append("    Try : oView.DisplayMode = orgDispMode : Catch : End Try")
    lines.append("    oCam.Eye = oTg2.CreatePoint(orgEyeX, orgEyeY, orgEyeZ)")
    lines.append("    oCam.Target = oTg2.CreatePoint(orgTgx, orgTgy, orgTgz)")
    lines.append("    oCam.UpVector = oTg2.CreateUnitVector(orgUpX, orgUpY, orgUpZ)")
    lines.append("    oCam.Perspective = orgPersp")
    lines.append("    If orgPersp Then : Try : oCam.PerspectiveAngle = orgPerspAng : Catch : End Try : End If")
    lines.append("    oCam.Apply() : oView.Update()")
    lines.append("    Exit Sub")
    lines.append("\nNormalCompletion:")
    lines.append("Try : oView.DisplayMode = orgDispMode : Catch : End Try")
    return "\n".join(lines)


# -------------------------------------------------------------------------
# CAM 1: CINEMATIC WALKTHROUGH (Maxskills Smooth Continuous)
def get_cam_1():
    scenes = [
        ("Fit To View Establishing", 100, "Shaded", """
    Dim t = i / fMax : Dim e = t
    oCam.ViewOrientationType = ViewOrientationTypeEnum.kIsoTopRightViewOrientation
    oCam.Fit()
    Dim extW As Double : Dim extH As Double : oCam.GetExtents(extW, extH)
    oCam.SetExtents(extW * 1.3 - (extW * 0.3) * e, extH * 1.3 - (extH * 0.3) * e) """),

        ("Epic 360 Flycam Sweep", 120, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim theta = Math.PI * 0.25 + (Math.PI * 2.0) * e
    Dim curR = max_dim * (1.8 - 0.4 * Math.Sin(Math.PI * e))
    Dim sweepY = cy + max_dim * 0.6 * Math.Cos(Math.PI * e)
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), sweepY, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, cy + max_dim * 0.1, cz)
    oCam.PerspectiveAngle = 0.6 """),

        ("Extreme Push-In Xa Gan", 50, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    Dim curR = max_dim * (2.8 - 2.4 * e)
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(Math.PI*0.35), cy + max_dim * (0.8 - 0.7*e), cz + curR * Math.Sin(Math.PI*0.35))
    oCam.Target = tg.CreatePoint(cx + max_dim*0.1*e, cy - max_dim*0.1*e, cz)
    oCam.PerspectiveAngle = 0.5 + 0.3 * e """),

        ("Blueprint Helicopter Orbit", 50, "Wireframe", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim theta = Math.PI * 1.5 + (Math.PI * 0.8) * e
    Dim curR = max_dim * (0.5 + 1.5 * e)
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), cy + max_dim*0.8, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.5 + 0.2 * e """),

        ("Fit To View SEO Hero Front", 140, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    oCam.ViewOrientationType = ViewOrientationTypeEnum.kIsoTopRightViewOrientation
    oCam.Fit()
    Dim extW As Double : Dim extH As Double : oCam.GetExtents(extW, extH)
    oCam.SetExtents(extW * 0.7 + (extW * 0.3) * e, extH * 0.7 + (extH * 0.3) * e) """)
    ]
    return generate_code(scenes, 1920, 1080)


# -------------------------------------------------------------------------
# CAM 2: TECHNICAL X-RAY (Orthogonal paths, strict wireframe/shaded toggles)
def get_cam_2():
    scenes = [
        ("Cinematic X-Ray Spin 180", 120, "Wireframe", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim curR = max_dim * 1.6
    Dim theta = Math.PI * 0.25 + Math.PI * 1.0 * e
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), cy + dy*0.3, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.7 """),

        ("Deep Internal Slide", 50, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 1.5)
    Dim curR = max_dim * (0.15 + 1.1 * e)
    Dim theta = Math.PI * 0.25 - (Math.PI * 0.2) * e
    Dim sweepY = cy - dy * 0.4 + (dy * 0.6) * e
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), sweepY, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 0.9 - 0.4 * e """),

        ("Majestic God Eye Spiral", 70, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    Dim theta = Math.PI * 0.0 + (Math.PI * 2.5) * e
    Dim curR = max_dim * (0.8 * (1.0 - e) + 0.01)
    Dim dropY = cy + max_dim * (1.8 - 1.2 * e)
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), dropY, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, cy + dy * 0.2 * e, cz)
    oCam.PerspectiveAngle = 0.7 - 0.3 * e """),

        ("X-Ray Fit To View Finale", 150, "Wireframe", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    oCam.ViewOrientationType = ViewOrientationTypeEnum.kIsoTopRightViewOrientation
    oCam.Fit()
    Dim extW As Double : Dim extH As Double : oCam.GetExtents(extW, extH)
    oCam.SetExtents(extW * 1.6 - (extW * 0.6) * e, extH * 1.6 - (extH * 0.6) * e) """)
    ]
    return generate_code(scenes, 1920, 1080)


# -------------------------------------------------------------------------
# CAM 3: SHORTS SUPERCAR V1 (Maxskills Aggressive Predator)
def get_cam_3():
    scenes = [
        ("Supercar Fit Establishing", 100, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    oCam.ViewOrientationType = ViewOrientationTypeEnum.kIsoTopRightViewOrientation
    oCam.Fit()
    Dim extW As Double : Dim extH As Double : oCam.GetExtents(extW, extH)
    oCam.SetExtents(extW * 0.7 + (extW * 0.3) * e, extH * 0.7 + (extH * 0.3) * e) """),

        ("FPV Kamikaze Dive", 60, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.5)
    Dim dropY = cy + max_dim * 2.0 - max_dim * 2.2 * e
    Dim theta = Math.PI * 0.25 + Math.PI * 0.8 * e
    Dim curR = max_dim * (1.5 - 1.1 * e)
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), dropY, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, cy - dy*0.2, cz)
    oCam.PerspectiveAngle = 0.5 + 0.4 * e """),

        ("Whip Reverse Dolly", 50, "Wireframe", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 4.0)
    Dim curR = max_dim * (0.2 + 1.8 * e)
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(Math.PI*0.35), cy + dy*0.2, cz + curR * Math.Sin(Math.PI*0.35))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 1.2 - 0.6 * e """),

        ("Ground Drift Sneak", 50, "Shaded", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0 * t)
    Dim theta = Math.PI * 0.15 + (Math.PI * 0.4) * e
    Dim curR = max_dim * (0.5 + 0.5 * Math.Sin(Math.PI * e))
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), cy - dy*0.45, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx - dx*0.2, cy + dy*0.1, cz + dz*0.2)
    oCam.PerspectiveAngle = 1.0 """),

        ("Supercar Fit To View Crash", 130, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Sin(Math.PI * 0.5 * t)
    oCam.ViewOrientationType = ViewOrientationTypeEnum.kIsoTopRightViewOrientation
    oCam.Fit()
    Dim extW As Double : Dim extH As Double : oCam.GetExtents(extW, extH)
    oCam.SetExtents(extW * 2.0 - (extW * 1.0) * e, extH * 2.0 - (extH * 1.0) * e) """)
    ]
    return generate_code(scenes, 1080, 1920)

# -------------------------------------------------------------------------
# CAM 4: SHORTS SUPERCAR V2 (Vertical Crane & Slides)
def get_cam_4():
    scenes = [
        ("Violent Crane Lift", 60, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    Dim theta = Math.PI * 0.25 + (Math.PI * 0.6) * e
    Dim curR = max_dim * (0.4 + 0.7 * e)
    Dim scanY = (cy - dy * 0.5) + (dy * 1.2) * e
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), scanY, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, scanY - dy * 0.3, cz)
    oCam.PerspectiveAngle = 0.8 - 0.2 * e """),

        ("Tension Top Orbit", 60, "Wireframe", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.5)
    Dim theta = Math.PI * 0.25 + (Math.PI * 1.5) * t
    Dim curR = max_dim * (1.2 - 0.7 * e)
    Dim eyeY = cy + dy*0.3 + max_dim * (1.2 - 0.8 * e)
    Dim topY = cy + dy * 0.2
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), eyeY, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, topY, cz)
    oCam.PerspectiveAngle = 0.7 """),

        ("Matrix Bullet Path", 50, "Shaded", """
    Dim t = i / fMax : Dim e = t * t * (3.0 - 2.0*t)
    Dim startTheta = Math.PI * 0.1
    Dim endTheta = Math.PI * 0.5
    Dim theta = startTheta + (endTheta - startTheta) * e
    Dim curR = max_dim * 1.5
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), cy + max_dim*0.6*Math.Sin(Math.PI*e), cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.PerspectiveAngle = 0.5 + 0.3 * Math.Sin(Math.PI*e) """),

        ("Flowline Fit Zoom", 140, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 2.0)
    oCam.ViewOrientationType = ViewOrientationTypeEnum.kIsoTopRightViewOrientation
    oCam.Fit()
    Dim extW As Double : Dim extH As Double : oCam.GetExtents(extW, extH)
    oCam.SetExtents(extW * 0.6 + (extW * 0.4) * e, extH * 0.6 + (extH * 0.4) * e) """)
    ]
    return generate_code(scenes, 1080, 1920)


# -------------------------------------------------------------------------
# CAM 5: SHORTS MACRO FOCUS (High Zoom, tight radius)
def get_cam_5():
    scenes = [
        ("Macro Detail Dive", 40, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.0)
    Dim theta = Math.PI * 0.35 + (Math.PI * 0.5) * e
    Dim curR = max_dim * (0.8 - 0.65 * e)
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), cy - dy*0.2 + (dy*0.5)*e, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx + dx*0.2, cy, cz + dz*0.2)
    oCam.PerspectiveAngle = 0.5 """),

        ("Creep Spin Focus", 40, "Wireframe", """
    Dim t = i / fMax : Dim theta = Math.PI * 0.1 + (Math.PI * 0.4) * t
    Dim curR = max_dim * 0.15
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), cy + dy*0.35, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx + dx*0.1, cy + dy*0.25, cz + dz*0.1)
    oCam.PerspectiveAngle = 0.35 + 0.3 * Math.Sin(Math.PI*t) """),

        ("Explosive Pull Away", 50, "Shaded", """
    Dim t = i / fMax : Dim e = Math.Pow(t, 2.5)
    Dim theta = Math.PI * 0.25
    Dim curR = max_dim * (0.1 + 1.8 * e)
    oCam.Eye = tg.CreatePoint(cx + curR * Math.Cos(theta), cy + dy*0.1 + dy*0.4*e, cz + curR * Math.Sin(theta))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.PerspectiveAngle = 1.0 - 0.5 * e """),

        ("Micro Fit Snap Finale", 150, "Shaded", """
    Dim t = i / fMax : Dim e = 1.0 - Math.Pow(1.0 - t, 3.0)
    oCam.ViewOrientationType = ViewOrientationTypeEnum.kIsoTopRightViewOrientation
    oCam.Fit()
    Dim extW As Double : Dim extH As Double : oCam.GetExtents(extW, extH)
    oCam.SetExtents(extW * 0.5 + (extW * 0.5) * e, extH * 0.5 + (extH * 0.5) * e) """)
    ]
    return generate_code(scenes, 1080, 1920)

def patch_file(filepath, scenes_func):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()

    new_content = scenes_func()
    
    pattern = r"(?s)(?:Dim isAborted As Boolean = False\r?\n)*(Dim orgDispMode = oView\.DisplayMode\r?\nTry : oView\.DisplayMode = DisplayModeEnum\.kShadedWithEdgesRendering : oView\.Update\(\) : Catch : End Try\r?\noCam\.Perspective = True).*?(?=\r?\n\s*RestoreCamera:)"
    
    m = re.search(pattern, content)
    if m:
        content = content[:m.start()] + new_content + "\n" + content[m.end():]
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        pattern_fallback = r"(?s)(?:Dim isAborted As Boolean = False\r?\n)*Dim orgDispMode = oView\.DisplayMode.*?RestoreCamera:"
        m2 = re.search(pattern_fallback, content)
        if m2:
            content = content[:m2.start()] + new_content + "\nRestoreCamera:" + content[m2.end():]
            with codecs.open(filepath, 'w', 'utf-8') as f:
                f.write(content)
            print(f"Patched (fallback) {filepath}")
        else:
            print(f"FAILED to find target block in {filepath}")

patch_file(r"d:\WT3D_Project\Z_Tools\CAM_1_YT_CinematicWalkthrough.iLogicVb", get_cam_1)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_2_YT_TechnicalXRay.iLogicVb", get_cam_2)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_3_SHORTS_Supercar_V1.iLogicVb", get_cam_3)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_4_SHORTS_Supercar_V2.iLogicVb", get_cam_4)
patch_file(r"d:\WT3D_Project\Z_Tools\CAM_5_SHORTS_MacroFocus.iLogicVb", get_cam_5)
