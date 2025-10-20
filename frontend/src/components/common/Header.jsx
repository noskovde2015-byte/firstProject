import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">
          📝 My ToDo List
        </h1>
        {user && (
          <div className="header-user">
            <span className="user-greeting">
              Привет, {user.name || user.username}!
            </span>
            <button
              onClick={logout}
              className="logout-btn"
            >
              Выйти
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;