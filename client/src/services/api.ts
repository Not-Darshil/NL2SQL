import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: (formData: FormData) => api.post('/auth/login', formData),
  register: (data: any) => api.post('/auth/register', data),
};

export const chatApi = {
  sendMessage: (message: string) => api.post('/chat/', { message }),
};

export default api;
