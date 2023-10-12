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
    size = 50
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50
        
        self.velocity_x = 4
        self.velocity_y = 0  # Vertical velocity, affected by gravity and jumps
        self.gravity = 1
        self.jump_strength = -18  # Negative because a jump goes upwards
#        self.ground = HEIGHT - self.size  # The "floor" where the muleteer stands
        self.ground = HEIGHT  # The "floor" where the muleteer stands

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 0), (self.x, self.y, self.size, self.size))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.x > 0:
            self.x -= self.velocity_x
        if keys[K_RIGHT] and self.x + self.size < WIDTH:
            self.x += self.velocity_x
        
        # Apply gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Ground collision
        if self.y + self.size > self.ground:
            self.y = self.ground - self.size
            self.velocity_y = 0

    def jump(self):
        if self.y + self.size == self.ground:  # Ensure muleteer is on the ground before allowing a jump
            self.velocity_y += self.jump_strength

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
    min_space = 100  # Minimum space between obstacles
    if obstacles and (WIDTH - (obstacles[-1].x + obstacles[-1].width)) < min_space:
        return  # Do not create a new obstacle if the last one is too close to the edge
    if random.randint(0, 100) < 10:  # 10% chance every frame to create an obstacle
        width = random.randint(50, 80)
        height = 50
        new_obstacle = Obstacle(WIDTH, HEIGHT-height, width, height)
        obstacles.append(new_obstacle)

def check_collision(character, obstacle):
    return (character.x < obstacle.x + obstacle.width and 
            character.x + character.size > obstacle.x and 
            character.y < obstacle.y + obstacle.height and 
            character.size + character.y > obstacle.y)

muleteer = Muleteer(WIDTH//2, HEIGHT - Muleteer.size)

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                muleteer.jump()

            
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

