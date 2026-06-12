from rich import print

BOARD_WIDTH, BOARD_HEIGHT = 40, 20
(UP, DOWN, LEFT, RIGHT) = range(4)

# snake
position = [(10,20), (10,19),(10,18)]
direction = RIGHT

def moveUp():
    pass
def moveDown():
    pass
def moveLeft():
    pass
def moveRight():
    pass
def moveForward():
    pass

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
    if action == 'z':
        moveUp()
    elif action == 's':
        moveDown()
    elif action == 'q':
        moveLeft()
    elif action == 'd':
        moveRight()
    else:
        moveForward()

    afficher()
