import pygame
import random
import time
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 500
PIXEL_SIZE = 25

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PIXEL_SIZE, PIXEL_SIZE))

    def move(self, direction):
        if direction == 0:  # left
            self.x -= PIXEL_SIZE
        elif direction == 1:  # right
            self.x += PIXEL_SIZE
        
        #Braking

        # Prevent out of boundaries
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - PIXEL_SIZE:
            self.x = SCREEN_WIDTH - PIXEL_SIZE



class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def update(self):
        self.y += self.speed

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

    def collides_with(self, pixel):
        return (self.x < pixel.x + PIXEL_SIZE and
                self.x + self.width > pixel.x and
                self.y < pixel.y + PIXEL_SIZE and
                self.y + self.height > pixel.y)

def can_spawn_obstacle(x, y, obstacles, width, height):
    for obstacle in obstacles:
        if obstacle.x < x + width and obstacle.x + obstacle.width > x and obstacle.y < y + height and obstacle.y + obstacle.height > y:
            return False
    return True


# Initialization of neural network
model = Sequential()
model.add(Dense(24, input_shape=(2,), activation='relu'))
model.add(Dense(24, activation='relu'))
model.add(Dense(3, activation='linear'))  # 3 actions: left, right, brake
model.compile(optimizer=Adam(lr=0.001), loss='mse')

# Initialization of obstacles
obstacles = []


OBSTACLE_SPAWN_CHANCE = 1  # 10% chance to spawn an obstacle each second

# Main loop
last_check_time = time.time()
player = Pixel(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PIXEL_SIZE * 2)
running = True

while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Choose action
    action = random.choice([0, 1])  # Currently random


    # Check for obstacle generation
    current_time = time.time()
    if current_time - last_check_time >= 1:  # Check every second
        if random.random() < OBSTACLE_SPAWN_CHANCE:
            x, y = random.randint(0, SCREEN_WIDTH - PIXEL_SIZE), -PIXEL_SIZE
            if can_spawn_obstacle(x, y, obstacles, PIXEL_SIZE, PIXEL_SIZE):
                speed = random.randint(12, 16)
                obstacles.append(Obstacle(x, y, PIXEL_SIZE, PIXEL_SIZE, speed))
        last_check_time = current_time

    # Update and draw obstacles
    for obstacle in obstacles:
        obstacle.update()
        obstacle.draw()
        if obstacle.collides_with(player):
            print("Collision!")
            #running = False
        if obstacle.is_off_screen():
            obstacles.remove(obstacle)

    # Updating player
    player.move(action)
    player.draw()

    # Updating display
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()