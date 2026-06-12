import curses

def main(stdscr):
    stdscr.keypad(True)
    y, x = 5, 5
    label = "Move me!"
    while True:
        stdscr.clear()
        stdscr.addstr(y, x, label)
        stdscr.refresh()
        key = stdscr.getch()
        rows, cols = stdscr.getmaxyx()
        if key == curses.KEY_UP:
            y = max(0, y - 1)
        elif key == curses.KEY_DOWN:
            y = min(rows - 1, y + 1)
        elif key == curses.KEY_LEFT:
            x = max(0, x - 1)
        elif key == curses.KEY_RIGHT:
            x = min(cols - len(label) - 1, x + 1)
        elif key == ord("q"):
            break

curses.wrapper(main)