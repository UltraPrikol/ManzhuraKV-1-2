--1
-- countEven :: [Int] -> Int
countEven :: [Int] -> Int
countEven xs = length (filter even xs)

--2
-- positiveSquares :: [Int] -> [Int]
positiveSquares :: [Int] -> [Int]
positiveSquares xs = map (\x -> x * x) (filter (\x -> x > 0) xs)

--3
-- bubbleSort :: [Int] -> [Int]
bubbleSort :: [Int] -> [Int]
bubbleSort [] = []
bubbleSort xs = 
    let 
        pass [] = []
        pass [x] = [x]
        pass (x:y:zs)
            | x > y     = y : pass (x:zs)
            | otherwise = x : pass (y:zs)
        
        (rest, [lastElem]) = splitAt (length xs - 1) (pass xs)
    in
        if pass xs == xs 
        then xs
        else bubbleSort rest ++ [lastElem]