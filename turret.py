import imp
import pygame
from enemy import Enemy
from game_object import GameObject
from custom_types import CellPosition
from grid import Grid
from game_state import GameState


class Turret(GameObject):
    def __init__(self, img: pygame.Surface, init_cell_pos: CellPosition, game_objects: list[GameObject]):
        self.img = pygame.transform.scale(img, (Grid.cell_width, Grid.cell_width))
        self.cell_pos = init_cell_pos
        self._pos: pygame.Vector2 = Grid.cell_to_pos(self.cell_pos)

        self.cool_down_time = 1000  # ms
        self.cool_down_current = self.cool_down_time

        # Store local ref to list of all game objects
        self.game_objects = game_objects

        self.damage = 50.0  # TODO: This should be in a config file or organized somehow
        self.range = 100.0  # TODO: This should be in a config file or organized somehow

    @property
    def tag(self):
        return 'Turret'

    @property
    def pos(self):
        return self._pos

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self._pos)

    def update(self):
        # Look for enemies and calculate their current distance to the turret
        enemies: list[tuple[Enemy, float]] = []
        for go in self.game_objects:
            if go.tag == 'Enemy':
                distance_to_enemy = self._pos.distance_to(go.pos)
                enemies.append((go, distance_to_enemy))
        enemies.sort(key=lambda elem: elem[1])

        if self.cool_down_current > 0:
            self.cool_down_current = self.cool_down_current - GameState.Time.delta_time
        elif len(enemies) != 0 and enemies[0][1] <= self.range:
            print("Turret shoots!")
            enemies[0][0].take_damage(self.damage)
            self.cool_down_current = self.cool_down_time

    def shall_be_removed(self) -> bool:
        return False
