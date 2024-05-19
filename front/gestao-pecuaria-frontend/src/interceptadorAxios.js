import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
});

// Função para criar e retornar um novo interceptor
const createInterceptor = () => {
  return api.interceptors.request.use(
    async (config) => {
      const accessToken = localStorage.getItem('access_token');

      if (accessToken) {
        const expirationTime = localStorage.getItem('access_exp') * 1000;
        const currentTime = new Date().getTime();

        if (expirationTime < currentTime || expirationTime === null) {
          await renovarToken();
          config.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`;
        } else {
          config.headers.Authorization = `Bearer ${accessToken}`;
        }
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
};

async function renovarToken() {
  const refreshToken = localStorage.getItem('refresh_token')
  const response = await axios.post('http://127.0.0.1:8000/token/refresh/', { refresh: refreshToken });
  localStorage.setItem('access_token', response.data.access)
  localStorage.setItem('access_exp', response.data.expires)
}

// Crie o interceptor ao carregar o módulo
createInterceptor();

export default api;
