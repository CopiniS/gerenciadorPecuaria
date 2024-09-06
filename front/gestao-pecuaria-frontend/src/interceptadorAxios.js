import axios from 'axios';
import router from '@/router';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/', 
});

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');    
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

let isRefreshing = false;
let refreshSubscribers = [];

function onRefreshed(token) {
  refreshSubscribers.map(callback => callback(token));
}

function addRefreshSubscriber(callback) {
  refreshSubscribers.push(callback);
}

api.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          addRefreshSubscriber((token) => {
            originalRequest.headers['Authorization'] = `Bearer ${token}`;
            resolve(api(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem('refresh_token');
      try {
        const response = await axios.post('http://127.0.0.1:8000/token/refresh/', {
          refresh: refreshToken,
        });

        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        api.defaults.headers['Authorization'] = `Bearer ${response.data.access}`;
        originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
        isRefreshing = false;
        onRefreshed(response.data.access);

        return api(originalRequest);
      } catch (err) {
        isRefreshing = false;
        localStorage.clear();
        alert('Sua sessão foi expirada');
        router.push({ name: 'login' });
      }
    }
    return Promise.reject(error);
  }
);

export default api;
