from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Добавляем тестового пользователя
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password) VALUES (1, 'admin', 'admin@example.com', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password) VALUES (2, 'user', 'user@example.com', 'user123')")
    
    conn.commit()
    conn.close()

API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set. Please set it before running.")

# HTML шаблон для главной страницы
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>User Management</title>
</head>
<body>
    <h1>User Management System</h1>
    <form action="/user" method="GET">
        <label>User ID:</label>
        <input type="text" name="id">
        <button type="submit">Get User</button>
    </form>
    
    <form action="/search" method="GET">
        <label>Search by username:</label>
        <input type="text" name="username">
        <button type="submit">Search</button>
    </form>
    
    <div id="result">
        {content}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE.format(content="<p>Enter user ID or search by username</p>"))

@app.route('/user')
def get_user():
    """Получение пользователя по ID — SQL-инъекция исправлена"""
    user_id = request.args.get('id')
    
    if not user_id:
        return jsonify({"error": "Missing id parameter"}), 400
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # БЕЗОПАСНО: Используем параметризованный запрос (?)
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"id": user[0], "username": user[1], "email": user[2]})
    return jsonify({"error": "User not found"}), 404

@app.route('/search')
def search_users():
    """Поиск пользователей по имени — содержит SQL-инъекцию"""
    username = request.args.get('username', '')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # ❌ УЯЗВИМЫЙ КОД: прямая конкатенация строк
    # TODO: Исправить SQL-инъекцию
    query = f"SELECT * FROM users WHERE username LIKE '%{username}%'"
    cursor.execute(query)
    
    users = cursor.fetchall()
    conn.close()
    
    result = [{"id": u[0], "username": u[1], "email": u[2]} for u in users]
    return jsonify(result)

@app.route('/api/data')
def get_data():
    """Эндпоинт с секретным ключом в коде"""
    # TODO: Убрать hardcoded ключ, использовать переменную окружения
    return jsonify({"api_key": API_KEY, "message": "This is sensitive data"})

@app.route('/execute')
def execute_command():
    """Эндпоинт для выполнения системных команд — Command Injection исправлен"""
    cmd = request.args.get('cmd', 'echo Hello')
    
    # БЕЗОПАСНО: Используем Allow-list (белый список)
    ALLOWED_COMMANDS = ['echo', 'date', 'whoami']
    
    # Разбиваем команду на список аргументов
    cmd_parts = cmd.split()
    if not cmd_parts:
        return jsonify({"error": "Empty command"}), 400
        
    base_cmd = cmd_parts[0]
    
    # Проверяем, разрешена ли базовая команда
    if base_cmd not in ALLOWED_COMMANDS:
        return jsonify({"error": f"Command '{base_cmd}' is not allowed"}), 403
    
    import subprocess
    try:
        # БЕЗОПАСНО: Выполняем список аргументов без shell=True
        result = subprocess.check_output(cmd_parts)
        return jsonify({"output": result.decode()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)