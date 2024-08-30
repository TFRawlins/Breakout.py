import pygame
import sys

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def handle_events(
    event,
    play_button_x,
    mouse_x,
    play_button_y,
    mouse_y,
    exit_button_x,
    exit_button_y,
    button_width,
    button_height,
):

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if (
            play_button_x <= mouse_x <= play_button_x + button_width
            and play_button_y <= mouse_y <= play_button_y + button_height
        ):
            return False

        if (
            exit_button_x <= mouse_x <= exit_button_x + button_width
            and exit_button_y <= mouse_y <= exit_button_y + button_height
        ):
            pygame.quit()
            sys.exit()
    return True


def main_menu():

    menu = True
    PLAY_BUTTON_COLOR = (61, 66, 242, 255)
    PLAY_BUTTON_HOVER_COLOR = (91, 96, 252, 255)
    TEXT_COLOR = (255, 255, 0)
    BORDER_COLOR = (255, 255, 255)

    EXIT_BUTTON_COLOR = (219, 69, 76, 255)
    EXIT_BUTTON_HOVER_COLOR = (222, 93, 141, 255)

    button_width = 200
    button_height = 50
    play_button_x = screen_width // 2 - button_width // 2
    play_button_y = screen_height // 2 + 50
    exit_button_x = screen_width // 2 - button_width // 2
    exit_button_y = play_button_y + button_height + 20

    while menu:

        for event in pygame.event.get():
            menu = handle_events(
                event,
                play_button_x,
                pygame.mouse.get_pos()[0],
                play_button_y,
                pygame.mouse.get_pos()[1],
                exit_button_x,
                exit_button_y,
                button_width,
                button_height,
            )
            print(menu)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if (
            play_button_x <= mouse_x <= play_button_x + button_width
            and play_button_y <= mouse_y <= play_button_y + button_height
        ):
            button_color = PLAY_BUTTON_HOVER_COLOR
        else:
            button_color = PLAY_BUTTON_COLOR

        if (
            exit_button_x <= mouse_x <= exit_button_x + button_width
            and exit_button_y <= mouse_y <= exit_button_y + button_height
        ):
            exit_button_color = EXIT_BUTTON_HOVER_COLOR
        else:
            exit_button_color = EXIT_BUTTON_COLOR

        screen.fill(BLACK)

        draw_text(
            screen,
            "BREAKOUT",
            pygame.font.Font(None, 74),
            WHITE,
            screen_width // 2,
            screen_height // 2 - 50,
        )

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            [
                play_button_x - 2,
                play_button_y - 2,
                button_width + 4,
                button_height + 4,
            ],
        )
        pygame.draw.rect(
            screen,
            button_color,
            [play_button_x, play_button_y, button_width, button_height],
        )
        draw_text(
            screen,
            "Play",
            pygame.font.Font(None, 50),
            TEXT_COLOR,
            screen_width // 2,
            screen_height // 2 + 75,
        )

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            [
                exit_button_x - 2,
                exit_button_y - 2,
                button_width + 4,
                button_height + 4,
            ],
        )
        pygame.draw.rect(
            screen,
            exit_button_color,
            [exit_button_x, exit_button_y, button_width, button_height],
        )
        draw_text(
            screen,
            "Exit",
            pygame.font.Font(None, 50),
            TEXT_COLOR,
            screen_width // 2,
            exit_button_y + 25,
        )

        pygame.display.flip()
        clock.tick(60)


def handle_ingame_events(
    event,
    continue_button_x,
    restart_button_x,
    mouse_x,
    continue_button_y,
    restart_button_y,
    mouse_y,
    exit_button_x,
    exit_button_y,
    button_width,
    button_height,
):

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if (
            continue_button_x <= mouse_x <= continue_button_x + button_width
            and continue_button_y
            <= mouse_y
            <= continue_button_y + button_height
        ):
            return "continue"
        if (
            restart_button_x <= mouse_x <= restart_button_x + button_width
            and restart_button_y <= mouse_y <= restart_button_y + button_height
        ):
            return "restart"
        if (
            exit_button_x <= mouse_x <= exit_button_x + button_width
            and exit_button_y <= mouse_y <= exit_button_y + button_height
        ):
            return "exit"


def handle_button_hover(
    mouse_x, mouse_y, button_x, button_y, button_width, button_height, type
):
    CONTINUE_BUTTON_COLOR = (61, 66, 242, 255)
    CONTINUE_BUTTON_HOVER_COLOR = (91, 96, 252, 255)
    RESTART_BUTTON_COLOR = (61, 66, 242, 255)
    RESTART_BUTTON_HOVER_COLOR = (91, 96, 252, 255)
    EXIT_BUTTON_COLOR = (219, 69, 76, 255)
    EXIT_BUTTON_HOVER_COLOR = (222, 93, 141, 255)

    colors_dict = {
        "continue": (CONTINUE_BUTTON_COLOR, CONTINUE_BUTTON_HOVER_COLOR),
        "restart": (RESTART_BUTTON_COLOR, RESTART_BUTTON_HOVER_COLOR),
        "exit": (EXIT_BUTTON_COLOR, EXIT_BUTTON_HOVER_COLOR),
    }

    if (
        button_x <= mouse_x <= button_x + button_width
        and button_y <= mouse_y <= button_y + button_height
    ):
        return colors_dict[type][1]
    return colors_dict[type][0]


def ingame_menu():
    TEXT_COLOR = (255, 255, 0)
    BORDER_COLOR = (255, 255, 255)

    button_width = 200
    button_height = 50
    continue_button_x = screen_width // 2 - button_width // 2
    continue_button_y = screen_height * 0.30
    restart_button_x = screen_width // 2 - button_width // 2
    restart_button_y = continue_button_y + button_height + 20
    exit_button_x = screen_width // 2 - button_width // 2
    exit_button_y = restart_button_y + button_height + 20

    ingame_menu = True
    while ingame_menu:

        for event in pygame.event.get():
            ingame_response = handle_ingame_events(
                event,
                continue_button_x,
                restart_button_x,
                pygame.mouse.get_pos()[0],
                continue_button_y,
                restart_button_y,
                pygame.mouse.get_pos()[1],
                exit_button_x,
                exit_button_y,
                button_width,
                button_height,
            )
            ingame_menu = (
                ingame_response != "continue" and ingame_response != "restart"
            )
            if ingame_response:
                return ingame_response
            print(ingame_menu)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        continue_button_color = handle_button_hover(
            mouse_x,
            mouse_y,
            continue_button_x,
            continue_button_y,
            button_width,
            button_height,
            "continue",
        )

        restart_button_color = handle_button_hover(
            mouse_x,
            mouse_y,
            restart_button_x,
            restart_button_y,
            button_width,
            button_height,
            "restart",
        )

        exit_button_color = handle_button_hover(
            mouse_x,
            mouse_y,
            exit_button_x,
            exit_button_y,
            button_width,
            button_height,
            "exit",
        )

        menu_surface = pygame.Surface(
            (screen_width, screen_height), pygame.SRCALPHA
        )
        menu_surface.fill((0, 0, 0, 50))
        screen.blit(menu_surface, (0, 0))

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            [
                continue_button_x - 2,
                continue_button_y - 2,
                button_width + 4,
                button_height + 4,
            ],
        )
        pygame.draw.rect(
            screen,
            continue_button_color,
            [
                continue_button_x,
                continue_button_y,
                button_width,
                button_height,
            ],
        )
        draw_text(
            screen,
            "Continue",
            pygame.font.Font(None, 50),
            TEXT_COLOR,
            screen_width // 2,
            continue_button_y + 25,
        )

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            [
                restart_button_x - 2,
                restart_button_y - 2,
                button_width + 4,
                button_height + 4,
            ],
        )
        pygame.draw.rect(
            screen,
            restart_button_color,
            [restart_button_x, restart_button_y, button_width, button_height],
        )
        draw_text(
            screen,
            "Restart",
            pygame.font.Font(None, 50),
            TEXT_COLOR,
            screen_width // 2,
            restart_button_y + 25,
        )

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            [
                exit_button_x - 2,
                exit_button_y - 2,
                button_width + 4,
                button_height + 4,
            ],
        )
        pygame.draw.rect(
            screen,
            exit_button_color,
            [exit_button_x, exit_button_y, button_width, button_height],
        )
        draw_text(
            screen,
            "Exit to Main Menu",
            pygame.font.Font(None, 30),
            TEXT_COLOR,
            screen_width // 2,
            exit_button_y + 25,
        )

        pygame.display.flip()
        clock.tick(60)
