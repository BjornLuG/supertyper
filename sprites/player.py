import pygame


# Sprite from https://www.gameart2d.com/the-knight-free-sprites.html
class Player(pygame.sprite.Sprite):
    def __init__(self, rect, damage, extra_damage, max_extra_damage):
        # Init sprite groups
        super().__init__(self.groups)

        # Define surface rect
        self.rect = rect

        # Current player state
        self.state = "idle"
        # Timer to slow down animation loop
        self.timer = 0
        # Damage
        self.damage = damage
        self.extra_damage = extra_damage
        self.max_extra_damage = max_extra_damage
        self.attack_callback = lambda damage: None
        # Current extra damage
        self.current_extra_damage = 0

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

        # Render the image on first frame
        self._update_image()

    def update(self, ms):
        self.timer += ms

        # Slow down image loop, updates at every 100ms
        if self.timer > 100:
            self._update_image()
            self.timer = 0

    def attack(self):
        self.state = "attack"

    def increase_damage(self):
        self.current_extra_damage = min(
            self.current_extra_damage + self.extra_damage,
            self.max_extra_damage
        )

    def reset_damage(self):
        self.current_damage = self.damage

    def _update_image(self):
        if self.state == "attack":
            # Iterate through attack frames
            self.image = self.attack_frames[self.attack_index]
            self.attack_index = (self.attack_index + 1) % len(self.attack_frames)

            # Once attack done, execute attack callback and return to idle
            if self.attack_index <= 0:
                # Send attack callback
                self.attack_callback(self.damage + self.current_extra_damage)
                self.state = "idle"
        else:
            # Iterate through idle frames
            self.image = self.idle_frames[self.idle_index]
            self.idle_index = (self.idle_index + 1) % len(self.idle_frames)
