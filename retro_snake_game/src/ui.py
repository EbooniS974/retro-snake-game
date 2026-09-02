import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE


class UI:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)
        self.main_font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)

    def draw_centered_text(self, screen, text, font, y, color=WHITE):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(WINDOW_WIDTH // 2, y))
        screen.blit(surface, rect)

    def draw_start_screen(self, screen, high_score):
        self.draw_centered_text(screen, "RETRO SNAKE GAME", self.title_font, WINDOW_HEIGHT // 2 - 130)
        self.draw_centered_text(screen, "Press ENTER to Start", self.main_font, WINDOW_HEIGHT // 2 - 45)
        self.draw_centered_text(screen, f"High Score: {high_score}", self.main_font, WINDOW_HEIGHT // 2)
        self.draw_centered_text(screen, "Arrow Keys: Move", self.small_font, WINDOW_HEIGHT // 2 + 45)
        self.draw_centered_text(screen, "B: Add Robot Snake", self.small_font, WINDOW_HEIGHT // 2 + 75)
        self.draw_centered_text(screen, "P: Pause / Resume", self.small_font, WINDOW_HEIGHT // 2 + 105)
        self.draw_centered_text(screen, "Q: Quit", self.small_font, WINDOW_HEIGHT // 2 + 135)

    def draw_pause_screen(self, screen):
        self.draw_centered_text(screen, "PAUSED", self.title_font, WINDOW_HEIGHT // 2 - 20)
        self.draw_centered_text(screen, "Press P to Resume", self.main_font, WINDOW_HEIGHT // 2 + 40)

    def draw_game_over_screen(self, screen, score, high_score):
        self.draw_centered_text(screen, "GAME OVER", self.title_font, WINDOW_HEIGHT // 2 - 70)
        self.draw_centered_text(screen, f"Final Score: {score}", self.main_font, WINDOW_HEIGHT // 2 - 10)
        self.draw_centered_text(screen, f"High Score: {high_score}", self.main_font, WINDOW_HEIGHT // 2 + 25)
        self.draw_centered_text(screen, "Press R to Restart", self.small_font, WINDOW_HEIGHT // 2 + 75)
        self.draw_centered_text(screen, "Press Q to Quit", self.small_font, WINDOW_HEIGHT // 2 + 105)
