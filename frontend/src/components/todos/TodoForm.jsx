import React, { useState } from 'react';

const TodoForm = ({ onAddTodo }) => {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState('medium');
  const [category, setCategory] = useState('general');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    onAddTodo({
      title: title.trim(),
      body: title.trim(),
      priority,
      category
    });

    setTitle('');
  };

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <div className="form-row">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Добавить новую задачу..."
          className="todo-input"
        />

        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          className="priority-select"
        >
          <option value="low">Низкий</option>
          <option value="medium">Средний</option>
          <option value="high">Высокий</option>
        </select>

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="category-select"
        >
          <option value="general">Общее</option>
          <option value="work">Работа</option>
          <option value="personal">Личное</option>
          <option value="shopping">Покупки</option>
        </select>

        <button type="submit" className="add-button">
          Добавить
        </button>
      </div>
    </form>
  );
};

export default TodoForm;