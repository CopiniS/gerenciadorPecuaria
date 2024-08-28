import axios from 'axios';

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

api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const { data } = await api.post('/token/refresh/', { token: refreshToken });
          
          localStorage.setItem('access_token', data.access_token);
          api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;
          
          return api(originalRequest);
        } catch (err) {
          // Lidar com erro ao obter novo token
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          alert('Sua sessão foi expirada');
          localStorage.clear();
          this.$router.push('/login');
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
