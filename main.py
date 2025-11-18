#!/usr/bin/env python3
"""
Main Entry Point for Modular Python Roguelike

This script serves as the primary entry point for the game, orchestrating:
1. Game initialization
2. Main game loop execution
3. Graceful shutdown and cleanup

Educational Note:
The `if __name__ == "__main__":` pattern ensures this code only runs when
the script is executed directly, not when imported as a module. This is a
Python best practice for creating reusable, testable code.
"""

import sys
from typing import Optional

from src.game_loop import Game


def main() -> int:
    """
    Main function coordinating game execution flow.

    Returns:
        int: Exit code (0 for success, non-zero for errors)

    Educational Note:
        Returning exit codes is a Unix/Linux convention that allows other
        programs or scripts to detect whether your program succeeded or failed.
        0 means success, non-zero values indicate various error conditions.
    """
    try:
        print("=" * 80)
        print(" " * 20 + "MODULAR PYTHON ROGUELIKE")
        print(" " * 15 + "Exploring Automotive ECU Systems")
        print("=" * 80)
        print("\nInitializing game...")

        # Create and run the game
        game = Game(width=80, height=45)
        game.run()

        return 0

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGame interrupted by user.")
        print("Thank you for playing!")
        return 0

    except Exception as e:
        # Catch unexpected errors and display helpful message
        print(f"\nERROR: An unexpected error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        print("\nPlease report this issue if it persists.", file=sys.stderr)
        return 1


# Entry point guard - this code only runs when script is executed directly
if __name__ == "__main__":
    # sys.exit() passes the return code to the operating system
    sys.exit(main())
