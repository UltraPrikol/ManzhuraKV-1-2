// Исходные данные
const user = {
    id: 1,
    name: 'John Doe',
    address: {
        city: 'New York',
        street: '123 Main St',
        coordinates: {
            lat: 40.7128,
            lng: -74.0060
        }
    },
    preferences: {
        theme: 'dark',
        notifications: true
    }
};

const cart = [
    { id: 1, name: 'Product A', quantity: 2 },
    { id: 2, name: 'Product B', quantity: 1 }
];

// Иммутабельные обновления с spread оператором
const updatedUser = {
    ...user,
    name: 'Jane Doe',
    preferences: {
        ...user.preferences,
        theme: 'light'
    }
};

console.log('Original user:', user);
console.log('Updated user:', updatedUser);

// Иммутабельное добавление в массив
const newCartItem = { id: 3, name: 'Product C', quantity: 1 };
const updatedCart = [...cart, newCartItem];
console.log('Updated cart:', updatedCart);

// Иммутабельное обновление элемента массива
const updatedCartQuantity = cart.map(item =>
    item.id === 1 ? { ...item, quantity: item.quantity + 1 } : item
);
console.log('Cart with updated quantity:', updatedCartQuantity);

// Иммутабельное удаление из массива
const filteredCart = cart.filter(item => item.id !== 2);
console.log('Cart after removal:', filteredCart);

// Глубокая иммутабельная update функция
const deepUpdate = (obj, path, value) => {
    const [key, ...rest] = path;
    
    if (rest.length === 0) {
        return { ...obj, [key]: value };
    }
    
    return {
        ...obj,
        [key]: deepUpdate(obj[key], rest, value)
    };
};

const userWithNewAddress = deepUpdate(user, ['address', 'city'], 'Boston');
console.log('User with new city:', userWithNewAddress);
