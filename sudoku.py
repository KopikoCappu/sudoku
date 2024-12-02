import pygame
from board import Board
from sudoku_generator import generate_sudoku


pygame.init()


SCREEN_WIDTH = 590
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


class SudokuGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sudoku")


        self.game_state = "START"
        self.board = None
        self.difficulty = None

    def draw_start_screen(self):

        self.screen.fill(WHITE)

        # Title
        font = pygame.font.Font(None, 60)
        title = font.render("Sudoku", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Difficulty buttons
        difficulties = ["EASY", "MEDIUM", "HARD"]
        button_font = pygame.font.Font(None, 40)

        for i, diff in enumerate(difficulties):
            button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250 + i * 100, 200, 60)
            pygame.draw.rect(self.screen, GRAY, button)

            text = button_font.render(diff, True, BLACK)
            text_rect = text.get_rect(center=button.center)
            self.screen.blit(text, text_rect)

            # Store button as an attribute for click detection
            setattr(self, f"{diff.lower()}_button", button)

    def draw_game_screen(self):
        self.screen.fill(WHITE)
        self.board.draw()

        button_font = pygame.font.Font(None, 30)
        button_texts = ["RESET", "RESTART", "EXIT"]
        button_rects = []

        # Calculate total width of all buttons including gaps
        button_width = 100
        button_gap = 20  # Space between buttons
        total_buttons_width = (button_width * 3) + (button_gap * 2)

        # Calculate starting x position to center the buttons
        start_x = (SCREEN_WIDTH - total_buttons_width) // 2

        for i, text in enumerate(button_texts):
            button = pygame.Rect(
                start_x + (i * (button_width + button_gap)),  # X position with gaps
                SCREEN_HEIGHT - 70,  # Y position
                button_width,
                50  # Height
            )
            pygame.draw.rect(self.screen, GRAY, button)

            rendered_text = button_font.render(text, True, BLACK)
            text_rect = rendered_text.get_rect(center=button.center)
            self.screen.blit(rendered_text, text_rect)

            button_rects.append(button)

        return button_rects

    def draw_game_over_screen(self, won):
        self.screen.fill(WHITE)

        font = pygame.font.Font(None, 60)
        text = "Congratulations! You won!" if won else "Game Over! Try again."

        rendered_text = font.render(text, True, BLACK)
        text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(rendered_text, text_rect)

    def run(self):
        running = True
        selected_cell = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.game_state == "START":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.easy_button.collidepoint(mouse_pos):
                            self.difficulty = "easy"
                            self.board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.difficulty)
                            self.game_state = "GAME"
                        elif self.medium_button.collidepoint(mouse_pos):
                            self.difficulty = "medium"
                            self.board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.difficulty)
                            self.game_state = "GAME"
                        elif self.hard_button.collidepoint(mouse_pos):
                            self.difficulty = "hard"
                            self.board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.difficulty)
                            self.game_state = "GAME"

                elif self.game_state == "GAME":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        board_click = self.board.click(mouse_pos[0], mouse_pos[1])

                        if board_click:
                            self.board.select(board_click[0], board_click[1])
                        button_rects = self.draw_game_screen()
                        if button_rects[0].collidepoint(mouse_pos):
                            self.board.reset_to_original()
                        elif button_rects[1].collidepoint(mouse_pos):
                            self.game_state = "START"
                        elif button_rects[2].collidepoint(mouse_pos):
                            running = False

                    if event.type == pygame.KEYDOWN:
                        if event.unicode.isdigit():
                            num = int(event.unicode)
                            if 1 <= num <= 9:
                                # Sketch the number
                                self.board.sketch(num)

                        if event.key == pygame.K_RETURN:
                            if self.board.selected_cell and self.board.selected_cell.sketched_value:
                                self.board.place_number(self.board.selected_cell.sketched_value)

                        if event.key == pygame.K_BACKSPACE:
                            self.board.clear()

                elif self.game_state == "GAME_OVER":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.game_state = "START"

            if self.game_state == "START":
                self.draw_start_screen()

            elif self.game_state == "GAME":
                self.draw_game_screen()

                if self.board.is_full():
                    if self.board.check_board():
                        self.game_state = "GAME_OVER"
                        self.draw_game_over_screen(won=True)
                    else:
                        self.game_state = "GAME_OVER"
                        self.draw_game_over_screen(won=False)

            elif self.game_state == "GAME_OVER":
                self.draw_game_over_screen(won=self.board.check_board())

            pygame.display.flip()

        pygame.quit()


def main():
    game = SudokuGame()
    game.run()


if __name__ == "__main__":
    main()