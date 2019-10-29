import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, font, text, onclick, antialias=False, color=(255, 255, 255), bgcolor=None):
        super().__init__(self.groups)
        self.rect = rect
        self.image = pygame.surface.Surface(rect.size)
        self.image.set_colorkey((0, 0, 0))
        self.font = font
        self.text = text
        self.onclick = onclick
        self.antialias = antialias
        self.color = color
        self.bgcolor = bgcolor

    def update(self, ms):
        self.image.fill((0, 0, 0))

        if self.bgcolor:
            text_surface = self.font.render(
                self.text, self.antialias, self.color, self.bgcolor)
            text_surface.set_color_key(self.bgcolor)
        else:
            text_surface = self.font.render(
                self.text, self.antialias, self.color)

        self.image.blit(text_surface, self.rect.topleft)

    def handle_event(self, event):
        # Mouse up and left click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos):
            self.onclick()
