@echo off
chcp 65001 >nul
echo ============================================
echo   高考祝福动画 - 生成独立HTML文件
echo ============================================
echo.

cd /d "%~dp0"

python 生成HTML.py

echo.
pause
