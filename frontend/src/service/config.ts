import axios from 'axios';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: import.meta.env.PROD ? '/api/finance' : 'http://127.0.0.1:8000/api/finance',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config) => {
    // You can add auth tokens here in the future
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    console.log(`[Request] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Any status code within the range of 2xx cause this function to trigger
    return response;
  },
  (error) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    console.error('[API Error]', error.response?.data || error.message);
    
    // You can handle global errors here (e.g., 401 Unauthorized)
    if (error.response?.status === 401) {
      // Handle logout or redirect to login
      console.warn('Unauthorized access');
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
