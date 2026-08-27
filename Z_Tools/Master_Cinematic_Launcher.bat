@echo off
set SCRIPT_DIR=%~dp0
set POWERSHELL_EXE=powershell.exe

echo ===================================================
echo     T A N P H A N   S T U D I O   M A S T E R     
echo ===================================================
echo.
echo [1] Kich hoat FFmpeg Auto-Stitcher De Render Video 
echo [2] Kich hoat DeepSeek AI De Lam Metadata SEO 
echo.

%POWERSHELL_EXE% -ExecutionPolicy Bypass -File "%SCRIPT_DIR%Auto_Stitch_Master.ps1"

echo.
echo Video da hoan thanh! Nhan Enter de ket thuc.
pause
