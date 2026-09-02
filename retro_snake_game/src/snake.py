from settings import UP, DOWN, LEFT, RIGHT


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = RIGHT
        self.grow_next = False

    def set_direction(self, new_direction):
        # Prevent direct reversal
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow_next:
            self.body.pop()
        else:
            self.grow_next = False

    def grow(self):
        self.grow_next = True

    def shrink_tail(self, amount=2):
        # Poison food drops part of the snake's tail.
        # Keep at least 2 segments so the snake remains playable.
        minimum_length = 2

        for _ in range(amount):
            if len(self.body) > minimum_length:
                self.body.pop()

    def head(self):
        return self.body[0]

    def collided_with_self(self):
        return self.head() in self.body[1:]
