import pygame
from pygame.math import Vector2
from pathlib import Path
from enemy import Enemy
from grid import Grid
from levelparser import Level, LevelParser
from game_object import GameObject
from custom_types import CellPosition
from game_state import GameState
from turret import Turret

# --- global constants ---
SCREEN_SIZE = (800, 400)


def draw(screen: pygame.Surface, game_objects: list[GameObject]):
    for go in game_objects:
        go.draw(screen)


def main():
    # initialize the pygame module
    pygame.init()

    lvl = LevelParser().parse_txt("./maps/test1.txt")

    grid = Grid(level=lvl)

    print(f"Lives: {GameState.lives}")

    turret_sprite = pygame.image.load(Path('./images/turretPlaceholder.png'))
    enemy_sprite = pygame.image.load(Path('./images/enemyPlaceholder.png'))

    game_objects: list[GameObject] = []

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(SCREEN_SIZE)

    enemy1 = Enemy(enemy_sprite, lvl.enemy_path)
    game_objects.append(enemy1)

    mouse_pos: Vector2 = (0, 0)

    # define a variable to control the main loop
    running = True
    screen.fill((255, 255, 255))

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_ingrid = Grid.pos_to_cell(mouse_pos)
                # TODO: if on this pos should be built
                if not grid.is_blocked(mouse_pos_ingrid):
                    turret = Turret(turret_sprite, mouse_pos_ingrid, game_objects)
                    game_objects.append(turret)
                    grid.block_on_grid(mouse_pos_ingrid)

        # Update the global time
        GameState.Time.update()

        # Update all game objects
        for obj in game_objects:
            if obj.shall_be_removed():
                game_objects.remove(obj)
            else:
                obj.update()

        if GameState.lives <= 0:
            print("Game over.")
            return
        # TODO: If enough time has passed to match the display frame rate
        # Draw all game objects
        grid.draw(screen)
        draw(screen, game_objects)
        pygame.display.update()


if __name__ == '__main__':
    main()
