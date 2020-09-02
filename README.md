# Sudoku solver using Computer Vision and Backtracking

## sudoku_solver
Execution steps : 
```python3
from sudoku_solver import main
main('0000.png')
```

The directory `temp` will be created as a result.

## backtracking

Uses backtracking to generate solved sudoku board from the input board

**TASKS :**

1. Digit recognizer - with weights saved in a file (can be downloaded from net itself)

Our system should load the stored weights and make predictions.

2. Create `main.py` which first calls `sudoku_solver`, then `digit_recognizer` and finally passes the digits recognized stored in 9x9 array to the `backtracking` code

## REFERENCES 

[Python solution in leetcode](https://leetcode.com/problems/sudoku-solver/discuss/15959/Accepted-Python-solution)
