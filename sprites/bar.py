import pygame


class Bar(pygame.sprite.Sprite):
    def __init__(self, rect, value=0, color=(255, 255, 255), bgcolor=(0, 0, 0)):
        # Init sprite groups
        super().__init__(self.groups)

        # Define surface rect
        self.rect = rect

        # Set image surface and black color as transparent
        self.image = pygame.surface.Surface(rect.size)

        self.value = value
        self.color = color
        self.bgcolor = bgcolor

    def update(self, ms):
        self.image.fill(self.bgcolor)

        width = round(self.rect.width * self.value)

        if width > 0:
            pygame.draw.rect(self.image, self.color, pygame.rect.Rect(
                0, 0, width, self.rect.height))
