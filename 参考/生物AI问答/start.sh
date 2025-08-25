#!/bin/bash

echo "🧬 启动高中生物智能问答系统"
echo "================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3，请先安装Python3"
    exit 1
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未找到Node.js，请先安装Node.js"
    exit 1
fi

# 检查API密钥
if [ -z "$MOONSHOT_API_KEY" ]; then
    echo "⚠️  警告：未设置MOONSHOT_API_KEY环境变量"
    echo "请在config.py中设置API密钥或设置环境变量"
fi

echo "📦 安装后端依赖..."
cd code/backend
pip install -r requirements.txt

echo "📦 安装前端依赖..."
cd ../frontend/vue
npm install

echo "🚀 启动后端服务..."
cd ../../backend
python app.py &
BACKEND_PID=$!

echo "🚀 启动前端服务..."
cd ../frontend/vue
npm run dev &
FRONTEND_PID=$!

echo "✅ 系统启动完成！"
echo "📱 前端地址：http://localhost:5173"
echo "🔧 后端地址：http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 