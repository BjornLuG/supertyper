import pygame


class TextBlock(pygame.sprite.Sprite):
    def __init__(self, text, rect, font, antialias=False, color=(255, 255, 255), bgcolor=None):
        # Init sprite groups
        super().__init__(self.groups)

        # Define surface rect
        self.rect = rect

        # Set image surface and black color as transparent
        self.image = pygame.surface.Surface(rect.size)
        self.image.set_colorkey((0, 0, 0))

        self.text = text
        self.font = font
        self.antialias = antialias
        self.color = color
        self.bgcolor = bgcolor

    def update(self, ms):
        # Clear blit
        self.image.fill((0, 0, 0))

        # Get total possible font height
        font_height = self.font.size('Bj')[1]
        # Copy text, will be sliced later
        cache_text = self.text
        # Current line y position
        y = 0

        # The following algorithm will go line by line to render
        # the possible texts of each line, producing a truncate effect
        while cache_text:
            i = 1

            # Text is lower than the rect's bound, break
            if y > self.rect.height:
                break

            # Find max index of text that reaches just before the rect's width
            while self.font.size(cache_text[:i])[0] < self.rect.width and i < len(cache_text):
                i += 1

            # Truncate text to nearest space to preserve word
            if i < len(cache_text):
                i = cache_text.rfind(" ", 0, i) + 1

            # Render font as text surface
            text_surface = self.font.render(
                cache_text[:i], self.antialias, self.color, self.bgcolor)

            # Blit text surface to image
            self.image.blit(text_surface, (0, y))

            # Increment y to go to next line
            y += font_height

            # Slice text to be used in next line
            cache_text = cache_text[i:]
