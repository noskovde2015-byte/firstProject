import api from './api';

export const authAPI = {
  login: (email, password) =>
    api.post('/login', { email, password }),

  register: (userData) =>
    api.post('/register', userData),

  logout: () =>
    api.post('/logout'),

  getProfile: () =>
    api.get('/profile'),
};