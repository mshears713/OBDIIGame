#!/usr/bin/env python3
"""Integration test for Pygame GUI.

This script verifies that the Pygame GUI correctly interfaces with
the game engine without running the full game.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import pygame
from gui.pygame_view import PygameConfig, PygameInputHandler
from gui.pygame_view.assets import AssetManager
from gui.pygame_view.animations import AnimationManager
from gui.pygame_view.renderer import PygameRenderer

from src.game_loop import Game
from src.components.position import PositionComponent
from src.components.health import HealthComponent
from src.systems.input_handler import Action


def test_config():
    """Test configuration system."""
    print("Testing configuration...")
    config = PygameConfig()
    assert config.tile_size == 16
    assert config.window_width == 1280
    assert config.window_height == 720
    assert config.fps == 60
    print("✓ Configuration system works")


def test_asset_manager():
    """Test asset management."""
    print("\nTesting asset manager...")
    pygame.init()

    asset_manager = AssetManager(tile_size=16)

    # Test sprite loading (fallback)
    sprite = asset_manager.get_tile_sprite('@', 'white')
    assert sprite is not None
    assert sprite.get_width() == 16
    assert sprite.get_height() == 16

    # Test font loading
    font = asset_manager.get_font('default')
    assert font is not None

    # Test text rendering
    text_surface = asset_manager.create_text_surface("Test", 'default', (255, 255, 255))
    assert text_surface is not None

    print("✓ Asset manager works")
    pygame.quit()


def test_animations():
    """Test animation system."""
    print("\nTesting animations...")
    pygame.init()

    anim_manager = AnimationManager(tile_size=16)

    # Test animated tiles
    assert anim_manager.is_animated('~')  # CAN pathway
    assert anim_manager.is_animated('*')  # Spark
    assert not anim_manager.is_animated('#')  # Wall (not animated)

    # Test frame retrieval
    frame = anim_manager.get_animation_frame('~')
    assert frame is not None
    assert frame.get_width() == 16

    # Test update
    anim_manager.update(0.1)

    print("✓ Animation system works")
    pygame.quit()


def test_input_handler():
    """Test input handling."""
    print("\nTesting input handler...")
    pygame.init()

    input_handler = PygameInputHandler()

    # Test key mappings
    assert pygame.K_w in input_handler.KEY_MAPPINGS
    assert pygame.K_UP in input_handler.KEY_MAPPINGS

    # Create a fake KEYDOWN event
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_w})
    command = input_handler.handle_event(event)

    assert command is not None
    assert command.action == Action.MOVE_UP
    assert command.dy == -1

    # Test movement action check
    assert input_handler.is_movement_action(Action.MOVE_UP)
    assert not input_handler.is_movement_action(Action.QUIT)

    print("✓ Input handler works")
    pygame.quit()


def test_renderer_creation():
    """Test renderer initialization."""
    print("\nTesting renderer...")
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    asset_manager = AssetManager(tile_size=16)
    config = PygameConfig(window_width=800, window_height=600)

    renderer = PygameRenderer(screen, asset_manager, config)

    assert renderer.viewport_width > 0
    assert renderer.viewport_height > 0
    assert renderer.animation_manager is not None

    print("✓ Renderer initializes correctly")
    pygame.quit()


def test_game_integration():
    """Test integration with game engine."""
    print("\nTesting game engine integration...")

    # Create game instance
    game = Game(width=80, height=45)

    # Verify game state
    assert game.game_map is not None
    assert game.player is not None
    assert len(game.entities) > 0

    # Verify player has required components
    pos = game.player.get_component(PositionComponent)
    assert pos is not None
    assert 0 <= pos.x < game.game_map.width
    assert 0 <= pos.y < game.game_map.height

    health = game.player.get_component(HealthComponent)
    assert health is not None
    assert health.current_hp > 0

    print("✓ Game engine integration works")


def test_rendering_integration():
    """Test that renderer can render game state."""
    print("\nTesting rendering integration...")
    pygame.init()

    # Create game
    game = Game(width=40, height=30)

    # Create renderer components
    screen = pygame.display.set_mode((800, 600))
    asset_manager = AssetManager(tile_size=16)
    config = PygameConfig(window_width=800, window_height=600)
    renderer = PygameRenderer(screen, asset_manager, config)

    # Try to render one frame
    try:
        renderer.render(
            game.game_map,
            game.entities,
            game.player,
            game.message_log,
            dt=0.016
        )
        print("✓ Rendering integration works")
    except Exception as e:
        print(f"✗ Rendering failed: {e}")
        raise

    pygame.quit()


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Pygame GUI Integration Tests")
    print("=" * 60)

    try:
        test_config()
        test_asset_manager()
        test_animations()
        test_input_handler()
        test_renderer_creation()
        test_game_integration()
        test_rendering_integration()

        print("\n" + "=" * 60)
        print("All integration tests passed! ✓")
        print("=" * 60)
        print("\nThe Pygame GUI is ready to use!")
        print("Run with: python run_pygame.py")
        return 0

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"Integration test failed: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
