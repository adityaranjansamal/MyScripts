@echo off
:: Generate battery report using PowerShell
powershell -Command "powercfg /batteryreport /output $env:USERPROFILE\battery-report.html"

:: Open the generated report in default browser
start "" "%USERPROFILE%\battery-report.html"

:: Optional pause if you want to see status
:: pause
