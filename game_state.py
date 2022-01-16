import pygame


class GameState():
    lives = 20

    class Time():
        last_ticks = 0
        delta_time = 0

        @staticmethod
        def update():
            new_ticks = pygame.time.get_ticks()
            GameState.Time.delta_time = new_ticks - GameState.Time.last_ticks
            GameState.Time.last_ticks = new_ticks
