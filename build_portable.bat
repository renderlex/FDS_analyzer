@echo off
REM ========================================================================
REM  Скрипт для збірки портативної версії FDS Analyzer
REM ========================================================================

echo.
echo ========================================================================
echo  FDS Analyzer - Збірка портативної версії
echo ========================================================================
echo.

REM Перевірка наявності PyInstaller
echo [1/3] Перевірка PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не знайдено. Встановлюю...
    python -m pip install pyinstaller
) else (
    echo PyInstaller вже встановлено.
)

echo.
echo [2/3] Збірка виконуваного файлу...
pyinstaller FDS_Analyzer.spec

if errorlevel 1 (
    echo.
    echo ПОМИЛКА: Збірка не вдалася!
    echo Перевірте лог помилок вище.
    pause
    exit /b 1
)

echo.
echo [3/3] Копіювання файлів до портативної папки...

REM Створення папки для портативної версії
if not exist "..\FDS_Analyzer_Portable" mkdir "..\FDS_Analyzer_Portable"

REM Копіювання виконуваного файлу
copy /Y "dist\FDS_Analyzer.exe" "..\FDS_Analyzer_Portable\" >nul

REM Копіювання README (якщо існує)
if exist "..\FDS_Analyzer_Portable\README.txt" (
    echo README.txt вже існує, пропускаю...
) else (
    echo README.txt не знайдено. Створіть його вручну.
)

echo.
echo ========================================================================
echo  УСПІХ! Портативна версія створена!
echo ========================================================================
echo.
echo Файли знаходяться в папці: ..\FDS_Analyzer_Portable\
echo.
echo Вміст:
dir /B "..\FDS_Analyzer_Portable\"
echo.
echo Натисніть будь-яку клавішу для завершення...
pause >nul
