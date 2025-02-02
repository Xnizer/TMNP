from abc import ABC, abstractmethod
from enum import Enum


class KeyboardKey(Enum):
    # Arrow Keys
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    # TODO: add more keys


class TerminalSize():
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.size = rows * columns


class TerminalWrapperBase(ABC):
    @abstractmethod
    def size(self) -> TerminalSize:
        pass

    @abstractmethod
    def cursor(self, visible: bool):
        pass

    @abstractmethod
    def write(self, row: int, col: int, text: str):
        pass

    @abstractmethod
    def clear(self, fill: str = ' '):
        pass

    @abstractmethod
    def read(self) -> KeyboardKey | None:
        pass