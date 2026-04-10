@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ==========================================
echo   LEMS - Lab Equipment Management System
echo   Full Stack Startup Script
echo ==========================================

:: ============================================
:: Step 1: Compile Backend
:: ============================================
echo.
echo [Step 1/10] Compiling backend project...
call mvn clean package -DskipTests -f %~dp0pom.xml
if %errorlevel% neq 0 (
    echo [ERROR] Backend compilation failed! Please check the error messages above.
    pause
    exit /b 1
)
echo [Step 1/10] Backend compilation successful.

:: ============================================
:: Step 2: Install Frontend Dependencies
:: ============================================
echo.
echo [Step 2/10] Checking frontend dependencies...
if not exist "%~dp0lems-ui\node_modules" (
    echo Frontend node_modules not found, installing dependencies...
    cd /d "%~dp0lems-ui"
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed! Please check Node.js installation.
        pause
        exit /b 1
    )
    echo [Step 2/10] Frontend dependencies installed.
) else (
    echo [Step 2/10] Frontend dependencies already exist, skipping npm install.
)

:: ============================================
:: Step 3: Start Nacos
:: ============================================
echo.
echo [Step 3/10] Starting Nacos (standalone mode)...

:: Clear old Nacos data to avoid stale service registrations
if exist "%~dp0env\nacos\data" (
    echo Clearing old Nacos data...
    rd /s /q "%~dp0env\nacos\data" 2>nul
)

start "Nacos" cmd /c "%~dp0env\nacos\bin\startup.cmd -m standalone & pause"

:: Wait for Nacos to be ready (up to 120s)
echo Waiting for Nacos to start (max 120s)...
set NACOS_READY=0
for /l %%i in (1,1,120) do (
    if !NACOS_READY!==0 (
        <nul set /p "=."
        timeout /t 1 /nobreak >nul
        curl -s -o nul -w "%%{http_code}" http://localhost:8848/nacos/ >nul 2>&1
        if !errorlevel! equ 0 (
            set NACOS_READY=1
        )
    )
)
echo.
if !NACOS_READY!==0 (
    echo [Step 3/10] Nacos started successfully.
) else (
    echo [WARNING] Nacos not ready after 120s. Services will retry connection.
)

:: ============================================
:: Step 4: Start Gateway (8080)
:: ============================================
echo.
echo [Step 4/10] Starting Gateway Service (port 8080)...
start "Gateway-8080" cmd /c "cd /d %~dp0 && java -Dspring.cloud.nacos.discovery.ip=127.0.0.1 -jar lab-gateway\target\lab-gateway-1.0.0.jar & echo. & echo [Gateway stopped] & pause"
timeout /t 10 /nobreak >nul
echo [Step 4/10] Gateway service launched.

:: ============================================
:: Step 5: Start Auth Service (8081)
:: ============================================
echo.
echo [Step 5/10] Starting Auth Service (port 8081)...
start "Auth-8081" cmd /c "cd /d %~dp0 && java -Dspring.cloud.nacos.discovery.ip=127.0.0.1 -jar lab-auth\target\lab-auth-1.0.0.jar & echo. & echo [Auth stopped] & pause"
timeout /t 5 /nobreak >nul
echo [Step 5/10] Auth service launched.

:: ============================================
:: Step 6: Start User Service (8082)
:: ============================================
echo.
echo [Step 6/10] Starting User Service (port 8082)...
start "User-8082" cmd /c "cd /d %~dp0 && java -Dspring.cloud.nacos.discovery.ip=127.0.0.1 -jar lab-user\target\lab-user-1.0.0.jar & echo. & echo [User stopped] & pause"
timeout /t 5 /nobreak >nul
echo [Step 6/10] User service launched.

:: ============================================
:: Step 7: Start Device Service (8083)
:: ============================================
echo.
echo [Step 7/10] Starting Device Service (port 8083)...
start "Device-8083" cmd /c "cd /d %~dp0 && java -Dspring.cloud.nacos.discovery.ip=127.0.0.1 -jar lab-device\target\lab-device-1.0.0.jar & echo. & echo [Device stopped] & pause"
timeout /t 5 /nobreak >nul
echo [Step 7/10] Device service launched.

:: ============================================
:: Step 8: Start Borrow Service (8084)
:: ============================================
echo.
echo [Step 8/10] Starting Borrow Service (port 8084)...
start "Borrow-8084" cmd /c "cd /d %~dp0 && java -Dspring.cloud.nacos.discovery.ip=127.0.0.1 -jar lab-borrow\target\lab-borrow-1.0.0.jar & echo. & echo [Borrow stopped] & pause"
timeout /t 5 /nobreak >nul
echo [Step 8/10] Borrow service launched.

:: ============================================
:: Step 9: Start Report Service (8085)
:: ============================================
echo.
echo [Step 9/10] Starting Report Service (port 8085)...
start "Report-8085" cmd /c "cd /d %~dp0 && java -Dspring.cloud.nacos.discovery.ip=127.0.0.1 -jar lab-report\target\lab-report-1.0.0.jar & echo. & echo [Report stopped] & pause"
timeout /t 5 /nobreak >nul
echo [Step 9/10] Report service launched.

:: ============================================
:: Step 10: Start Frontend (3000)
:: ============================================
echo.
echo [Step 10/10] Starting Frontend (port 3000)...

:: Start Frontend (Vite dev server)
start "Frontend-3000" cmd /c "cd /d %~dp0lems-ui && npm run dev & echo. & echo [Frontend stopped] & pause"

:: ============================================
:: Done
:: ============================================
echo.
echo ==========================================
echo   All services launched!
echo ==========================================
echo.
echo   Frontend:    http://localhost:3000
echo   Gateway API: http://localhost:8080
echo   Nacos:       http://localhost:8848/nacos
echo   Nacos:       nacos / nacos
echo.
echo   Microservices:
echo     Auth   -> 8081
echo     User   -> 8082
echo     Device -> 8083
echo     Borrow -> 8084
echo     Report -> 8085
echo.
echo ==========================================
echo   TIPS:
echo   - Each service runs in its own window
echo   - If a window closes, check that window's
echo     error log for details
echo   - Make sure MySQL (3306) and Redis (6379)
echo     are running before starting
echo ==========================================
echo.
pause
