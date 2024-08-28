import pygame
import sys
from classes import Paddle, Ball, Block
from menu_functions import main_menu, ingame_menu

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")

# Colores
BLACK = (0, 0, 0)
FRAME_COLOR = (150, 150, 150)

# Velocidad del juego
clock = pygame.time.Clock()
blocks = pygame.sprite.Group()

block_width = 75
block_height = 20

def game_loop():
    running = True
    paused = False
    lives = 3
    
    HEADER_HEIGHT = 50
    FRAME_THICKNESS = 11
    BLOCK_SPACING_TOP = 30
    
    paddle, ball, blocks, all_sprites, lives = reset_game(screen_width, screen_height, FRAME_THICKNESS, HEADER_HEIGHT, BLOCK_SPACING_TOP)
    
    # Calcular el número de bloques que caben en la pantalla
    block_columns = 8
    block_rows = 7
    block_width = (screen_width - FRAME_THICKNESS * 2) // block_columns
    block_height = 20
    
    ball = Ball(screen_width, screen_height, FRAME_THICKNESS, HEADER_HEIGHT)
    paddle = Paddle(screen_width, screen_height, FRAME_THICKNESS)
    
    # Crear los bloques
    blocks = pygame.sprite.Group()
    for i in range(block_columns):
        for j in range(block_rows):
            block_x = FRAME_THICKNESS + i * block_width
            block_y = HEADER_HEIGHT + FRAME_THICKNESS + BLOCK_SPACING_TOP + j * block_height
            block = Block(block_x, block_y, block_width, block_height, j)
            blocks.add(block)

    # Crear el grupo de todos los sprites
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
            # Movimiento de la paleta
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move(-1)
            if keys[pygame.K_RIGHT]:
                paddle.move(1)

            # Actualizar la posición de la bola
            ball.update()

            # Colisión entre la bola y la paleta
            if pygame.sprite.collide_rect(ball, paddle):
                ball.bounce()

            # Colisión entre la bola y los bloques
            block_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
            if block_hit_list:
                ball.bounce()

            screen.fill(BLACK)

            # Dibujar el marco
            pygame.draw.rect(screen, FRAME_COLOR, (0, HEADER_HEIGHT, screen_width, FRAME_THICKNESS))
            pygame.draw.rect(screen, FRAME_COLOR, (0, screen_height - FRAME_THICKNESS, screen_width, FRAME_THICKNESS))
            pygame.draw.rect(screen, FRAME_COLOR, (0, HEADER_HEIGHT, FRAME_THICKNESS, screen_height - HEADER_HEIGHT))
            pygame.draw.rect(screen, FRAME_COLOR, (screen_width - FRAME_THICKNESS - 1, HEADER_HEIGHT, FRAME_THICKNESS + 1, screen_height - HEADER_HEIGHT))

            # Dibujar la sección superior
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_width, HEADER_HEIGHT))

            all_sprites.draw(screen)
            pygame.display.flip()

        else:
            action = ingame_menu()
            if action == 'continue':
                paused = False
            elif action == 'restart':
                paddle, ball, blocks, all_sprites, lives = reset_game(screen_width, screen_height, FRAME_THICKNESS, HEADER_HEIGHT, BLOCK_SPACING_TOP)
                paused = False
            elif action == 'exit':
                return

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def reset_game(screen_width, screen_height, FRAME_THICKNESS, HEADER_HEIGHT, BLOCK_SPACING_TOP):
    # Reinicializar la paleta
    paddle = Paddle(screen_width, screen_height, FRAME_THICKNESS)

    # Reinicializar la bola
    ball = Ball(screen_width, screen_height, FRAME_THICKNESS, HEADER_HEIGHT)

    # Reinicializar los bloques
    blocks = pygame.sprite.Group()
    block_columns = 8
    block_rows = 7
    block_width = (screen_width - FRAME_THICKNESS * 2) // block_columns
    block_height = 20
    for i in range(block_columns):
        for j in range(block_rows):
            block_x = FRAME_THICKNESS + i * block_width
            block_y = HEADER_HEIGHT + FRAME_THICKNESS + BLOCK_SPACING_TOP + j * block_height
            block = Block(block_x, block_y, block_width, block_height, j)
            blocks.add(block)

    # Crear el grupo de todos los sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    all_sprites.add(blocks)

    lives = 3
    return paddle, ball, blocks, all_sprites, lives

while True:
    main_menu()
    game_loop()


