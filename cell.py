import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = None
        self.row = row
        self.col = col
        self.screen = screen
        self.is_selected = False

        # Cell dimensions and positioning
        self.width = 60
        self.height = 60
        self.margin = 5

        # Calculate cell position
        self.x = col * (self.width + self.margin) + self.margin
        self.y = row * (self.height + self.margin) + self.margin

    def set_cell_value(self, value):
        """
        Set the value of the cell

        :param value: Value to set
        """
        self.value = value

    def set_sketched_value(self, value):
        """
        Set the sketched value of the cell

        :param value: Sketched value to set
        """
        self.sketched_value = value

    def draw(self):
        """
        Draw the cell on the screen
        """
        # Define colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        LIGHT_BLUE = (173, 216, 230)

        # Draw cell background
        if self.is_selected:
            pygame.draw.rect(self.screen, LIGHT_BLUE, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.screen, WHITE, (self.x, self.y, self.width, self.height))

        # Draw cell border
        pygame.draw.rect(self.screen, BLACK, (self.x, self.y, self.width, self.height), 2)

        # Draw cell value if present
        font = pygame.font.Font(None, 36)

        # Draw main value
        if self.value != 0:
            text = font.render(str(self.value), True, BLACK)
            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            self.screen.blit(text, text_rect)

        # Draw sketched value
        if self.sketched_value is not None and self.value == 0:
            small_font = pygame.font.Font(None, 24)
            sketched_text = small_font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(sketched_text, (self.x + 5, self.y + 5))