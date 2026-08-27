@echo off
set BLENDER="C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
set SCRIPT="d:\WT3D_Project\Z_Tools\MAXSKILLS_MultiAI_Director.py"

echo ===================================================
echo MAXSKILLS MULTI-AI CINEMATIC DIRECTOR (BLENDER)
echo ===================================================
echo.
echo Drag and drop your .obj or .step or .fbx file here and press Enter:
set /p OBJ_FILE=

set OUT_FILE=%OBJ_FILE%_MultiAIAwards.png

echo.
echo THE COUNCIL OF AI EXPERTS IS WAKING UP...
%BLENDER% -b -P %SCRIPT% -- "%OBJ_FILE%" "%OUT_FILE%"

echo.
echo SUCCESS! Opening image...
start "" "%OUT_FILE%"
pause
