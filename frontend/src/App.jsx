import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Header from './components/common/Header';
import AuthForm from './components/auth/AuthForm';
import Dashboard from './pages/Dashboard';
import PostsPage from './pages/PostsPage';
import AdminPage from './pages/AdminPage';
import ProfilePage from './pages/ProfilePage';
import Loading from './components/common/Loading';
import './App.css';

const AppContent = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return <Loading />;
  }

  return (
    <Router>
      <div className="app">
        {user && <Header />}
        <main className="main-content">
          <Routes>
            {!user ? (
              <>
                <Route path="/" element={<AuthForm />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </>
            ) : (
              <>
                <Route path="/" element={<Dashboard />} />
                <Route path="/posts" element={<PostsPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/admin" element={<AdminPage />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </>
            )}
          </Routes>
        </main>
      </div>
    </Router>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;