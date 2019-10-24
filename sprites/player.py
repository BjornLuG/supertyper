import pygame


# Sprite from https://www.gameart2d.com/the-knight-free-sprites.html
class Player(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__(self.groups)
        self.rect = rect
        # Current player state
        self.state = "idle"
        # Timer to slow down animation loop
        self.timer = 0

        # Load idle frames
        self.idle_index = 0
        self.idle_frames = []
        for i in range(10):
            self.idle_frames.append(pygame.transform.scale(
                pygame.image.load(f"images/player/Idle ({i + 1}).png"), rect.size))

        # Load attack frames
        self.attack_index = 0
        self.attack_frames = []
        for i in range(10):
            self.attack_frames.append(pygame.transform.scale(
                pygame.image.load(f"images/player/Attack ({i + 1}).png"), rect.size))

        self._update_image()

    def update(self, ms):
        self.timer += ms

        # Slow down image loop
        if self.timer > 100:
            self._update_image()
            self.timer = 0

    def attack(self):
        self.state = "attack"

    def _update_image(self):
        if self.state == "attack":
            self.image = self.attack_frames[self.attack_index]
            self.attack_index = (self.attack_index +
                                 1) % len(self.attack_frames)

            # Once attack done, return to idle
            if self.attack_index <= 0:
                self.state = "idle"
        else:
            self.image = self.idle_frames[self.idle_index]
            self.idle_index = (self.idle_index + 1) % len(self.idle_frames)
