import pygame

class ColorButton:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.rect = pygame.Rect(position[0] - 10, position[1] - 10, 20, 20)

    def draw(self, surface, hover=False):
        if hover:
            brighter = tuple(min(c + 50, 255) for c in self.color)
            pygame.draw.rect(surface, brighter, self.rect, border_radius=5)
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=5)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)