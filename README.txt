# Retro Snake Game

## Requirements

* Python 3.x
* PyGame library

## Installation

Navigate into the project folder:

cd retro_snake_game

Create and activate virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## How to Run

python3 src/main.py

## Controls

* Arrow Keys -> Move snake
* ENTER -> Start game
* B -> Add robot snake during gameplay
* P -> Pause / Resume
* R -> Restart after game over
* Q -> Quit game

## Gameplay Mechanics

* The snake moves continuously across a grid.
* Each normal food consumed increases the snake's length and score.
* The game introduces multi-level difficulty as the score increases.
* The game speed increases as the level increases.
* A robot snake can be added by pressing B.
* From Level 2 onward, the robot snake can also appear during gameplay.
* The robot snake wanders randomly and does not chase food or trophies.
* If the player's snake hits the robot snake, the game ends.
* If the robot snake hits the player's snake body, the robot disappears for 30 seconds.
* From Level 3 onward, special collectable foods may appear.
* INV food gives temporary invincibility.
* Poison food drops part of the snake's tail.
* Slow food temporarily slows down the game.
* The game ends when the snake collides with the wall or itself.
* The player can restart the game after losing.
* The high score is saved persistently.
