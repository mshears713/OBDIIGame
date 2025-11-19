"""
Input Handler

Translates Arcade keyboard input into game commands.
Maintains compatibility with the existing game engine's input system.
"""

import arcade
from src.systems.input_handler import Action, Command
from typing import Optional


class ArcadeInputHandler:
    """
    Handles keyboard input for the Arcade GUI and translates to game commands.

    This bridges between Arcade's event system and the game engine's
    command-based input system.
    """

    def __init__(self):
        """Initialize the input handler."""
        # Track currently pressed keys for continuous movement
        self.keys_pressed = set()

        # Key mappings
        self._setup_key_mappings()

    def _setup_key_mappings(self):
        """Set up keyboard mappings to game actions."""
        # Movement mappings
        self.movement_keys = {
            # Arrow keys
            arcade.key.UP: (0, 1),
            arcade.key.DOWN: (0, -1),
            arcade.key.LEFT: (-1, 0),
            arcade.key.RIGHT: (1, 0),

            # WASD
            arcade.key.W: (0, 1),
            arcade.key.S: (0, -1),
            arcade.key.A: (-1, 0),
            arcade.key.D: (1, 0),

            # Numpad
            arcade.key.NUM_8: (0, 1),
            arcade.key.NUM_2: (0, -1),
            arcade.key.NUM_4: (-1, 0),
            arcade.key.NUM_6: (1, 0),
            arcade.key.NUM_7: (-1, 1),
            arcade.key.NUM_9: (1, 1),
            arcade.key.NUM_1: (-1, -1),
            arcade.key.NUM_3: (1, -1),
        }

        # Action mappings
        self.action_keys = {
            arcade.key.SPACE: 'wait',
            arcade.key.PERIOD: 'wait',
            arcade.key.NUM_5: 'wait',

            arcade.key.I: 'inventory',
            arcade.key.G: 'get',
            arcade.key.E: 'use',
            arcade.key.R: 'drop',

            arcade.key.SLASH: 'help',  # '?' key (with shift)
            arcade.key.H: 'help',

            arcade.key.Q: 'quit',
            arcade.key.ESCAPE: 'quit',

            # Subsystem navigation (future)
            arcade.key.GREATER: 'descend',  # '>' key
            arcade.key.LESS: 'ascend',      # '<' key
        }

    def on_key_press(self, key: int, modifiers: int) -> Optional[Command]:
        """
        Handle key press event.

        Args:
            key: The key that was pressed (arcade.key constant)
            modifiers: Modifier keys held (shift, ctrl, etc.)

        Returns:
            Command object if the key maps to an action, None otherwise
        """
        self.keys_pressed.add(key)

        # Check for movement
        if key in self.movement_keys:
            dx, dy = self.movement_keys[key]
            return self._create_movement_command(dx, dy)

        # Check for actions
        if key in self.action_keys:
            action_name = self.action_keys[key]
            return self._create_action_command(action_name)

        return None

    def on_key_release(self, key: int, modifiers: int):
        """
        Handle key release event.

        Args:
            key: The key that was released
            modifiers: Modifier keys held
        """
        self.keys_pressed.discard(key)

    def _create_movement_command(self, dx: int, dy: int) -> Command:
        """
        Create a movement command.

        Args:
            dx: X direction (-1, 0, or 1)
            dy: Y direction (-1, 0, or 1)

        Returns:
            Command object for movement
        """
        # Map dx/dy to Action
        if dx == 0 and dy == 1:
            action = Action.MOVE_NORTH
        elif dx == 0 and dy == -1:
            action = Action.MOVE_SOUTH
        elif dx == -1 and dy == 0:
            action = Action.MOVE_WEST
        elif dx == 1 and dy == 0:
            action = Action.MOVE_EAST
        elif dx == -1 and dy == 1:
            action = Action.MOVE_NORTHWEST
        elif dx == 1 and dy == 1:
            action = Action.MOVE_NORTHEAST
        elif dx == -1 and dy == -1:
            action = Action.MOVE_SOUTHWEST
        elif dx == 1 and dy == -1:
            action = Action.MOVE_SOUTHEAST
        else:
            action = Action.WAIT

        return Command(action=action, dx=dx, dy=dy)

    def _create_action_command(self, action_name: str) -> Command:
        """
        Create an action command.

        Args:
            action_name: Name of the action (e.g., 'wait', 'quit')

        Returns:
            Command object for the action
        """
        action_map = {
            'wait': Action.WAIT,
            'quit': Action.QUIT,
            'inventory': Action.INVENTORY,
            'get': Action.GET,
            'use': Action.USE,
            'drop': Action.DROP,
            'help': Action.HELP,
            'descend': Action.DESCEND,
            'ascend': Action.ASCEND,
        }

        action = action_map.get(action_name, Action.WAIT)
        return Command(action=action, dx=0, dy=0)

    def is_key_pressed(self, key: int) -> bool:
        """
        Check if a key is currently pressed.

        Args:
            key: The key to check

        Returns:
            True if the key is pressed
        """
        return key in self.keys_pressed
