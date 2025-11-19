"""Main game window for Pygame GUI.

This module manages the Pygame window, event loop, and coordinates
all GUI systems while interfacing with the existing game engine.
"""

import pygame
import sys
from typing import Optional
from enum import Enum

from src.game_loop import Game, GameState
from src.components.position import PositionComponent
from src.components.health import HealthComponent
from src.systems.input_handler import Action

from .config import PygameConfig, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from .renderer import PygameRenderer
from .input import PygameInputHandler
from .assets import AssetManager


class WindowState(Enum):
    """States for the game window."""
    RUNNING = "running"
    PAUSED = "paused"
    QUIT = "quit"


class GameWindow:
    """Main Pygame window for OBD-II Chronicles."""

    def __init__(self, config: Optional[PygameConfig] = None):
        """Initialize the game window.

        Args:
            config: Pygame configuration (uses defaults if None)
        """
        self.config = config or PygameConfig()

        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        # Create window
        self.screen = None
        self.clock = None
        self.running = False

        # Game systems
        self.game: Optional[Game] = None
        self.renderer: Optional[PygameRenderer] = None
        self.input_handler = PygameInputHandler()
        self.asset_manager: Optional[AssetManager] = None

        # Window state
        self.state = WindowState.RUNNING
        self.last_damage_dealt = {}  # Track damage for floating text

    def init_window(self):
        """Initialize the Pygame window and subsystems."""
        # Create screen
        self.screen = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height)
        )
        pygame.display.set_caption("OBD-II Chronicles")

        # Create clock for FPS control
        self.clock = pygame.time.Clock()

        # Initialize asset manager
        self.asset_manager = AssetManager(self.config.tile_size)

        # Initialize renderer
        self.renderer = PygameRenderer(
            self.screen,
            self.asset_manager,
            self.config
        )

        # Load music if enabled
        if self.config.enable_sound:
            if self.asset_manager.load_music("ambient"):
                self.asset_manager.play_music(self.config.music_volume)

        # Create game instance
        # Calculate map size based on viewport
        map_width = max(80, self.config.viewport_width * 2)
        map_height = max(45, self.config.viewport_height * 2)
        self.game = Game(width=map_width, height=map_height)

        # Mark as running
        self.running = True

        print("Pygame window initialized successfully!")
        print(f"Window size: {self.config.window_width}x{self.config.window_height}")
        print(f"Tile size: {self.config.tile_size}px")
        print(f"Map size: {map_width}x{map_height} tiles")
        print("\nControls:")
        print("  WASD / Arrow Keys / Vi keys (hjkl) - Move")
        print("  Q/E/Z/C - Diagonal movement")
        print("  Space / Period - Wait")
        print("  ESC - Quit")

    def run_loop(self):
        """Run the main game loop."""
        if not self.running:
            raise RuntimeError("Window must be initialized before running loop")

        while self.running and self.game.state == GameState.PLAYING:
            # Calculate delta time
            dt = self.clock.tick(self.config.fps) / 1000.0

            # Handle events
            self.handle_events()

            # Render frame
            self.render_frame(dt)

            # Update display
            pygame.display.flip()

        # Game over
        self._show_game_over_screen()

    def handle_events(self):
        """Handle Pygame events and convert to game commands."""
        for event in pygame.event.get():
            # Handle event
            command = self.input_handler.handle_event(event)

            # Check for quit
            if self.input_handler.quit_requested:
                self.running = False
                self.game.state = GameState.QUIT
                return

            # Process command if valid
            if command:
                self._process_game_command(command)

    def _process_game_command(self, command):
        """Process a game command and update game state.

        Args:
            command: Command object to process
        """
        # Get player position before action
        player_pos = self.game.player.get_component(PositionComponent)
        if not player_pos:
            return

        # Handle quit action
        if command.action == Action.QUIT:
            self.running = False
            self.game.state = GameState.QUIT
            return

        # Handle movement actions
        if self.input_handler.is_movement_action(command.action):
            target_x = player_pos.x + command.dx
            target_y = player_pos.y + command.dy

            # Check for entity at target position
            target_entity = self.game.combat_system.get_entity_at_position(
                target_x, target_y, self.game.entities
            )

            if target_entity:
                # Get health before attack
                target_health = target_entity.get_component(HealthComponent)
                hp_before = target_health.current_hp if target_health else 0

                # Attack
                self.game.combat_system.attack(
                    self.game.player,
                    target_entity,
                    self.game.message_log
                )

                # Calculate damage dealt
                if target_health:
                    damage = hp_before - target_health.current_hp
                    if damage > 0 and self.config.enable_floating_text:
                        # Add floating text
                        self.renderer.add_floating_text(
                            f"-{damage}",
                            target_x,
                            target_y,
                            (255, 100, 100)
                        )

                    # Add particles on hit
                    if damage > 0 and self.config.enable_particles:
                        self._spawn_hit_particles(target_x, target_y)

                # Play attack sound
                if self.config.enable_sound:
                    self.asset_manager.play_sound("attack", self.config.sfx_volume)

                # End turn
                self.game.end_turn()

            else:
                # Try to move
                success = self.game.movement_system.try_move(
                    self.game.player,
                    command.dx,
                    command.dy,
                    self.game.entities
                )

                if success:
                    # Auto-pickup items
                    self.game.try_auto_pickup()

                    # Play movement sound
                    if self.config.enable_sound:
                        self.asset_manager.play_sound("step", self.config.sfx_volume)

                    # End turn
                    self.game.end_turn()
                else:
                    # Play blocked sound
                    if self.config.enable_sound:
                        self.asset_manager.play_sound("blocked", self.config.sfx_volume)

        # Handle wait action
        elif command.action == Action.WAIT:
            self.game.end_turn()

    def _spawn_hit_particles(self, x: int, y: int, count: int = 5):
        """Spawn particle effects at a position.

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            count: Number of particles to spawn
        """
        import random

        for _ in range(count):
            # Random velocity
            vx = random.uniform(-50, 50)
            vy = random.uniform(-50, 50)

            # Red/orange/yellow particles
            color_choice = random.choice([
                (255, 100, 100),  # Red
                (255, 150, 50),   # Orange
                (255, 255, 100)   # Yellow
            ])

            self.renderer.add_particle(
                x, y, vx, vy,
                color_choice,
                size=random.randint(2, 5),
                lifetime=random.uniform(0.3, 0.8)
            )

    def render_frame(self, dt: float):
        """Render a single frame.

        Args:
            dt: Delta time since last frame
        """
        if not self.renderer or not self.game:
            return

        # Render game state
        self.renderer.render(
            self.game.game_map,
            self.game.entities,
            self.game.player,
            self.game.message_log,
            dt
        )

    def _show_game_over_screen(self):
        """Show game over screen."""
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Determine message
        if self.game.state == GameState.PLAYER_DEAD:
            title = "GAME OVER"
            message = "You have been defeated!"
            color = (220, 50, 50)
        elif self.game.state == GameState.VICTORY:
            title = "VICTORY!"
            message = "You have completed the mission!"
            color = (50, 220, 50)
        else:
            title = "QUIT"
            message = "Thanks for playing!"
            color = (200, 200, 200)

        # Render title
        title_surface = self.asset_manager.create_text_surface(
            title, 'title', color
        )
        title_rect = title_surface.get_rect(
            center=(self.config.window_width // 2,
                   self.config.window_height // 2 - 50)
        )
        self.screen.blit(title_surface, title_rect)

        # Render message
        message_surface = self.asset_manager.create_text_surface(
            message, 'hud', (200, 200, 200)
        )
        message_rect = message_surface.get_rect(
            center=(self.config.window_width // 2,
                   self.config.window_height // 2 + 20)
        )
        self.screen.blit(message_surface, message_rect)

        # Update display
        pygame.display.flip()

        # Wait for user input to close
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    waiting = False

            self.clock.tick(30)

    def cleanup(self):
        """Clean up resources and shutdown Pygame."""
        if self.asset_manager:
            self.asset_manager.cleanup()

        pygame.mixer.quit()
        pygame.quit()

    def __enter__(self):
        """Context manager entry."""
        self.init_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
