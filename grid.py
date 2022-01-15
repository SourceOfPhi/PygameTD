import pygame
from pygame.math import Vector2
from levelparser import Level
from custom_types import CellPosition


class Grid():
    cell_width: int = 50

    def __init__(self, level: Level) -> None:
        self.cell_cnt_x = level.col_cnt
        self.cell_cnt_y = level.row_cnt

        self.blocked_cells = level.blocked_positions
        self.path_cells = level.blocked_positions
        print(self.blocked_cells)

        global SCREEN_SIZE
        SCREEN_SIZE = (Grid.cell_width * self.cell_cnt_x,
                       Grid.cell_width * self.cell_cnt_y)

    @staticmethod
    def pos_to_cell(pos: Vector2) -> CellPosition:
        return (int(pos[0] / Grid.cell_width), int(pos[1] / Grid.cell_width))

    @staticmethod
    def cell_to_pos(cell_pos: CellPosition | list[CellPosition]) -> Vector2 | list[Vector2]:
        if not type(cell_pos) is list:
            return Vector2(cell_pos[0] * Grid.cell_width, cell_pos[1] * Grid.cell_width)
        else:
            return [Grid.cell_to_pos(elem) for elem in cell_pos]

    def block_on_grid(self, cell_pos: CellPosition):
        if not cell_pos in self.blocked_cells:
            self.blocked_cells.append(cell_pos)

    def is_blocked(self, cell_pos: CellPosition):
        return cell_pos in self.blocked_cells

    def draw(self, screen: pygame.Surface):
        for y in range(self.cell_cnt_y):
            for x in range(self.cell_cnt_x):
                width = 1
                color = (0, 0, 0)
                if (x, y) in self.path_cells:
                    width = 0
                    color = (150, 150, 150)
                cell_pos = (x * Grid.cell_width, y * Grid.cell_width)
                pygame.draw.rect(screen, color, pygame.Rect(cell_pos, (Grid.cell_width, Grid.cell_width)), width=width)
