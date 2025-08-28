@echo off
title Ethernet Adapter Control

:: --- ADMIN CHECK ---
:: This section checks for administrative privileges.
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Administrative privileges are required.
    echo Please right-click this script and select "Run as administrator".
    echo.
    pause
    exit /b
)

:: -----------------------------------------------------------------
:: CONFIGURATION: Set your Ethernet adapter name here.
:: To find your adapter name:
:: 1. Press Windows Key + R
:: 2. Type "ncpa.cpl" and press Enter.
:: 3. The name is shown under the Ethernet icon (e.g., "Ethernet", "Ethernet 2").
:: -----------------------------------------------------------------
set "adapterName=Ethernet"


:menu
cls
echo ====================================
echo   Ethernet Adapter Control Script
echo ====================================
echo.
echo  Target Adapter: "%adapterName%"
echo.
echo  [1] Disable Ethernet
echo  [2] Enable Ethernet
echo  [3] Exit
echo.

set /p "choice=Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto disable
if "%choice%"=="2" goto enable
if "%choice%"=="3" goto :eof

echo Invalid choice. Press any key to try again.
pause >nul
goto menu


:disable
cls
echo Disabling "%adapterName%"...
netsh interface set interface name="%adapterName%" admin=disabled
echo.
echo "%adapterName%" has been disabled successfully.
echo.
pause
goto menu


:enable
cls
echo Enabling "%adapterName%"...
netsh interface set interface name="%adapterName%" admin=enabled
echo.
echo "%adapterName%" has been enabled successfully.
echo.
pause
goto menu