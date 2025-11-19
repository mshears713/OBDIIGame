"""
Arcade Game Window

Main window class that integrates the Arcade GUI with the game engine.
Handles setup, update loop, rendering, and input without changing core game logic.
"""

import arcade
from typing import Optional
from src.game_loop import Game, GameState
from src.entities.player import get_player_position
from .renderer import ArcadeRenderer
from .hud import HUD
from .input import ArcadeInputHandler
from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, TARGET_FPS,
    SHOW_FPS, FULLSCREEN
)


class GameWindow(arcade.Window):
    """
    Main game window for the Arcade GUI.

    This class bridges the Arcade event loop with the turn-based game engine,
    preserving all existing game logic while adding a modern visual layer.
    """

    def __init__(self, game: Optional[Game] = None):
        """
        Initialize the game window.

        Args:
            game: Optional existing Game instance. If None, creates a new one.
        """
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
            fullscreen=FULLSCREEN,
            update_rate=1/TARGET_FPS
        )

        # Game instance
        self.game = game if game is not None else Game(width=80, height=45)

        # GUI components
        self.renderer: Optional[ArcadeRenderer] = None
        self.hud: Optional[HUD] = None
        self.input_handler: Optional[ArcadeInputHandler] = None

        # Pending command (from keyboard input)
        self.pending_command = None

        # Frame time tracking
        self.frame_time = 0.0

        # Setup flag
        self.is_setup = False

    def setup(self):
        """
        Set up the game window.

        This initializes all GUI systems after the window is created.
        """
        # Initialize renderer
        self.renderer = ArcadeRenderer(self.game.game_map)

        # Initialize HUD
        self.hud = HUD()

        # Initialize input handler
        self.input_handler = ArcadeInputHandler()

        # Mark as setup
        self.is_setup = True

        print("Arcade GUI initialized!")
        print(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"Map: {self.game.game_map.width}x{self.game.game_map.height}")

    def on_draw(self):
        """
        Render the game.

        Called automatically by Arcade at the target frame rate.
        """
        if not self.is_setup:
            return

        # Clear the screen
        self.clear()

        # Draw game world
        if self.renderer:
            self.renderer.draw()

        # Draw HUD
        if self.hud:
            enemy_count = sum(1 for e in self.game.entities
                             if e.has_tag("enemy") and e != self.game.player)

            self.hud.draw(
                self.game.player,
                self.game.turn_count,
                enemy_count
            )

        # Draw FPS counter
        if SHOW_FPS:
            arcade.draw_text(
                f"FPS: {1/self.frame_time:.0f}" if self.frame_time > 0 else "FPS: --",
                10,
                SCREEN_HEIGHT - 25,
                arcade.color.YELLOW,
                12
            )

    def on_update(self, delta_time: float):
        """
        Update game state.

        Args:
            delta_time: Time elapsed since last update in seconds
        """
        if not self.is_setup:
            self.setup()
            return

        self.frame_time = delta_time

        # Update renderer (camera, animations, effects)
        if self.renderer:
            player_pos = get_player_position(self.game.player)
            self.renderer.update(delta_time, self.game.entities, player_pos)

        # Update HUD
        if self.hud:
            self.hud.update(self.game.player, self.game.turn_count, self.game.message_log)

        # Process pending command (turn-based gameplay)
        if self.pending_command:
            self._process_game_turn(self.pending_command)
            self.pending_command = None

        # Check game over
        if self.game.state != GameState.PLAYING:
            self._handle_game_over()

    def on_key_press(self, key: int, modifiers: int):
        """
        Handle key press events.

        Args:
            key: The key that was pressed
            modifiers: Modifier keys (shift, ctrl, etc.)
        """
        if not self.input_handler:
            return

        # Get command from input handler
        command = self.input_handler.on_key_press(key, modifiers)

        if command:
            # Handle special commands immediately
            if command.action.name == 'HELP':
                self._show_help()
                return

            # Queue command for next update
            self.pending_command = command

    def on_key_release(self, key: int, modifiers: int):
        """
        Handle key release events.

        Args:
            key: The key that was released
            modifiers: Modifier keys
        """
        if self.input_handler:
            self.input_handler.on_key_release(key, modifiers)

    def _process_game_turn(self, command):
        """
        Process a game turn with the given command.

        This integrates with the existing game engine logic.

        Args:
            command: The Command to execute
        """
        # Let the game process the command (uses existing game logic)
        self.game.process_command(command)

        # Create visual effects based on what happened
        self._create_turn_effects()

    def _create_turn_effects(self):
        """
        Create visual effects based on recent game events.

        This analyzes the message log to trigger appropriate particle effects.
        """
        if not self.renderer or not self.game.message_log:
            return

        # Get most recent messages
        recent_messages = self.game.message_log[-5:]

        for message in recent_messages:
            message_lower = message.lower()

            # Combat effects
            if 'hit' in message_lower or 'attack' in message_lower:
                # Create impact effect at player position
                player_pos = get_player_position(self.game.player)
                self.renderer.create_effect('impact', player_pos[0], player_pos[1])
                self.renderer.add_screen_shake(5, 0.2)

            elif 'damage' in message_lower:
                # Create spark effect
                player_pos = get_player_position(self.game.player)
                self.renderer.create_effect('spark', player_pos[0], player_pos[1])

            # Item pickup
            elif 'picked up' in message_lower:
                player_pos = get_player_position(self.game.player)
                self.renderer.create_effect('data', player_pos[0], player_pos[1])

            # Signal collection
            elif 'collected' in message_lower and 'signal' in message_lower:
                player_pos = get_player_position(self.game.player)
                self.renderer.create_effect('voltage', player_pos[0], player_pos[1])

    def _show_help(self):
        """Display help information."""
        help_text = """
OBD-II Chronicles - Controls

Movement:
  WASD or Arrow Keys - Move in 4 directions
  Numpad (1-9) - Move in 8 directions

Actions:
  Space/Period - Wait (skip turn)
  I - Inventory
  G - Get/Pick up items
  E - Use/Equip item
  R - Drop item

  > - Descend stairs
  < - Ascend stairs

Other:
  Q or ESC - Quit
  H - Help

Tips:
  - Walk into enemies to attack them
  - Collect signals from defeated enemies
  - Explore all subsystems to win!
"""
        print(help_text)
        self.game.add_message("Help displayed in console")

    def _handle_game_over(self):
        """Handle game over state."""
        if self.game.state == GameState.PLAYER_DEAD:
            self._show_death_screen()
        elif self.game.state == GameState.QUIT:
            self.close()
        elif self.game.state == GameState.VICTORY:
            self._show_victory_screen()

    def _show_death_screen(self):
        """Display death screen overlay."""
        # Draw semi-transparent overlay
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (0, 0, 0, 200)
        )

        # Draw "Game Over" text
        arcade.draw_text(
            "SYSTEM FAILURE",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.RED,
            48,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            f"You survived {self.game.turn_count} turns",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press Q to quit",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center"
        )

    def _show_victory_screen(self):
        """Display victory screen overlay."""
        # Draw semi-transparent overlay
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (0, 50, 0, 200)
        )

        # Draw "Victory" text
        arcade.draw_text(
            "SYSTEM RESTORED",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.GREEN,
            48,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            f"Victory in {self.game.turn_count} turns!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press Q to quit",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center"
        )


def run_arcade_game(game: Optional[Game] = None):
    """
    Run the game with Arcade GUI.

    Args:
        game: Optional existing Game instance
    """
    window = GameWindow(game)
    arcade.run()
