import api from './api';

export const usersAPI = {
  getUsers: () =>
    api.get('/user'),

  makeAdmin: (userId) =>
    api.post('/admin', { user_id: userId }),

  deleteUser: (userId) =>
    api.delete(`/user/delete?user_id=${userId}`),
};