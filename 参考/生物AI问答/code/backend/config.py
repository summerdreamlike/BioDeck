import os

class Config:
    # API密钥配置
    MOONSHOT_API_KEY = os.environ.get('MOONSHOT_API_KEY', 'sk-746pWBxcT0Mk05CURLFiT3k0h9PLdNMT5mmnzEEa23rNOyYq')  # 请将'your-api-key-here'替换为您的实际API密钥
    
    # 服务器配置
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG = True
    
    # 默认模型配置
    DEFAULT_MODEL = 'moonshot-v1-32k'
    # 视觉模型配置
    VISION_MODEL = 'moonshot-v1-8k-vision-preview'
    
    @staticmethod
    def get_api_key():
        """获取API密钥"""
        return Config.MOONSHOT_API_KEY
    
    @staticmethod
    def ensure_temp_dir():
        """确保临时目录存在"""
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        return temp_dir