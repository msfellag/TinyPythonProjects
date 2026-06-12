from rich import print
import os

BOARD_WIDTH, BOARD_HEIGHT = 40, 20
(UP, DOWN, LEFT, RIGHT) = range(4)

# snake
position = [(10,20), (10,19),(10,18)]
direction = RIGHT

def update(newDirection):
    global direction
    position.pop()
    position.insert(0, newHead(newDirection))
    direction = newDirection

def newHead(direction):
    if direction == UP:
        return (position[0][0] - 1, position[0][1])
    elif direction == DOWN:
        return (position[0][0] + 1, position[0][1])
    elif direction == LEFT:
        return (position[0][0], position[0][1] - 1)
    elif direction == RIGHT:
        return (position[0][0], position[0][1] + 1)
    else:
        raise ValueError("The value of <direction> is out of bound")

def moveUp():
    update(UP)

def moveDown():
    update(DOWN)

def moveLeft():
    update(LEFT)

def moveRight():
    update(RIGHT)

def moveForward():
    update(direction)


def afficher():
    for y in range(BOARD_HEIGHT):
        line = ['[white on blue]']
        for x in range(BOARD_WIDTH):
            # Affichage de snake
            if (y,x) in position:
                if (y,x) == position[0]:
                    line.append('@')
                elif (y,x) == position[-1]:
                    line.append('+')
                else:
                    line.append('o')
            # affichage de la grille (virtuelle)
            else:
                line.append(' ')
        line.append('[white on blue]')
        print(''.join(line))

while True:
    #  Z      W
    # QSD    ASD
    action = input('> ')
    if action == 'w':
        moveUp()
    elif action == 's':
        moveDown()
    elif action == 'a':
        moveLeft()
    elif action == 'd':
        moveRight()
    else:
        moveForward()
    os.system('clear')
    afficher()
