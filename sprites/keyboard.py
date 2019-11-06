import pygame

class Keyboard(pygame.sprite.Sprite):
    
    def __init__(self, rect, font, text, antialias = False, color = (0, 0,0), bgcolor = (0, 0, 255)):
        super().__init__(self.groups)

        self.rect = rect
        self.image = pygame.surface.Surface(rect.size)
        self.font = font
        self.text = text
        self.antialias = antialias
        self.color = color
        self.bgcolor = bgcolor

    def update(self, ms):
        self.image.fill(self.bgcolor)

        text_surface = self.font.render(self.text, self.antialias, self.color)

        self.image.blit(text_surface, ((self.rect.width - text_surface.get_rect().width) / 2,
                                       (self.rect.height - text_surface.get_rect().height) / 2))

