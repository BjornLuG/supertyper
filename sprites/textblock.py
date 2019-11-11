import pygame


class TextPosition:
    LEFT = 1
    RIGHT = 2
    CENTER = 4

class TextBlock(pygame.sprite.Sprite):
    def __init__(self, text, rect, font, position=TextPosition.LEFT, antialias=False, color=(255, 255, 255), bgcolor=None):
        # Init sprite groups
        super().__init__(self.groups)

        # Define surface rect
        self.rect = rect

        # Set image surface and black color as transparent
        self.image = pygame.surface.Surface(rect.size)
        self.image.set_colorkey((0, 0, 0))

        self.text = text
        self.font = font
        self.position = position
        self.antialias = antialias
        self.color = color
        self.bgcolor = bgcolor

        # Allow hiding
        self.hidden = False

    def update(self, ms):
        if self.hidden:
            self.image.fill((0, 0, 0))
            return

        # Clear blit
        self.image.fill((0, 0, 0))

        # Get total possible font height
        font_height = self.font.size('Bj')[1]
        # Copy text, will be sliced later
        cache_text = str(self.text)
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
            if self.position == TextPosition.LEFT:
                x = 0
            elif self.position == TextPosition.RIGHT:
                x = self.rect.width - text_surface.get_rect().width
            else:
                x = (self.rect.width - text_surface.get_rect().width) / 2

            self.image.blit(text_surface, (x, y))

            # Increment y to go to next line
            y += font_height

            # Slice text to be used in next line
            cache_text = cache_text[i:]
