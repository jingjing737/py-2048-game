#!/usr/bin/env python3
"""
py-2048-game — 终端版 2048 游戏
使用 curses 渲染，纯 ASCII 边框
"""
import os
import random
import sys

try:
    import curses
except ImportError:
    print("❌ 此项目需要 curses 库，macOS/Linux 自带")
    sys.exit(1)


class Game2048:
    SIZE = 4
    WIN_VALUE = 2048

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

    def get_cell_width(self, val):
        """获取数字占位宽度"""
        if val == 0:
            return 4
        return len(str(val)) + 2

    def render(self, stdscr):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # 标题
        title = f"  2048 — 得分: {self.score}"
        stdscr.addnstr(0, max(0, (w - len(title)) // 2), title, w - 1)

        # 画框
        cell_w = 6  # 每格宽度
        gap = 1
        total_w = self.SIZE * (cell_w + gap) - gap
        start_x = max(0, (w - total_w) // 2)
        start_y = 2

        # 顶线
        top_line = "+" + ("-" * cell_w + "+") * self.SIZE
        stdscr.addnstr(start_y, start_x, top_line, w - 1)

        for r in range(self.SIZE):
            # 横线
            if r < self.SIZE - 1:
                line = "+" + ("-" * cell_w + "+") * self.SIZE
                stdscr.addnstr(start_y + r * 2 + 1, start_x, line, w - 1)

            # 格子内容
            y = start_y + r * 2
            for c in range(self.SIZE):
                val = self.board[r][c]
                if val:
                    text = str(val)
                    padding = cell_w - len(text)
                    cell = " " + text + " " * (padding - 1)
                else:
                    cell = "    "
                stdscr.addnstr(y, start_x + c * (cell_w + gap) + 1, cell, cell_w - 1)

        # 底线
        line = "+" + ("-" * cell_w + "+") * self.SIZE
        stdscr.addnstr(start_y + self.SIZE * 2, start_x, line, w - 1)

        # 底部提示
        hint = " ↑↓←→ 移动  R 重来  Q 退出 "
        hint_y = start_y + self.SIZE * 2 + 2
        if hint_y < h:
            stdscr.addnstr(hint_y, max(0, (w - len(hint)) // 2), hint, w - 1)

        stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    game = Game2048()

    while True:
        game.render(stdscr)
        if any(2048 in row for row in game.board):
            msg = " 🎉 恭喜达到 2048！继续挑战更高分！ "
            stdscr.addnstr(0, max(0, (stdscr.getmaxyx()[1] - len(msg)) // 2), msg, stdscr.getmaxyx()[1] - 1)
            stdscr.refresh()
        if not game.can_move():
            msg = f" 💀 游戏结束！最终得分: {game.score} "
            stdscr.addnstr(0, max(0, (stdscr.getmaxyx()[1] - len(msg)) // 2), msg, stdscr.getmaxyx()[1] - 1)
            stdscr.refresh()
            break

        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            msg = f" 退出，得分: {game.score} "
            stdscr.addnstr(0, max(0, (stdscr.getmaxyx()[1] - len(msg)) // 2), msg, stdscr.getmaxyx()[1] - 1)
            stdscr.refresh()
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
