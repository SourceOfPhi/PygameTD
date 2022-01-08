import pygame
from abc import ABC, abstractmethod

class GameObject(ABC):
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        ...