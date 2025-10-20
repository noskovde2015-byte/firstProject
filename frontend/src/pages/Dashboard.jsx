import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { todosAPI } from '../services/todos';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [postsCount, setPostsCount] = useState(0);

  useEffect(() => {
    fetchPostsCount();
  }, []);

  const fetchPostsCount = async () => {
    try {
      const response = await todosAPI.getTodos();
      setPostsCount(response.data.length);
    } catch (error) {
      console.error('Failed to fetch posts count:', error);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="welcome-section">
        <h1>Добро пожаловать!</h1>
        <p>Вы успешно вошли в систему ToDoApp</p>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <div className="feature-header">
            <h2>Мои посты</h2>
            <span className="posts-count">{postsCount}</span>
          </div>
          <p>Перейти к управлению постами</p>
          <div className="feature-actions">
            <Link to="/posts" className="feature-button">
              Перейти к моим постам →
            </Link>
          </div>
        </div>

        <div className="feature-card">
          <div className="feature-header">
            <h2>Профиль</h2>
          </div>
          <p>Управление аккаунтом</p>
          <div className="feature-actions">
            <Link to="/profile" className="feature-button">
              Управление профилем →
            </Link>
          </div>
        </div>

        {user?.role === 'admin' && (
          <div className="feature-card">
            <div className="feature-header">
              <h2>Админ панель</h2>
            </div>
            <p>Управление пользователями</p>
            <div className="feature-actions">
              <Link to="/admin" className="feature-button">
                Панель администратора →
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;