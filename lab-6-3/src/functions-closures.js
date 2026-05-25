// Стрелочные функции
const square = x => x * x;
const add = (a, b) => a + b;
const greet = name => `Hello, ${name}!`;

console.log('Square of 5:', square(5));
console.log('Add 3 and 4:', add(3, 4));
console.log(greet('John'));

// Замыкания
const createCounter = () => {
    let count = 0;
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
};

const counter = createCounter();
console.log('Counter:', counter.increment()); // 1
console.log('Counter:', counter.increment()); // 2
console.log('Counter:', counter.getCount());  // 2

// Каррирование
const multiply = a => b => a * b;
const double = multiply(2);
const triple = multiply(3);

console.log('Double 5:', double(5));   // 10
console.log('Triple 5:', triple(5));   // 15

// Функциональная композиция
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const add5 = x => x + 5;
const multiply3 = x => x * 3;
const subtract10 = x => x - 10;

const composed = compose(subtract10, multiply3, add5);
const piped = pipe(add5, multiply3, subtract10);

console.log('Composed result:', composed(5)); // (5 + 5) * 3 - 10 = 20
console.log('Piped result:', piped(5));       // (5 + 5) * 3 - 10 = 20
