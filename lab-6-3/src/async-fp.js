// Промисы и async/await в функциональном стиле
const fetchData = (url) => {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
};

// Функциональная обработка асинхронных операций
const processUserData = async (userId) => {
    try {
        const user = await fetchData(`/api/users/${userId}`);
        const posts = await fetchData(`/api/users/${userId}/posts`);
        
        return {
            ...user,
            posts: posts.map(post => ({
                ...post,
                excerpt: post.content.substring(0, 100) + '...'
            }))
        };
    } catch (error) {
        console.error('Error processing user data:', error);
        throw error;
    }
};

// Композиция асинхронных функций
const asyncPipe = (...fns) => x => fns.reduce(async (acc, fn) => fn(await acc), x);

const validateInput = async (data) => {
    if (!data.email) throw new Error('Email is required');
    return data;
};

const sanitizeData = async (data) => ({
    ...data,
    email: data.email.toLowerCase().trim()
});

const saveToDatabase = async (data) => {
    // Симуляция сохранения в базу данных
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({ ...data, id: Math.random(), createdAt: new Date() });
        }, 1000);
    });
};

const userRegistration = asyncPipe(
    validateInput,
    sanitizeData,
    saveToDatabase
);

// Демонстрация
const userData = { email: '  JOHN@EXAMPLE.COM  ', name: 'John' };
userRegistration(userData).then(result => {
    console.log('Registered user:', result);
});
