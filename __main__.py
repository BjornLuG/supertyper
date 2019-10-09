import pygame
import json
import random
import constants

def main():
    # Initialize pygame
    pygame.init()

    # Set title
    pygame.display.set_caption(constants.APP_NAME)

    # Create screen display
    screen = pygame.display.set_mode((constants.APP_WIDTH, constants.APP_HEIGHT))

    running = True

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

    print("Type:", all_texts[current_text_index])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not end_game:
                if event.type == pygame.KEYDOWN:
                    if event.unicode == all_texts[current_text_index][current_type_index]:
                        print(event.unicode)
                        current_type_index += 1

                        if current_type_index >= len(all_texts[current_text_index]):
                            print('You win!')
                            end_game = True
                            win = True

if __name__ == "__main__":
    main()
