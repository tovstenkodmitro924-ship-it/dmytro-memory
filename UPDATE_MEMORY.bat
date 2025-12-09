@echo off
chcp 65001 > nul
title Eternal Memory Updater

echo.
echo ================================================
echo           ETERNAL MEMORY UPDATER
echo ================================================
echo.

cd /d "%~dp0"
python update_memory.py

echo.
echo Натисни будь-яку клавішу щоб закрити...
pause > nul
