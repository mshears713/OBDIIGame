"""
Input Handler System

This module processes player input and translates it into game commands.

Educational Notes:
------------------
Input handling is a core game system that bridges the gap between raw
user input (keyboard, mouse) and game actions. This module:

1. Reads player input (keyboard keys)
2. Validates input (is this a valid command?)
3. Translates input to actions (key → movement direction)
4. Returns structured commands for the game loop to process

In a turn-based game, input handling is simpler than real-time games
because we:
- Wait for input before proceeding
- Process one command per turn
- Don't need to handle timing or buffering
"""

from enum import Enum, auto
from typing import Optional, Tuple
from dataclasses import dataclass


class Action(Enum):
    """
    Enumeration of possible player actions.

    Educational Note:
        Using an Enum ensures type safety and prevents typos.
        Actions represent high-level player intentions.

        Movement actions include diagonal directions for 8-way movement.
        Non-movement actions will be added in future phases.
    """
    # Movement actions (8 directions)
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP_LEFT = auto()
    MOVE_UP_RIGHT = auto()
    MOVE_DOWN_LEFT = auto()
    MOVE_DOWN_RIGHT = auto()

    # Wait action (skip turn)
    WAIT = auto()

    # Game flow actions
    QUIT = auto()

    # Future actions (to be implemented)
    # PICKUP_ITEM = auto()
    # DROP_ITEM = auto()
    # USE_ITEM = auto()
    # SHOW_INVENTORY = auto()
    # DESCEND_STAIRS = auto()
    # ASCEND_STAIRS = auto()


@dataclass
class Command:
    """
    Structured command representing a player action.

    Attributes:
        action: The action to perform
        dx: X direction for movement (-1, 0, 1)
        dy: Y direction for movement (-1, 0, 1)
        data: Optional additional data for complex commands

    Educational Note:
        Commands encapsulate all information needed to execute an action.
        For movement, we include delta values (dx, dy) so the movement
        system knows which direction to move.

        Using a dataclass makes commands easy to create, read, and debug.

    Example:
        >>> # Move right
        >>> cmd = Command(action=Action.MOVE_RIGHT, dx=1, dy=0)
        >>>
        >>> # Move diagonally up-left
        >>> cmd = Command(action=Action.MOVE_UP_LEFT, dx=-1, dy=-1)
        >>>
        >>> # Wait (do nothing this turn)
        >>> cmd = Command(action=Action.WAIT, dx=0, dy=0)
    """
    action: Action
    dx: int = 0
    dy: int = 0
    data: Optional[dict] = None


class InputHandler:
    """
    Handles player input and converts it to game commands.

    Educational Note:
        This class maps raw input strings to structured commands.
        It provides a clean interface for the game loop:
        - Game loop calls handle_input(user_input)
        - InputHandler returns a Command object
        - Game loop processes the command

        Separating input handling from game logic makes it easy to:
        - Support multiple control schemes (vi keys, arrow keys, numpad)
        - Add new commands without changing game loop
        - Test input parsing independently
    """

    # Key mappings for different control schemes
    # Educational Note: Supporting multiple key layouts improves accessibility

    # Arrow key-like controls (WASD)
    WASD_KEYS = {
        'w': (0, -1, Action.MOVE_UP),
        's': (0, 1, Action.MOVE_DOWN),
        'a': (-1, 0, Action.MOVE_LEFT),
        'd': (1, 0, Action.MOVE_RIGHT),
        'q': (-1, -1, Action.MOVE_UP_LEFT),
        'e': (1, -1, Action.MOVE_UP_RIGHT),
        'z': (-1, 1, Action.MOVE_DOWN_LEFT),
        'c': (1, 1, Action.MOVE_DOWN_RIGHT),
    }

    # Vi-style keys (hjkl)
    VI_KEYS = {
        'k': (0, -1, Action.MOVE_UP),
        'j': (0, 1, Action.MOVE_DOWN),
        'h': (-1, 0, Action.MOVE_LEFT),
        'l': (1, 0, Action.MOVE_RIGHT),
        'y': (-1, -1, Action.MOVE_UP_LEFT),
        'u': (1, -1, Action.MOVE_UP_RIGHT),
        'b': (-1, 1, Action.MOVE_DOWN_LEFT),
        'n': (1, 1, Action.MOVE_DOWN_RIGHT),
    }

    # Arrow keys (using arrow symbols)
    ARROW_KEYS = {
        'up': (0, -1, Action.MOVE_UP),
        'down': (0, 1, Action.MOVE_DOWN),
        'left': (-1, 0, Action.MOVE_LEFT),
        'right': (1, 0, Action.MOVE_RIGHT),
    }

    # Special keys
    SPECIAL_KEYS = {
        '.': (0, 0, Action.WAIT),      # Wait/rest
        ' ': (0, 0, Action.WAIT),      # Space also waits
        'quit': (0, 0, Action.QUIT),   # Quit game
        'exit': (0, 0, Action.QUIT),   # Exit game
    }

    def __init__(self):
        """
        Initialize input handler.

        Educational Note:
            Currently no initialization needed, but having __init__
            allows future expansion (e.g., customizable key bindings).
        """
        pass

    def handle_input(self, user_input: str) -> Optional[Command]:
        """
        Process user input and return a command.

        Args:
            user_input: Raw input string from user

        Returns:
            Command object if input is valid, None if invalid

        Educational Note:
            This method is the main entry point for input handling.
            It tries multiple key mappings in order, returning the first match.

            Returns None for invalid input, allowing the game loop to:
            - Display error message
            - Prompt for new input
            - Not consume a turn

        Example:
            >>> handler = InputHandler()
            >>> cmd = handler.handle_input('w')
            >>> assert cmd.action == Action.MOVE_UP
            >>> assert cmd.dx == 0 and cmd.dy == -1
            >>>
            >>> cmd = handler.handle_input('invalid')
            >>> assert cmd is None
        """
        # Normalize input (lowercase, strip whitespace)
        normalized = user_input.lower().strip()

        # Try WASD keys
        if normalized in self.WASD_KEYS:
            dx, dy, action = self.WASD_KEYS[normalized]
            return Command(action=action, dx=dx, dy=dy)

        # Try Vi keys
        if normalized in self.VI_KEYS:
            dx, dy, action = self.VI_KEYS[normalized]
            return Command(action=action, dx=dx, dy=dy)

        # Try arrow keys
        if normalized in self.ARROW_KEYS:
            dx, dy, action = self.ARROW_KEYS[normalized]
            return Command(action=action, dx=dx, dy=dy)

        # Try special keys
        if normalized in self.SPECIAL_KEYS:
            dx, dy, action = self.SPECIAL_KEYS[normalized]
            return Command(action=action, dx=dx, dy=dy)

        # No valid mapping found
        return None

    def get_movement_delta(self, action: Action) -> Tuple[int, int]:
        """
        Get movement deltas for an action.

        Args:
            action: The action to get deltas for

        Returns:
            (dx, dy) tuple, or (0, 0) for non-movement actions

        Educational Note:
            Helper method to extract movement from an action.
            Useful when you have an Action enum value and need
            the corresponding movement vector.

        Example:
            >>> handler = InputHandler()
            >>> dx, dy = handler.get_movement_delta(Action.MOVE_UP)
            >>> assert dx == 0 and dy == -1
        """
        movement_map = {
            Action.MOVE_UP: (0, -1),
            Action.MOVE_DOWN: (0, 1),
            Action.MOVE_LEFT: (-1, 0),
            Action.MOVE_RIGHT: (1, 0),
            Action.MOVE_UP_LEFT: (-1, -1),
            Action.MOVE_UP_RIGHT: (1, -1),
            Action.MOVE_DOWN_LEFT: (-1, 1),
            Action.MOVE_DOWN_RIGHT: (1, 1),
        }
        return movement_map.get(action, (0, 0))

    def is_movement_action(self, action: Action) -> bool:
        """
        Check if an action is a movement action.

        Args:
            action: Action to check

        Returns:
            True if action is movement, False otherwise

        Example:
            >>> handler = InputHandler()
            >>> assert handler.is_movement_action(Action.MOVE_UP) is True
            >>> assert handler.is_movement_action(Action.WAIT) is False
        """
        return action in [
            Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT,
            Action.MOVE_UP_LEFT, Action.MOVE_UP_RIGHT,
            Action.MOVE_DOWN_LEFT, Action.MOVE_DOWN_RIGHT
        ]

    def get_help_text(self) -> str:
        """
        Get help text showing available commands.

        Returns:
            Multi-line string describing controls

        Educational Note:
            In-game help is essential for usability. This text can be
            displayed when player presses '?' or 'help'.

        Example:
            >>> handler = InputHandler()
            >>> print(handler.get_help_text())
        """
        return """
╔═══════════════════════════════════════════════════════════╗
║                    GAME CONTROLS                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Movement (WASD):                                         ║
║    q w e      Move with WASD + QE/ZC for diagonals       ║
║    a   d                                                  ║
║    z   c                                                  ║
║                                                           ║
║  Movement (Vi keys):                                      ║
║    y k u      Classic roguelike controls                 ║
║    h   l                                                  ║
║    b j n                                                  ║
║                                                           ║
║  Other Commands:                                          ║
║    . or space  - Wait (skip turn)                        ║
║    quit/exit   - Quit game                               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """.strip()
