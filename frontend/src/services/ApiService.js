import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

class ApiService {
  constructor() {
    this.tokenKey = 'authToken';
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000,
      withCredentials: false,
    });
    this.#setupInterceptors();
  }

  async login(email, password) {
    const response = await this.api.post('/api/v1/auth/login', {
      email,
      password,
    });

    const data = response.data;

    if (data.access_token) {
      this.#setToken(data.access_token);
    }

    return data;
  }

  async logout() {
    this.#removeToken();
  }

  isAuthenticated() {
    const token = this.#getToken();

    return !!token;
  }

  async getEmployeeTasks() {
    const response = await this.api.get('/api/v1/employee/tasks');

    return response.data;
  }

  async startTimeLog(projectId, taskId, description = '', systemInfo = {}) {
    const payload = {
      type: 'manual',
      projectId: projectId,
      taskId: taskId,
      timezoneOffset: systemInfo.timezoneOffset || 0,
      user: systemInfo.user || 'Unknown',
      note: description || null,
      operatingSystem: systemInfo.os || '',
      osVersion: systemInfo.osVersion || '',
      computer: systemInfo.computer || '',
      domain: systemInfo.domain || '',
      hwid: systemInfo.hwid || '',
      overtime: false,
      shiftId: null,
    };
    const response = await this.api.post('/api/v1/time-log/start', payload);

    return response.data;
  }

  async updateTimeLog(timeLogId) {
    const response = await this.api.put(
      `/api/v1/time-log/${timeLogId}/update`,
    );

    return response.data;
  }

  #setToken(token) {
    try {
      if (!token) {
        localStorage.removeItem(this.tokenKey);

        return;
      }

      localStorage.setItem(this.tokenKey, token);
    } catch (error) {
      console.error('Error setting token in localStorage:', error);
    }
  }

  #getToken() {
    try {
      const token = localStorage.getItem(this.tokenKey);

      return token;
    } catch (error) {
      console.error('Error getting token from localStorage:', error);

      return null;
    }
  }

  #removeToken() {
    try {
      localStorage.removeItem(this.tokenKey);
    } catch (error) {
      console.error('Error removing token from localStorage:', error);
    }
  }

  #setupInterceptors() {
    this.api.interceptors.request.use(
      (config) => {
        const token = this.#getToken();

        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }

        config.headers['Accept'] = 'application/json';

        return config;
      },
      (error) => {
        return Promise.reject(error);
      },
    );
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.#removeToken();
        }

        return Promise.reject(error);
      },
    );
  }
}
export default new ApiService();
