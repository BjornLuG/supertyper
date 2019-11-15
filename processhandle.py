# Handles various process in game

import random
import json
import constants as c


def get_all_texts():
    with open(c.text_file_name) as f:
        return json.load(f)


def get_text(all_texts):
    """Get one text from all texts and remove it from the list"""
    return all_texts.pop(int(random.random() * len(all_texts)))


def get_best_time():
    try:
        with open(c.best_time_file_name, "r") as f:
            return f.read()
    except:
        return ""


def compare_best_time(current_time):
    best_time = get_best_time()

    if best_time == "" or float(current_time) < float(best_time):
        with open(c.best_time_file_name, "w") as f:
            f.write(str(round(current_time, 3)))

        return True
    else:
        return False


def setup_player_enemy_interaction(player, enemy, enemy_hp_bar):
    """This is where the player actually deal damage after attack animation"""
    def player_attack(damage):
        # Damage
        enemy.hurt_damage(damage)
        # Update enemy hp bar
        enemy_hp_bar.value = enemy.current_health / enemy.health

    player.attack_callback = player_attack


def reset_state(player, enemy):
    player.reset_damage()
    enemy.current_health = c.ENEMY_HEALTH
