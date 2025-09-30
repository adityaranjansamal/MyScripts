@echo off
title Network Adapter Control
color 0A

:menu1
cls
echo ==============================
echo    Network Adapter Control
echo ==============================
echo.
echo Select the adapter:
echo 1. Wi-Fi
echo 2. Ethernet
echo 3. Exit
echo.
set /p choice=Enter choice (1-3): 

if "%choice%"=="1" set adapter="Wi-Fi" & goto menu2
if "%choice%"=="2" set adapter="Ethernet" & goto menu2
if "%choice%"=="3" exit
echo Invalid choice! Try again.
pause
goto menu1

:menu2
cls
echo ==============================
echo   Selected Adapter: %adapter%
echo ==============================
echo.
echo 1. Enable
echo 2. Disable
echo 3. Back to main menu
echo.
set /p action=Enter choice (1-3): 

if "%action%"=="1" goto enable
if "%action%"=="2" goto disable
if "%action%"=="3" goto menu1
echo Invalid choice! Try again.
pause
goto menu2

:enable
cls
echo Enabling %adapter%...
netsh interface set interface name=%adapter% admin=ENABLED
echo Done.
pause
goto menu1

:disable
cls
echo Disabling %adapter%...
netsh interface set interface name=%adapter% admin=DISABLED
echo Done.
pause
goto menu1
