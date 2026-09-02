import sys
import os
import random
import pygame

from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CELL_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    INITIAL_FPS,
    MAX_FPS,
    FOODS_PER_LEVEL,
    ROBOT_LEVEL,
    SPECIAL_FOOD_LEVEL,
    ROBOT_RESPAWN_DELAY_MS,
    ROBOT_MOVE_INTERVAL_MS,
    SPECIAL_FOOD_DURATION_MS,
    SLOW_MOTION_DURATION_MS,
    SLOW_MOTION_FPS,
    INVINCIBILITY_DURATION_MS,
    BLACK,
    GREEN,
    DARK_GREEN,
    RED,
    WHITE,
    GRAY,
    BLUE,
    ORANGE,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)
from snake import Snake
from food import Food, SpecialFood
from robot_snake import RobotSnake
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Retro Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)
        self.tiny_font = pygame.font.SysFont("Arial", 16)

        self.ui = UI()

        self.state = "MENU"
        self.high_score_file = os.path.join(os.path.dirname(__file__), "..", "high_score.txt")
        self.high_score = self.load_high_score()

        self.fps = INITIAL_FPS
        self.level = 1

        self.robot_snake = None
        self.robot_respawn_time = 0
        self.last_robot_move_time = 0

        self.special_food = None
        self.next_special_food_score = 0
        self.slow_until_time = 0
        self.invincible_until_time = 0

        self.reset_game()

    def load_high_score(self):
        try:
            with open(self.high_score_file, "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        with open(self.high_score_file, "w", encoding="utf-8") as file:
            file.write(str(self.high_score))

    def reset_game(self):
        self.snake = Snake()
        self.food = Food(self.snake.body, GRID_WIDTH, GRID_HEIGHT)

        self.score = 0
        self.level = 1
        self.fps = INITIAL_FPS

        self.robot_snake = None
        self.robot_respawn_time = 0
        self.last_robot_move_time = 0

        self.special_food = None
        self.next_special_food_score = 3
        self.slow_until_time = 0
        self.invincible_until_time = 0

    def start_game(self):
        self.reset_game()
        self.state = "PLAYING"

    def update_difficulty(self):
        self.level = 1 + (self.score // FOODS_PER_LEVEL)
        self.fps = min(MAX_FPS, INITIAL_FPS + (self.level - 1) * 2)

    def get_current_fps(self):
        current_time = pygame.time.get_ticks()

        if current_time < self.slow_until_time:
            return SLOW_MOTION_FPS

        return self.fps

    def is_invincible(self):
        return pygame.time.get_ticks() < self.invincible_until_time

    def handle_game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        self.state = "GAME_OVER"

    def get_forbidden_positions(self):
        forbidden = []

        if self.robot_snake is not None and self.robot_snake.active:
            forbidden.extend(self.robot_snake.body)

        if self.special_food is not None and self.special_food.active:
            forbidden.append(self.special_food.position)

        forbidden.append(self.food.position)

        return forbidden

    def add_robot_snake(self):
        current_time = pygame.time.get_ticks()

        if self.robot_snake is None:
            self.robot_snake = RobotSnake(self.snake.body)
            self.last_robot_move_time = current_time
            return

        if not self.robot_snake.active:
            self.robot_snake.spawn(self.snake.body)
            self.last_robot_move_time = current_time

    def ensure_robot_snake(self):
        current_time = pygame.time.get_ticks()

        if self.level < ROBOT_LEVEL:
            return

        if self.robot_snake is None:
            self.robot_snake = RobotSnake(self.snake.body)
            self.last_robot_move_time = current_time
            return

        if not self.robot_snake.active and current_time >= self.robot_respawn_time:
            self.robot_snake.spawn(self.snake.body)
            self.last_robot_move_time = current_time

    def update_robot_snake(self):
        if self.robot_snake is None or not self.robot_snake.active:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.last_robot_move_time >= ROBOT_MOVE_INTERVAL_MS:
            self.robot_snake.move()
            self.last_robot_move_time = current_time

    def deactivate_robot_snake(self):
        if self.robot_snake is None:
            return

        self.robot_snake.deactivate()
        self.robot_respawn_time = pygame.time.get_ticks() + ROBOT_RESPAWN_DELAY_MS

    def maybe_spawn_special_food(self):
        current_time = pygame.time.get_ticks()

        if self.level < SPECIAL_FOOD_LEVEL:
            return

        if self.special_food is not None and self.special_food.active:
            if current_time - self.special_food.spawn_time > SPECIAL_FOOD_DURATION_MS:
                self.special_food.deactivate()
            return

        if self.score >= self.next_special_food_score:
            forbidden = self.get_forbidden_positions()
            self.special_food = SpecialFood(self.snake.body, forbidden)
            self.special_food.spawn(self.snake.body, forbidden, current_time)

            self.next_special_food_score = self.score + random.randint(4, 7)

    def apply_special_food_effect(self):
        if self.special_food is None or not self.special_food.active:
            return

        if self.snake.head() != self.special_food.position:
            return

        current_time = pygame.time.get_ticks()

        if self.special_food.kind == "invincibility":
            self.invincible_until_time = current_time + INVINCIBILITY_DURATION_MS
            self.score += 1

        elif self.special_food.kind == "poison":
            self.snake.shrink_tail(2)

        elif self.special_food.kind == "slow":
            self.slow_until_time = current_time + SLOW_MOTION_DURATION_MS
            self.score += 1

        self.special_food.deactivate()
        self.update_difficulty()

    def check_robot_collisions(self):
        if self.robot_snake is None or not self.robot_snake.active:
            return

        # If the player's snake hits the robot snake:
        # normal state -> game over
        # invincible state -> robot disappears instead
        if self.snake.head() in self.robot_snake.body:
            if self.is_invincible():
                self.deactivate_robot_snake()
            else:
                self.handle_game_over()
            return

        # If the robot snake hits the player's snake body, the robot disappears for 30 seconds.
        if self.robot_snake.head() in self.snake.body[1:]:
            self.deactivate_robot_snake()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                if self.state == "MENU":
                    if event.key == pygame.K_RETURN:
                        self.start_game()

                elif self.state == "PLAYING":
                    if event.key == pygame.K_UP:
                        self.snake.set_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.set_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.set_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.set_direction(RIGHT)
                    elif event.key == pygame.K_p:
                        self.state = "PAUSED"
                    elif event.key == pygame.K_b:
                        self.add_robot_snake()

                elif self.state == "PAUSED":
                    if event.key == pygame.K_p:
                        self.state = "PLAYING"

                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self.start_game()

    def update(self):
        if self.state != "PLAYING":
            return

        self.ensure_robot_snake()
        self.maybe_spawn_special_food()

        self.snake.move()

        head_x, head_y = self.snake.head()

        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            self.handle_game_over()
            return

        if self.snake.collided_with_self():
            self.handle_game_over()
            return

        if self.snake.head() == self.food.position:
            self.snake.grow()
            self.score += 1
            self.update_difficulty()

            forbidden = self.get_forbidden_positions()
            self.food.respawn(self.snake.body, forbidden)

        self.apply_special_food_effect()

        self.update_robot_snake()
        self.check_robot_collisions()

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))

        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))

    def draw_snake(self):
        for i, segment in enumerate(self.snake.body):
            x, y = segment
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if i == 0 else DARK_GREEN

            if self.is_invincible() and i == 0:
                color = WHITE

            pygame.draw.rect(self.screen, color, rect, border_radius=4)

    def draw_robot_snake(self):
        if self.robot_snake is None or not self.robot_snake.active:
            return

        for i, segment in enumerate(self.robot_snake.body):
            x, y = segment
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = BLUE if i == 0 else ORANGE
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

    def draw_food(self):
        x, y = self.food.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED, rect, border_radius=6)

    def draw_special_food(self):
        if self.special_food is None or not self.special_food.active:
            return

        x, y = self.special_food.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(self.screen, self.special_food.get_color(), rect, border_radius=8)

        label = self.special_food.get_label()
        text = self.tiny_font.render(label, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def draw_hud(self):
        current_time = pygame.time.get_ticks()

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, WHITE)

        self.screen.blit(score_text, (10, 8))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(high_score_text, (10, 66))

        y_offset = 92

        if self.robot_snake is not None and not self.robot_snake.active:
            remaining = max(0, (self.robot_respawn_time - current_time) // 1000)
            robot_text = self.small_font.render(f"Robot returns in: {remaining}s", True, WHITE)
            self.screen.blit(robot_text, (10, y_offset))
            y_offset += 26

        if current_time < self.slow_until_time:
            remaining = max(0, (self.slow_until_time - current_time) // 1000)
            slow_text = self.small_font.render(f"Slow motion: {remaining}s", True, WHITE)
            self.screen.blit(slow_text, (10, y_offset))
            y_offset += 26

        if current_time < self.invincible_until_time:
            remaining = max(0, (self.invincible_until_time - current_time) // 1000)
            invincible_text = self.small_font.render(f"Invincible: {remaining}s", True, WHITE)
            self.screen.blit(invincible_text, (10, y_offset))

    def draw_playing_screen(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_food()
        self.draw_special_food()
        self.draw_snake()
        self.draw_robot_snake()
        self.draw_hud()

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == "MENU":
            self.ui.draw_start_screen(self.screen, self.high_score)

        elif self.state == "PLAYING":
            self.draw_playing_screen()

        elif self.state == "PAUSED":
            self.draw_playing_screen()
            self.ui.draw_pause_screen(self.screen)

        elif self.state == "GAME_OVER":
            self.draw_playing_screen()
            self.ui.draw_game_over_screen(self.screen, self.score, self.high_score)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.get_current_fps())
