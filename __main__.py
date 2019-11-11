import pygame
import json
import random
import constants
from sprites.textblock import TextBlock, TextPosition
from sprites.texttype import TextType
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.button import Button
from sprites.keyboard import Keyboard
from sprites.bar import Bar


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
    font_small = pygame.font.SysFont(constants.FONT_NAME, 12)
    font_large = pygame.font.SysFont(constants.FONT_NAME, 30, 1)

    # Background
    background = pygame.surface.Surface(
        (screen.get_width(), screen.get_height()))
    background.fill((11, 11, 11))
    screen.blit(background, (0, 0))

    # Game stuff
    running = True
    clock = pygame.time.Clock()
    fps = constants.FPS
    timer = 0

    # Clock to keep track key press interval
    key_press_clock = pygame.time.Clock()
    # Max interval between key press, else reset damage
    max_press_interval = 500

    # Load texts
    all_texts = get_all_texts()

    # Currents
    current_text = all_texts.pop(int(random.random() * len(all_texts)))
    current_type_index = 0

    correct_combo = 0

    start_game = False
    end_game = False

    enemy_hp = 1000

    # Sprite group
    all_group = pygame.sprite.Group()
    event_group = pygame.sprite.Group()

    # Assign sprites to group
    TextBlock.groups = all_group
    TextType.groups = all_group
    Player.groups = all_group
    Enemy.groups = all_group
    Button.groups = all_group, event_group
    Keyboard.groups = all_group
    Bar.groups = all_group

    # Sprites
    player = Player(pygame.rect.Rect(5, 5, 147, 177), 5, 5, 50)

    enemy = Enemy(pygame.rect.Rect(300, 0, 200, 200), enemy_hp)

    enemy_hp_bar = Bar(
        pygame.rect.Rect(10, 180, constants.APP_WIDTH - 20, 18),
        1,
        (200, 0, 0),
        (88, 88, 88)
    )

    TextBlock(
        "Enemy health",
        pygame.rect.Rect((constants.APP_WIDTH - 80) / 2, 180, 80, 100),
        font_small
    )

    end_game_text = TextBlock(
        "Supertyper",
        pygame.rect.Rect((constants.APP_WIDTH - 200) / 2, 40, 200, 100),
        font_large,
        TextPosition.CENTER
    )

    final_score_text = TextBlock(
        "Type as fast as you can",
        pygame.rect.Rect((constants.APP_WIDTH - 200) / 2, 75, 200, 100),
        font,
        TextPosition.CENTER
    )

    timer_text = TextBlock(
        timer,
        pygame.rect.Rect((constants.APP_WIDTH - 400)/ 2, 0, 400, 200),
        font_large,
        TextPosition.CENTER
    )

    def restart_game():
        nonlocal start_game
        nonlocal end_game
        nonlocal current_text
        nonlocal current_type_index
        nonlocal correct_combo
        nonlocal timer
        # Load texts
        all_texts = get_all_texts()

        # Currents
        current_text = all_texts.pop(int(random.random() * len(all_texts)))
        current_type_index = 0

        correct_combo = 0

        current_text_type.text = current_text
        current_text_type.type_index = 0
    
        # Reset enemy health
        enemy.current_health = enemy_hp
        enemy.isdead = False
        enemy_hp_bar.value = 1

        timer = 0
        timer_text.text = 0

        # Hide GUI
        end_game_text.hidden = True
        final_score_text.hidden = True
        start_btn.hidden = True

        # Start game
        start_game = True
        end_game = False

    start_btn = Button(
        pygame.rect.Rect((constants.APP_WIDTH - 100) / 2, 105, 100, 30),
        font,
        "Start",
        restart_game,
        bgcolor=(88, 88, 88)
    )

    current_text_type = TextType(
        current_text,
        pygame.rect.Rect(5, 200, constants.APP_WIDTH - 10, 250),
        font,
        color_normal=(255, 255, 255),
        color_active=(100, 100, 100)
    )

    keyletter = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"]
    keyboardkeys = []
    lastpressedkey = []
    keyX = 5
    keyY = 325
    keywidth = 40
    keyheight = 40
    for letter in keyletter:
        keyboardkey = Keyboard(pygame.rect.Rect(keyX, keyY, keywidth, keyheight), font, letter)
        keyboardkeys.append(keyboardkey)
        keyX += keywidth
        if keyletter.index(letter) == 9:
            keyX = 5
            keyY += keyheight
        elif keyletter.index(letter) == 18:
            keyX = 5
            keyY += keyheight

    # Setup player attack (Called on every attack animation)
    def player_attack(damage):
        # Damage
        enemy.hurt_damage(damage)
        # Update enemy hp bar
        enemy_hp_bar.value = enemy.current_health / enemy.health

    player.attack_callback = player_attack

    while running:
        # Check enemy dead to end game
        if not end_game and enemy.isdead:
            print("You win!")
            end_game = True
            end_game_text.text = "Game over!"
            end_game_text.hidden = False
            final_score_text.text = "Your time: " + str(round(timer, 3)) + "s"
            final_score_text.hidden = False
            start_btn.text = "Retry"
            start_btn.hidden = False

        # Reference: http://thepythongamebook.com/en:pygame:step014
        ms = clock.tick(fps)
        if start_game and not end_game:
            timer += ms/1000
            timer_text.text = round(timer, 3)

        for event in pygame.event.get():
            # If pygame quiting, terminate self
            if event.type == pygame.QUIT:
                running = False

            # Provide events for event group sprites to handle
            for sprite in event_group.sprites():
                sprite.handle_event(event)

            if start_game and not end_game:
                if event.type == pygame.KEYDOWN:
                    if event.unicode.lower() in keyletter:
                        keyboardkeys[keyletter.index(event.unicode.lower())].bgcolor = (211, 211, 211)
                        lastpressedkey.append(event.unicode.lower())

                    # Compare key press
                    if event.unicode == current_text[current_type_index]:
                        print(event.unicode)
                        correct_combo += 1
                        player.attack()
                        enemy.hurt()
                        current_type_index += 1

                        # Update current type text
                        current_text_type.type_index = current_type_index

                        if current_type_index >= len(current_text):
                            current_text_type.text = current_text = all_texts.pop(int(random.random() * len(all_texts)))
                            current_text_type.type_index = current_type_index = 0

                        # If performs combo, add extra damage
                        if correct_combo > 0 and key_press_clock.tick() <= max_press_interval:
                            player.increase_damage()
                        else:
                            # Took too long, reset
                            correct_combo = 0
                            player.reset_damage()
                    else:
                        # Wrong key, reset combo and player damage
                        correct_combo = 0
                        player.reset_damage()

                elif event.type == pygame.KEYUP:
                    for i in lastpressedkey:
                        if i in keyletter:
                            keyboardkeys[keyletter.index(i)].bgcolor = (128, 128, 128)
                    lastpressedkey = []

        # Clear, update and draw for all sprites
        all_group.clear(screen, background)
        all_group.update(ms)
        all_group.draw(screen)

        # Flip display
        pygame.display.flip()


def get_all_texts():
    with open("texts.json") as read_file:
        return json.load(read_file)


if __name__ == "__main__":
    main()
