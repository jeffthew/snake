#!/usr/bin/python
import pygame
import random
from snakeenums import Directions as dir
pygame.mixer.init()

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
eat_sound = pygame.mixer.Sound("./sounds/pickupCoin.wav")
crash_sound = pygame.mixer.Sound("./sounds/explosion.wav")

# Implement the snake as a linked list
class SnakePixel:
    def __init__(self, rectangle, nextPixel, x, y):
        self.rectangle = rectangle
        self.nextPixel = nextPixel
        self.x = x
        self.y = y

class SnakeGame:
    # Constructor
    def __init__(self, screen, speed, tile_size=30, direction=dir.RIGHT):
        self.screen = screen
        self.speed = speed
        self.tile_size = tile_size
        self.direction = direction
        self.food_x = 0
        self.food_y = 0
        self.food_exists = False
        self.score = 0

        # Create the initial body of the snake
        self.curr_pos = pygame.Vector2(96, 96)

        body2 = pygame.Rect(self.curr_pos.x - 2*self.tile_size,self.curr_pos.y,self.tile_size,self.tile_size)
        bodypart2 = SnakePixel(body2, None, self.curr_pos.x - 2*self.tile_size, self.curr_pos.y)

        body1 = pygame.Rect(self.curr_pos.x - self.tile_size,self.curr_pos.y,self.tile_size,self.tile_size)
        bodypart1 = SnakePixel(body1, bodypart2, self.curr_pos.x - self.tile_size, self.curr_pos.y)

        head = pygame.Rect(self.curr_pos.x,self.curr_pos.y,self.tile_size,self.tile_size)
        self.snake = SnakePixel(head, bodypart1, self.curr_pos.x, self.curr_pos.y)
        
    
    # Create grid
    def draw_grid(self):
        # Fill the screen
        self.screen.fill("lightgreen")

        # Draw vertical lines
        for x in range(self.tile_size, SCREEN_WIDTH, self.tile_size):
            pygame.draw.line(self.screen, "darkgreen", (x, 0), (x, SCREEN_HEIGHT))

        # Draw horizontal lines
        for y in range(self.tile_size, SCREEN_HEIGHT, self.tile_size):
            pygame.draw.line(self.screen, "darkgreen", (0, y), (SCREEN_WIDTH, y))
    
    # Draw the snake
    def draw_snake(self):
        curr = self.snake
        while curr != None:
            pygame.draw.rect(self.screen, "black", curr.rectangle)
            curr = curr.nextPixel
    
    # Update the snake's movement and position 
    def update_snake(self) -> SnakePixel:
        curr = self.snake
        rect = pygame.Rect(self.curr_pos.x, self.curr_pos.y, self.tile_size, self.tile_size)
        new_head = SnakePixel(rect, curr, self.curr_pos.x, self.curr_pos.y)
        food_not_eaten = True

        while curr != None:
            if curr.nextPixel != None:
                if curr.nextPixel.nextPixel == None:
                    if self.curr_pos.x == self.food_x and self.curr_pos.y == self.food_y:
                        new_rect = pygame.Rect(curr.nextPixel.x, curr.nextPixel.y, self.tile_size, self.tile_size)
                        curr.nextPixel = SnakePixel(new_rect, None, curr.nextPixel.x, curr.nextPixel.y)
                        # play eating sound
                        pygame.mixer.Sound.play(eat_sound)
                        self.score += 5
                        food_not_eaten = False
                    else:
                        curr.nextPixel = None

            curr = curr.nextPixel
        return (new_head, food_not_eaten)
    
    # Get score
    def get_score(self):
        return self.score
    
    # Get the current position of the snake
    def get_snake_positions(self) -> list[(float, float)]:
        curr = self.snake
        positions = []
        while curr != None:
            positions.append((curr.x, curr.y))
            curr = curr.nextPixel
        
        return positions
    
    # Generate food coordinates for the next food generation
    def generate_food_coords(self):
        food_x = 0
        food_y = 0
        positions = self.get_snake_positions()
        food_placed = False
        
        while not food_placed:
            # Generate a random x coordinate (multiple of self.tile_size)    
            food_x = random.randrange(self.tile_size, SCREEN_WIDTH, self.tile_size)

            # Generate a random y coordinate (multiple of self.tile_size)
            food_y = random.randrange(self.tile_size, SCREEN_HEIGHT, self.tile_size)

            # Check if food is located inside the snake
            if (food_x, food_y) not in positions:
                food_placed = True
        
        return (food_x, food_y)

    # Run the actual snake gameplay
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.draw_grid()
            self.draw_snake()

            if not self.food_exists:
                (self.food_x, self.food_y) = self.generate_food_coords()
                self.food_exists = True
            
            # Draw food
            apple = pygame.image.load('./images/apple.png')
            self.screen.blit(apple, (self.food_x, self.food_y))
            #pygame.draw.rect(self.screen, "red", pygame.Rect(self.food_x, self.food_y, self.tile_size, self.tile_size))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.direction != dir.DOWN:
                self.direction = dir.UP
            elif keys[pygame.K_DOWN] and self.direction != dir.UP:
                self.direction = dir.DOWN
            elif keys[pygame.K_LEFT] and self.direction != dir.RIGHT:
                self.direction = dir.LEFT
            elif keys[pygame.K_RIGHT] and self.direction != dir.LEFT:
                self.direction = dir.RIGHT

            if self.direction == dir.UP:
                self.curr_pos.y -= self.tile_size
            elif self.direction == dir.DOWN:
                self.curr_pos.y += self.tile_size
            elif self.direction == dir.LEFT:
                self.curr_pos.x -= self.tile_size
            elif self.direction == dir.RIGHT:
                self.curr_pos.x += self.tile_size
            
            (self.snake, self.food_exists) = self.update_snake()

            # Collisions with snake body --> Game over
            if (self.curr_pos.x, self.curr_pos.y) in self.get_snake_positions()[1:]:
                pygame.mixer.Sound.play(crash_sound)
                running = False

            # Snake out of bounds --> Game over
            if (self.curr_pos.x >= SCREEN_WIDTH or self.curr_pos.x < 0 or self.curr_pos.y >= SCREEN_HEIGHT or self.curr_pos.y < 0):
                pygame.mixer.Sound.play(crash_sound)
                running = False

            pygame.display.flip()
            pygame.time.Clock().tick(self.speed)