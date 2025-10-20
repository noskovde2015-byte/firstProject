// src/services/todos.js
import api from './api';

export const todosAPI = {
  getTodos: () =>
    api.get('/post'),

  createTodo: (todoData) =>
    api.post('/post', todoData),

  updateTodo: (todoId, todoData) =>
    api.patch(`/post?post_id=${todoId}`, todoData),

  deleteTodo: (todoId) =>
    api.delete(`/post?post_id=${todoId}`),

  getActiveTodos: () =>
    api.get('/post/active_post'),

  getTodosByCategory: (category) =>
    api.get(`/post/by_categories?categories=${category}`),
};