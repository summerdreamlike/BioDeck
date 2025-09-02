from flask import Flask, jsonify, request, g
from flask_cors import CORS
import sqlite3
import os
import traceback
from datetime import datetime, timedelta
from flask_socketio import SocketIO, emit, join_room, leave_room

# 统一错误处理
import sys
sys.path.append('.')  # 添加在文件顶部
from core.errors import ApiError, ErrorCode
from core.responses import ok_response, error_response
from core.helpers import close_db

# 创建应用实例
app = Flask(__name__)
CORS(app)  # 启用跨域支持
socketio = SocketIO(app, cors_allowed_origins='*')

# JWT 配置
from flask_jwt_extended import JWTManager
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-change-me')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # 缩短访问令牌有效期
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # 刷新令牌有效期30天
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_ERROR_MESSAGE_KEY'] = 'msg'
jwt = JWTManager(app)

# 注册数据库连接关闭函数
app.teardown_appcontext(close_db)

# 全局错误处理中间件
@app.errorhandler(ApiError)
def handle_api_error(error):
    """全局API错误处理器"""
    app.logger.error(f"API Error: {error.message} (Code: {error.code})")
    return error_response(
        message=error.message,
        code=error.code,
        payload=error.payload
    )

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """全局未预期异常处理器"""
    app.logger.error(f"Unexpected Error: {str(error)}")
    app.logger.error(traceback.format_exc())
    return error_response(
        message="服务器内部错误",
        code=ErrorCode.SERVER_ERROR,
        http_status=500
    )

# 注册路由
from api.v1.api import register_routes
register_routes(app)

# SocketIO事件处理
@socketio.on('connect')
def handle_connect():
    app.logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    app.logger.info(f"Client disconnected: {request.sid}")

@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    if room:
        join_room(room)
        app.logger.info(f"Client {request.sid} joined room: {room}")
        emit('room_joined', {'room': room, 'message': '加入房间成功'}, to=request.sid)

@socketio.on('leave')
def handle_leave(data):
    room = data.get('room')
    if room:
        leave_room(room)
        app.logger.info(f"Client {request.sid} left room: {room}")

@socketio.on('message')
def handle_message(data):
    room = data.get('room')
    message = data.get('message')
    
    if room and message:
        app.logger.info(f"Message to room {room}: {message}")
        emit('message', {'sender': request.sid, 'message': message}, to=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 