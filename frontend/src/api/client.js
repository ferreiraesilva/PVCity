import axios from 'axios';

export const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 10000, // 10 segundos para persistência operacional resiliente
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Tratamento global de erros pode ir aqui
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);
