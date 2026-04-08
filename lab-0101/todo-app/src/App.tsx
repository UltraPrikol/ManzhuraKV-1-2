import React, { useState } from 'react';

// 1. Определение типа задачи
interface Task {
  id: number;
  text: string;
  completed: boolean;
}

function App() {
  // Состояние для списка задач
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: 'Изучить React', completed: true },
    { id: 2, text: 'Написать To-Do приложение', completed: false }
  ]);

  // Состояние для текста новой задачи
  const [newTask, setNewTask] = useState('');

  // Функция добавления
  const addTask = () => {
    if (newTask.trim() === '') return;
    const task: Task = {
      id: Date.now(),
      text: newTask,
      completed: false
    };
    setTasks([...tasks, task]);
    setNewTask('');
  };

  // А. Реализация удаления (Задание из лабы)
  const removeTask = (id: number) => {
    // Используем filter: оставляем только те задачи, ID которых НЕ совпадает с удаляемым
    setTasks(tasks.filter(task => task.id !== id));
  };

  // B. Реализация переключения статуса (Задание из лабы)
  const toggleTask = (id: number) => {
    // Используем map: если ID совпал, инвертируем completed, иначе возвращаем как есть
    setTasks(tasks.map(task => 
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  // D. Подсчет статистики
  const completedCount = tasks.filter(t => t.completed).length;

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-xl p-8">
        <h1 className="text-3xl font-extrabold text-center mb-8 text-gray-800">
          📝 Мой Список Задач
        </h1>
        
        {/* Форма ввода */}
        <div className="flex gap-2 mb-8">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addTask()}
            placeholder="Что нужно сделать?"
            className="flex-grow px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition-all"
          />
          <button
            onClick={addTask}
            className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
          >
            Добавить
          </button>
        </div>

        {/* Список задач */}
        <div className="space-y-4">
          {tasks.map(task => (
            <div 
              key={task.id} 
              className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center gap-4">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(task.id)}
                  className="w-5 h-5 cursor-pointer accent-blue-600"
                />
                <span className={`text-lg ${task.completed ? 'line-through text-gray-400' : 'text-gray-700'}`}>
                  {task.text}
                </span>
              </div>
              
              {/* С. Кнопка удаления */}
              <button
                onClick={() => removeTask(task.id)}
                className="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                title="Удалить задачу"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d=" orbit-19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          ))}

          {/* E. Сообщение о пустом списке */}
          {tasks.length === 0 && (
            <div className="text-center py-10">
              <p className="text-gray-400 italic">Список пуст. Время отдыхать! ☕</p>
            </div>
          )}
        </div>

        {/* Статистика */}
        <div className="mt-8 pt-6 border-t border-gray-100 flex justify-between text-sm font-medium text-gray-500">
          <span>Всего задач: {tasks.length}</span>
          <span className="text-blue-600">Выполнено: {completedCount}</span>
        </div>
      </div>
    </div>
  );
}

export default App;