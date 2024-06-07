import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

// 기본적으로 토큰을 사용하지 않도록 설정
// 필요한 경우 특정 요청에서만 토큰을 추가
export default api;
