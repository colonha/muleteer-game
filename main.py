import pygame
from pygame.locals import *
import random

pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (50, 50, 50)  # Gray color

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Muleteer Adventure')

class Muleteer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50
        self.velocity = 5

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 0), (self.x, self.y, self.size, self.size))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.x > 0:  # added boundary check
            self.x -= self.velocity
        if keys[K_RIGHT] and self.x + self.size < WIDTH:  # added boundary check
            self.x += self.velocity
        if keys[K_UP] and self.y > 0:  # added boundary check
            self.y -= self.velocity
        if keys[K_DOWN] and self.y + self.size < HEIGHT:  # added boundary check
            self.y += self.velocity

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = -5

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.velocity

obstacles = []
def create_obstacle():
    if random.randint(0, 100) < 10:  # 10% chance every frame to create an obstacle
        width = random.randint(20, 60)
        height = random.randint(20, 40)
        new_obstacle = Obstacle(WIDTH, HEIGHT-height, width, height)
        obstacles.append(new_obstacle)

def check_collision(character, obstacle):
    return (character.x < obstacle.x + obstacle.width and 
            character.x + character.size > obstacle.x and 
            character.y < obstacle.y + obstacle.height and 
            character.size + character.y > obstacle.y)

muleteer = Muleteer(WIDTH//2, HEIGHT-60)

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
    muleteer.move()
    muleteer.draw(screen)
    
    create_obstacle()
    for obstacle in obstacles:
        obstacle.move()
        obstacle.draw(screen)
        if check_collision(muleteer, obstacle):
            running = False  # end game for now
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limiting our game to run at 60 frames per second.

pygame.quit()

