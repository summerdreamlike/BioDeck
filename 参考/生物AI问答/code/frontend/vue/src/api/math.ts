import axios from 'axios';

// 从环境变量获取API基础URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
console.log('API Base URL:', API_BASE_URL); // 添加日志

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30秒超时
  headers: {
    'Content-Type': 'application/json'
  }
});

// 添加请求拦截器
api.interceptors.request.use(
  config => {
    console.log('发送请求:', config.url, config.data);
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 添加响应拦截器
api.interceptors.response.use(
  response => {
    console.log('收到响应:', response.data);
    return response;
  },
  error => {
    console.error('响应错误:', error);
    if (error.response) {
      console.error('错误状态码:', error.response.status);
      console.error('错误数据:', error.response.data);
    } else if (error.request) {
      console.error('请求错误:', error.request);
    } else {
      console.error('错误信息:', error.message);
    }
    return Promise.reject(error);
  }
);

export const mathApi = {
  // 发送数学问题
  async sendQuestion(question: string, stream: boolean = false) {
    console.log('发送问题:', question);
    try {
      const response = await api.post('/api/ask', {
        question,
        stream,
        session_id: localStorage.getItem('sessionId') || ''
      });
      return response.data;
    } catch (error) {
      console.error('发送问题失败:', error);
      throw error;
    }
  },

  // 上传图片并解题
  async uploadImage(image: File, question: string = '请解答这个数学问题', stream: boolean = false) {
    console.log('上传图片:', image.name);
    try {
      const formData = new FormData();
      formData.append('image', image);
      formData.append('question', question);
      formData.append('stream', stream.toString());
      formData.append('session_id', localStorage.getItem('sessionId') || '');

      const response = await api.post('/api/upload-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      console.error('上传图片失败:', error);
      throw error;
    }
  },

  // 获取历史记录
  async getHistory(sessionId: string) {
    console.log('获取历史记录:', sessionId);
    try {
      const response = await api.get('/api/history', {
        params: { session_id: sessionId }
      });
      return response.data;
    } catch (error) {
      console.error('获取历史记录失败:', error);
      // 如果获取历史记录失败，返回空历史
      return { history: [] };
    }
  },

  // 清除历史记录
  async clearHistory() {
    try {
      const response = await api.post('/api/clear-history', {
        session_id: localStorage.getItem('sessionId') || ''
      });
      return response.data;
    } catch (error) {
      console.error('清除历史记录失败:', error);
      throw error;
    }
  }
}; 