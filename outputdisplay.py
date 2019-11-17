# Manages all of the sprites

import pygame
import constants as c
from sprites.textblock import TextBlock, TextPosition
from sprites.texttype import TextType
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.button import Button
from sprites.keyboard import Keyboard
from sprites.bar import Bar

# Declare sprite groups
all_group = pygame.sprite.Group()
event_group = pygame.sprite.Group()

# Assign sprites to group
TextBlock.groups = all_group
TextType.groups = all_group
Player.groups = all_group
Enemy.groups = all_group
Button.groups = all_group, event_group
Keyboard.groups = all_group, event_group
Bar.groups = all_group


def setup_display():
    # Set title
    pygame.display.set_caption(c.APP_NAME)

    # Create screen display
    global screen
    screen = pygame.display.set_mode((c.APP_WIDTH, c.APP_HEIGHT))

    # Init fonts
    global font_small
    global font_medium
    global font_large
    font_small = pygame.font.SysFont(c.FONT_NAME, c.FONT_SMALL_SIZE)
    font_medium = pygame.font.SysFont(c.FONT_NAME, c.FONT_MEDIUM_SIZE)
    font_large = pygame.font.SysFont(c.FONT_NAME, c.FONT_LARGE_SIZE, 1)

    # Background
    global background
    background = pygame.surface.Surface((c.APP_WIDTH, c.APP_HEIGHT))
    background.fill(c.APP_BG_COLOR)
    screen.blit(background, (0, 0))


def setup_sprites(best_time, restart_game):
    global player
    player = Player(
        pygame.rect.Rect(c.PLAYER_X, c.PLAYER_Y, c.PLAYER_W, c.PLAYER_H),
        c.PLAYER_DAMAGE,
        c.PLAYER_EXTRA_DAMAGE,
        c.PLAYER_MAX_EXTRA_DAMAGE
    )

    global enemy
    enemy = Enemy(
        pygame.rect.Rect(c.ENEMY_X, c.ENEMY_Y, c.ENEMY_W, c.ENEMY_H),
        c.ENEMY_HEALTH
    )

    global enemy_hp_bar
    enemy_hp_bar = Bar(
        pygame.rect.Rect(10, 180, c.APP_WIDTH - 20, 18),
        1,
        (200, 0, 0),
        (88, 88, 88)
    )

    TextBlock(
        "Enemy health",
        pygame.rect.Rect((c.APP_WIDTH - 80) / 2, 180, 80, 100),
        font_small
    )

    global end_game_text
    end_game_text = TextBlock(
        "Supertyper",
        pygame.rect.Rect((c.APP_WIDTH - 200) / 2, 40, 200, 100),
        font_large,
        TextPosition.CENTER
    )

    global final_score_text
    final_score_text = TextBlock(
        "Type as fast as you can",
        pygame.rect.Rect((c.APP_WIDTH - 200) / 2, 75, 200, 100),
        font_medium,
        TextPosition.CENTER
    )

    global timer_text
    timer_text = TextBlock(
        0,
        pygame.rect.Rect((c.APP_WIDTH - 400) / 2, 0, 400, 200),
        font_large,
        TextPosition.CENTER
    )

    global best_time_text
    best_time_text = TextBlock(
        "Best time: " + str(best_time) + "s",
        pygame.rect.Rect(300, 0, 200, 100),
        font_medium,
        TextPosition.RIGHT
    )

    global start_btn
    start_btn = Button(
        pygame.rect.Rect((c.APP_WIDTH - 100) / 2, 105, 100, 30),
        font_medium,
        "Start",
        restart_game,
        bgcolor=(88, 88, 88)
    )

    global current_text_type
    current_text_type = TextType(
        "",
        pygame.rect.Rect(5, 200, c.APP_WIDTH - 10, 250),
        font_medium,
        color_normal=(255, 255, 255),
        color_active=(100, 100, 100)
    )

    # Create keyboard
    keyletter = [
        "q", "w", "e", "r", "t", "y", "u", "i", "o", "p",
        "a", "s", "d", "f", "g", "h", "j", "k", "l",
        "z", "x", "c", "v", "b", "n", "m"
    ]

    # Create all keyboard sprites
    for idx, letter in enumerate(keyletter):
        # Calculate position of key
        if idx <= 9:
            x = c.KEY_X_ROW_1 + idx * c.KEY_SIZE
            y = c.KEY_Y
        elif idx <= 18:
            x = c.KEY_X_ROW_2 + (idx - 10) * c.KEY_SIZE
            y = c.KEY_Y + c.KEY_SIZE
        else:
            x = c.KEY_X_ROW_3 + (idx - 19) * c.KEY_SIZE
            y = c.KEY_Y + 2 * c.KEY_SIZE

        Keyboard(
            pygame.rect.Rect(x, y, c.KEY_SIZE, c.KEY_SIZE),
            font_medium,
            letter
        )


def refresh_sprites(ms):
    # Clear, update and draw for all sprites
    all_group.clear(screen, background)
    all_group.update(ms)
    all_group.draw(screen)

    # Flip display
    pygame.display.flip()


def show_end_game(time):
    end_game_text.text = "You win!"
    final_score_text.text = "Your time: " + str(round(time, 3)) + "s"
    start_btn.text = "Retry"

    show_menu_gui()


def show_menu_gui():
    end_game_text.hidden = False
    final_score_text.hidden = False
    start_btn.hidden = False


def hide_menu_gui():
    end_game_text.hidden = True
    final_score_text.hidden = True
    start_btn.hidden = True


def set_best_time(time):
    best_time_text.text = "Best time: " + str(round(time, 3)) + "s"


def set_timer_text(text):
    timer_text.text = text


def set_current_type_text(text):
    current_text_type.text = text


def set_current_type_index(idx):
    current_text_type.type_index = idx


def increment_current_type_index():
    set_current_type_index(current_text_type.type_index + 1)


def reset_state(new_text):
    """Reset sprite state (For restart game)"""
    # Set display text
    set_current_type_text(new_text)
    # Reset type index
    set_current_type_index(0)
    enemy_hp_bar.value = 1
    # Reset timer
    set_timer_text(0)
    # Hide GUI
    hide_menu_gui()
