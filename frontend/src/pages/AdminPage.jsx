import React, { useState, useEffect } from 'react';
import { usersAPI } from '../services/users';
import './AdminPage.css';

const AdminPage = () => {
  const [users, setUsers] = useState([]);
  const [activeTab, setActiveTab] = useState('users');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await usersAPI.getUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  };

  const makeAdmin = async (userId) => {
    try {
      await usersAPI.makeAdmin(userId);
      fetchUsers();
    } catch (error) {
      console.error('Failed to make admin:', error);
    }
  };

  const deleteUser = async (userId) => {
    if (window.confirm('Вы уверены, что хотите удалить этого пользователя?')) {
      try {
        await usersAPI.deleteUser(userId);
        fetchUsers();
      } catch (error) {
        console.error('Failed to delete user:', error);
      }
    }
  };

  return (
    <div className="admin-page">
      <h1>Панель администратора</h1>

      <div className="admin-tabs">
        <button
          className={activeTab === 'users' ? 'tab-btn active' : 'tab-btn'}
          onClick={() => setActiveTab('users')}
        >
          Пользователи
        </button>
        <button
          className={activeTab === 'posts' ? 'tab-btn active' : 'tab-btn'}
          onClick={() => setActiveTab('posts')}
        >
          Все посты
        </button>
      </div>

      {activeTab === 'users' && (
        <div className="users-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>EMAIL</th>
                <th>РОЛЬ</th>
                <th>ДЕЙСТВИЯ</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.email}</td>
                  <td>{user.role?.name || 'User'}</td>
                  <td className="actions-cell">
                    <button
                      className="make-admin-btn"
                      onClick={() => makeAdmin(user.id)}
                    >
                      Сделать админом
                    </button>
                    <button
                      className="delete-user-btn"
                      onClick={() => deleteUser(user.id)}
                    >
                      Удалить
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdminPage;