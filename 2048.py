#!/usr/bin/env python3
"""
py-2048-game — 终端版 2048 游戏
使用 print 渲染，固定宽度，纯 ASCII 边框
"""
import os
import random
import sys
import time


class Game2048:
    SIZE = 4
    WIN_VALUE = 2048

    # 每格固定宽度
    CELL_W = 6

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
        if direction == "left":
            grid = self.board
        elif direction == "right":
            grid = [row[::-1] for row in self.board]
        elif direction == "up":
            grid = [list(col) for col in zip(*self.board)]
        elif direction == "down":
            grid = [list(col)[::-1] for col in zip(*self.board)]
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

        # 固定宽度分隔线
        sep = "+" + ("-" * self.CELL_W + "+") * self.SIZE

        print(f"\n  \033[1m2048\033[0m — 得分: {self.score}\n")
        print(sep)
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                val = self.board[r][c]
                if val:
                    text = str(val)
                    cell = f"\033[1m{text:^{self.CELL_W}}\033[0m"
                else:
                    cell = " " * self.CELL_W
                print("|" + cell, end="")
            print("|")
            if r < self.SIZE - 1:
                print(sep)
        print(sep)
        print("\n  ↑↓←→ 移动  R 重来  Q 退出\n")


def main():
    game = Game2048()

    while True:
        game.render()
        if any(2048 in row for row in game.board):
            print("\n  🎉 恭喜达到 2048！继续挑战更高分！\n")
        if not game.can_move():
            print(f"\n  💀 游戏结束！最终得分: {game.score}\n")
            break

        key = input("输入方向 (up/down/left/right) 或 R/Q: ").strip().lower()
        if key in ('q', 'esc'):
            print(f"\n  退出，得分: {game.score}\n")
            break
        if key in ('r', 'restart'):
            game = Game2048()
            continue

        dir_map = {'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right',
                   'w': 'up', 's': 'down', 'a': 'left', 'd': 'right',
                   '↑': 'up', '↓': 'down', '←': 'left', '→': 'right'}
        direction = dir_map.get(key)
        if direction:
            if game.move(direction):
                game.spawn()
        else:
            print("  无效输入，按回车继续...")
            input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  再见！")
