import pygame
import constants as c
import userinput as i
import processhandle as p
import outputdisplay as o


def main():
    # Initialize pygame
    pygame.init()

    # Setup GUI display
    o.setup_display()

    # Control game loop
    running = True
    # Clock for game FPS
    clock = pygame.time.Clock()
    # Clock to keep track key press interval
    key_press_clock = pygame.time.Clock()
    # Load texts
    all_texts = p.get_all_texts()

    # Game state
    is_playing = False
    current_combo = 0
    timer = 0

    def restart_game():
        # Get new fresh state
        nonlocal current_combo
        nonlocal timer
        current_combo = 0
        timer = 0

        # Reset proccess state
        p.reset_state(o.player, o.enemy)
        o.reset_state(p.get_text(all_texts))

        # Start game
        nonlocal is_playing
        is_playing = True

    o.setup_sprites(p.get_best_time(), restart_game)

    # Setup player - enemy interaction
    # Here is where player actually deal damage
    p.setup_player_enemy_interaction(o.player, o.enemy, o.enemy_hp_bar)

    # Show menu screen
    o.show_menu_gui()

    while running:
        ms = clock.tick(c.FPS)

        all_events = pygame.event.get()

        # Check enter press
        if not is_playing and i.get_is_enter(all_events):
            restart_game()

        if is_playing:
            # Increment timer
            timer += ms / 1000
            o.set_timer_text(round(timer, 3))

            # Check enemy dead to end game
            if o.enemy.is_dead():
                is_playing = False
                o.show_end_game(round(timer, 3))

                # Compare best time
                if p.compare_best_time(timer):
                    o.set_best_time(round(timer, 3))

            for u in i.get_keydown_unicodes(all_events):
                # Compare key press
                if u == o.current_text_type.get_current_char():
                    if key_press_clock.tick() <= c.KEY_PRESS_INTERVAL:
                        o.player.increase_damage()
                    else:
                        # Took too long, player damage
                        o.player.reset_damage()

                    o.player.attack()
                    o.enemy.hurt()
                    o.increment_current_type_index()

                    # NOTE
                    # When player attack, damage is not dealt until animation ends
                    # A callback will be called when animation end, that's handled in
                    # `p.setup_player_enemy_interaction(o.player, o.enemy, o.enemy_hp_bar)`

                    # Provide new text to type if end
                    if o.current_text_type.is_exceed_text():
                        o.set_current_type_text(p.get_text(all_texts))
                        o.set_current_type_index(0)
                else:
                    # Wrong key, player damage
                    o.player.reset_damage()

        # Check if game quit
        running = not i.handle_quit(all_events)

        # Provide events for event group sprites to handle
        i.handle_event_group_sprites(all_events, o.event_group)

        # Refresh all sprites
        o.refresh_sprites(ms)


if __name__ == "__main__":
    main()
