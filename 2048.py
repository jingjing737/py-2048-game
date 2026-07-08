#!/usr/bin/env python3
"""
py-2048-game — 终端版 2048 游戏
使用 Unicode 方块 + 键盘方向键操作
"""
import os
import random
import sys

try:
    import curses
except ImportError:
    print("❌ 此项目需要 curses 库，macOS/Linux 自带，Windows 请安装 windows-curses")
    sys.exit(1)


class Game2048:
    SIZE = 4
    WIN_VALUE = 2048

    COLORS = {
        0:    ("", ""),
        2:    ("\033[38;5;231m", "\033[0m"),       # 近白
        4:    ("\033[38;5;230m", "\033[0m"),       # 浅黄
        8:    ("\033[38;5;214m", "\033[0m"),       # 橙
        16:   ("\033[38;5;208m", "\033[0m"),       # 深橙
        32:   ("\033[38;5;202m", "\033[0m"),       # 红橙
        64:   ("\033[38;5;196m", "\033[0m"),       # 红
        128:  ("\033[38;5;226m", "\033[0m"),       # 金黄
        256:  ("\033[38;5;220m", "\033[0m"),       # 亮金
        512:  ("\033[38;5;190m", "\033[0m"),       # 黄
        1024: ("\033[38;5;118m", "\033[0m"),       # 绿
        2048: ("\033[38;5;46m",  "\033[0m"),       # 亮绿
    }

    def __init__(self):
        self.board = [[0] * self.SIZE for _ in range(self.SIZE)]
        self.score = 0
        self.spawn()
        self.spawn()

    def spawn(self):
        empty = [(r, c) for r in range(self.SIZE)
                 for c in range(self.SIZE) if self.board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = 4 if random.random() < 0.1 else 2

    def slide(self, row):
        new = [x for x in row if x != 0]
        merged = []
        skip = False
        for i in range(len(new)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new) and new[i] == new[i + 1]:
                merged.append(new[i] * 2)
                self.score += new[i] * 2
                skip = True
            else:
                merged.append(new[i])
        return merged + [0] * (self.SIZE - len(merged))

    def move(self, direction):
        rotated = False
        if direction == "left":
            grid = self.board
        elif direction == "right":
            grid = [row[::-1] for row in self.board]
            rotated = True
        elif direction == "up":
            grid = [list(col) for col in zip(*self.board)]
        elif direction == "down":
            grid = [list(col)[::-1] for col in zip(*self.board)]
            rotated = True
        else:
            return False

        moved = False
        new_grid = []
        for row in grid:
            new_row = self.slide(row)
            new_grid.append(new_row)
            if new_row != row:
                moved = True

        if direction == "right":
            new_grid = [row[::-1] for row in new_grid]
        elif direction == "up":
            new_grid = [list(col) for col in zip(*new_grid)]
        elif direction == "down":
            new_grid = [list(col)[::-1] for col in zip(*new_grid)]

        self.board = new_grid
        return moved

    def can_move(self):
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.board[r][c] == 0:
                    return True
                if c + 1 < self.SIZE and self.board[r][c] == self.board[r][c + 1]:
                    return True
                if r + 1 < self.SIZE and self.board[r][c] == self.board[r + 1][c]:
                    return True
        return False

    def render(self):
        os.system("clear" if os.name == "posix" else "cls")
        print(f"\n  \033[1m2048\033[0m — 得分: {self.score}\n")
        line = "  +" + "--+" * self.SIZE + "--"
        print(line)
        for r, row in enumerate(self.board):
            cells = []
            for val in row:
                fg, reset = self.COLORS.get(val, ("", ""))
                if val:
                    cells.append(f"{fg}{str(val).center(3)}{reset}")
                else:
                    cells.append("   ")
            print("  |".join(cells))
            if r < self.SIZE - 1:
                print("  +" + "--+" * self.SIZE + "--")
        print(line)
        print("\n  ↑↓←→ 移动  R 重来  Q 退出")


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    game = Game2048()

    while True:
        game.render()
        if any(2048 in row for row in game.board):
            print("\n  🎉 恭喜达到 2048！继续挑战更高分！")
        if not game.can_move():
            print(f"\n  💀 游戏结束！最终得分: {game.score}")
            break

        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            print(f"\n  退出，得分: {game.score}")
            break
        if key == ord('r') or key == ord('R'):
            game = Game2048()
            continue

        dir_map = {curses.KEY_UP: "up", curses.KEY_DOWN: "down",
                   curses.KEY_LEFT: "left", curses.KEY_RIGHT: "right"}
        direction = dir_map.get(key)
        if direction:
            if game.move(direction):
                game.spawn()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\n\n  再见！")
