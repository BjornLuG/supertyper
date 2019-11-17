# Handles various processes in game

import random
import json
import constants as c


def get_all_texts():
    """Retrieve texts from JSON"""
    try:
        with open(c.text_file_name, "r") as f:
            return json.load(f)
    except:
        return ["texts.json doesn't exist. Run reqtexts.py first."]


def get_text(all_texts):
    """Get one text from all texts and remove it from the list (Mutates list)"""
    text = all_texts.pop(int(random.random() * len(all_texts)))

    if len(all_texts) <= 0:
        all_texts.extend(get_all_texts())

    return text


def get_best_time():
    try:
        with open(c.best_time_file_name, "r") as f:
            return f.read()
    except:
        return ""


def compare_best_time(current_time):
    """Compare best time, and if so saves best time to txt file"""
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
    """Reset player damage and enemy health (For restart game)"""
    player.reset_damage()
    enemy.current_health = c.ENEMY_HEALTH
