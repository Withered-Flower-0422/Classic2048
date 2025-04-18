from random import randint
from typing import Literal, TypeVar

T = TypeVar("T")
type Board = list[list[int]]
type Direction = Literal["left", "right", "up", "down"]


class Classic2048:
    def __init__(self, row: int = 4, col: int = 4):
        self.row: int = row
        self.col: int = col
        self.board: Board = [[0 for _ in range(col)] for _ in range(row)]
        self.next_boards: dict[Direction, Board] = {
            "left": [[0 for _ in range(col)] for _ in range(row)],
            "right": [[0 for _ in range(col)] for _ in range(row)],
            "up": [[0 for _ in range(col)] for _ in range(row)],
            "down": [[0 for _ in range(col)] for _ in range(row)],
        }

        self.score: int = 0
        self.game_over: bool = False

        self.generate_tile_and_update_next_boards()

    def generate_tile_and_update_next_boards(self) -> None:
        # helper functions
        def get_trans_board(board: Board, direction: Direction) -> Board:
            return {
                "left": lambda: [[n for n in row] for row in board],
                "right": lambda: [[n for n in row[::-1]] for row in board][::-1],
                "up": lambda: [[n for n in row] for row in zip(*board)],
                "down": lambda: [[n for n in row[::-1]] for row in zip(*board)][::-1],
            }[direction]()

        def merge(arr: list[int]) -> list[int]:
            res = []

            tmp = 0
            for num in arr:
                if num != 0:
                    if tmp == 0:
                        tmp = num
                    else:
                        if num == tmp:
                            res.append(tmp * 2)
                            tmp = 0
                        else:
                            res.append(tmp)
                            tmp = num
            if tmp != 0:
                res.append(tmp)

            return res + [0] * (len(arr) - len(res))

        def get_random_item(lst: list[T]) -> T | None:
            return lst[randint(0, len(lst) - 1)] if lst else None

        # generate tile
        random_empty_cell = get_random_item(
            [
                (i, j)
                for i in range(self.row)
                for j in range(self.col)
                if self.board[i][j] == 0
            ]
        )
        if random_empty_cell:
            i, j = random_empty_cell
            self.board[i][j] = 2 if randint(0, 1) else 4

        # update next boards
        for direction in ("left", "right", "up", "down"):
            trans_board = get_trans_board(self.board, direction)
            for i, row in enumerate(trans_board):
                trans_board[i] = merge(row)
            self.next_boards[direction] = get_trans_board(trans_board, direction)

    def move(self, direction: Direction) -> bool:
        """return True if move successfully, False otherwise"""
        if not self.game_over and self.board != self.next_boards[direction]:
            self.board = [[num for num in row] for row in self.next_boards[direction]]
            self.generate_tile_and_update_next_boards()
            self.score = self.cal_score()
            self.game_over = self.is_game_over()
            return True
        return False

    def cal_score(self) -> int:
        return sum(int(num / 4) ** 2 for row in self.board for num in row)

    def is_game_over(self) -> bool:
        return all(board == self.board for board in self.next_boards.values())


if __name__ == "__main__":
    from pprint import pprint

    game = Classic2048()
    for direction in ("left", "right", "up", "down"):
        pprint(game.board)
        pprint(direction)
        game.move(direction)
        pprint(game.board)
        pprint(game.next_boards)
        pprint(game.score)
        pprint(game.game_over)
        pprint("-" * 20)
