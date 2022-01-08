import pygame
from game_object import GameObject
from grid import Grid


class Enemy(GameObject):
    DIST_THRESH = 0.1

    def __init__(self, img: pygame.Surface, init_pos: tuple[int, int], path: list[tuple[int, int]]) -> None:
        self.position: tuple[float, float] = (float(init_pos[0]), float(init_pos[1]))
        self.path = Grid.cell_to_pos(path)
        self.curr_path_idx = 0
        self.target = self.path[0]
        self.speed: float = 0.1
        self.img = img

    def update(self):
        dist = pygame.math.Vector2(self.position).distance_to(self.target)
        if dist < Enemy.DIST_THRESH:
            self.curr_path_idx = self.curr_path_idx + 1
            if self.curr_path_idx > len(self.path):
                print("Enemy reached end!")
                return
            self.target = self.path[self.curr_path_idx]
        self.position = tuple(pygame.math.Vector2(self.position) + (pygame.math.Vector2(self.target) -
                              pygame.math.Vector2(self.position)).normalize() * self.speed)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.position)
