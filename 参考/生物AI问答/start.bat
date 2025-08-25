@echo off
chcp 65001 >nul
echo 🧬 启动高中生物智能问答系统
echo ================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)

echo 📦 安装后端依赖...
cd code\backend
pip install -r requirements.txt

echo 📦 安装前端依赖...
cd ..\frontend\vue
npm install

echo 🚀 启动后端服务...
cd ..\..\backend
start "生物问答系统后端" python app.py

echo 🚀 启动前端服务...
cd ..\frontend\vue
start "生物问答系统前端" npm run dev

echo ✅ 系统启动完成！
echo 📱 前端地址：http://localhost:5173
echo 🔧 后端地址：http://localhost:5000
echo.
echo 服务已在后台启动，请访问上述地址使用系统
pause 