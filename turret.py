import imp
import pygame
from game_object import GameObject
from custom_types import CellPosition
from grid import Grid
from game_state import GameState


class Turret(GameObject):
    def __init__(self, img: pygame.Surface, init_cell_pos: CellPosition):
        self.img = pygame.transform.scale(img, (Grid.cell_width, Grid.cell_width))
        self.cell_pos = init_cell_pos
        self.pos = Grid.cell_to_pos(self.cell_pos)

        self.cool_down_time = 1000  # ms
        self.cool_down_current = self.cool_down_time

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.pos)

    def update(self):
        if self.cool_down_current > 0:
            self.cool_down_current = self.cool_down_current - GameState.Time.delta_time
        else:
            print("Turret shoots!")
            self.cool_down_current = self.cool_down_time

    def shall_be_removed(self) -> bool:
        return False
