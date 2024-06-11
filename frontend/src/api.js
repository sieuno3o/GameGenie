import axios from 'axios';

const api = axios.create({
  baseURL: 'http://52.79.116.122/api/',  // EC2 인스턴스의 퍼블릭 IP 주소
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

export default api;
