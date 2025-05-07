import pygame
from snakebackend import SnakeGame
from snakeenums import CursorState as cursor
from snakeenums import DisplayState as disp

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
LINKED_IN_LOGO = pygame.image.load('./images/linkedin_pixel_logo_icon.png')
select_sound = pygame.mixer.Sound("./sounds/blipSelect.wav")
credits_sound = pygame.mixer.Sound("./sounds/credits.wav")

class SnakeMenu:
    # Constructor
    def __init__(self, snake_game: SnakeGame, screen, font_path, state=cursor.CURSOR_PLAY, curr_display=disp.MAIN_MENU_DISPLAY):
        self.snake_game = snake_game
        self.screen = screen
        self.font_path = font_path
        self.state = state
        self.curr_display = curr_display
        self.running = True
        self.exit = False
    
    # Draw text on the screen at coords (x,y) with a specified font size
    def draw_text(self, text, size, x, y):
        my_font = pygame.font.Font(self.font_path, size)
        text_surface = my_font.render(text, False, (0,0,0))
        self.screen.blit(text_surface, (x,y))

    # Create the menu
    def create_menu(self):
        self.draw_text("SNAKE", 120, 150, 120)
        self.draw_text("PLAY", 60, 270, 330)
        self.draw_text("CREDITS", 60, 225, 420)
        self.draw_text("QUIT", 60, 280, 510)
        pygame.display.flip()
    
    # Update the cursor
    def update_cursor(self):
        if self.state == cursor.CURSOR_PLAY:
            self.draw_text(">", 60, 220, 330)
        elif self.state == cursor.CURSOR_CREDITS:
            self.draw_text(">", 60, 175, 420)
        elif self.state == cursor.CURSOR_QUIT:
            self.draw_text(">", 60, 230, 510)
    
    # Display the main menu
    def main_menu(self):
        # initialize the menu environment
        self.screen.fill("lightgreen")
        self.update_cursor()
        self.create_menu()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select_sound)
                    if self.state == cursor.CURSOR_PLAY:
                        self.state = cursor.CURSOR_CREDITS
                    elif self.state == cursor.CURSOR_CREDITS:
                        self.state = cursor.CURSOR_QUIT
                    elif self.state == cursor.CURSOR_QUIT:
                        self.state = cursor.CURSOR_PLAY
                elif event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select_sound)
                    if self.state == cursor.CURSOR_PLAY:
                        self.state = cursor.CURSOR_QUIT
                    elif self.state == cursor.CURSOR_CREDITS:
                        self.state = cursor.CURSOR_PLAY
                    elif self.state == cursor.CURSOR_QUIT:
                        self.state = cursor.CURSOR_CREDITS
                elif event.key == pygame.K_RETURN:
                    if self.state == cursor.CURSOR_PLAY:
                        # Run the game
                        self.snake_game = SnakeGame(self.snake_game.screen, self.snake_game.speed, self.snake_game.tile_size)
                        self.snake_game.run()
                        self.curr_display = disp.GAME_OVER_DISPLAY
                    elif self.state == cursor.CURSOR_CREDITS:
                        pygame.mixer.Sound.play(credits_sound)
                        self.curr_display = disp.CREDITS_DISPLAY
                    elif self.state == cursor.CURSOR_QUIT:
                        self.exit = True
            elif event.type == pygame.QUIT:
                self.exit = True

            pygame.display.flip()
    
    # Display the credits
    def credits(self):
        self.screen.fill("lightgreen")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.curr_display = disp.MAIN_MENU_DISPLAY
            elif event.type == pygame.QUIT:
                self.exit = True
        
        self.draw_text("MADE BY", 40, 270, SCREEN_HEIGHT // 2 - 200)
        self.draw_text("JEFFREY THEWSUVAT :D", 40, 120, SCREEN_HEIGHT // 2 - 150)
        self.screen.blit(LINKED_IN_LOGO, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 50))
        self.draw_text("linkedin.com/in/jeffreythew", 30, 125, SCREEN_HEIGHT // 2 + 50)
        self.draw_text("Press any key to return", 30, 150, SCREEN_HEIGHT - 100)
        pygame.display.flip()
    
    # Display the game over screen
    def game_over(self):
        self.screen.fill("lightgreen")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.curr_display = disp.MAIN_MENU_DISPLAY
            elif event.type == pygame.QUIT:
                self.exit = True
        
        self.draw_text("GAME OVER!", 60, 165, SCREEN_HEIGHT // 2 - 150)
        self.draw_text("Your score:", 60, 155, SCREEN_HEIGHT // 2 - 50)
        self.draw_text("%d" %(self.snake_game.get_score()), 60, SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 50)
        self.draw_text("Press Enter to return", 30, 150, SCREEN_HEIGHT - 100)
        pygame.display.flip()

    # Run the menu
    def run(self):
        while self.running:
            if self.curr_display == disp.MAIN_MENU_DISPLAY:
                self.main_menu()
            elif self.curr_display == disp.CREDITS_DISPLAY:
                self.credits()
            elif self.curr_display == disp.GAME_OVER_DISPLAY:
                self.game_over()
            
            if self.exit:
                self.running = False