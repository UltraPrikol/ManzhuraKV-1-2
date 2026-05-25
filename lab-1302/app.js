const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const axios = require('axios');
const crypto = require('crypto');

const app = express();
const port = 3000;

// БЕЗОПАСНО: Добавляем CSP (Content Security Policy) для защиты от XSS
app.use((req, res, next) => {
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    );
    next();
});

app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const db = new sqlite3.Database('./comments.db');

db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
    
    db.run(`INSERT OR IGNORE INTO comments (id, username, comment) VALUES 
        (1, 'admin', 'Добро пожаловать на сайт!'),
        (2, 'user1', 'Отличный ресурс'),
        (3, 'user2', 'Очень полезная информация')`);
});

// БЕЗОПАСНО: Читаем ключ из окружения
const API_KEY = process.env.API_KEY;

// Функция санитизации HTML
const sanitizeHtml = (input) => {
    if (!input) return '';
    return input.toString()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/\//g, '&#x2F;');
};

app.get('/', (req, res) => {
    db.all(`SELECT * FROM comments ORDER BY created_at DESC`, (err, comments) => {
        if (err) return res.status(500).send('Database error');
        res.render('index', { comments: comments, error: null });
    });
});

app.post('/comment', (req, res) => {
    let { username, comment } = req.body;
    
    // БЕЗОПАСНО: Санитизация данных перед сохранением
    username = sanitizeHtml(username || 'Anonymous');
    comment = sanitizeHtml(comment || '');
    
    // БЕЗОПАСНО: Параметризованный запрос
    db.run(`INSERT INTO comments (username, comment) VALUES (?, ?)`, 
        [username, comment], 
        (err) => {
            if (err) return res.status(500).send('Error saving comment');
            res.redirect('/');
        });
});

app.get('/api/comments', (req, res) => {
    const sortParam = req.query.sort || 'created_at DESC';
    
    // БЕЗОПАСНО: Allow-list для сортировки
    const allowedSort = ['created_at DESC', 'created_at ASC', 'username ASC', 'username DESC'];
    if (!allowedSort.includes(sortParam)) {
        return res.status(400).json({ error: 'Invalid sort parameter' });
    }
    
    db.all(`SELECT * FROM comments ORDER BY ${sortParam}`, (err, comments) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        res.json(comments);
    });
});

app.get('/api/search', (req, res) => {
    const search = req.query.q || '';
    
    // БЕЗОПАСНО: Параметризованный запрос для LIKE
    db.all(`SELECT * FROM comments WHERE comment LIKE ?`, [`%${search}%`], (err, comments) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        res.json(comments);
    });
});

app.get('/api/config', (req, res) => {
    if (!API_KEY) return res.status(500).json({ error: 'API_KEY is not set' });
    res.json({ api_key: API_KEY, environment: 'development', debug: true });
});

app.get('/api/external', async (req, res) => {
    const url = req.query.url || 'https://api.github.com/';
    
    // БЕЗОПАСНО: Базовая проверка SSRF (разрешаем только определенные домены)
    try {
        const parsedUrl = new URL(url);
        if (parsedUrl.hostname !== 'api.github.com' && parsedUrl.hostname !== 'jsonplaceholder.typicode.com') {
            return res.status(403).json({ error: 'Access to this domain is forbidden' });
        }
        const response = await axios.get(url);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'External request failed or invalid URL' });
    }
});

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});