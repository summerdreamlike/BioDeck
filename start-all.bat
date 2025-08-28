@echo off
chcp 65001 >nul
echo ========================================
echo 启动多媒体教学系统
echo ========================================

echo.
echo 1. 检查环境...
echo 检查Node.js...
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 找不到npm命令，请确保已安装Node.js
    echo 请访问 https://nodejs.org 下载并安装Node.js
    pause
    exit /b 1
)

echo 检查Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 找不到python命令，请确保已安装Python
    echo 请访问 https://python.org 下载并安装Python
    pause
    exit /b 1
)

echo 环境检查通过！

echo 2. 检查项目文件...
if not exist "frontend\package.json" (
    echo 错误: 找不到前端项目文件
    echo 请确保在项目根目录下运行此脚本
    pause
    exit /b 1
)

if not exist "backend\app.py" (
    echo 错误: 找不到后端项目文件
    echo 请确保在项目根目录下运行此脚本
    pause
    exit /b 1
)

echo 项目文件检查通过！

echo 3. 启动服务...
echo 按任意键开始启动前后端服务...

echo.
echo 正在启动后端服务器...
start "后端服务器" cmd /k "cd backend && python app.py"

echo 等待后端服务器启动...
timeout /t 3 /nobreak >nul

echo 正在启动前端服务器...
start "前端服务器" cmd /k "cd frontend && npm run serve"

echo.
echo 服务启动完成！
REM 等待端口可用并自动打开前端页面
powershell -NoProfile -ExecutionPolicy Bypass -Command "
  $ErrorActionPreference='SilentlyContinue';
  while(-not (Test-NetConnection -ComputerName 'localhost' -Port 5000 -InformationLevel Quiet)) { Start-Sleep -Seconds 1 }
  while(-not (Test-NetConnection -ComputerName 'localhost' -Port 8080 -InformationLevel Quiet)) { Start-Sleep -Seconds 1 }
  Start-Sleep -Seconds 1
"
start "" "http://localhost:8080/"
echo.
echo 其他设备可以通过以下地址访问:
echo 前端: http://%IP%:8080
echo 后端: http://%IP%:5000
echo.
echo 提示:
echo - 前端服务器需要等待依赖安装完成
echo - 如果前端启动失败，请手动进入frontend目录运行 npm install
echo - 如果后端启动失败，请手动进入backend目录运行 pip install -r requirements.txt
echo.
