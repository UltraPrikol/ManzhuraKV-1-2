-- main.hs
module Main where

-- Импорты других модулей
import Basics
import Recursion
import Patterns
import HigherOrder
import Types
import Practice

main :: IO ()
main = do
    putStrLn "=== Демонстрация работы функций ==="
    
    -- Базовые функции
    print $ square 5
    print $ grade 85
    
    -- Рекурсия
    print $ factorial 5
    print $ sumList [1, 2, 3, 4, 5]
    
    -- Pattern matching
    print $ addVectors (1, 2) (3, 4)
    
    -- Функции высшего порядка
    print $ map' square [1, 2, 3, 4]
    print $ filter' even [1, 2, 3, 4, 5, 6]
    
    -- Алгебраические типы
    print $ distance (Point 0 0) (Point 3 4)
    print $ isWeekend Saturday
    
    --функция, которая вычисляет количество четных чисел в списке
    putStrLn "\n--- Функции высшего порядка (новые) ---"
    putStr "countEven [1, 2, 3, 4, 5, 6]: "
    print $ countEven [1, 2, 3, 4, 5, 6] 
    
    --функция, которая возвращает список квадратов только положительных чисел
    putStr "positiveSquares [1, -2, 3, -4, 5]: "
    print $ positiveSquares [1, -2, 3, -4, 5]
    
    --алгоритм пузырьковой сортировки
    putStr "bubbleSort [5, 1, 4, 2, 8]: "
    print $ bubbleSort [5, 1, 4, 2, 8]
