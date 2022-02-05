import pygame
from abc import ABC, abstractmethod


class GameObject(ABC):
    @property
    @abstractmethod
    def tag(self):
        ...

    @property
    @abstractmethod
    def pos(self) -> pygame.Vector2:
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        ...

    @abstractmethod
    def shall_be_removed(self) -> bool:
        ...
