import React, { useState, useEffect } from 'react';
import { todosAPI } from '../services/todos';
import './PostsPage.css';

const PostsPage = () => {
  const [posts, setPosts] = useState([]);
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingPost, setEditingPost] = useState(null);
  const [postForm, setPostForm] = useState({
    title: '',
    body: '',
    priority: 'medium',
    category: 'general',
    is_active: true
  });

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await todosAPI.getTodos();
      setPosts(response.data);
    } catch (error) {
      console.error('Failed to fetch posts:', error);
    }
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    try {
      await todosAPI.createTodo(postForm);
      setShowCreateForm(false);
      resetForm();
      fetchPosts();
    } catch (error) {
      console.error('Failed to create post:', error);
      alert('Ошибка при создании поста');
    }
  };

  const handleEditPost = (post) => {
    setEditingPost(post);
    setPostForm({
      title: post.title,
      body: post.body,
      priority: post.priority,
      category: post.category,
      is_active: post.is_active
    });
    setShowCreateForm(true);
  };

  const handleUpdatePost = async (e) => {
    e.preventDefault();
    try {
      await todosAPI.updateTodo(editingPost.id, postForm);
      setShowCreateForm(false);
      setEditingPost(null);
      resetForm();
      fetchPosts();
    } catch (error) {
      console.error('Failed to update post:', error);
      alert('Ошибка при обновлении поста');
    }
  };

  const handleDelete = async (postId) => {
    if (window.confirm('Вы уверены, что хотите удалить этот пост?')) {
      try {
        await todosAPI.deleteTodo(postId);
        fetchPosts();
      } catch (error) {
        console.error('Failed to delete post:', error);
        alert('Ошибка при удалении поста');
      }
    }
  };

  const resetForm = () => {
    setPostForm({
      title: '',
      body: '',
      priority: 'medium',
      category: 'general',
      is_active: true
    });
    setEditingPost(null);
  };

  const handleCancel = () => {
    setShowCreateForm(false);
    resetForm();
  };

  const filteredPosts = posts.filter(post => {
    const matchesSearch = post.title.toLowerCase().includes(search.toLowerCase()) ||
                         post.body.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === 'all' ||
                         (filter === 'active' && post.is_active);

    return matchesSearch && matchesFilter;
  });

  return (
    <div className="posts-page">
      <div className="page-header">
        <h1>Мои посты</h1>
      </div>

      <div className="controls-section">
        <div className="search-section">
          <input
            type="text"
            placeholder="Поиск по категории..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
          <button className="search-btn">Найти</button>
        </div>

        <div className="filter-section">
          <button
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            Все посты
          </button>
          <button
            className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
            onClick={() => setFilter('active')}
          >
            Активные
          </button>
          <button
            className="create-post-btn"
            onClick={() => {
              resetForm();
              setShowCreateForm(true);
            }}
          >
            + Создать пост
          </button>
        </div>
      </div>

      {showCreateForm && (
        <div className="create-modal">
          <div className="modal-content">
            <h3>{editingPost ? 'Редактировать пост' : 'Создать новый пост'}</h3>
            <form onSubmit={editingPost ? handleUpdatePost : handleCreatePost}>
              <input
                type="text"
                placeholder="Заголовок поста"
                value={postForm.title}
                onChange={(e) => setPostForm({...postForm, title: e.target.value})}
                className="modal-input"
                required
              />
              <textarea
                placeholder="Текст поста"
                value={postForm.body}
                onChange={(e) => setPostForm({...postForm, body: e.target.value})}
                className="modal-textarea"
                required
              />

              <div className="form-row">
                <div className="form-group">
                  <label>Категория</label>
                  <input
                    type="text"
                    placeholder="Введите категорию"
                    value={postForm.category}
                    onChange={(e) => setPostForm({...postForm, category: e.target.value})}
                    className="modal-input"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Приоритет</label>
                  <select
                    value={postForm.priority}
                    onChange={(e) => setPostForm({...postForm, priority: e.target.value})}
                    className="modal-select"
                  >
                    <option value="low">Низкий</option>
                    <option value="medium">Средний</option>
                    <option value="high">Высокий</option>
                  </select>
                </div>
              </div>

              <div className="checkbox-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={postForm.is_active}
                    onChange={(e) => setPostForm({...postForm, is_active: e.target.checked})}
                    className="checkbox-input"
                  />
                  <span className="checkmark"></span>
                  Активный пост
                </label>
              </div>

              <div className="modal-actions">
                <button type="submit" className="modal-submit">
                  {editingPost ? 'Сохранить изменения' : 'Создать'}
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="modal-cancel"
                >
                  Отмена
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="posts-container">
        {filteredPosts.map(post => (
          <div key={post.id} className="post-item">
            <div className="post-main">
              <h3 className="post-title">{post.title}</h3>
              <p className="post-content">{post.body}</p>
            </div>

            <div className="post-details">
              <span className="post-category">{post.category}</span>
              <span className={`priority priority-${post.priority}`}>
                {post.priority === 'low' ? 'Низкий' :
                 post.priority === 'medium' ? 'Средний' : 'Высокий'}
              </span>
              {!post.is_active && <span className="inactive-label">Неактивный</span>}
            </div>

            <div className="post-actions">
              <button
                className="action-btn edit"
                onClick={() => handleEditPost(post)}
              >
                Редактировать
              </button>
              <button
                className="action-btn delete"
                onClick={() => handleDelete(post.id)}
              >
                Удалить
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredPosts.length === 0 && !showCreateForm && (
        <div className="no-posts">
          <p>Пока нет постов</p>
        </div>
      )}
    </div>
  );
};

export default PostsPage;