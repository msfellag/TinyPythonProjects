from rich import print
import os
import random

BOARD_WIDTH, BOARD_HEIGHT = 40, 20
(UP, DOWN, LEFT, RIGHT) = range(4)

# snake
class Snake:
    def __init__(self):
        self.position = [(10,20), (10,19),(10,18)]
        self.direction = RIGHT

    def update(self, newDirection):
        self.position.pop()
        self.position.insert(0, self.newHead(newDirection))
        self.direction = newDirection

    def newHead(self, newDirection):
        if newDirection == UP:
            return (self.position[0][0] - 1, self.position[0][1])
        elif newDirection == DOWN:
            return (self.position[0][0] + 1, self.position[0][1])
        elif newDirection == LEFT:
            return (self.position[0][0], self.position[0][1] - 1)
        elif newDirection == RIGHT:
            return (self.position[0][0], self.position[0][1] + 1)
        else:
            raise ValueError("The value of <direction> is out of bound")

    def moveUp(self):
        if self.direction == LEFT or self.direction == RIGHT:
            self.update(UP)
        else:
            self.moveForward()

    def moveDown(self):
        if self.direction == LEFT or self.direction == RIGHT:
            self.update(DOWN)
        else:
            self.moveForward()

    def moveLeft(self):
        if self.direction == UP or self.direction == DOWN:
            self.update(LEFT)
        else:
            self.moveForward()

    def moveRight(self):
        if self.direction == UP or self.direction == DOWN:
            self.update(RIGHT)
        else:
            self.moveForward()

    def moveForward(self):
        self.update(self.direction)

# Pomme
class Apple:
    def __init__(self, snake : Snake):
        self.position = None
        self.snake = snake
        self.new()

    def new(self):
        while True:
            self.position = (random.randint(0, BOARD_HEIGHT - 1), random.randint(0, BOARD_WIDTH - 1))
            if self.position not in self.snake.position:
                break

def afficher():
    for y in range(BOARD_HEIGHT):
        line = ['[white on blue]']
        for x in range(BOARD_WIDTH):
            # Affichage de snake
            if (y,x) in snake.position:
                if (y,x) == snake.position[0]:
                    line.append('@')
                elif (y,x) == snake.position[-1]:
                    line.append('+')
                else:
                    line.append('o')

            # Affichage Pomme
            elif (y,x) == apple.position:
                line.append('$')

            # affichage de la grille (virtuelle)
            else:
                line.append(' ')
        line.append('[white on blue]')
        print(''.join(line))

snake = Snake()
apple = Apple(snake)
score = 0
gameOver = False
while gameOver == False:
    #  Z      W
    # QSD    ASD
    action = input('> ')
    if action == 'w':
        snake.moveUp()
    elif action == 's':
        snake.moveDown()
    elif action == 'a':
        snake.moveLeft()
    elif action == 'd':
        snake.moveRight()
    else:
        snake.moveForward()

    # mise a jour du jeu
    if apple.position == snake.position[0]:
        apple.new()
        score += 10
    # detection des collisions avec le bord de la grille
    if snake.position[0][0] > (BOARD_HEIGHT - 1) or snake.position[0][0] < 0 \
    or snake.position[0][1] > (BOARD_WIDTH - 1) or snake.position[0][1] < 0:
        gameOver = True

    # detection of collision with self
    if snake.position[0] in snake.position[1:]:
        gameOver = True

    os.system('clear')
    afficher()
