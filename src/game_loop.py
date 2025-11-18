"""
Turn-Based Game Loop

This module implements the main game loop for the turn-based roguelike.

Educational Notes:
------------------
The game loop is the heart of any game. In a turn-based game, the loop:
1. Displays the current game state
2. Waits for player input
3. Processes the input (validate, execute action)
4. Updates game state
5. Checks for game over conditions
6. Repeats

This differs from real-time game loops which run continuously and handle
timing/frame rates. Turn-based loops are simpler:
- No timing concerns (game waits for player)
- Discrete steps (one action per turn)
- Easier to debug (can pause and inspect state)

Key Design Principles:
- Clear phase separation (render, input, update)
- Each phase has single responsibility
- State transitions are explicit
- Easy to extend (add new phases/systems)
"""

from typing import List, Optional
from enum import Enum, auto

from src.models import Map
from src.entities.entity import Entity
from src.entities.player import (
    create_player,
    is_player_alive,
    get_player_position
)
from src.procedural import DungeonGenerator, Room
from src.systems.renderer import Renderer
from src.systems.movement import MovementSystem
from src.systems.input_handler import InputHandler, Action, Command
from src.components import PositionComponent


class GameState(Enum):
    """
    Enumeration of possible game states.

    Educational Note:
        Games have multiple states (menus, gameplay, game over, etc.).
        Using an Enum makes state management clearer and prevents bugs
        from typos in state names.
    """
    PLAYING = auto()      # Normal gameplay
    PLAYER_DEAD = auto()  # Player died
    QUIT = auto()         # Player quit
    VICTORY = auto()      # Player won (future)


class Game:
    """
    Main game controller managing the turn-based game loop.

    Attributes:
        game_map: The current dungeon floor
        player: The player entity
        entities: List of all entities in the game
        renderer: System for drawing the game
        movement_system: System for handling movement
        input_handler: System for processing input
        state: Current game state
        turn_count: Number of turns elapsed
        message_log: List of messages to display

    Educational Note:
        The Game class is the central coordinator. It:
        - Owns all game state
        - Manages systems (renderer, movement, etc.)
        - Controls the main loop
        - Enforces game rules

        This is sometimes called a "manager" or "controller" pattern.
    """

    def __init__(self, width: int = 80, height: int = 45):
        """
        Initialize the game.

        Args:
            width: Dungeon width in tiles
            height: Dungeon height in tiles

        Educational Note:
            Initialization sets up the game world. We:
            1. Generate the dungeon
            2. Create the player
            3. Spawn the player in the first room
            4. Initialize systems
            5. Set initial game state
        """
        # Game state
        self.state = GameState.PLAYING
        self.turn_count = 0
        self.message_log: List[str] = []

        # Generate dungeon
        generator = DungeonGenerator(width=width, height=height)
        self.game_map = generator.generate()
        self.rooms = generator.get_rooms()

        # Create player in first room
        if self.rooms:
            start_x, start_y = self.rooms[0].center()
        else:
            start_x, start_y = width // 2, height // 2

        self.player = create_player(x=start_x, y=start_y, name="Player")

        # Entity list (player + enemies + items in future)
        self.entities: List[Entity] = [self.player]

        # Initialize systems
        self.renderer = Renderer(self.game_map)
        self.movement_system = MovementSystem(self.game_map)
        self.input_handler = InputHandler()

        # Welcome message
        self.add_message("Welcome to the OBDII Game! Explore the ECU system.")
        self.add_message("Press '?' for help.")

    def run(self) -> None:
        """
        Run the main game loop.

        Educational Note:
            This is the core game loop. It runs until the game ends
            (player dies, quits, or wins).

            The loop structure:
            - while game is running:
                1. Render
                2. Get input
                3. Process input
                4. Update state
                5. Check game over

            Each iteration is one "turn" in the turn-based system.
        """
        while self.state == GameState.PLAYING:
            # Phase 1: Render current state
            self.render()

            # Phase 2: Get player input
            command = self.get_player_input()

            # Phase 3: Process input
            if command:
                self.process_command(command)

            # Phase 4: Check game over conditions
            self.check_game_over()

        # Game ended - show end screen
        self.render()
        self.show_end_screen()

    def render(self) -> None:
        """
        Render the current game state.

        Educational Note:
            Rendering displays the game world to the player. We show:
            - The dungeon map
            - All entities (player, enemies, items)
            - Player stats (HP, etc.)
            - Recent messages

            We render in a specific order (back to front):
            1. Map tiles
            2. Items (render_order=1)
            3. Creatures (render_order=3)
            4. Effects (render_order=4)

            The renderer handles the details, we just call it.
        """
        # Clear screen (in a real terminal, we'd use curses or similar)
        print("\n" * 2)  # Simple newlines for now

        # Render map and entities
        self.renderer.render_all(self.entities, get_player_position(self.player))

        # Render UI info
        self.render_ui()

    def render_ui(self) -> None:
        """
        Render UI elements (stats, messages).

        Educational Note:
            The UI shows important information:
            - Player health
            - Turn counter
            - Recent messages
            - Controls reminder

            We separate UI rendering from map rendering for clarity.
        """
        # Get player stats
        from src.entities.player import get_player_health
        current_hp, max_hp = get_player_health(self.player)
        hp_percentage = (current_hp / max_hp) * 100 if max_hp > 0 else 0

        # Create HP bar
        bar_width = 20
        filled = int((current_hp / max_hp) * bar_width) if max_hp > 0 else 0
        hp_bar = '█' * filled + '░' * (bar_width - filled)

        # Display stats
        print("\n" + "═" * 80)
        print(f"HP: [{hp_bar}] {current_hp}/{max_hp} ({hp_percentage:.0f}%)")
        print(f"Turn: {self.turn_count}")

        # Display recent messages (last 5)
        print("\n" + "─" * 80)
        print("Messages:")
        for msg in self.message_log[-5:]:
            print(f"  {msg}")
        print("─" * 80)

    def get_player_input(self) -> Optional['Command']:
        """
        Get and validate player input.

        Returns:
            Command object if input valid, None otherwise

        Educational Note:
            This method handles the input phase:
            1. Prompt for input
            2. Read user input
            3. Parse input into command
            4. Validate command
            5. Return command or None

            Invalid input doesn't consume a turn - player can retry.
        """
        while True:
            user_input = input("\n> ").strip()

            # Special case: help
            if user_input.lower() in ['?', 'help']:
                print(self.input_handler.get_help_text())
                continue

            # Parse input
            command = self.input_handler.handle_input(user_input)

            if command:
                return command
            else:
                print("Invalid command. Press '?' for help.")

    def process_command(self, command: 'Command') -> None:
        """
        Process a player command.

        Args:
            command: The command to execute

        Educational Note:
            Command processing is where game rules are enforced.
            Different command types have different handlers:
            - Movement: try to move, handle collisions
            - Wait: skip turn
            - Quit: end game
            - etc.

            Each command may or may not consume a turn.
        """
        # Handle different command types
        if command.action == Action.QUIT:
            self.state = GameState.QUIT
            self.add_message("Thanks for playing!")
            return

        elif command.action == Action.WAIT:
            self.add_message("You wait...")
            self.end_turn()
            return

        elif self.input_handler.is_movement_action(command.action):
            # Try to move player
            success = self.movement_system.try_move(self.player, command.dx, command.dy)

            if success:
                # Movement succeeded
                self.add_message(f"You move.")
                self.end_turn()
            else:
                # Movement failed (wall, etc.)
                self.add_message("You can't move there!")
                # Don't end turn - let player try again

    def end_turn(self) -> None:
        """
        End the current turn and update game state.

        Educational Note:
            Ending a turn triggers all time-based updates:
            - Increment turn counter
            - Process enemy turns (future)
            - Apply status effects (future)
            - Regeneration (future)
            - etc.

            For now, we just increment the counter.
        """
        self.turn_count += 1

        # Future: Process enemy turns here
        # for entity in self.entities:
        #     if entity != self.player and entity.has_component(AIComponent):
        #         ai_system.process(entity)

    def check_game_over(self) -> None:
        """
        Check for game over conditions.

        Educational Note:
            Game over checks happen after each turn. Conditions include:
            - Player death
            - Player quit
            - Victory (reaching final floor)

            We update game state accordingly, which exits the main loop.
        """
        if not is_player_alive(self.player):
            self.state = GameState.PLAYER_DEAD
            self.add_message("You have died!")

    def add_message(self, message: str) -> None:
        """
        Add a message to the message log.

        Args:
            message: The message text

        Educational Note:
            Messages provide feedback to the player. Good roguelikes
            have rich, informative messages:
            - "You hit the goblin for 5 damage."
            - "The goblin misses you."
            - "You pick up a health potion."

            We store messages in a list and display the most recent ones.
        """
        self.message_log.append(message)

    def show_end_screen(self) -> None:
        """
        Display the end game screen.

        Educational Note:
            The end screen shows:
            - Why game ended (death, quit, victory)
            - Final statistics
            - Encouraging message

            This provides closure and motivates replaying.
        """
        print("\n" + "═" * 80)
        print(" " * 30 + "GAME OVER")
        print("═" * 80)

        if self.state == GameState.PLAYER_DEAD:
            print("\n  You have perished in the ECU dungeon...")
            print(f"  You survived {self.turn_count} turns.")

        elif self.state == GameState.QUIT:
            print("\n  Thanks for playing!")
            print(f"  You played for {self.turn_count} turns.")

        elif self.state == GameState.VICTORY:
            print("\n  Congratulations! You have conquered the ECU!")
            print(f"  Victory achieved in {self.turn_count} turns.")

        print("\n" + "═" * 80)
