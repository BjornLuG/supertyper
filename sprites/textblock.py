import pygame


class TextBlock(pygame.sprite.Sprite):
    def __init__(self, text, rect, font, antialias=False, color=(255, 255, 255), bgcolor=None):
        super().__init__(self.groups)
        self.image = pygame.surface.Surface(rect.size)
        self.image.set_colorkey((0, 0, 0))
        self.text = text
        self.rect = rect
        self.font = font
        self.antialias = antialias
        self.color = color
        self.bgcolor = bgcolor

    def update(self, ms):
        font_height = self.font.size('Bj')[1]
        cache_text = self.text
        y = self.rect.top

        while cache_text:
            i = 1

            if y > self.rect.bottom:
                break

            while self.font.size(cache_text[:i])[0] < self.rect.width and i < len(cache_text):
                i += 1

            if i < len(cache_text):
                i = cache_text.rfind(" ", 0, i) + 1

            if self.bgcolor:
                text_surface = self.font.render(
                    cache_text[:i], self.antialias, self.color, self.bgcolor)
                text_surface.set_color_key(self.bgcolor)
            else:
                text_surface = self.font.render(
                    cache_text[:i], self.antialias, self.color)

            self.image.blit(text_surface, (self.rect.left, y))
            y += font_height

            cache_text = cache_text[i:]
