import random

from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    RED,
    PURPLE,
    CYAN,
    PINK,
)


class Food:
    def __init__(self, snake_body, grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.kind = "normal"
        self.position = self.generate_position(snake_body)

    def generate_position(self, snake_body, forbidden_positions=None):
        if forbidden_positions is None:
            forbidden_positions = []

        blocked_positions = list(snake_body) + list(forbidden_positions)

        while True:
            pos = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1),
            )

            if pos not in blocked_positions:
                return pos

    def respawn(self, snake_body, forbidden_positions=None):
        self.kind = "normal"
        self.position = self.generate_position(snake_body, forbidden_positions)


class SpecialFood:
    TYPES = ["invincibility", "poison", "slow"]

    def __init__(self, snake_body, forbidden_positions=None):
        self.kind = random.choice(self.TYPES)
        self.position = self.generate_position(snake_body, forbidden_positions)
        self.spawn_time = 0
        self.active = False

    def generate_position(self, snake_body, forbidden_positions=None):
        if forbidden_positions is None:
            forbidden_positions = []

        blocked_positions = list(snake_body) + list(forbidden_positions)

        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )

            if pos not in blocked_positions:
                return pos

    def spawn(self, snake_body, forbidden_positions=None, current_time=0):
        self.kind = random.choice(self.TYPES)
        self.position = self.generate_position(snake_body, forbidden_positions)
        self.spawn_time = current_time
        self.active = True

    def deactivate(self):
        self.active = False

    def get_color(self):
        if self.kind == "invincibility":
            return PINK

        if self.kind == "poison":
            return PURPLE

        if self.kind == "slow":
            return CYAN

        return RED

    def get_label(self):
        if self.kind == "invincibility":
            return "INV"

        if self.kind == "poison":
            return "-TAIL"

        if self.kind == "slow":
            return "SLOW"

        return ""
