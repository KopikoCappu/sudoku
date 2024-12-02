import random
import math


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells

        # Initialize the board with zeros
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        if not self.valid_in_row(row, num):
            return False

        if not self.valid_in_col(col, num):
            return False

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        if not self.valid_in_box(box_row, box_col, num):
            return False

        return True

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)

        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                self.board[row][col] = nums.pop()

    def fill_diagonal(self):
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if col >= self.row_length:
            row += 1
            col = 0

        if row >= self.row_length:
            return True

        if self.board[row][col] != 0:
            return self.fill_remaining(row, col + 1)

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num

                if self.fill_remaining(row, col + 1):
                    return True

                self.board[row][col] = 0

        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 3)

    def remove_cells(self):
        cells_to_remove = self.removed_cells
        while cells_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1

    def generate_sudoku(self):
        self.fill_values()

        # Create a copy of the solution
        solution = [row.copy() for row in self.board]

        # Remove cells
        self.remove_cells()

        return self.board, solution


def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    return generator.generate_sudoku()