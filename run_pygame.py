#!/usr/bin/env python3
"""Entry point for Pygame GUI version of OBD-II Chronicles.

This script launches the game with the Pygame graphical interface
instead of the CLI ASCII renderer.

Usage:
    python run_pygame.py [options]

Options:
    --width WIDTH       Window width in pixels (default: 1280)
    --height HEIGHT     Window height in pixels (default: 720)
    --tile-size SIZE    Tile size in pixels (default: 16)
    --fps FPS           Target frames per second (default: 60)
    --no-animations     Disable tile animations
    --no-particles      Disable particle effects
    --no-sound          Disable sound and music
    --no-minimap        Disable minimap overlay
    --no-float-text     Disable floating combat text
    --fullscreen        Run in fullscreen mode
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.pygame_view import GameWindow, PygameConfig


def parse_args():
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="OBD-II Chronicles - Pygame GUI Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python run_pygame.py

  # Run in a larger window
  python run_pygame.py --width 1920 --height 1080

  # Run with larger tiles
  python run_pygame.py --tile-size 24

  # Run with effects disabled (better performance)
  python run_pygame.py --no-animations --no-particles

  # Run in fullscreen
  python run_pygame.py --fullscreen
        """
    )

    # Display options
    parser.add_argument(
        '--width',
        type=int,
        default=1280,
        help='Window width in pixels (default: 1280)'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=720,
        help='Window height in pixels (default: 720)'
    )
    parser.add_argument(
        '--tile-size',
        type=int,
        default=16,
        help='Tile size in pixels (default: 16)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=60,
        help='Target frames per second (default: 60)'
    )
    parser.add_argument(
        '--fullscreen',
        action='store_true',
        help='Run in fullscreen mode'
    )

    # Feature toggles
    parser.add_argument(
        '--no-animations',
        action='store_true',
        help='Disable tile animations'
    )
    parser.add_argument(
        '--no-particles',
        action='store_true',
        help='Disable particle effects'
    )
    parser.add_argument(
        '--no-sound',
        action='store_true',
        help='Disable sound and music'
    )
    parser.add_argument(
        '--no-minimap',
        action='store_true',
        help='Disable minimap overlay'
    )
    parser.add_argument(
        '--no-float-text',
        action='store_true',
        help='Disable floating combat text'
    )

    # Audio options
    parser.add_argument(
        '--music-volume',
        type=float,
        default=0.3,
        help='Music volume (0.0 to 1.0, default: 0.3)'
    )
    parser.add_argument(
        '--sfx-volume',
        type=float,
        default=0.5,
        help='Sound effects volume (0.0 to 1.0, default: 0.5)'
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point for Pygame GUI.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Parse command-line arguments
    args = parse_args()

    # Create configuration
    config = PygameConfig(
        tile_size=args.tile_size,
        window_width=args.width,
        window_height=args.height,
        fps=args.fps,
        music_volume=args.music_volume,
        sfx_volume=args.sfx_volume,
        enable_animations=not args.no_animations,
        enable_particles=not args.no_particles,
        enable_sound=not args.no_sound,
        enable_minimap=not args.no_minimap,
        enable_floating_text=not args.no_float_text,
    )

    # Print startup information
    print("=" * 60)
    print("OBD-II Chronicles - Pygame GUI Edition")
    print("=" * 60)
    print(f"Window size: {config.window_width}x{config.window_height}")
    print(f"Tile size: {config.tile_size}px")
    print(f"Target FPS: {config.fps}")
    print()
    print("Features:")
    print(f"  Animations: {'Enabled' if config.enable_animations else 'Disabled'}")
    print(f"  Particles: {'Enabled' if config.enable_particles else 'Disabled'}")
    print(f"  Sound: {'Enabled' if config.enable_sound else 'Disabled'}")
    print(f"  Minimap: {'Enabled' if config.enable_minimap else 'Disabled'}")
    print(f"  Floating text: {'Enabled' if config.enable_floating_text else 'Disabled'}")
    print("=" * 60)
    print()

    try:
        # Create and run game window
        with GameWindow(config) as window:
            window.run_loop()

        print("\nThank you for playing OBD-II Chronicles!")
        return 0

    except KeyboardInterrupt:
        print("\n\nGame interrupted by user")
        return 130

    except Exception as e:
        print(f"\n\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
