import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './ProfilePage.css';

const ProfilePage = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    if (user) {
      setProfile({
        id: user.id,
        name: user.name || 'Не указано',
        email: user.email,
        age: user.age || null,
        post_count: user.post_count || 0,
        avatar_url: user.avatar_url || null,
        created_at: user.created_at || new Date().toISOString()
      });
    }
  }, [user]);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('ru-RU');
  };

  if (!profile) {
    return (
      <div className="profile-page">
        <div className="loading">Загрузка профиля...</div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <h1>Профиль</h1>
      </div>

      <div className="profile-card">
        <div className="profile-avatar">
          {profile.avatar_url ? (
            <img src={profile.avatar_url} alt="Аватар" />
          ) : (
            <div className="avatar-placeholder">
              {profile.name?.charAt(0)?.toUpperCase() || 'U'}
            </div>
          )}
        </div>

        <div className="profile-info">
          <div className="info-item">
            <strong>Имя:</strong>
            <span>{profile.name}</span>
          </div>

          <div className="info-item">
            <strong>Email:</strong>
            <span>{profile.email}</span>
          </div>

          <div className="info-item">
            <strong>Возраст:</strong>
            <span>{profile.age ? `${profile.age} лет` : 'Не указан'}</span>
          </div>

          <div className="info-item">
            <strong>Дата регистрации:</strong>
            <span>{formatDate(profile.created_at)}</span>
          </div>

          <div className="info-item">
            <strong>Количество постов:</strong>
            <span>{profile.post_count}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;