import pygame
from pygame.math import Vector2
from game_object import GameObject
from grid import Grid
from custom_types import CellPosition
from game_state import GameState


class Enemy(GameObject):
    DIST_THRESH = 0.1

    def __init__(self, img: pygame.Surface, path: list[CellPosition]) -> None:
        self.path = Enemy.calc_path_coords(path)
        self.position = Vector2(self.path[0])
        self.curr_path_idx = 0
        self.target = self.path[1]
        self.speed: float = 0.1
        self.size = Vector2(20, 20)
        self.img = pygame.transform.scale(img, self.size)
        self.is_dead = False

    @staticmethod
    def calc_path_coords(path: list[CellPosition]) -> list[Vector2]:
        out_path = list[Vector2](Grid.cell_to_pos(path))
        # correct first
        # find out on which side of the grid it is
        if path[0][0] == 0:  # left
            out_path[0] = (out_path[0][0], out_path[0][1] + (Grid.cell_width / 2))
        elif path[0][1] == 0:  # top
            out_path[0] = (out_path[0][0] + (Grid.cell_width / 2), out_path[0][1])
        else:
            print("Error: Start position is not left or top")

        # TODO: correct last

        # center others
        out_path[1:] = [pos + (Grid.cell_width / 2, Grid.cell_width / 2) for pos in out_path[1:]]

        return out_path

    def update(self):
        dist = self.position.distance_to(self.target)
        if dist < Enemy.DIST_THRESH:
            self.curr_path_idx = self.curr_path_idx + 1
            if self.curr_path_idx >= len(self.path):
                print("Enemy reached end!")
                GameState.lives = GameState.lives - 1
                print(f"Lives: {GameState.lives}")
                self.is_dead = True
                return
            self.target = self.path[self.curr_path_idx]
        self.position = self.position + (self.target - self.position).normalize() * self.speed

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.position - (self.size / 2))

    def shall_be_removed(self) -> bool:
        return self.is_dead
