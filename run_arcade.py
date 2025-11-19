#!/usr/bin/env python3
"""
Arcade GUI Entry Point for OBD-II Chronicles

This script launches the game with the Arcade-based graphical interface.
Falls back to CLI mode if Arcade is not available.

Usage:
    python run_arcade.py

Requirements:
    - Python 3.8+
    - arcade >= 2.6.17 (install with: pip install arcade)
"""

import sys


def check_arcade_available() -> bool:
    """
    Check if Arcade is available.

    Returns:
        True if arcade can be imported, False otherwise
    """
    try:
        import arcade
        return True
    except ImportError:
        return False


def run_arcade_gui():
    """Run the game with Arcade GUI."""
    try:
        from gui.arcade_view import GameWindow
        import arcade

        print("=" * 80)
        print(" " * 20 + "OBD-II CHRONICLES - ARCADE GUI")
        print(" " * 15 + "Exploring Automotive ECU Systems")
        print("=" * 80)
        print("\nInitializing Arcade GUI...")
        print(f"Arcade version: {arcade.VERSION}")

        # Create and run game window
        window = GameWindow()
        arcade.run()

        return 0

    except Exception as e:
        print(f"\nERROR: Failed to start Arcade GUI: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def run_cli_fallback():
    """Run the game with CLI interface (fallback)."""
    print("\n" + "=" * 80)
    print("Arcade not available - falling back to CLI mode")
    print("=" * 80)
    print("\nTo use the Arcade GUI, install arcade:")
    print("  pip install arcade\n")

    # Import and run CLI version
    from main import main
    return main()


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success)
    """
    # Check for --cli flag to force CLI mode
    if '--cli' in sys.argv:
        print("CLI mode forced via --cli flag")
        return run_cli_fallback()

    # Check if Arcade is available
    if check_arcade_available():
        return run_arcade_gui()
    else:
        return run_cli_fallback()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        print("Thank you for playing!")
        sys.exit(0)
