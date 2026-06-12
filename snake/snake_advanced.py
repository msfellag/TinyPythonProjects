import curses
import time
import random

# snake[x] => tuple(y,x)
# snake[0] == HEAD '@'
# snake[-1] == TAIL '+'
# in-between : BODY 'o'
# food : $
def main(stdscr : curses.window):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.curs_set(0)

    BOARD_WIDTH, BOARD_HEIGHT = 40, 20
    height, width = stdscr.getmaxyx()
    body = stdscr.subwin(height - 3, width, 3, 0)
    footer = stdscr.subwin(3, BOARD_WIDTH+3, 0, 0)

    (UP, DOWN, LEFT, RIGHT) = range(4)
    (SPIDER, FROG, FLY) = range(3)
    SNAKE_HEADS = ["⮝", "⮟", "⮜", "⮞"]
    APPLE = "🉠" #"❦"
    level_time = 0.5
    score = 0
    level = 1

    class Game:
        def __init__(self, snake, apple, monster):
            self.score = 0
            self.level = 1
            self.speed = 500
            self.gameOver = False

            self.snake = snake
            self.apple = apple
            self.monster = monster

            apple.newApple()
            # next monster spawn time
            self.spawnTime = time.time() + random.randint(10, 100)

        def logic(self):
            # timers

            # ----- Collision detection ------

            # eating Apple
            if self.snake.position[0] == self.apple.position:
                self.apple.newApple()
                self.snake.food = True
                self.score += level * 10

            # eating Monster
            elif self.snake.position[0] == self.monster.position:
                self.monster.newMonster()
                self.snake.food = True
                self.score += level * 50
            # level-up
            if self.score >= self.level * 100:
                self.level += 1
                if self.speed >= 50:
                    self.speed -= 50

            # contact with self
            if self.snake.position[0] in self.snake.position[1:]:
                self.gameOver = True
            
            # contact with board edges or obstacle
            elif self.snake.position[0][0] > BOARD_HEIGHT -1 or \
                self.snake.position[0][0] < 0 or \
                self.snake.position[0][1] > BOARD_WIDTH -1 or \
                self.snake.position[0][1] < 0 :
                    self.gameOver = True


    class Snake:
        def __init__(self):
            self.position = [(10,20), (10,19),(10,18)]
            self.direction = RIGHT
            self.food = False
            self.food_position = []

        def ingestFood(self):
            if self.food:
                self.food = False
                self.food_position.append(self.position[0])
            else:
                self.position.pop()
            
            for e in self.food_position:
                if e not in self.position:
                    self.food_position.remove(e)

        def moveUp(self):
            if self.direction == RIGHT or self.direction == LEFT:
                self.position.insert(0,(self.position[0][0] - 1, self.position[0][1]))
                self.direction = UP
                self.ingestFood()
            else:
                self.moveForeward()

        def moveDown(self):
            if self.direction == RIGHT or self.direction == LEFT:
                self.position.insert(0,(self.position[0][0] + 1, self.position[0][1]))
                #self.position.pop()
                self.ingestFood()
                self.direction = DOWN
            else:
                self.moveForeward()

        def moveLeft(self):
            if self.direction == UP or self.direction == DOWN:
                self.position.insert(0,(self.position[0][0], self.position[0][1] - 1))
                #self.position.pop()
                self.ingestFood()
                self.direction = LEFT
            else:
                self.moveForeward()

        def moveRight(self):
            if self.direction == UP or self.direction == DOWN:
                self.position.insert(0,(self.position[0][0], self.position[0][1] + 1))
                #self.position.pop()
                self.ingestFood()
                self.direction = RIGHT
            else:
                self.moveForeward()

        def moveForeward(self):
            #self.position.pop()
            self.ingestFood()
            if self.direction == UP:
                self.position.insert(0,(self.position[0][0] - 1, self.position[0][1]))
            elif self.direction == DOWN:
                self.position.insert(0,(self.position[0][0] + 1, self.position[0][1]))
            elif self.direction == LEFT:
                self.position.insert(0,(self.position[0][0], self.position[0][1] - 1))
            elif self.direction == RIGHT:
                self.position.insert(0,(self.position[0][0], self.position[0][1] + 1))

    # apple : (y,x)
    class Apple:
        def __init__(self, snake):
            self.position = None
            self.snake = snake

        def newApple(self):
            while True:
                pos = (random.randint(1, BOARD_HEIGHT), random.randint(1, BOARD_WIDTH))
                if pos not in self.snake.position:
                    self.position = pos
                    break
        
        def timeOut(self, t):
            if self.startTime - time.time() >= t:
                return True
            
    class Monster:
        def __init__(self, snake, apple):
            self.position = None
            self.type = None
            self.startTime = None

        def newMonster(self):
            while True:
                pos = (random.randint(0, BOARD_HEIGHT-1), random.randint(0, BOARD_WIDTH-1))
                if pos not in self.snake.position and pos != apple.position:
                    self.position = pos
                    self.startTime = time.time()
                    break


    snake = Snake()
    apple = Apple(snake)
    monster = Monster(snake, apple)
    game = Game(snake, apple, monster)
    

    stdscr.nodelay(True)

    while True:
        #curses.flushinp()
        key = stdscr.getch()
        # rows, cols = stdscr.getmaxyx()
        # if rows < BOARD_HEIGHT or cols < BOARD_WIDTH:
        #     print("Error : Screen is too small to display the game")
        #     break

        # input
        if key == ord("q"):
            break
        elif key == curses.KEY_UP:
            snake.moveUp()
        elif key == curses.KEY_DOWN:
            snake.moveDown()
        elif key == curses.KEY_LEFT:
            snake.moveLeft()
        elif key == curses.KEY_RIGHT:
            snake.moveRight()
        else :
            snake.moveForeward()
                
        #body.box()
        game.logic()
        if game.gameOver:
            stdscr.nodelay(False)
            body.addstr(BOARD_HEIGHT//2, 3, "--- Game over ---".center(BOARD_WIDTH), curses.color_pair(3))
            body.refresh()
            stdscr.getch()
            break
        body.erase()
        # drawing 
        for y in range(0, BOARD_HEIGHT):
            line = []
            for x in range(1, BOARD_WIDTH):

                if (y,x) in snake.position:
                    if (y,x) == snake.position[0]:
                        line.append(SNAKE_HEADS[snake.direction])
                    elif (y,x) == snake.position[-1]:
                        line.append('+')
                    elif (y, x) in snake.food_position:
                        line.append('O')
                    else:
                        line.append('o')

                elif (y,x) == apple.position:
                    line.append(APPLE)

                else:
                    line.append(' ')

            line_txt = ''.join(line)
            body.addstr(y, 3, line_txt, curses.color_pair(1))
        body.refresh()
        footer.erase()
        footer.box()
        footer.addstr(1,1, f"Lvl {game.level} | Score {game.score:08d} speed {game.speed}".center(BOARD_WIDTH), curses.color_pair(3))
        footer.refresh()
        #time.sleep(level_time)
        curses.napms(game.speed)
        

curses.wrapper(main)