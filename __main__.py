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

  while running:
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        running = False

if __name__ == "__main__":
  main()
