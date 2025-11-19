"""Pygame-based GUI for OBD-II Chronicles.

This package provides a graphical user interface layer for the game
using Pygame, while preserving all existing game logic.
"""

from .window import GameWindow
from .renderer import PygameRenderer
from .input import PygameInputHandler
from .config import PygameConfig

__all__ = ['GameWindow', 'PygameRenderer', 'PygameInputHandler', 'PygameConfig']
