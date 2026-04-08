const express = require('express'); // Оставить только один раз вверху!
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const tasksRouter = require('./routes/tasks');
const { notFoundHandler, errorHandler } = require('./middleware/errorHandler');

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());

// Логирование
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  next();
});

// Корневые маршруты
app.get('/', (req, res) => {
  res.json({ name: 'Task Manager API', version: '1.0.0', docs: '/api/tasks' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Роуты API
app.use('/api/tasks', tasksRouter);

// Обработка ошибок
app.use(notFoundHandler);
app.use(errorHandler);

module.exports = app;