import re

cams = {
    r"d:\WT3D_Project\Z_Tools\CAM_1_YT_CinematicWalkthrough.iLogicVb": r"""Dim orgDispMode = oView.DisplayMode
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.Perspective = True

' Cảnh 1: Worm Eye Drop (100f) - Thả rơi góc thấp gắt
oCam.PerspectiveAngle = 0.65
Dim ang1 = Math.PI * 0.25
For i = 1 To 100
    Dim t = i / 100.0 : Dim e = 1 - Math.Pow(1 - t, 4)
    Dim R = max_dim * (2.0 - 0.7 * e)
    oCam.Eye = tg.CreatePoint(cx + R * Math.Cos(ang1), rb.MaxPoint.Y + max_dim * (1.5 - 1.35 * e), cz + R * Math.Sin(ang1))
    oCam.Target = tg.CreatePoint(cx, cy - dy*0.2 + dy*0.4*e, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 2: Macro Strike (80f) - Zoom in sát rạt
oCam.PerspectiveAngle = 0.4
Dim ang2 = ang1 + Math.PI * 0.5
For i = 1 To 80
    Dim t = i / 80.0 : Dim e = Math.Pow(t, 2)
    Dim R = max_dim * (1.5 - 0.9 * e)
    oCam.Eye = tg.CreatePoint(cx + R * Math.Cos(ang2), cy + dy*0.1, cz + R * Math.Sin(ang2))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 3: Wireframe Whip (90f) - X-Ray quét nhanh
Try : oView.DisplayMode = DisplayModeEnum.kWireframeNoHiddenEdges : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.55
For i = 1 To 90
    Dim t = i / 90.0 : Dim e = t * t * (3 - 2 * t)
    Dim curAng = ang2 + Math.PI * e
    Dim R = max_dim * 0.6
    oCam.Eye = tg.CreatePoint(cx + R * Math.Cos(curAng), cy - dy*0.1 + e*dy*0.3, cz + R * Math.Sin(curAng))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 4: Dutch Angle Pull (100f)
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.7
Dim ang4 = ang2 + Math.PI
For i = 1 To 100
    Dim t = i / 100.0 : Dim e = 1 - Math.Pow(1 - t, 3)
    Dim R = max_dim * (0.6 + 1.2 * e)
    oCam.Eye = tg.CreatePoint(cx + R * Math.Cos(ang4), cy + dy*0.3, cz + R * Math.Sin(ang4))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    Dim tilt = Math.Sin(e * Math.PI) * 0.2
    oCam.UpVector = tg.CreateUnitVector(tilt, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 5: Hero Orbit (110f)
oCam.PerspectiveAngle = 0.45
For i = 1 To 110
    Dim t = i / 110.0 : Dim e = Math.Sin(t * Math.PI / 2)
    Dim curAng = ang4 - e * Math.PI * 0.3
    Dim R = max_dim * (1.8 - 0.2 * t)
    oCam.Eye = tg.CreatePoint(cx + R * Math.Cos(curAng), minY - dy*0.1 + dy*0.2*e, cz + R * Math.Sin(curAng))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

Try : oView.DisplayMode = orgDispMode : Catch : End Try
""",
    r"d:\WT3D_Project\Z_Tools\CAM_2_YT_TechnicalXRay.iLogicVb": r"""Dim orgDispMode = oView.DisplayMode
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.Perspective = True

' Cảnh 1: Shaded approach (110f)
oCam.PerspectiveAngle = 0.5
For i = 1 To 110
    Dim t = i / 110.0 : Dim e = t * t * (3 - 2 * t)
    Dim R = max_dim * (1.5 - 0.7*e)
    Dim ang = Math.PI * 0.1 + e * Math.PI * 0.2
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.5 - dy*0.3*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 2: Fast Wireframe Scan X-Ray (120f)
Try : oView.DisplayMode = DisplayModeEnum.kWireframeNoHiddenEdges : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.6
For i = 1 To 120
    Dim t = i / 120.0 : Dim e = Math.Pow(t, 2)
    Dim R = max_dim * (0.8 + 0.4*e)
    Dim ang = Math.PI * 0.3 + e * Math.PI * 0.8
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), minY - dy*0.1 + dy*0.4*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 3: Top to Bottom Wireframe Drop (110f)
For i = 1 To 110
    Dim t = i / 110.0 : Dim e = 1 - Math.Pow(1 - t, 3)
    oCam.Eye = tg.CreatePoint(cx + max_dim*0.01, rb.MaxPoint.Y + max_dim*(1.2 - 0.7*e), cz + max_dim*0.01)
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    Dim spin = e * Math.PI
    oCam.UpVector = tg.CreateUnitVector(Math.Cos(spin), 0, Math.Sin(spin)) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 4: Extreme Shaded Dolly Pull (140f)
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.8
For i = 1 To 140
    Dim t = i / 140.0 : Dim e = Math.Sin(t * Math.PI / 2)
    Dim R = max_dim * (0.4 + 1.2*e)
    Dim ang = Math.PI * 1.5 - e * Math.PI * 0.25
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2*e, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1920, 1080) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

Try : oView.DisplayMode = orgDispMode : Catch : End Try
""",
    r"d:\WT3D_Project\Z_Tools\CAM_3_SHORTS_Supercar_V1.iLogicVb": r"""Dim orgDispMode = oView.DisplayMode
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.Perspective = True

' Cảnh 1: Dive & Sweep (90f)
oCam.PerspectiveAngle = 0.8
For i = 1 To 90
    Dim t = i / 90.0 : Dim e = 1 - Math.Pow(1 - t, 3)
    Dim R = max_dim * (2.2 - 1.0 * e)
    Dim ang = Math.PI * 0.25 + e * Math.PI * 0.2
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), rb.MaxPoint.Y + max_dim*(1.5 - 1.2*e), cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy - dy*0.2, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 2: Macro Tracking (80f)
oCam.PerspectiveAngle = 0.45
For i = 1 To 80
    Dim t = i / 80.0 : Dim e = Math.Pow(t, 2)
    Dim R = max_dim * (1.2 - 0.7 * e)
    Dim ang = Math.PI * 0.45 + e * Math.PI * 0.1
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.1, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx - dx*0.2*e, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 3: Wireframe Spin (80f)
Try : oView.DisplayMode = DisplayModeEnum.kWireframeNoHiddenEdges : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.7
For i = 1 To 80
    Dim t = i / 80.0 : Dim e = t * t * (3 - 2 * t)
    Dim R = max_dim * 0.8
    Dim ang = Math.PI * 0.55 + Math.PI * 0.8 * e
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.2 + dy*0.4*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.2, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 4: Dutch Worm Eye (100f)
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.95
For i = 1 To 100
    Dim t = i / 100.0 : Dim e = Math.Sin(t * Math.PI / 2)
    Dim R = max_dim * (0.6 + 0.6 * e)
    Dim ang = Math.PI * 1.35 - e * Math.PI * 0.3
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), minY - dy*0.1, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.4*e, cz)
    Dim tilt = Math.Sin(t * Math.PI) * 0.3
    oCam.UpVector = tg.CreateUnitVector(tilt, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 5: Hero Pull-out (100f)
oCam.PerspectiveAngle = 0.6
For i = 1 To 100
    Dim t = i / 100.0 : Dim e = 1 - Math.Pow(1 - t, 3)
    Dim R = max_dim * (1.2 + 1.2 * e)
    Dim ang = Math.PI * 1.05 + e * Math.PI * 0.2
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.3*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

Try : oView.DisplayMode = orgDispMode : Catch : End Try
""",
    r"d:\WT3D_Project\Z_Tools\CAM_4_SHORTS_Supercar_V2.iLogicVb": r"""Dim orgDispMode = oView.DisplayMode
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.Perspective = True

' Cảnh 1: Boom Drop (90f)
oCam.PerspectiveAngle = 0.85
For i = 1 To 90
    Dim t = i / 90.0 : Dim e = 1 - Math.Pow(1 - t, 4)
    Dim R = max_dim * (2.0 - 1.2 * e)
    Dim ang = Math.PI * 0.75 + e * Math.PI * 0.15
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), rb.MaxPoint.Y + max_dim*(1.0 - 0.8*e), cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 2: Whip Pan Wireframe (80f)
Try : oView.DisplayMode = DisplayModeEnum.kWireframeNoHiddenEdges : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.65
For i = 1 To 80
    Dim t = i / 80.0 : Dim e = t * t * (3 - 2 * t)
    Dim R = max_dim * 0.8
    Dim ang = Math.PI * 0.9 + Math.PI * 0.6 * e
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.2, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 3: Push-in Strike Shaded (90f)
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.5
For i = 1 To 90
    Dim t = i / 90.0 : Dim e = Math.Pow(t, 2)
    Dim R = max_dim * (1.5 - 0.9 * e)
    Dim ang = Math.PI * 1.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.1 + dy*0.3*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 4: Dutch Tracking (90f)
oCam.PerspectiveAngle = 0.9
For i = 1 To 90
    Dim t = i / 90.0 : Dim e = Math.Sin(t * Math.PI / 2)
    Dim R = max_dim * (0.6 + 0.4 * e)
    Dim ang = Math.PI * 1.5 + e * Math.PI * 0.4
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), minY - dy*0.1, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.3*e, cz)
    Dim tilt = 0.2 * Math.Sin(t * Math.PI)
    oCam.UpVector = tg.CreateUnitVector(tilt, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 5: Final Launch (100f)
oCam.PerspectiveAngle = 0.55
For i = 1 To 100
    Dim t = i / 100.0 : Dim e = 1 - Math.Pow(1 - t, 3)
    Dim R = max_dim * (1.0 + 1.3 * e)
    Dim ang = Math.PI * 1.9 + e * Math.PI * 0.35
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.1 + dy*0.3*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

Try : oView.DisplayMode = orgDispMode : Catch : End Try
""",
    r"d:\WT3D_Project\Z_Tools\CAM_5_SHORTS_MacroFocus.iLogicVb": r"""Dim orgDispMode = oView.DisplayMode
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.Perspective = True

' Cảnh 1: Fast Turntable Close-up (90f)
oCam.PerspectiveAngle = 0.45
For i = 1 To 90
    Dim t = i / 90.0 : Dim e = Math.Sin(t * Math.PI / 2)
    Dim R = max_dim * (1.1 - 0.3 * e)
    Dim ang = e * Math.PI * 1.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.2, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 2: Deep Dive (80f)
oCam.PerspectiveAngle = 0.65
For i = 1 To 80
    Dim t = i / 80.0 : Dim e = Math.Pow(t, 2)
    Dim R = max_dim * (0.8 - 0.4 * e)
    Dim ang = Math.PI * 1.5 + e * Math.PI * 0.1
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), rb.MaxPoint.Y + max_dim*(0.8 - 0.6*e), cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 3: Wireframe Macro Reveal (100f)
Try : oView.DisplayMode = DisplayModeEnum.kWireframeNoHiddenEdges : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.5
For i = 1 To 100
    Dim t = i / 100.0 : Dim e = t * t * (3 - 2 * t)
    Dim R = max_dim * 0.4
    Dim ang = Math.PI * 1.6 + e * Math.PI * 0.5
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy - dy*0.1, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy + dy*0.3*e, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 4: Dutch Glide Shaded (80f)
Try : oView.DisplayMode = DisplayModeEnum.kShadedWithEdgesRendering : oView.Update() : Catch : End Try
oCam.PerspectiveAngle = 0.85
For i = 1 To 80
    Dim t = i / 80.0 : Dim e = Math.Pow(t, 2)
    Dim R = max_dim * (0.4 + 0.5 * e)
    Dim ang = Math.PI * 2.1 + e * Math.PI * 0.2
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.2, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    Dim tilt = Math.Sin(e * Math.PI) * 0.25
    oCam.UpVector = tg.CreateUnitVector(tilt, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

' Cảnh 5: Smooth Retreat (100f)
oCam.PerspectiveAngle = 0.4
For i = 1 To 100
    Dim t = i / 100.0 : Dim e = 1 - Math.Pow(1 - t, 3)
    Dim R = max_dim * (0.9 + 1.5 * e)
    Dim ang = Math.PI * 2.3 + e * Math.PI * 0.1
    oCam.Eye = tg.CreatePoint(cx + R*Math.Cos(ang), cy + dy*0.2 + dy*0.2*e, cz + R*Math.Sin(ang))
    oCam.Target = tg.CreatePoint(cx, cy, cz)
    oCam.UpVector = tg.CreateUnitVector(0, 1, 0) : oCam.ApplyWithoutTransition() : ThisApplication.UserInterfaceManager.DoEvents()
    oCam.SaveAsBitmap(saveFolder & "\frame_" & frameCount.ToString("0000") & ".png", 1080, 1920) : frameCount += 1
    If System.Windows.Input.Keyboard.IsKeyDown(System.Windows.Input.Key.Escape) Then GoTo RestoreCamera
Next

Try : oView.DisplayMode = orgDispMode : Catch : End Try
"""
}

# Run the patches
for path, new_content in cams.items():
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "CAM_1" in path:
        m = re.search(r'(?s)(oCam\.UpVector = tg\.CreateUnitVector\(\s*0,\s*1,\s*0\s*\)\r?\n\s*oCam\.Perspective\s*=\s*(?:True|False)).*?(?=\r?\n\s*RestoreCamera:)', content)
    elif "CAM_2" in path:
        m = re.search(r'(?s)(\' Cảnh 1:).*?(?=\r?\n\s*RestoreCamera:)', content)
    elif "CAM_3" in path or "CAM_4" in path:
        m = re.search(r'(?s)(oCam\.UpVector = upVec\r?\n).*?(?=\r?\n\s*RestoreCamera:)', content)
    elif "CAM_5" in path:
        m = re.search(r'(?s)(\' Cảnh 1:).*?(?=\r?\n\s*RestoreCamera:)', content)
        
    if m:
        if "CAM_3" in path or "CAM_4" in path:
             content = content[:m.start(1) + len(m.group(1))] + "\\n" + new_content + content[m.end():]
        else:
             content = content[:m.start()] + new_content + content[m.end():]
    else:
        print(f"Could not find regex for {path}")
        continue
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patching complete!")
