import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, font, text, onclick, antialias=False, color=(255, 255, 255), bgcolor=None):
        # Init sprite groups
        super().__init__(self.groups)

        # Define surface rect
        self.rect = rect

        # Set image surface and black color as transparent
        self.image = pygame.surface.Surface(rect.size)

        # If bgcolor defined: set black as transparent by default
        if bgcolor:
            self.image.set_colorkey((0, 0, 0))

        self.font = font
        self.text = text
        self.onclick = onclick
        self.antialias = antialias
        self.color = color
        self.bgcolor = bgcolor

    def update(self, ms):
        # Clear blit, use bgcolor if defined, else use the default black
        self.image.fill(self.bgcolor if self.bgcolor else (0, 0, 0))

        # Render font as text surface
        text_surface = self.font.render(self.text, self.antialias, self.color)

        # Blit text surface to image and center it
        self.image.blit(text_surface, ((self.rect.width - text_surface.get_rect().width) / 2,
                                       (self.rect.height - text_surface.get_rect().height) / 2))

    def handle_event(self, event):
        # Mouse up and left click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos):
            self.onclick()
