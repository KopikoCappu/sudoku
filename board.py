import pygame
from cell import Cell


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        # Map difficulty to number of removed cells
        difficulty_map = {'easy': 30, 'medium': 40, 'hard': 50}
        self.removed_cells = difficulty_map[difficulty]

        # Initialize board
        from sudoku_generator import generate_sudoku
        self.board, self.solution = generate_sudoku(9, self.removed_cells)

        # Create cell objects
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                self.cells[row][col] = Cell(self.board[row][col], row, col, screen)

        # Tracking selected cell
        self.selected_cell = None

    def draw(self):
        # Colors
        BLACK = (0, 0, 0)

        # Draw cells
        for row in range(9):
            for col in range(9):
                self.cells[row][col].draw()

        # Draw bold lines to delineate 3x3 boxes
        for i in range(0, 10, 3):
            pygame.draw.line(self.screen, BLACK, (i * 65, 0), (i * 65, 540), 4)
            pygame.draw.line(self.screen, BLACK, (0, i * 65), (540, i * 65), 4)

    def select(self, row, col):
        # Deselect previous cell
        if self.selected_cell:
            self.selected_cell.is_selected = False

        # Select new cell
        self.selected_cell = self.cells[row][col]
        self.selected_cell.is_selected = True

    def click(self, x, y):
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                if cell.x <= x < cell.x + cell.width and cell.y <= y < cell.y + cell.height:
                    return row, col
        return None

    def clear(self):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(None)

    def sketch(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.set_sketched_value(None)

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].set_cell_value(self.board[row][col])
                self.cells[row][col].set_sketched_value(None)

    def is_full(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return False
        return True

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.board[row][col] = self.cells[row][col].value

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return row, col
        return None

    def check_board(self):
        self.update_board()

        # Check rows
        for row in range(9):
            row_nums = []
            for col in range(9):
                num = self.board[row][col]
                if num in row_nums:
                    return False
                row_nums.append(num)

        # Check columns
        for col in range(9):
            col_nums = []
            for row in range(9):
                num = self.board[row][col]
                if num in col_nums:
                    return False
                col_nums.append(num)

        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box_nums = []
                for i in range(3):
                    for j in range(3):
                        num = self.board[box_row + i][box_col + j]
                        if num in box_nums:
                            return False
                        box_nums.append(num)

        return True
