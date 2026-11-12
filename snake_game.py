
import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH = 600
HEIGHT = 600
CELL = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Muhammad Anas")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

# Colors
BLACK = (20, 20, 20)
GREEN = (0, 200, 80)
DARK_GREEN = (0, 120, 50)
RED = (230, 50, 50)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
YELLOW = (240, 200, 40)

# Obstacles are stored as grid coordinates
OBSTACLES = [
    (5, 5), (6, 5), (7, 5),
    (15, 8), (15, 9), (15, 10),
    (5, 17), (6, 17), (7, 17)
]


def create_food(snake):
    while True:
        position = (
            random.randrange(0, WIDTH // CELL),
            random.randrange(0, HEIGHT // CELL)
        )
        if position not in snake and position not in OBSTACLES:
            return position


def reset_game():
    snake = [(10, 10), (9, 10), (8, 10)]
    direction = (1, 0)
    food = create_food(snake)
    score = 0
    return snake, direction, food, score


def draw_text(message, y, selected_font=font, color=WHITE):
    text = selected_font.render(message, True, color)
    rect = text.get_rect(center=(WIDTH // 2, y))
    screen.blit(text, rect)


snake, direction, food, score = reset_game()
paused = False
game_over = False
running = True

while running:

    # Handle keyboard and window events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_p and not game_over:
                paused = not paused

            if event.key == pygame.K_r and game_over:
                snake, direction, food, score = reset_game()
                game_over = False
                paused = False

            if not paused and not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)

                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)

                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)

                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

    # Update game
    if not paused and not game_over:

        head_x, head_y = snake[0]
        new_head = (
            head_x + direction[0],
            head_y + direction[1]
        )

        # Wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH // CELL
            or new_head[1] < 0
            or new_head[1] >= HEIGHT // CELL
        ):
            game_over = True

        # Self and obstacle collision
        elif new_head in snake[:-1] or new_head in OBSTACLES:
            game_over = True

        else:
            snake.insert(0, new_head)

            # Food collection
            if new_head == food:
                score += 10
                food = create_food(snake)
            else:
                snake.pop()

    # Draw background
    screen.fill(BLACK)

    # Draw grid
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (35, 35, 35), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (35, 35, 35), (0, y), (WIDTH, y))

    # Draw obstacles
    for block in OBSTACLES:
        pygame.draw.rect(
            screen, GRAY,
            (block[0] * CELL, block[1] * CELL, CELL, CELL)
        )

    # Draw snake
    for index, segment in enumerate(snake):
        color = GREEN if index == 0 else DARK_GREEN
        pygame.draw.rect(
            screen, color,
            (segment[0] * CELL, segment[1] * CELL, CELL - 2, CELL - 2)
        )

    # Draw food
    pygame.draw.rect(
        screen, RED,
        (food[0] * CELL, food[1] * CELL, CELL - 2, CELL - 2)
    )

    # Score and controls
    draw_text(f"Score: {score}", 20, small_font, YELLOW)

    if paused:
        draw_text("GAME PAUSED", HEIGHT // 2)
        draw_text("Press P to Resume", HEIGHT // 2 + 40, small_font)

    if game_over:
        draw_text("GAME OVER!", HEIGHT // 2 - 30, font, RED)
        draw_text(f"Final Score: {score}", HEIGHT // 2 + 10)
        draw_text("Press R to Restart or ESC to Exit",
                  HEIGHT // 2 + 55, small_font)

    pygame.display.flip()

    # Speed increases with score, up to 20 FPS
    speed = min(8 + score // 50, 20)
    clock.tick(speed)

pygame.quit()
sys.exit()
