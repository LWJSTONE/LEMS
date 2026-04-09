@echo off
chcp 65001 >nul
title LEMS - 实验设备管理系统启动脚本
echo ============================================================
echo   LEMS 实验设备管理系统 - 一键启动脚本
echo ============================================================
echo.

echo [1/7] 检查Java环境...
java -version 2>&1 | findstr "1.8" >nul
if %errorlevel% neq 0 (
    echo [错误] 未找到JDK 1.8，请先安装JDK 8
    pause
    exit /b 1
)
echo [√] Java环境正常
echo.

echo [2/7] 检查MySQL服务...
sc query MySQL80 >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] MySQL服务未运行，请确保MySQL已启动
)
echo [√] MySQL检查完成
echo.

echo [3/7] 初始化数据库...
echo 请确保MySQL已创建数据库 lab_device_mgt 并执行 sql/init.sql
echo.

echo [4/7] 启动Nacos...
echo 请确保Nacos已启动 (bin/startup.cmd)
echo 默认地址: http://localhost:8848/nacos
echo.

echo [5/7] 编译后端项目...
cd /d %~dp0
call mvn clean package -DskipTests
if %errorlevel% neq 0 (
    echo [错误] 编译失败
    pause
    exit /b 1
)
echo [√] 编译成功
echo.

echo [6/7] 启动后端微服务...
echo 启动网关 (8080)...
start "LEMS-Gateway" cmd /k "java -jar lab-gateway/target/lab-gateway-1.0.0.jar"
timeout /t 5 /nobreak >nul

echo 启动认证服务 (8081)...
start "LEMS-Auth" cmd /k "java -jar lab-auth/target/lab-auth-1.0.0.jar"
timeout /t 5 /nobreak >nul

echo 启动用户服务 (8082)...
start "LEMS-User" cmd /k "java -jar lab-user/target/lab-user-1.0.0.jar"
timeout /t 5 /nobreak >nul

echo 启动设备服务 (8083)...
start "LEMS-Device" cmd /k "java -jar lab-device/target/lab-device-1.0.0.jar"
timeout /t 5 /nobreak >nul

echo 启动借用服务 (8084)...
start "LEMS-Borrow" cmd /k "java -jar lab-borrow/target/lab-borrow-1.0.0.jar"
timeout /t 5 /nobreak >nul

echo 启动报表服务 (8085)...
start "LEMS-Report" cmd /k "java -jar lab-report/target/lab-report-1.0.0.jar"
timeout /t 5 /nobreak >nul
echo.

echo [7/7] 启动Nginx...
echo 请确保Nginx已配置并启动
echo.

echo ============================================================
echo   所有服务已启动!
echo   网关地址: http://localhost:8080
echo   前端地址: http://localhost (通过Nginx代理)
echo   Nacos控制台: http://localhost:8848/nacos
echo   默认管理员: admin / admin123
echo ============================================================
pause
