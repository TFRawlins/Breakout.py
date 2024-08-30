import pygame
import sys
from classes import (
    Paddle,
    Ball,
    Block,
    calculate_bounce_centrality,
    check_block_collision,
)
from menu_functions import main_menu, ingame_menu

pygame.init()
# ignore

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")

BLACK = (0, 0, 0)
FRAME_COLOR = (150, 150, 150)

clock = pygame.time.Clock()
blocks = pygame.sprite.Group()

block_width = 75
block_height = 20


def display_lives(screen, lives, screen_width):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(text, (screen_width - 120, 10))


def game_loop():
    running = True
    paused = False

    HEADER_HEIGHT = 50
    FRAME_THICKNESS = 11
    BLOCK_SPACING_TOP = 30

    paddle, ball, blocks, all_sprites, lives = reset_game(
        screen_width,
        screen_height,
        FRAME_THICKNESS,
        HEADER_HEIGHT,
        BLOCK_SPACING_TOP,
    )

    block_columns = 8
    block_rows = 7
    block_width = (screen_width - FRAME_THICKNESS * 2) // block_columns
    block_height = 20

    ball = Ball(screen_width, screen_height, FRAME_THICKNESS, HEADER_HEIGHT)
    paddle = Paddle(screen_width, screen_height, FRAME_THICKNESS)

    blocks = pygame.sprite.Group()
    for i in range(block_columns):
        for j in range(block_rows):
            block_x = FRAME_THICKNESS + i * block_width
            block_y = (
                HEADER_HEIGHT
                + FRAME_THICKNESS
                + BLOCK_SPACING_TOP
                + j * block_height
            )
            block = Block(block_x, block_y, block_width, block_height, j)
            blocks.add(block)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    all_sprites.add(blocks)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused

        if not paused:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move(-1)
            if keys[pygame.K_RIGHT]:
                paddle.move(1)

            ball.update()

            if pygame.sprite.collide_rect(ball, paddle):
                if ball.y_speed > 0:
                    centrality = calculate_bounce_centrality(ball, paddle)
                    ball.paddle_bounce(centrality)

            block_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
            if block_hit_list:
                sideornot = check_block_collision(ball, block_hit_list[0])
                ball.block_bounce(sideornot)

            ball_offset = 20
            if ball.rect.bottom + ball_offset > screen_height:
                print("Ball out of bounds")
                lives -= 1
                print(f"Lives: {lives}")
                if lives > 0:
                    # Reset ball and paddle positions
                    _lives = lives
                    paddle, ball, blocks, all_sprites, _lives = reset_game(
                        screen_width,
                        screen_height,
                        FRAME_THICKNESS,
                        HEADER_HEIGHT,
                        BLOCK_SPACING_TOP,
                    )
                else:
                    # Game over
                    running = False
                    print("Game Over!")
                    return
            screen.fill(BLACK)

            pygame.draw.rect(
                screen,
                FRAME_COLOR,
                (0, HEADER_HEIGHT, screen_width, FRAME_THICKNESS),
            )
            pygame.draw.rect(
                screen,
                FRAME_COLOR,
                (
                    0,
                    screen_height - FRAME_THICKNESS,
                    screen_width,
                    FRAME_THICKNESS,
                ),
            )
            pygame.draw.rect(
                screen,
                FRAME_COLOR,
                (
                    0,
                    HEADER_HEIGHT,
                    FRAME_THICKNESS,
                    screen_height - HEADER_HEIGHT,
                ),
            )
            pygame.draw.rect(
                screen,
                FRAME_COLOR,
                (
                    screen_width - FRAME_THICKNESS - 1,
                    HEADER_HEIGHT,
                    FRAME_THICKNESS + 1,
                    screen_height - HEADER_HEIGHT,
                ),
            )
            pygame.draw.rect(
                screen, (0, 0, 0), (0, 0, screen_width, HEADER_HEIGHT)
            )

            display_lives(screen, lives, screen_width)

            all_sprites.draw(screen)
            pygame.display.flip()

        else:
            action = ingame_menu()
            print(action)
            if action == "continue":
                paused = False
            elif action == "restart":
                paddle, ball, blocks, all_sprites, lives = reset_game(
                    screen_width,
                    screen_height,
                    FRAME_THICKNESS,
                    HEADER_HEIGHT,
                    BLOCK_SPACING_TOP,
                )
                paused = False
            elif action == "exit":
                return

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def reset_game(
    screen_width,
    screen_height,
    FRAME_THICKNESS,
    HEADER_HEIGHT,
    BLOCK_SPACING_TOP,
):

    paddle = Paddle(screen_width, screen_height, FRAME_THICKNESS)
    ball = Ball(screen_width, screen_height, FRAME_THICKNESS, HEADER_HEIGHT)

    blocks = pygame.sprite.Group()
    block_columns = 8
    block_rows = 7
    block_width = (screen_width - FRAME_THICKNESS * 2) // block_columns
    block_height = 20
    for i in range(block_columns):
        for j in range(block_rows):
            block_x = FRAME_THICKNESS + i * block_width
            block_y = (
                HEADER_HEIGHT
                + FRAME_THICKNESS
                + BLOCK_SPACING_TOP
                + j * block_height
            )
            block = Block(block_x, block_y, block_width, block_height, j)
            blocks.add(block)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    all_sprites.add(blocks)

    lives = 3
    return paddle, ball, blocks, all_sprites, lives


while True:
    main_menu()
    game_loop()
