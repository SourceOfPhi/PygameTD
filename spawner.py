from dataclasses import dataclass

import pygame
from custom_types import CellPosition
from game_object import GameObject
from game_state import GameState
from enemy import Enemy


class Spawner():
    def __init__(self, cooldown: float, game_objects: list[GameObject], enemy_path: list[CellPosition], enemy_sprite: pygame.Surface):
        self._COOLDOWN = cooldown
        self._wave_timer = self._COOLDOWN

        self._game_objects = game_objects  # local reference to the global list
        self._enemy_path = enemy_path

        self.current_wave_num: int = 0
        self._current_wave = Wave(1000.0, 1, 100.0, 1)
        self._spawn_timer = self._current_wave.inbetween_time_ms

        self.enemy_sprite = enemy_sprite

    def update(self):
        self._wave_timer = self._wave_timer - GameState.Time.delta_time
        self._spawn_timer = self._spawn_timer - GameState.Time.delta_time

        if self._wave_timer <= 0:
            self._wave_timer = self._COOLDOWN
            self.spawn_wave()

        if self._spawn_timer <= 0 and self._current_wave.remaining_enemies > 0:
            self._spawn_timer = self._current_wave.inbetween_time_ms
            enemy = Enemy(self.enemy_sprite, self._enemy_path)
            self._game_objects.append(enemy)
            self._current_wave.remaining_enemies = self._current_wave.remaining_enemies - 1

    def spawn_wave(self):
        print("Spawning next wave! Here it comes!")
        self.current_wave_num = self.current_wave_num + 1
        self._current_wave = Wave(1000.0, 1, 100.0, self.current_wave_num)  # TODO: There shall be a config for this


@dataclass
class Wave():
    inbetween_time_ms: float
    enemy_count: int
    enemy_health: float
    remaining_enemies: int
