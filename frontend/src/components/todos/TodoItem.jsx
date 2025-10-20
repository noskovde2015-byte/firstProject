import React from 'react';

const TodoItem = ({ todo, onDelete }) => {
  const getPriorityLabel = (priority) => {
    const labels = {
      low: 'Низкий',
      medium: 'Средний',
      high: 'Высокий'
    };
    return labels[priority] || priority;
  };

  const getPriorityClass = (priority) => {
    return `priority-badge priority-${priority}`;
  };

  return (
    <div className={`todo-item ${!todo.is_active ? 'completed' : ''}`}>
      <div className="todo-content">
        <div className="todo-header">
          <span className="todo-title">{todo.title}</span>
          <button
            onClick={() => onDelete(todo.id)}
            className="delete-button"
            title="Удалить"
          >
            ×
          </button>
        </div>

        <div className="todo-meta">
          <span className={getPriorityClass(todo.priority)}>
            {getPriorityLabel(todo.priority)}
          </span>
          <span className="category-badge">
            {todo.category}
          </span>
          {todo.created_at && (
            <span className="date-badge">
              {new Date(todo.created_at).toLocaleDateString()}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default TodoItem;