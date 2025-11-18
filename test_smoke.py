#!/usr/bin/env python3
"""
Smoke test for game initialization and tutorial floor loading.
This script performs basic sanity checks on the game systems.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...", end=" ")
    try:
        from src.game_loop import Game
        from src.models import Map, Tile
        from src.data_loader.floor_builder import FloorBuilder
        from src.data_loader.entity_factory import EntityFactory
        from src.data_loader.json_loader import JSONLoader
        from src.entities.player import create_player
        from src.systems.renderer import Renderer
        from src.systems.movement import MovementSystem
        from src.systems.ai import AISystem
        from src.systems.combat import CombatSystem
        print("✓ OK")
        return True
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        return False

def test_json_configs():
    """Test that all JSON configuration files are valid."""
    print("Testing JSON configurations...", end=" ")
    try:
        from src.data_loader.json_loader import JSONLoader
        loader = JSONLoader()

        # Test floor loading
        floor_0 = loader.load_floor(0)
        if floor_0 is None:
            raise ValueError("Failed to load floor 0 (tutorial)")

        floor_1 = loader.load_floor(1)
        if floor_1 is None:
            raise ValueError("Failed to load floor 1")

        # Test enemy loading
        training_dummy = loader.load_enemy("training_dummy")
        if training_dummy is None:
            raise ValueError("Failed to load training_dummy enemy")

        weak_glitch = loader.load_enemy("weak_glitch")
        if weak_glitch is None:
            raise ValueError("Failed to load weak_glitch enemy")

        # Test item loading
        signal_boost = loader.load_item("signal_boost")
        if signal_boost is None:
            raise ValueError("Failed to load signal_boost item")

        starter_pack = loader.load_item("starter_pack")
        if starter_pack is None:
            raise ValueError("Failed to load starter_pack item")

        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_floor_building():
    """Test that floors can be built from JSON configurations."""
    print("Testing floor building...", end=" ")
    try:
        from src.data_loader.floor_builder import FloorBuilder
        builder = FloorBuilder()

        # Build tutorial floor
        tutorial_floor = builder.build_floor(0)
        if tutorial_floor is None:
            raise ValueError("Failed to build tutorial floor")

        # Verify floor properties
        if tutorial_floor.floor_id != 0:
            raise ValueError(f"Floor ID mismatch: expected 0, got {tutorial_floor.floor_id}")

        if tutorial_floor.width != 25 or tutorial_floor.height != 15:
            raise ValueError(f"Floor dimensions mismatch: expected 25x15, got {tutorial_floor.width}x{tutorial_floor.height}")

        # Build floor 1
        floor_1 = builder.build_floor(1)
        if floor_1 is None:
            raise ValueError("Failed to build floor 1")

        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_entity_factory():
    """Test that entities can be created from JSON configurations."""
    print("Testing entity factory...", end=" ")
    try:
        from src.data_loader.entity_factory import EntityFactory
        factory = EntityFactory()

        # Create training dummy
        dummy = factory.create_enemy("training_dummy", x=5, y=5)
        if dummy is None:
            raise ValueError("Failed to create training_dummy")

        # Create weak glitch
        glitch = factory.create_enemy("weak_glitch", x=10, y=10)
        if glitch is None:
            raise ValueError("Failed to create weak_glitch")

        # Create items
        boost = factory.create_item("signal_boost", x=15, y=15)
        if boost is None:
            raise ValueError("Failed to create signal_boost")

        pack = factory.create_item("starter_pack", x=20, y=20)
        if pack is None:
            raise ValueError("Failed to create starter_pack")

        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_player_creation():
    """Test that player entity can be created."""
    print("Testing player creation...", end=" ")
    try:
        from src.entities.player import create_player
        player = create_player(x=5, y=5)

        if player is None:
            raise ValueError("Failed to create player")

        # Verify player has required components
        from src.components import (
            PositionComponent, HealthComponent, CombatComponent,
            InventoryComponent, NameComponent, RenderComponent, InputComponent
        )

        if not player.get_component(PositionComponent):
            raise ValueError("Player missing PositionComponent")

        if not player.get_component(HealthComponent):
            raise ValueError("Player missing HealthComponent")

        if not player.get_component(CombatComponent):
            raise ValueError("Player missing CombatComponent")

        if not player.get_component(InventoryComponent):
            raise ValueError("Player missing InventoryComponent")

        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_game_initialization():
    """Test that the Game class can be initialized."""
    print("Testing game initialization...", end=" ")
    try:
        from src.game_loop import Game

        # Create game instance
        game = Game(width=80, height=45)

        if game is None:
            raise ValueError("Failed to create Game instance")

        # Verify game has required attributes
        if not hasattr(game, 'game_map'):
            raise ValueError("Game missing game_map attribute")

        if not hasattr(game, 'player'):
            raise ValueError("Game missing player attribute")

        if not hasattr(game, 'entities'):
            raise ValueError("Game missing entities attribute")

        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all smoke tests."""
    print("=" * 60)
    print("OBDII Game - Smoke Test Suite")
    print("=" * 60)
    print()

    tests = [
        test_imports,
        test_json_configs,
        test_floor_building,
        test_entity_factory,
        test_player_creation,
        test_game_initialization,
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✓ All {total} tests passed!")
        print("=" * 60)
        return 0
    else:
        failed = total - passed
        print(f"✗ {failed} of {total} tests failed")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
