@set PYTHONDONTWRITEBYTECODE=1
@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo  WT3D FAB EXTENSION - Auto-Sync Projects from 01_PROJECTS
echo ============================================================
echo.
python -B "%~dp0wt3d_sync_projects.py"
echo.
echo ============================================================
echo  DONE! Reload extension in Chrome/Edge browser.
echo ============================================================
pause
