import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './AuthForm.css';

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    age: 18
  });
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isLogin) {
        await login(formData.email, formData.password);
      } else {
        await register(formData);
      }
    } catch (error) {
      alert(error.response?.data?.detail || 'Произошла ошибка');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <h1 className="auth-title">
            {isLogin ? 'Добро пожаловать' : 'Создать аккаунт'}
          </h1>

          <p className="auth-subtitle">
            {isLogin ? 'Войдите в свой аккаунт' : 'Присоединяйтесь к нашему сообществу'}
          </p>

          <form onSubmit={handleSubmit} className="auth-form">
            {!isLogin && (
              <div className="form-group">
                <label>Полное имя</label>
                <input
                  type="text"
                  name="name"
                  placeholder="Иван Иванов"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="auth-input"
                />
              </div>
            )}

            <div className="form-group">
              <label>Email адрес</label>
              <input
                type="email"
                name="email"
                placeholder="noskov@gmail.com"
                value={formData.email}
                onChange={handleChange}
                required
                className="auth-input"
              />
            </div>

            <div className="form-group">
              <label>Пароль</label>
              <input
                type="password"
                name="password"
                placeholder="••••••"
                value={formData.password}
                onChange={handleChange}
                required
                className="auth-input"
              />
            </div>

            {!isLogin && (
              <div className="form-group">
                <label>Возраст</label>
                <input
                  type="number"
                  name="age"
                  placeholder="18+"
                  value={formData.age}
                  onChange={handleChange}
                  min="1"
                  max="120"
                  className="auth-input"
                />
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="auth-submit-btn"
            >
              {loading ? 'Загрузка...' : (isLogin ? 'Войти в аккаунт' : 'Создать аккаунт')}
            </button>
          </form>

          <p className="auth-switch">
            {isLogin ? 'Еще нет аккаунта? ' : 'Уже есть аккаунт? '}
            <span
              onClick={() => setIsLogin(!isLogin)}
              className="auth-link"
            >
              {isLogin ? 'Зарегистрироваться' : 'Войти'}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;