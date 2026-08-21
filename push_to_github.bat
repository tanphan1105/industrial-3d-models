@echo off
title Push WaterTreatment3D Studio to GitHub
echo ========================================================
echo  Dang day du lieu len GitHub (tanphan1105/industrial-3d-models)...
echo ========================================================
cd /d "D:\WT3D_Project\industrial-3d-models"
git add studio.html publishing-studio.html
git commit -m "feat: Add WaterTreatment3D RO2000 Mobile Publishing Studio"
git push origin main
echo.
echo ========================================================
echo  HOAN TAT! Link vinh vien cua ban:
echo  https://tanphan1105.github.io/industrial-3d-models/studio.html
echo ========================================================
pause
