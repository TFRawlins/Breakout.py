import pygame
import sys

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



# Funcion para dibujar el texto
def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main_menu():
    
    PLAY_BUTTON_COLOR = (61, 66, 242, 255) 
    PLAY_BUTTON_HOVER_COLOR = (8, 236, 239, 255)
    TEXT_COLOR = (255, 255, 0)  
    BORDER_COLOR = (255, 255, 255) 
    
    EXIT_BUTTON_COLOR = (219, 69, 76, 255)
    EXIT_BUTTON_HOVER_COLOR = (222, 93, 141, 255)

    
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_x <= mouse_x <= play_button_x + button_width and play_button_y <= mouse_y <= play_button_y + button_height:
                    menu = False
                    
                if exit_button_x <= mouse_x <= exit_button_x + button_width and exit_button_y <= mouse_y <= exit_button_y + button_height:
                    pygame.quit()
                    sys.exit()
                
        # Obtener la posición del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Definir la posición y dimensiones del botón
        button_width = 200
        button_height = 50
        play_button_x = screen_width // 2 - button_width // 2
        play_button_y = screen_height // 2 + 50
        exit_button_x = screen_width // 2 - button_width // 2
        exit_button_y = play_button_y + button_height + 20


        # Verificar si el mouse está sobre el botón
        if play_button_x <= mouse_x <= play_button_x + button_width and play_button_y <= mouse_y <= play_button_y + button_height:
            button_color = PLAY_BUTTON_HOVER_COLOR
        else:
            button_color = PLAY_BUTTON_COLOR
            
        if exit_button_x <= mouse_x <= exit_button_x + button_width and exit_button_y <= mouse_y <= exit_button_y + button_height:
            exit_button_color = EXIT_BUTTON_HOVER_COLOR
        else:
            exit_button_color = EXIT_BUTTON_COLOR

        # Dibujar la pantalla de fondo
        screen.fill(BLACK)

        # Dibujar el texto "BREAKOUT"
        draw_text(screen, "BREAKOUT", pygame.font.Font(None, 74), WHITE, screen_width // 2, screen_height // 2 - 50)

        # Dibujar boton "Play"
        pygame.draw.rect(screen, BORDER_COLOR, [play_button_x - 2, play_button_y - 2, button_width + 4, button_height + 4])
        pygame.draw.rect(screen, button_color, [play_button_x, play_button_y, button_width, button_height])
        draw_text(screen, "Play", pygame.font.Font(None, 50), TEXT_COLOR, screen_width // 2, screen_height // 2 + 75)

        # Dibujar el borde y el botón "Exit"
        pygame.draw.rect(screen, BORDER_COLOR, [exit_button_x - 2, exit_button_y - 2, button_width + 4, button_height + 4])
        pygame.draw.rect(screen, exit_button_color, [exit_button_x, exit_button_y, button_width, button_height])
        draw_text(screen, "Exit", pygame.font.Font(None, 50), TEXT_COLOR, screen_width // 2, exit_button_y + 25)


        pygame.display.flip()
        clock.tick(60)
        
        
def ingame_menu():
    CONTINUE_BUTTON_COLOR = (61, 66, 242, 255)
    CONTINUE_BUTTON_HOVER_COLOR = (8, 236, 239, 255)
    
    RESTART_BUTTON_COLOR = (61, 66, 242, 255)
    RESTART_BUTTON_HOVER_COLOR = (8, 236, 239, 255)
    EXIT_BUTTON_COLOR = (219, 69, 76, 255)
    EXIT_BUTTON_HOVER_COLOR = (222, 93, 141, 255)
    TEXT_COLOR = (255, 255, 0)
    BORDER_COLOR = (255, 255, 255)

    ingame_menu = True
    while ingame_menu:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_x <= mouse_x <= continue_button_x + button_width and continue_button_y <= mouse_y <= continue_button_y + button_height:
                    ingame_menu = False
                    return 'continue'
                if restart_button_x <= mouse_x <= restart_button_x + button_width and restart_button_y <= mouse_y <= restart_button_y + button_height:
                    ingame_menu = False
                    return 'restart'
                if exit_button_x <= mouse_x <= exit_button_x + button_width and exit_button_y <= mouse_y <= exit_button_y + button_height:
                    return 'exit'

        # Definir la posición y dimensiones de los botones
        button_width = 200
        button_height = 50
        continue_button_x = screen_width // 2 - button_width // 2
        continue_button_y = screen_height * 0.30
        restart_button_x = screen_width // 2 - button_width // 2
        restart_button_y = continue_button_y + button_height + 20
        exit_button_x = screen_width // 2 - button_width // 2
        exit_button_y = restart_button_y + button_height + 20

        # Verificar si el mouse está sobre el botón "Continue"
        if continue_button_x <= mouse_x <= continue_button_x + button_width and continue_button_y <= mouse_y <= continue_button_y + button_height:
            continue_button_color = CONTINUE_BUTTON_HOVER_COLOR
        else:
            continue_button_color = CONTINUE_BUTTON_COLOR

        # Verificar si el mouse está sobre el botón "Restart"
        if restart_button_x <= mouse_x <= restart_button_x + button_width and restart_button_y <= mouse_y <= restart_button_y + button_height:
            restart_button_color = RESTART_BUTTON_HOVER_COLOR
        else:
            restart_button_color = RESTART_BUTTON_COLOR

        # Verificar si el mouse está sobre el botón "Exit to Main Menu"
        if exit_button_x <= mouse_x <= exit_button_x + button_width and exit_button_y <= mouse_y <= exit_button_y + button_height:
            exit_button_color = EXIT_BUTTON_HOVER_COLOR
        else:
            exit_button_color = EXIT_BUTTON_COLOR

        # Crear una superficie para el fondo del menú
        menu_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        menu_surface.fill((0, 0, 0, 150))
        screen.blit(menu_surface, (0, 0))

        # Dibujar el borde y el botón "Continue"
        pygame.draw.rect(screen, BORDER_COLOR, [continue_button_x - 2, continue_button_y - 2, button_width + 4, button_height + 4])
        pygame.draw.rect(screen, continue_button_color, [continue_button_x, continue_button_y, button_width, button_height])
        draw_text(screen, "Continue", pygame.font.Font(None, 50), TEXT_COLOR, screen_width // 2, continue_button_y + 25)

        # Dibujar el borde y el botón "Restart"
        pygame.draw.rect(screen, BORDER_COLOR, [restart_button_x - 2, restart_button_y - 2, button_width + 4, button_height + 4])
        pygame.draw.rect(screen, restart_button_color, [restart_button_x, restart_button_y, button_width, button_height])
        draw_text(screen, "Restart", pygame.font.Font(None, 50), TEXT_COLOR, screen_width // 2, restart_button_y + 25)

        # Dibujar el borde y el botón "Exit to Main Menu"
        pygame.draw.rect(screen, BORDER_COLOR, [exit_button_x - 2, exit_button_y - 2, button_width + 4, button_height + 4])
        pygame.draw.rect(screen, exit_button_color, [exit_button_x, exit_button_y, button_width, button_height])
        draw_text(screen, "Exit to Main Menu", pygame.font.Font(None, 30), TEXT_COLOR, screen_width // 2, exit_button_y + 25)

        pygame.display.flip()
        clock.tick(60)