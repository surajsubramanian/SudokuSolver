import sys
from sudoku_solver import sudoku_solver
from digit_recognizer import digit_recognizer
from backtracking import backtracking

def main(img_path):
    sudoku_solver('0000.png')
    board = digit_recognizer()
    backtracking(board)

if __name__ == '__main__':
    img_path = sys.argv[1]
    main(img_path)
