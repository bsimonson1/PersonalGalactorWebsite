import pygame
from asteroid import Asteroids
import time
from world_button import World_Button
from button import Button
#determine error for laser
from laser import Laser
import Resume
#high score 384 Alan
class Game:
    def __init__(self, screen):
        self.start_time = time.time()
        self.player_speed = 10

        #initialize the game objects and variables
        self.screen = screen
        #using my own font for the game score and other text
        font_path = r"C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\rishgular-font\RishgularTry-x30DO.ttf"
        font_size = 36
        self.font = pygame.font.Font(font_path, font_size)
        
        scale_factor = 0.05

        #load the spaceship image
        self.spaceship_images = [
            pygame.image.load("player_char_one.png"),
            pygame.image.load("player_char_two.png"),
            pygame.image.load("player_char_three.png")
        ]

        self.planet1 = pygame.image.load("Baren.png").convert_alpha()
        self.planet2 = pygame.image.load("Black_hole.png").convert_alpha()
        self.planet3 = pygame.image.load("Ice.png").convert_alpha()
        self.planet4 = pygame.image.load("Lava.png").convert_alpha()
        self.planet5 = pygame.image.load("Terran.png").convert_alpha()

        #these instance variables will be used when i want to "animate the player images"
        self.animation_timer = 0
        #random speed set for the interval between each image generation
        self.animation_interval = 200  
        self.current_frame_index = 0

        spaceship_image = self.spaceship_images[self.current_frame_index]
        initial_image = pygame.image.load("background_image.png").convert()
        new_width = 1000  
        new_height = 800  

        # Resize the image to the new dimensions
        self.background_image = pygame.transform.scale(initial_image, (new_width, new_height))
        #set the boundaries for the player to travel and handle in the update method
        self.min_x = 0
        self.max_x = screen.get_width() - spaceship_image.get_width()
        self.min_y = 0
        self.max_y = screen.get_height() - spaceship_image.get_height()

        #default positions and states for the player
        self.spaceship_x = 0
        self.spaceship_y = 500
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self._paused = False
        #initialize the asteroids object from the Asteroid class
        self.asteroids = Asteroids(self.screen)

        self.player_score = 0

        #call in labels to be used for buttons in this game
        self.play_img = pygame.image.load("play.png").convert_alpha()
        self.quit_img = pygame.image.load("quit.png").convert_alpha()
        self.paused_img = pygame.image.load("pause.png").convert_alpha()
        self.retry_img = pygame.image.load("retry.png").convert_alpha()
        self.resume_img = pygame.image.load("resume.png").convert_alpha()
        self.score_img = pygame.image.load("score.png").convert_alpha()
        self.high_score_img = pygame.image.load("high_score.png").convert_alpha()
        self.controls_img = pygame.image.load("controls.png").convert_alpha()

        self.crashed = False

        self.toggle_mute = False

    def handle_events(self):
        #handle events such as user input
        #if the key ispressed this is entered
        #this achieves either a pressing effect for when the plauer presses a key or a holdinge ffect for when the player hodls a key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.moving_down = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.moving_up = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.moving_right = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.moving_left = True
                elif event.key == pygame.K_ESCAPE:
                    self._paused = not self._paused
                    #if the key is not pressed then this is entered and resets the values
                elif event.key == pygame.K_m:
                    self.toggle_mute = not self.toggle_mute
                    if self.toggle_mute:
                        pygame.mixer.music.set_volume(0.0)
                    else:
                        pygame.mixer.music.set_volume(0.2)
                elif event.key == pygame.K_SPACE:
                    # This will be the key to enter the "worlds" for my information
                    continue
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.moving_down = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.moving_up = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.moving_right = False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.moving_left = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                     # This will be the key to enter the "worlds" for my information
                    continue
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        #update the game state
        if not self._paused:
            self.handle_events()

        if self.moving_down and self.spaceship_y < self.max_y:
            self.spaceship_y += self.player_speed
        if self.moving_up and self.spaceship_y > self.min_y:
            self.spaceship_y -= self.player_speed
        if self.moving_right and self.spaceship_x < self.max_x:
            self.spaceship_x += self.player_speed
        if self.moving_left and self.spaceship_x > self.min_x:
            self.spaceship_x -= self.player_speed

        self.current_time = time.time()
        self.elapsed_time = self.current_time - self.start_time
        if self.elapsed_time > 0.5:
            self.player_score += 1
            self.start_time = self.current_time

        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer >= self.animation_interval:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.spaceship_images)
            self.animation_timer = current_time

        spaceship_image = self.spaceship_images[self.current_frame_index]
        spaceship_rect = spaceship_image.get_rect()
        spaceship_rect.x = self.spaceship_x
        spaceship_rect.y = self.spaceship_y

        #pass the lasers list to the update method of the Asteroids object
        self.asteroids.update(self.player_score)  

        for asteroid_rect, _, _, _ in self.asteroids.asteroid_rects:
            if spaceship_rect.colliderect(asteroid_rect):
                self.game_over()
                self.player_score = 0
                self.asteroid_interval = 2000
                self.player_speed = 10

    """
    the methods below are used in conjunction to handle if the player has lost the game
    Ie. the player has collided with an asteroid
    """
    def reset(self):
        #reset all necessary variables and states to their initial values
        self.player_speed = 10
        self.spaceship_x = 0
        self.spaceship_y = 500
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self._paused = False
        self.asteroids = Asteroids(self.screen)

    def game_over(self):
        pygame.mixer.music.stop()
        self.crashed = True
        #game over logic 
        self.reset()  
        # Reset the game
        self.render()  
        # render the game objects on the screen
        pygame.display.update()  
        # update the display

        #wait for the player to press space or click the start button to start a new game
        while self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.crashed = False
                        return  
                    #return to the main file to start a new game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.crashed = True
                self.render()
        
    def render(self):
        #draw the background image
        self.screen.blit(self.background_image, (0, 0))
        #render the game objects on the screen
        self.planet1_button.draw()
        self.planet2_button.draw()
        self.planet3_button.draw()
        self.planet4_button.draw()
        self.planet5_button.draw()
        spaceship_image = self.spaceship_images[self.current_frame_index]
        self.screen.blit(spaceship_image, (self.spaceship_x, self.spaceship_y))
        score_text = self.font.render(f'Score: {self.player_score}', True, (100, 100, 100))
        self.screen.blit(score_text, (800, 5))
        #render the aseroids 
        self.asteroids.render() 

        if self._paused:
            self.resume_button = Button(320, 295, self.resume_img, 0.2534, self.screen)
            self.quit_button = Button(335, 525, self.quit_img, 0.2548, self.screen)
            self.paused_button = Button(335, 75, self.paused_img, 0.25, self.screen)
            self.paused_button.draw()
            if self.resume_button.draw():
                self._paused = not self._paused
                return
            if self.quit_button.draw():
                pygame.quit()
                quit()

        if self.crashed:
            self.retry = Button(335, 215, self.retry_img, 0.25, self.screen)
            self.quit_button_crashed = Button(335, 415, self.quit_img, 0.255, self.screen)
            if self.retry.draw():
                self.crashed = False
                return
            if self.quit_button_crashed.draw():
                pygame.quit()
                quit()

    def paused(self):
        while self._paused: 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._paused = not self._paused
                        return  # Resume the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            #once unpaused the object must be redraw and the display must be updated to display them
            self.render()  
            pygame.display.update()  

    def run(self):
        pygame.display.set_caption("Website")
        # main game loop
        clock = pygame.time.Clock()  
        # create a clock object for controlling the frame rate
        asteroid_timer = 0
        self.asteroid_interval = 2000
        self.planet1_button = World_Button(400, 115, self.planet1, 6, self.screen)
        self.planet2_button = World_Button(500, 515, self.planet2, 7, self.screen)
        self.planet3_button = World_Button(750, 212, self.planet3, 6, self.screen)
        self.planet4_button = World_Button(75, 550, self.planet4, 7, self.screen)
        self.planet5_button = World_Button(50, 50, self.planet5, 6, self.screen)
        while True:
            clock.tick(60)
            #continuously update the state of the game with new objects and old objects new positions
            self.update()  

            current_time = pygame.time.get_ticks()
            if current_time - asteroid_timer >= self.asteroid_interval:
                self.asteroids.generate_asteroid(self.player_score)
                asteroid_timer = current_time
            self.render()  
            pygame.display.update() 

            if self.planet1_button.draw():
                Resume.resume_render()

            if self.planet2_button.draw():
                Resume.resume_render()

            if self.planet3_button.draw():
                Resume.resume_render()

            if self.planet4_button.draw():
                Resume.resume_render()

            if self.planet5_button.draw():
                Resume.resume_render()
                
            self.render()  

            #render the game objects on the screen
            pygame.display.update()  
            #update the display

            if self._paused:
                self.paused()
