import pygame
import json
import random
import constants
from sprites.textblock import TextBlock
from sprites.player import Player
from sprites.button import Button


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

    end_game = False
    win = False

    # Sprite group
    all_group = pygame.sprite.Group()
    event_group = pygame.sprite.Group()

    # Assign sprites to group
    TextBlock.groups = all_group
    Player.groups = all_group
    Button.groups = all_group, event_group

    # Sprites
    player = Player(pygame.rect.Rect(5, 5, 147, 177))
    current_text = TextBlock(all_texts[current_text_index], pygame.rect.Rect(
        0, 100, constants.APP_WIDTH, 250), font, color=(255, 255, 255))
    current_type_text = TextBlock("", pygame.rect.Rect(
        0, 100, constants.APP_WIDTH, 250), font, color=(100, 100, 100))

    while running:
        # Reference: http://thepythongamebook.com/en:pygame:step014
        ms = clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for sprite in event_group.sprites():
                sprite.handle_event(event)

            if not end_game:
                if event.type == pygame.KEYDOWN:
                    # Compare key press
                    if event.unicode == all_texts[current_text_index][current_type_index]:
                        print(event.unicode)
                        player.attack()
                        current_type_index += 1

                        # Update current type text
                        current_type_text.text = all_texts[current_text_index][:current_type_index]

                        if current_type_index >= len(all_texts[current_text_index]):
                            print('You win!')
                            end_game = True
                            win = True

        # Clear, update and draw for all sprites
        all_group.clear(screen, background)
        all_group.update(ms)
        all_group.draw(screen)

        # Flip display
        pygame.display.flip()


if __name__ == "__main__":
    main()
