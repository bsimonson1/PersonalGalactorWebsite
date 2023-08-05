import pygame
from game import Game
from button import Button

def main():
    """
    The main method contains everything needed to start and run the game. It uses pygame and calls the run method from the 
    Game class in game.py to start the game upon correct user input.
    """
    # pygame setup
    pygame.init()
    # set the background to the minimum sized background image
    screen = pygame.display.set_mode((1000, 800))
    # caption of the pygame window is main menu
    pygame.display.set_caption("Main Menu")
    
    # Load images for buttons
    play_img = pygame.image.load("play.png").convert_alpha()
    quit_img = pygame.image.load("quit.png").convert_alpha()

    running = True
    while running:
        # clear the screen with a black color
        screen.fill((0, 0, 0)) 

        # Create buttons
        play_button = Button(305, 115, play_img, 0.25, screen)
        quit_button = Button(335, 515, quit_img, 0.25, screen)

        # Check if the play button is clicked
        if play_button.draw():
            # Start the game loop for the game
            game = Game(screen)
            game.run()  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

        # Check if the quit button is clicked
        if quit_button.draw():
            running = False

        # Check for events to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

