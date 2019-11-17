import pygame


class TextType(pygame.sprite.Sprite):
    def __init__(self, text, rect, font, type_index=0, antialias=False, color_normal=(255, 255, 255), color_active=(255, 255, 255)):
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
        self.color_normal = color_normal
        self.color_active = color_active
        self.type_index = type_index

    def update(self, ms):
        # Clear blit
        self.image.fill((0, 0, 0))

        # Get total possible font height
        font_height = self.font.size("Bj")[1]
        # Copy text, will be sliced later
        cache_text = self.text
        # Current line y position
        y = 0
        current_index = 0

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

            if current_index >= self.type_index:
                # Current line is more than type index, all use color_normal
                text_surface = self.font.render(
                    cache_text[:i], self.antialias, self.color_normal)

                # Blit text surface to image
                self.image.blit(text_surface, (0, y))

            elif current_index + i <= self.type_index:
                # Current line is less than type index, all use color_active
                text_surface = self.font.render(
                    cache_text[:i], self.antialias, self.color_active)

                # Blit text surface to image
                self.image.blit(text_surface, (0, y))

            else:
                # Current line has two different colors, render both
                relative_index = self.type_index - current_index

                text_surface_left = self.font.render(
                    cache_text[:relative_index], self.antialias, self.color_active)
                text_surface_right = self.font.render(
                    cache_text[relative_index:i], self.antialias, self.color_normal)

                # Blit text surface to image (each for left and right)
                self.image.blit(text_surface_left, (0, y))
                self.image.blit(
                    text_surface_right, (text_surface_left.get_rect().width, y))

            # Increment y to go to next line
            y += font_height

            # Slice text to be used in next line
            cache_text = cache_text[i:]
            current_index += i

    def get_current_char(self):
        return self.text[self.type_index]

    def is_exceed_text(self):
        return self.type_index >= len(self.text)
