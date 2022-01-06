import pygame
from abc import ABC, abstractmethod
from pathlib import Path
from levelparser import Level, LevelParser

# --- global constants ---
SCREEN_SIZE = (800, 400)


class Grid():
    def __init__(self, cell_width: int, level: Level) -> None:
        self.cell_width = cell_width
        self.cell_cnt_x = level.col_cnt  # int(SCREEN_SIZE[0] / cell_width)
        self.cell_cnt_y = level.row_cnt  # int(SCREEN_SIZE[1] / cell_width)

        self.blocked_cells: list[tuple[int, int]] = level.blocked_positions
        self.path_cells = level.blocked_positions
        print(self.blocked_cells)

        global SCREEN_SIZE
        SCREEN_SIZE = (cell_width * self.cell_cnt_x,
                       cell_width * self.cell_cnt_y)

    def pos_to_cell(self, pos: tuple[int, int]) -> tuple[int, int]:
        return (int(pos[0] / self.cell_width), int(pos[1] / self.cell_width))

    def cell_to_pos(self, cell_pos: tuple[int, int]) -> tuple[int, int]:
        return(cell_pos[0] * self.cell_width, cell_pos[1] * self.cell_width)

    def block_on_grid(self, cell_pos: tuple[int, int]):
        if not cell_pos in self.blocked_cells:
            self.blocked_cells.append(cell_pos)

    def is_blocked(self, cell_pos: tuple[int, int]):
        return cell_pos in self.blocked_cells

    def draw(self, screen: pygame.Surface):
        for y in range(self.cell_cnt_y):
            for x in range(self.cell_cnt_x):
                width = 1
                color = (0,0,0)
                if (x,y) in self.path_cells:
                    width = 0
                    color = (150,150,150)
                cell_pos = (x * self.cell_width, y * self.cell_width)
                pygame.draw.rect(screen, color,
                                 pygame.Rect(cell_pos, (self.cell_width, self.cell_width)), width=width)


class GameObject(ABC):
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        ...


class Turret(GameObject):
    def __init__(self, img: pygame.Surface, init_cell_pos: tuple[int, int], grid: Grid):
        self.img = pygame.transform.scale(
            img, (grid.cell_width, grid.cell_width))
        self.cell_pos = init_cell_pos
        self.pos = grid.cell_to_pos(self.cell_pos)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.pos)


def draw(screen: pygame.Surface, game_objects: list[GameObject]):
    for go in game_objects:
        go.draw(screen)


def main():
    # initialize the pygame module
    pygame.init()

    lvl = LevelParser().parse_txt("./maps/test1.txt")

    grid = Grid(cell_width=50, level=lvl)

    turret_sprite = pygame.image.load(Path('./images/turretPlaceholder.png'))

    game_objects = []

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(SCREEN_SIZE)

    mouse_pos: tuple[int, int] = 0, 0

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
                mouse_pos_ingrid = grid.pos_to_cell(mouse_pos)
                # TODO: if on this pos should be built
                if not grid.is_blocked(mouse_pos_ingrid):
                    turret = Turret(turret_sprite, mouse_pos_ingrid, grid)
                    game_objects.append(turret)
                    grid.block_on_grid(mouse_pos_ingrid)
        # TODO: Update all game objects

        # TODO: If enough time has passed to match the display frame rate
        # Draw all game objects
        grid.draw(screen)
        draw(screen, game_objects)
        pygame.display.update()
        #draw(screen, game_objects)


if __name__ == '__main__':
    main()
