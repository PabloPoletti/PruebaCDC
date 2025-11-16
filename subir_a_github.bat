@echo off
echo ========================================
echo   SUBIR BOT CDC A GITHUB
echo ========================================
echo.

echo [1/4] Inicializando Git...
git init

echo.
echo [2/4] Agregando archivos...
git add .

echo.
echo [3/4] Creando commit...
git commit -m "Bot CDC - Sistema de turnos con IA"

echo.
echo [4/4] Subiendo a GitHub...
git branch -M main
git remote add origin https://github.com/PabloPoletti/PruebaCDC.git
git push -u origin main

echo.
echo ========================================
echo   COMPLETADO!
echo ========================================
echo.
echo Ahora ve a: https://share.streamlit.io/
echo Y sigue las instrucciones en INSTRUCCIONES_DEPLOY.md
echo.
pause

