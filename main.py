author = 'Saksham Singh'

# Importing the Modules
import pygame
import random
import os
import sys

# Initialization
pygame.init()
pygame.mixer.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
snakegreen = (35, 45, 40)

# Screen dimensions
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake By Saksham")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 35)

# Load image with fallback
def load_image(path, fallback_color=(200, 200, 200)):
    try:
        return pygame.image.load(path).convert()
    except Exception as e:
        print(f"Error loading {path}: {e}")
        fallback = pygame.Surface((screen_width, screen_height))
        fallback.fill(fallback_color)
        return fallback

# Load images
bg2 = load_image("Screen/bg2.png")
intro = load_image("Screen/intro1.png")
outro = load_image("Screen/outro.png")

# Play music
def play_music(path, volume=0.6, loop=True):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1 if loop else 0)
        pygame.mixer.music.set_volume(volume)
    except Exception as e:
        print(f"Error loading music {path}: {e}")

# Score helpers
def load_highscore():
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        return int(f.read())

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Text display
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Draw snake
def plot_snake(win, color, snk_list, size):
    for x, y in snk_list:
        pygame.draw.rect(win, color, [x, y, size, size])

# Welcome screen
def welcome():
    play_music("music/wc.mp3")
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0, 0))
        text_screen("Press ENTER to Start", black, 300, 500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.fadeout(300)
                play_music("music/bgm.mp3")
                gameloop()
        pygame.display.update()
        clock.tick(60)

# Main game loop
def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_size = 30
    init_velocity = 5
    fps = 60
    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)
    score = 0
    snk_list = []
    snk_length = 1
    highscore = load_highscore()

    while not exit_game:
        if game_over:
            save_highscore(highscore)
            gameWindow.blit(outro, (0, 0))
            text_screen(f"Score: {score}", snakegreen, 385, 350)
            text_screen("Press ENTER to Restart", red, 290, 400)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and velocity_x == 0:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT and velocity_x == 0:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP and velocity_y == 0:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN and velocity_y == 0:
                        velocity_y = init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_q:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            # Food collision
            if abs(snake_x - food_x) < snake_size and abs(snake_y - food_y) < snake_size:
                score += 10
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
                snk_length += 5
                if score > highscore:
                    highscore = score

            gameWindow.blit(bg2, (0, 0))
            text_screen(f"Score: {score}  Highscore: {highscore}", snakegreen, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Collision with self
            if head in snk_list[:-1]:
                game_over = True
                play_music("music/bgm1.mp3")

            # Collision with wall
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                play_music("music/bgm2.mp3")

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

# Start the game
welcome()
