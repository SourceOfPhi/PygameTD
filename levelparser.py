from pathlib import Path
from dataclasses import dataclass


@dataclass
class Level():
    row_cnt: int
    col_cnt: int
    enemy_path: list[tuple[int, int]]
    blocked_positions: list[tuple[int, int]]


class LevelParser():
    def parse_txt(self, file_path: Path) -> Level:
        with open(file_path, 'r') as map_file:
            map_lines_all = map_file.read()
            map_lines = map_lines_all.split('\n')

            row_cnt = len(map_lines)
            col_cnt = len(map_lines[0])

            highest_num = int(max([char for char in map_lines_all if char.isdigit()]))
            lowest_num = int(min([char for char in map_lines_all if char.isdigit()]))
            enemy_path_position_cnt = highest_num - lowest_num + 1
            enemy_path_cell_positions: list[tuple[int, int]] = [(0, 0)] * enemy_path_position_cnt

            blocked_cell_positions: list[tuple[int, int]] = []

            for row, line in enumerate(map_lines):
                for col, char in enumerate(line):
                    if(char.isdigit()):
                        enemy_path_cell_positions[int(char)-lowest_num] = (col, row)
                    elif(char == '#' or char.isdigit()):
                        blocked_cell_positions.append((col, row))

            return Level(row_cnt, col_cnt, enemy_path_cell_positions, blocked_cell_positions)
