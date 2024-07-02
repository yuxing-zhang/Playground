qs :: (Ord a) => [a] -> [a]
qs [] = []
qs (x:xs) = qs [i | i <- xs, i < x] ++ [i | i <- xs, i == x] ++ [x] ++
            qs [i | i <- xs, i > x]

main :: IO ()
main = print (qs [1, 3, 2, 0])
