import curses

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    stdscr.box()
    height, width = stdscr.getmaxyx()
    label = "Hello, curses!"
    stdscr.addstr(
        height // 2,
        width // 2 - len(label) // 2,
        label,
        curses.color_pair(1) | curses.A_BOLD,
    )
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)