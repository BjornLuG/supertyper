import pygame
import constants

def main():
  # Initialize pygame
  pygame.init()

  # Set title
  pygame.display.set_caption(constants.APP_NAME)

  # Create screen display
  screen = pygame.display.set_mode((constants.APP_WIDTH, constants.APP_HEIGHT))
  
  running = True

  # Temp
  test_text = "Hello World"
  current_index = 0
  end_game = False
  win = False

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      
      if not end_game:
        if event.type == pygame.KEYDOWN:
          print("Key pressed:", event.unicode)
          
          if event.unicode == test_text[current_index]:
            print("Key correct!")
            current_index += 1

            if current_index >= len(test_text):
              print('You win!')
              end_game = True
              win = True

if __name__ == "__main__":
  main()
