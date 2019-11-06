import pygame
import json
import random
import constants
from sprites.textblock import TextBlock
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.button import Button
from sprites.keyboard import Keyboard


def main():
    # Initialize pygame
    pygame.init()

    # Set title
    pygame.display.set_caption(constants.APP_NAME)

    # Create screen display
    screen = pygame.display.set_mode(
        (constants.APP_WIDTH, constants.APP_HEIGHT))

    # Init font
    font = pygame.font.SysFont(constants.FONT_NAME, 20)

    # Background
    background = pygame.surface.Surface(
        (screen.get_width(), screen.get_height()))
    background.fill((11, 11, 11))
    screen.blit(background, (0, 0))

    # Game stuff
    running = True
    clock = pygame.time.Clock()
    fps = constants.FPS

    # Load texts
    texts_file = "texts.json"
    all_texts = []

    with open(texts_file) as read_file:
        all_texts = json.load(read_file)

    # Currents
    current_text_index = int(random.random() * len(all_texts))
    current_type_index = 0

    correct_combo = 0

    end_game = False
    win = False

    # Sprite group
    all_group = pygame.sprite.Group()
    event_group = pygame.sprite.Group()

    # Assign sprites to group
    TextBlock.groups = all_group
    Player.groups = all_group
    Enemy.groups = all_group
    Button.groups = all_group, event_group
    Keyboard.groups = all_group

    # Sprites
    player = Player(pygame.rect.Rect(5, 5, 147, 177), 5, 5, lambda damage: enemy.hurt_damage(damage))
    enemy = Enemy(pygame.rect.Rect(300, 0, 200, 200), 1000)
    current_text = TextBlock(all_texts[current_text_index], pygame.rect.Rect(
        0, 100, constants.APP_WIDTH, 250), font, color=(255, 255, 255))
    current_type_text = TextBlock("", pygame.rect.Rect(
        0, 100, constants.APP_WIDTH, 250), font, color=(100, 100, 100))

    keyletter = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd','f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n','m']
    keyboardkeys = []
    lastpressedkey = ""
    for letter in keyletter:
        keyboardkey = Keyboard(pygame.rect.Rect(5, 300, 50, 50), font, letter)
        keyboardkeys.append(keyboardkey)

    while running:
        # Reference: http://thepythongamebook.com/en:pygame:step014
        ms = clock.tick(fps)

        for event in pygame.event.get():
            # If pygame quiting, terminate self
            if event.type == pygame.QUIT:
                running = False

            # Provide events for event group sprites to handle
            for sprite in event_group.sprites():
                sprite.handle_event(event)

            if not end_game:
                if event.type == pygame.KEYDOWN:
                    if event.unicode in keyletter:
                        keyboardkeys[keyletter.index(event.unicode)].bgcolor = (255, 0, 0)
                        lastpressedkey = event.unicode

                    # Compare key press
                    if event.unicode == all_texts[current_text_index][current_type_index]:
                        print(event.unicode)
                        correct_combo += 1
                        player.attack()
                        enemy.hurt()
                        current_type_index += 1

                        # Update current type text
                        current_type_text.text = all_texts[current_text_index][:current_type_index]

                        # Check enemy dead to end game
                        if enemy.isdead:
                            # enemy.die()
                            print('You win!')
                            end_game = True
                            win = True

                        # If performs combo, add extra damage
                        if correct_combo > 0:
                            player.increase_damage()
                    else:
                        # Wrong key, reset combo and player damage
                        correct_combo = 0
                        player.reset_damage()
                    
                elif event.type == pygame.KEYUP:
                    if lastpressedkey in keyletter:
                        keyboardkeys[keyletter.index(lastpressedkey)].bgcolor = (0, 0, 255)

        # Clear, update and draw for all sprites
        all_group.clear(screen, background)
        all_group.update(ms)
        all_group.draw(screen)

        # Flip display
        pygame.display.flip()


if __name__ == "__main__":
    main()
