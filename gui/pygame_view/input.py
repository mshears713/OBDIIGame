"""Pygame input handler for OBD-II Chronicles.

This module extends the existing InputHandler to work with Pygame events
while maintaining compatibility with the existing command system.
"""

import pygame
from typing import Optional
from src.systems.input_handler import Command, Action


class PygameInputHandler:
    """Handles Pygame keyboard and mouse input, converting to game commands."""

    # Map pygame keys to actions and movement deltas
    KEY_MAPPINGS = {
        # Arrow keys
        pygame.K_UP: (Action.MOVE_UP, 0, -1),
        pygame.K_DOWN: (Action.MOVE_DOWN, 0, 1),
        pygame.K_LEFT: (Action.MOVE_LEFT, -1, 0),
        pygame.K_RIGHT: (Action.MOVE_RIGHT, 1, 0),

        # WASD keys
        pygame.K_w: (Action.MOVE_UP, 0, -1),
        pygame.K_s: (Action.MOVE_DOWN, 0, 1),
        pygame.K_a: (Action.MOVE_LEFT, -1, 0),
        pygame.K_d: (Action.MOVE_RIGHT, 1, 0),

        # Numpad
        pygame.K_KP8: (Action.MOVE_UP, 0, -1),
        pygame.K_KP2: (Action.MOVE_DOWN, 0, 1),
        pygame.K_KP4: (Action.MOVE_LEFT, -1, 0),
        pygame.K_KP6: (Action.MOVE_RIGHT, 1, 0),
        pygame.K_KP7: (Action.MOVE_UP_LEFT, -1, -1),
        pygame.K_KP9: (Action.MOVE_UP_RIGHT, 1, -1),
        pygame.K_KP1: (Action.MOVE_DOWN_LEFT, -1, 1),
        pygame.K_KP3: (Action.MOVE_DOWN_RIGHT, 1, 1),
        pygame.K_KP5: (Action.WAIT, 0, 0),

        # Vi keys (hjkl)
        pygame.K_h: (Action.MOVE_LEFT, -1, 0),
        pygame.K_j: (Action.MOVE_DOWN, 0, 1),
        pygame.K_k: (Action.MOVE_UP, 0, -1),
        pygame.K_l: (Action.MOVE_RIGHT, 1, 0),
        pygame.K_y: (Action.MOVE_UP_LEFT, -1, -1),
        pygame.K_u: (Action.MOVE_UP_RIGHT, 1, -1),
        pygame.K_b: (Action.MOVE_DOWN_LEFT, -1, 1),
        pygame.K_n: (Action.MOVE_DOWN_RIGHT, 1, 1),

        # Wait/rest
        pygame.K_PERIOD: (Action.WAIT, 0, 0),
        pygame.K_SPACE: (Action.WAIT, 0, 0),
    }

    # Diagonal movement with modifier keys
    DIAGONAL_MAPPINGS = {
        # Q and E for diagonals (common in roguelikes)
        pygame.K_q: (Action.MOVE_UP_LEFT, -1, -1),
        pygame.K_e: (Action.MOVE_UP_RIGHT, 1, -1),
        pygame.K_z: (Action.MOVE_DOWN_LEFT, -1, 1),
        pygame.K_c: (Action.MOVE_DOWN_RIGHT, 1, 1),
    }

    # Add diagonal mappings to main mappings
    KEY_MAPPINGS.update(DIAGONAL_MAPPINGS)

    def __init__(self):
        """Initialize the Pygame input handler."""
        self.last_command: Optional[Command] = None
        self.mouse_position: Optional[tuple[int, int]] = None
        self.quit_requested = False

    def handle_event(self, event: pygame.event.Event) -> Optional[Command]:
        """Handle a Pygame event and return a command if applicable.

        Args:
            event: Pygame event to handle

        Returns:
            Command object if event corresponds to a game action, None otherwise
        """
        if event.type == pygame.QUIT:
            self.quit_requested = True
            return Command(action=Action.QUIT)

        elif event.type == pygame.KEYDOWN:
            return self._handle_keydown(event)

        elif event.type == pygame.MOUSEMOTION:
            self.mouse_position = event.pos

        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_click(event)

        return None

    def _handle_keydown(self, event: pygame.event.Event) -> Optional[Command]:
        """Handle a key press event.

        Args:
            event: Pygame KEYDOWN event

        Returns:
            Command object if key corresponds to a game action, None otherwise
        """
        # Check for Escape or Q to quit
        if event.key == pygame.K_ESCAPE or (event.key == pygame.K_q and
                                            event.mod & pygame.KMOD_CTRL):
            self.quit_requested = True
            return Command(action=Action.QUIT)

        # Check for mapped keys
        if event.key in self.KEY_MAPPINGS:
            action, dx, dy = self.KEY_MAPPINGS[event.key]
            command = Command(action=action, dx=dx, dy=dy)
            self.last_command = command
            return command

        # No command for this key
        return None

    def _handle_mouse_click(self, event: pygame.event.Event) -> Optional[Command]:
        """Handle a mouse click event.

        Args:
            event: Pygame MOUSEBUTTONDOWN event

        Returns:
            Command object for mouse action, or None
        """
        # Left click - could be used for movement or interaction
        # For now, we'll leave this as a hook for future implementation
        if event.button == 1:  # Left click
            # TODO: Implement click-to-move or click-to-attack
            pass

        return None

    def is_movement_action(self, action: Action) -> bool:
        """Check if an action is a movement action.

        Args:
            action: Action to check

        Returns:
            True if action is movement, False otherwise
        """
        movement_actions = {
            Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT,
            Action.MOVE_UP_LEFT, Action.MOVE_UP_RIGHT,
            Action.MOVE_DOWN_LEFT, Action.MOVE_DOWN_RIGHT
        }
        return action in movement_actions

    def reset(self):
        """Reset the input handler state."""
        self.last_command = None
        self.mouse_position = None
        self.quit_requested = False
