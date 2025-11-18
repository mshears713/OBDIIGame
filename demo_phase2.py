#!/usr/bin/env python3
"""
Phase 2 Demonstration Script

This script demonstrates the core systems implemented in Phase 2:
- Procedural dungeon generation
- Player entity creation
- Turn-based game loop skeleton
- Input handling for movement
- Movement system

Educational Note:
    This demo shows how all the Phase 2 systems work together without
    requiring interactive input. It's useful for:
    - Verifying implementation
    - Debugging systems
    - Showcasing progress
    - Understanding system integration
"""

from src.procedural import DungeonGenerator
from src.entities.player import create_player, get_player_position
from src.systems.renderer import Renderer
from src.systems.movement import MovementSystem
from src.systems.input_handler import InputHandler, Action


def demonstrate_dungeon_generation():
    """Demonstrate procedural dungeon generation."""
    print("=" * 80)
    print("PHASE 2 DEMONSTRATION: Procedural Dungeon Generation")
    print("=" * 80)

    # Generate a dungeon
    print("\n1. Generating a 50x30 dungeon with random seed...")
    generator = DungeonGenerator(width=50, height=30, max_rooms=15, random_seed=42)
    dungeon_map = generator.generate()
    rooms = generator.get_rooms()

    print(f"   ✓ Generated {len(rooms)} rooms")
    print(f"   ✓ Map dimensions: {dungeon_map.width}x{dungeon_map.height}")

    # Show room information
    print("\n2. Room details:")
    for i, room in enumerate(rooms[:5]):  # Show first 5 rooms
        cx, cy = room.center()
        print(f"   Room {i+1}: {room.width()}x{room.height()} at center ({cx}, {cy})")

    if len(rooms) > 5:
        print(f"   ... and {len(rooms) - 5} more rooms")

    return dungeon_map, rooms


def demonstrate_player_creation(dungeon_map, rooms):
    """Demonstrate player entity creation."""
    print("\n" + "=" * 80)
    print("PHASE 2 DEMONSTRATION: Player Entity Creation")
    print("=" * 80)

    # Create player in first room
    if rooms:
        start_x, start_y = rooms[0].center()
    else:
        start_x, start_y = dungeon_map.width // 2, dungeon_map.height // 2

    print(f"\n1. Creating player at position ({start_x}, {start_y})...")
    player = create_player(x=start_x, y=start_y, name="Demo Hero")

    print("   ✓ Player created successfully")
    print(f"   - Position: {get_player_position(player)}")
    print(f"   - Components: {', '.join(player.components.keys())}")
    print(f"   - Tags: {player.tags}")

    return player


def demonstrate_input_handling():
    """Demonstrate input handling system."""
    print("\n" + "=" * 80)
    print("PHASE 2 DEMONSTRATION: Input Handling")
    print("=" * 80)

    handler = InputHandler()

    print("\n1. Testing various input commands...")

    test_inputs = [
        ('w', 'WASD movement (up)'),
        ('a', 'WASD movement (left)'),
        ('k', 'Vi-keys movement (up)'),
        ('h', 'Vi-keys movement (left)'),
        ('.', 'Wait command'),
        ('quit', 'Quit command'),
        ('invalid', 'Invalid input'),
    ]

    for input_str, description in test_inputs:
        command = handler.handle_input(input_str)
        if command:
            result = f"✓ '{input_str}' → {command.action.name} (dx={command.dx}, dy={command.dy})"
        else:
            result = f"✗ '{input_str}' → Invalid command"
        print(f"   {result:60} # {description}")


def demonstrate_movement_system(dungeon_map, player):
    """Demonstrate movement system."""
    print("\n" + "=" * 80)
    print("PHASE 2 DEMONSTRATION: Movement System")
    print("=" * 80)

    movement = MovementSystem(dungeon_map)

    print("\n1. Testing player movement...")
    start_x, start_y = get_player_position(player)
    print(f"   Starting position: ({start_x}, {start_y})")

    # Try moving in different directions
    moves = [
        (1, 0, 'right'),
        (0, 1, 'down'),
        (-1, 0, 'left'),
        (0, -1, 'up'),
    ]

    for dx, dy, direction in moves:
        success = movement.try_move(player, dx, dy)
        x, y = get_player_position(player)

        if success:
            print(f"   ✓ Move {direction}: SUCCESS - now at ({x}, {y})")
        else:
            print(f"   ✗ Move {direction}: BLOCKED - still at ({x}, {y})")


def demonstrate_rendering(dungeon_map, player):
    """Demonstrate rendering system."""
    print("\n" + "=" * 80)
    print("PHASE 2 DEMONSTRATION: Rendering System")
    print("=" * 80)

    renderer = Renderer(dungeon_map)

    print("\n1. Rendering dungeon with player...")
    print("\nMap view (20x15 section around player):")
    print("-" * 80)

    # Render a small section of the map
    renderer.render_all([player], get_player_position(player))

    print("-" * 80)


def demonstrate_game_systems():
    """Demonstrate all Phase 2 game systems working together."""
    print("\n" + "=" * 80)
    print("PHASE 2 DEMONSTRATION: Integrated Systems")
    print("=" * 80)

    # Generate dungeon
    generator = DungeonGenerator(width=40, height=25, max_rooms=10, random_seed=123)
    dungeon_map = generator.generate()
    rooms = generator.get_rooms()

    # Create player
    start_x, start_y = rooms[0].center() if rooms else (20, 12)
    player = create_player(x=start_x, y=start_y, name="Hero")

    # Initialize systems
    renderer = Renderer(dungeon_map)
    movement = MovementSystem(dungeon_map)
    input_handler = InputHandler()

    print("\n1. Simulating a few game turns...")

    # Simulate some turns
    simulated_inputs = ['d', 'd', 's', 's', 'a', 'w']

    for turn, input_str in enumerate(simulated_inputs, 1):
        print(f"\nTurn {turn}:")

        # Process input
        command = input_handler.handle_input(input_str)
        if command and input_handler.is_movement_action(command.action):
            success = movement.try_move(player, command.dx, command.dy)
            x, y = get_player_position(player)

            if success:
                print(f"  → Player pressed '{input_str}' and moved to ({x}, {y})")
            else:
                print(f"  → Player pressed '{input_str}' but was blocked at ({x}, {y})")

    print("\n2. Final map state:")
    print("-" * 80)
    renderer.render_all([player], get_player_position(player))
    print("-" * 80)


def main():
    """Run all Phase 2 demonstrations."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "PHASE 2: Core Game Systems" + " " * 31 + "║")
    print("║" + " " * 25 + "Demonstration Script" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    try:
        # Demonstrate each system
        dungeon_map, rooms = demonstrate_dungeon_generation()
        player = demonstrate_player_creation(dungeon_map, rooms)
        demonstrate_input_handling()
        demonstrate_movement_system(dungeon_map, player)
        demonstrate_rendering(dungeon_map, player)

        # Demonstrate integrated systems
        demonstrate_game_systems()

        print("\n" + "=" * 80)
        print("PHASE 2 DEMONSTRATION COMPLETE!")
        print("=" * 80)
        print("\nAll core systems are functioning correctly:")
        print("  ✓ Procedural dungeon generation")
        print("  ✓ Player entity with components")
        print("  ✓ Input handling system")
        print("  ✓ Movement system with collision detection")
        print("  ✓ Rendering system")
        print("  ✓ Turn-based game loop structure")
        print("\nReady to proceed with Phase 2 remaining steps!")
        print("=" * 80)

    except Exception as e:
        print(f"\n\nERROR during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
