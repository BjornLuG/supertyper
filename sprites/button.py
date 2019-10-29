import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, font, text, onclick, antialias=False, color=(255, 255, 255), bgcolor=None):
        # Init sprite groups
        super().__init__(self.groups)

        # Define surface rect
        self.rect = rect

        # Set image surface and black color as transparent
        self.image = pygame.surface.Surface(rect.size)
        self.image.set_colorkey((0, 0, 0))

        self.font = font
        self.text = text
        self.onclick = onclick
        self.antialias = antialias
        self.color = color
        self.bgcolor = bgcolor

    def update(self, ms):
        # Clear blit
        self.image.fill((0, 0, 0))

        # Render font as text surface, if has bgcolor, set it as transparent
        if self.bgcolor:
            text_surface = self.font.render(
                self.text, self.antialias, self.color, self.bgcolor)
            text_surface.set_color_key(self.bgcolor)
        else:
            text_surface = self.font.render(
                self.text, self.antialias, self.color)

        # Blit text surface to image
        self.image.blit(text_surface, self.rect.topleft)

    def handle_event(self, event):
        # Mouse up and left click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos):
            self.onclick()
