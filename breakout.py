import pygame
import sys
from classes import (
    Paddle,
    Ball,
    Block,
    PowerUp,
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


def display_score(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))


def update_score(score, block):
    score += block.get_color() * 100
    return score


def game_loop():
    running = True
    paused = False

    score = 0

    header_height = 50
    frame_thickness = 11
    block_spacing_top = 30

    paddle, ball, blocks, all_sprites, lives = reset_game(
        screen_width,
        screen_height,
        frame_thickness,
        header_height,
        block_spacing_top,
    )

    block_columns = 8
    block_rows = 7
    block_width = (screen_width - frame_thickness * 2) // block_columns
    block_height = 20

    ball = Ball(screen_width, screen_height, frame_thickness, header_height)
    paddle = Paddle(screen_width, screen_height, frame_thickness)
    power_ups = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    for i in range(block_columns):
        for j in range(block_rows):
            block_x = frame_thickness + i * block_width
            block_y = (
                header_height
                + frame_thickness
                + block_spacing_top
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
            power_ups.update()

            if pygame.sprite.collide_rect(ball, paddle) and ball.y_speed > 0:
                centrality = calculate_bounce_centrality(ball, paddle)
                ball.paddle_bounce(centrality)
                if ball.y_speed > -1:
                    ball.y_speed = -1

            block_hit_list = pygame.sprite.spritecollide(ball, blocks, False)

            if block_hit_list:
                score = update_score(score, block_hit_list[0])
                for block in block_hit_list:
                    sideornot = check_block_collision(ball, block)
                    ball.block_bounce(sideornot)
                    if block.hit():
                        if PowerUp.should_spawn():
                            power_up = PowerUp(block.rect.x, block.rect.y)
                            power_ups.add(power_up)
                        block.kill()
                    
            for power_up in power_ups.copy():
                if power_up.rect.top > screen_height:
                    power_ups.remove(power_up)
                elif pygame.sprite.collide_rect(power_up, paddle):
                    lives += 1
                    power_ups.remove(power_up)

            ball_offset = 20
            if ball.rect.bottom + ball_offset > screen_height:
                print("Ball out of bounds")
                lives -= 1
                print(f"Lives: {lives}")
                if lives > 0:
                    ball = Ball(
                        screen_width,
                        screen_height,
                        frame_thickness,
                        header_height,
                    )
                    paddle = Paddle(
                        screen_width, screen_height, frame_thickness
                    )
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(paddle)
                    all_sprites.add(ball)
                    all_sprites.add(blocks)
                    power_ups.empty()
                else:
                    running = False
                    print("Game Over!")
                    return

            screen.fill(BLACK)

            pygame.draw.rect(
                screen,
                FRAME_COLOR,
                (0, header_height, screen_width, frame_thickness),
            )
            pygame.draw.rect(
                screen,
                FRAME_COLOR,
                (
                    0,
                    screen_height - frame_thickness,
                    screen_width,
                    frame_thickness,
                ),
            )
            pygame.draw.rect(
                screen,
                FRAME_COLOR,
                (
                    0,
                    header_height,
                    frame_thickness,
                    screen_height - header_height,
                ),
            )
            pygame.draw.rect(
                screen,
                FRAME_COLOR,
                (
                    screen_width - frame_thickness - 1,
                    header_height,
                    frame_thickness + 1,
                    screen_height - header_height,
                ),
            )
            pygame.draw.rect(
                screen, (0, 0, 0), (0, 0, screen_width, header_height)
            )

            display_lives(screen, lives, screen_width)
            display_score(screen, score)

            all_sprites.draw(screen)
            power_ups.draw(screen)
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
                    frame_thickness,
                    header_height,
                    block_spacing_top,
                )
                power_ups.empty()
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
    frame_thickness,
    header_height,
    block_spacing_top,
):

    paddle = Paddle(screen_width, screen_height, frame_thickness)
    ball = Ball(screen_width, screen_height, frame_thickness, header_height)

    blocks = pygame.sprite.Group()
    block_columns = 8
    block_rows = 7
    block_width = (screen_width - frame_thickness * 2) // block_columns
    block_height = 20
    for i in range(block_columns):
        for j in range(block_rows):
            block_x = frame_thickness + i * block_width
            block_y = (
                header_height
                + frame_thickness
                + block_spacing_top
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
