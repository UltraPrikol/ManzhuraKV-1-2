import { useState } from 'react';

/* =========================
   ЗАДАНИЕ 1
   Обработка массива пользователей
========================= */

const processUsers = (users) => {
    const total = users.length;

    const averageAge = total === 0
        ? 0
        : users.reduce((sum, u) => sum + u.age, 0) / total;

    const usersByCity = users.reduce((acc, u) => {
        acc[u.city] = (acc[u.city] || 0) + 1;
        return acc;
    }, {});

    const activeEmails = users
        .filter(u => u.active)
        .map(u => u.email);

    return {
        averageAge,
        usersByCity,
        activeEmails
    };
};


/* =========================
   ЗАДАНИЕ 2
   Кастомный хук useForm
========================= */

const useForm = (initialValues) => {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});

    const validate = () => {
        const newErrors = {};
        Object.keys(values).forEach(key => {
            if (!values[key]) {
                newErrors[key] = 'Обязательное поле';
            }
        });
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setValues(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (callback) => (e) => {
        e.preventDefault();
        if (validate()) {
            callback(values);
        }
    };

    return {
        values,
        errors,
        handleChange,
        handleSubmit
    };
};


/* =========================
   ЗАДАНИЕ 3
   Функция debounce
========================= */

const debounce = (func, delay) => {
    let timeout;

    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func(...args);
        }, delay);
    };
};


/* =========================
   DEMO
========================= */

const users = [
    { name: 'John', age: 25, city: 'New York', active: true, email: 'john@example.com' },
    { name: 'Jane', age: 30, city: 'Boston', active: false, email: 'jane@example.com' },
    { name: 'Mike', age: 28, city: 'New York', active: true, email: 'mike@example.com' }
];

console.log('Processed users:', processUsers(users));

const debouncedLog = debounce((msg) => {
    console.log('Debounced:', msg);
}, 500);

debouncedLog('Hello');
debouncedLog('Hello again');
