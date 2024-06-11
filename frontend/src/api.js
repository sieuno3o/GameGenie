import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response && error.response.status === 401) {
      const originalRequest = error.config;
      const refreshToken = localStorage.getItem('refresh');
      if (refreshToken && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
          const response = await axios.post('http://localhost:8000/api/accounts/refresh/', { refresh: refreshToken });
          localStorage.setItem('access', response.data.access);
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
          return api(originalRequest);
        } catch (refreshError) {
          console.error('Token refresh failed:', refreshError);
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
          localStorage.removeItem('nickname');
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;