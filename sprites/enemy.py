import pygame


# Sprite from https://craftpix.net/freebies/2d-game-troll-free-character-sprites/
class Enemy(pygame.sprite.Sprite):
    def __init__(self, rect, health):
        super().__init__(self.groups)
        self.rect = rect
        self.state = "idle"
        self.timer = 0

        self.health = health
        self.current_health = health

        self.idle_index = 0
        self.idle_frames = []
        for i in range(10):
            self.idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(f"images/enemy/Idle ({i + 1}).png"),
                    rect.size
                )
            )

        self.hurt_index = 0
        self.hurt_frames = []
        for i in range(10):
            self.hurt_frames.append(
                pygame.transform.scale(
                    pygame.image.load(f"images/enemy/Hurt ({i + 1}).png"),
                    rect.size
                )
            )

        self.dead_index = 0
        self.dead_frames = []
        for i in range(10):
            self.dead_frames.append(
                pygame.transform.scale(
                    pygame.image.load(f"images/enemy/Dead ({i + 1}).png"),
                    rect.size
                )
            )

        self.animfin = False
        self._update_image()

    def update(self, ms):
        self.timer += ms

        if self.timer > 100:
            self._update_image()
            self.timer = 0

    def hurt(self):
        self.state = "hurt"

    def hurt_damage(self, damage):
        self.current_health -= damage

    def is_dead(self):
        return self.current_health <= 0

    def _update_image(self):
        if self.current_health > 0:
            if self.state == "hurt":
                self.image = self.hurt_frames[self.hurt_index]
                self.hurt_index = (self.hurt_index + 1) % len(self.hurt_frames)

                if self.hurt_index <= 0:
                    self.state = "idle"

            else:
                self.image = self.idle_frames[self.idle_index]
                self.idle_index = (self.idle_index + 1) % len(self.idle_frames)
        elif not self.animfin:
            self.image = self.dead_frames[self.dead_index]
            self.dead_index = (self.dead_index + 1) % len(self.dead_frames)

            if self.dead_index == 0:
                self.animfin = True
