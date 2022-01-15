import pygame
from pygame.math import Vector2
from game_object import GameObject
from grid import Grid
from custom_types import CellPosition
from game_state import GameState


class Enemy(GameObject):
    DIST_THRESH = 0.1

    def __init__(self, img: pygame.Surface, init_pos: Vector2, path: list[CellPosition]) -> None:
        self.position = Vector2(init_pos)
        self.path = list[Vector2](Grid.cell_to_pos(path))
        self.curr_path_idx = 0
        self.target = self.path[0]
        self.speed: float = 0.1
        self.img = pygame.transform.scale(img, (20, 20))
        self.is_dead = False

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
        screen.blit(self.img, self.position)

    def shall_be_removed(self) -> bool:
        return self.is_dead
