import pygame
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Параметри гри
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PIXEL_SIZE = 50
FALL_SPEED = 5

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PIXEL_SIZE, PIXEL_SIZE))

    def move(self, direction):
        if direction == 0:  # вліво
            self.x -= PIXEL_SIZE
        elif direction == 1:  # вправо
            self.x += PIXEL_SIZE
        # Не реалізовано гальмування

        # Запобігання виходу за межі екрану
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - PIXEL_SIZE:
            self.x = SCREEN_WIDTH - PIXEL_SIZE

# Ініціалізація нейронної мережі
model = Sequential()
model.add(Dense(24, input_shape=(2,), activation='relu'))
model.add(Dense(24, activation='relu'))
model.add(Dense(3, activation='linear'))  # 3 дії: вліво, вправо, гальмування
model.compile(optimizer=Adam(lr=0.001), loss='mse')

# Головний цикл гри
player = Pixel(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PIXEL_SIZE * 2)
running = True
while running:
    screen.fill(BLACK)
    
    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Вибір дії (потрібно інтегрувати з моделлю RL)
    action = random.choice([0, 1])  # Наразі випадковий вибір

    # Оновлення стану гри
    player.move(action)
    player.draw()

    # Оновлення екрану
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()