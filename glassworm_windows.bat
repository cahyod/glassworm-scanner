@echo off
REM GlassWorm Advanced Scanner for Windows
REM Batch script untuk menjalankan scanner di Windows

echo ===========================================
echo GlassWorm Advanced Scanner for Windows
echo ===========================================

REM Cek apakah Python tersedia
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python tidak ditemukan di sistem.
    echo Harap instal Python dan pastikan ada di PATH.
    pause
    exit /b 1
)

REM Buat direktori laporan jika belum ada
if not exist "%USERPROFILE%\glassworm-report" mkdir "%USERPROFILE%\glassworm-report"

echo [+] Menjalankan GlassWorm Scanner...
echo [+] Direktori laporan: %USERPROFILE%\glassworm-report

REM Jalankan scanner Python
python "%~dp0\gwscan_crossplatform.py"

echo.
echo [+] Scan selesai!
echo Laporan tersedia di: %USERPROFILE%\glassworm-report
echo.
echo Tekan tombol apapun untuk membuka laporan di browser...
pause >nul
start "" "%USERPROFILE%\glassworm-report\report.html"