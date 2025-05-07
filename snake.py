import pygame
from snakemenu import SnakeMenu
from snakebackend import SnakeGame

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

def main():
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    snakegame = SnakeGame(screen, 11, 48)
    menu = SnakeMenu(snakegame, screen, './fonts/slkscr.ttf')
    menu.run()

main()