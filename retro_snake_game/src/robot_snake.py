import random

from settings import DIRECTIONS, GRID_WIDTH, GRID_HEIGHT


class RobotSnake:
    def __init__(self, snake_body):
        self.body = []
        self.direction = random.choice(DIRECTIONS)
        self.active = True
        self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            x = random.randint(2, GRID_WIDTH - 3)
            y = random.randint(2, GRID_HEIGHT - 3)

            candidate_body = [(x, y), (x - 1, y), (x - 2, y)]

            if all(segment not in snake_body for segment in candidate_body):
                self.body = candidate_body
                self.direction = random.choice(DIRECTIONS)
                self.active = True
                return

    def head(self):
        return self.body[0]

    def choose_random_direction(self):
        possible_directions = []

        for direction in DIRECTIONS:
            dx, dy = direction
            new_x = self.head()[0] + dx
            new_y = self.head()[1] + dy

            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                possible_directions.append(direction)

        if possible_directions:
            self.direction = random.choice(possible_directions)

    def move(self):
        if not self.active:
            return

        # Robot snake wanders randomly. It does not chase the player.
        if random.random() < 0.30:
            self.choose_random_direction()

        dx, dy = self.direction
        head_x, head_y = self.head()
        new_head = (head_x + dx, head_y + dy)

        # If the robot reaches a wall, choose another random valid direction.
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.choose_random_direction()
            dx, dy = self.direction
            new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        self.body.pop()

    def deactivate(self):
        self.active = False
        self.body = []
