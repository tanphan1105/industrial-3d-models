@echo off
set BLENDER="C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
set SCRIPT="d:\WT3D_Project\Z_Tools\Blender_Cinematic_Test.py"

echo ===================================================
echo TANPHAN CINEMATIC BLENDER TEST ENGINE
echo ===================================================
echo Drag and drop your .obj or .step file here and press Enter:
set /p OBJ_FILE=

set OUT_FILE=%OBJ_FILE%_Render.png

echo.
echo Rendering super high-quality image... Please wait!
%BLENDER% -b -P %SCRIPT% -- "%OBJ_FILE%" "%OUT_FILE%"

echo.
echo Render complete! Opening image...
start "" "%OUT_FILE%"
pause
