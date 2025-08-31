import pygame
from logging_manager import logger

class ToolButton:
    def __init__(self, text, symbol, position, color):
        self.text = text
        self.symbol = symbol
        self.position = position
        self.color = color
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(symbol, True, (0, 0, 0))
        self.button_rect = self.text_surface.get_rect(center=position).inflate(40, 20) # Increased hitbox size

    def draw(self, screen, hover=False, clicked=False):
        if clicked:
            rect_color = (max(0, self.color[0] - 100), max(0, self.color[1] - 100), max(0, self.color[2] - 100))
        elif hover:
            rect_color = (max(0, self.color[0] - 50), max(0, self.color[1] - 50), max(0, self.color[2] - 50))
        else:
            rect_color = self.color

        pygame.draw.rect(screen, rect_color, self.button_rect, border_radius=5)
        screen.blit(self.text_surface, self.text_surface.get_rect(center=self.button_rect.center))

    def is_clicked(self, pos):
        clicked = self.button_rect.collidepoint(pos)
        logger.debug(f"Checking button '{self.text}' at {self.button_rect} for click at {pos}: {'Clicked' if clicked else 'Not Clicked'}")
        return clicked