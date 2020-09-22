# Sudoku solver using Computer Vision and Backtracking

## sudoku_solver
Execution steps : 
```python3
python main.py
```

## WORKING

`sudoku_solver` splits given image into 81 images and stores them in the `temp` directory. Each of these images represent one box in the 9x9 grid

`digit_recognizer` recognizes each of the 81 images and stores them in an array passing it to the `backtracking` function which solves the sudoku problem.


## REFERENCES 

[Python solution to solve sudoku using backtracking in leetcode](https://leetcode.com/problems/sudoku-solver/discuss/15959/Accepted-Python-solution)

[Digit Recognition using OpenCV and pytesseract](https://stackoverflow.com/a/58032585/10077354)
