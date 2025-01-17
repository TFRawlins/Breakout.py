import pygame
import math
import random

screen_width = 800
screen_height = 600

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (61, 66, 242, 255)
RED = (219, 69, 76, 255)
GREEN = (69, 167, 64, 255)
ORANGE = (231, 112, 58, 255)
YELLOW = (240, 190, 10, 255)
LIGHT_BLUE = (8, 236, 239, 255)
PINK = (222, 93, 141, 255)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, game_width, game_height, frame_thickness):
        super().__init__()
        self.image = pygame.Surface([100, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 8
        self.game_width = game_width
        self.game_height = game_height
        self.frame_thickness = frame_thickness
        self.rect.x = game_width // 2 - self.rect.width // 2
        self.rect.y = (
            game_height - self.frame_thickness - self.rect.height - 20
        )

    def move(self, x_direction):
        self.rect.x += x_direction * self.speed
        if self.rect.x < self.frame_thickness:
            self.rect.x = self.frame_thickness
        elif (
            self.rect.x
            > self.game_width - self.frame_thickness - self.rect.width
        ):
            self.rect.x = (
                self.game_width - self.frame_thickness - self.rect.width
            )


def calculate_bounce_centrality(ball, paddle):
    distance = pygame.math.Vector2(ball.rect.center) - pygame.math.Vector2(
        paddle.rect.center
    )
    distance_normalized = distance.length() / paddle.rect.width
    if ball.rect.centerx < paddle.rect.centerx:
        distance_normalized = -distance_normalized
    return distance_normalized


def check_block_collision(ball, block):
    if pygame.sprite.collide_rect(ball, block):
        if (
            abs(ball.rect.centery - block.rect.centery)
            < ball.rect.height / 2.1
        ):
            return 1  # Hit top or bottom
        else:
            return -1  # aHit side
    return 0  # No hit


class Ball(pygame.sprite.Sprite):
    def __init__(
        self, game_width, game_height, frame_thickness, header_height
    ):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = game_width // 2
        self.rect.y = game_height // 2
        self.x_speed = 0
        self.y_speed = 5
        self.game_width = game_width
        self.game_height = game_height
        self.frame_thickness = frame_thickness
        self.header_height = header_height

    def update(self):
        next_x = self.rect.x + self.x_speed
        next_y = self.rect.y + self.y_speed

        if (
            next_x <= self.frame_thickness
            or next_x
            >= self.game_width - self.frame_thickness - self.rect.width
        ):
            self.x_speed = -self.x_speed
        else:
            self.rect.x = next_x

        if next_y <= self.header_height + self.frame_thickness:
            self.y_speed = abs(self.y_speed)

        elif (
            next_y
            >= self.game_height - self.frame_thickness - self.rect.height
        ):
            self.rect.x = self.game_width // 2
            self.rect.y = self.game_height // 2
            self.y_speed = -abs(
                self.y_speed
            )  # Reinicia la bola si toca el fondo
        else:
            self.rect.y = next_y

    def paddle_bounce(self, centrality=-1):
        EXAGERATION = 1.13
        self.y_speed = -self.y_speed
        if centrality == -1:
            return

        current_angle = math.degrees(math.atan2(self.y_speed, self.x_speed))

        current_magnitude = math.sqrt(self.x_speed**2 + self.y_speed**2)
        new_horizontal_speed = current_magnitude * math.cos(
            math.radians(current_angle + centrality * 80 * EXAGERATION)
        )
        new_vertical_speed = current_magnitude * math.sin(
            math.radians(current_angle + centrality * 80 * EXAGERATION)
        )

        if new_vertical_speed > 0:
            new_vertical_speed = -new_vertical_speed



        self.x_speed = new_horizontal_speed
        self.y_speed = new_vertical_speed

    def block_bounce(self, hit_type):
        if hit_type == -1:
            self.y_speed = -self.y_speed
        else:
            self.x_speed = -self.x_speed

    def check_speed(self):
        if abs(self.y_speed) < 1:
            magnitud = self.x_speed**2 + self.y_speed**2
            if self.y_speed > 0:
                self.y_speed = 1
                new_x = math.sqrt(magnitud - self.y_speed**2)
                if new_x < 0:
                    self.x_speed = new_x * -1
                else:
                    self.x_speed = new_x
            else:
                self.y_speed = -1
                new_x = math.sqrt(magnitud - self.y_speed**2)
                if new_x < 0:
                    self.x_speed = new_x * -1
                else:
                    self.x_speed = new_x

    


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, row):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.row = row
        self.lives = self.set_lives_and_color()
        pygame.draw.rect(self.image, (0, 0, 0, 0), [0, 0, width, height], 1)

    def set_lives_and_color(self):
        if self.row == 0:
            self.image.fill(PINK)
            return 7
        elif self.row == 1:
            self.image.fill(RED)
            return 6
        elif self.row == 2:
            self.image.fill(ORANGE)
            return 5
        elif self.row == 3:
            self.image.fill(YELLOW)
            return 4
        elif self.row == 4:
            self.image.fill(GREEN)
            return 3
        elif self.row == 5:
            self.image.fill(BLUE)
            return 2
        else:
            self.image.fill(LIGHT_BLUE)
            return 1

    def update_color(self):
        if self.lives == 7:
            self.image.fill(PINK)
        elif self.lives == 6:
            self.image.fill(RED)
        elif self.lives == 5:
            self.image.fill(ORANGE)
        elif self.lives == 4:
            self.image.fill(YELLOW)
        elif self.lives == 3:
            self.image.fill(GREEN)
        elif self.lives == 2:
            self.image.fill(BLUE)
        elif self.lives == 1:
            self.image.fill(LIGHT_BLUE)
    def get_color(self):
        return self.lives

    def hit(self):
        self.lives -= 1
        if self.lives <= 0:
            return True
        self.update_color()
        return False

    def should_spawn_power_up(self):
        return PowerUp.should_spawn()
    

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 30
        self.height = 30
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.draw_power_up()

    def draw_power_up(self):
        
        pygame.draw.rect(self.image, (255, 215, 0), [0, 0, self.width, self.height]) 
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width, self.height], 2) 

        heart_color = (255, 0, 0)
        heart_width = self.width - 10
        heart_height = self.height - 10
        
        heart_surface = pygame.Surface((heart_width, heart_height), pygame.SRCALPHA)

        pygame.draw.polygon(heart_surface, heart_color, [
            (heart_width // 2, heart_height // 5),
            (heart_width // 5, 0),
            (0, heart_height // 3),
            (heart_width // 2, heart_height),
            (heart_width, heart_height // 3),
            (4 * heart_width // 5, 0),
        ])
        
        pygame.draw.circle(heart_surface, heart_color, (heart_width // 4, heart_height // 4), heart_width // 4)
        pygame.draw.circle(heart_surface, heart_color, (3 * heart_width // 4, heart_height // 4), heart_width // 4)
        
        self.image.blit(heart_surface, (5, 5))

    def update(self):
        self.rect.y += self.speed

    @staticmethod
    def should_spawn():
        return random.random() < 0.8 

