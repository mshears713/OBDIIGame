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
from src.systems.ai import AISystem
from src.systems.combat import CombatSystem
from src.components import (
    PositionComponent,
    AIComponent,
    HealthComponent,
    InventoryComponent,
    NameComponent,
    SignalComponent
)


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

        # Populate dungeon with enemies and items
        spawned_entities = generator.populate_dungeon(
            dungeon_map=self.game_map,
            floor_level=1,
            enemies_per_room=(1, 2),
            items_per_room=(0, 1),
            enemy_chance=0.7,
            item_chance=0.4
        )

        # Entity list (player + spawned entities)
        self.entities: List[Entity] = [self.player] + spawned_entities

        # Initialize systems
        self.renderer = Renderer(self.game_map)
        self.movement_system = MovementSystem(self.game_map)
        self.input_handler = InputHandler()
        self.combat_system = CombatSystem()
        self.ai_system = AISystem(self.game_map, self.movement_system)

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
            - Inventory status
            - Turn counter
            - Visible enemies
            - Recent messages
            - Controls reminder

            We separate UI rendering from map rendering for clarity.
        """
        # Get player stats
        from src.entities.player import get_player_health
        current_hp, max_hp = get_player_health(self.player)
        hp_percentage = (current_hp / max_hp) * 100 if max_hp > 0 else 0

        # Create HP bar with color coding
        bar_width = 20
        filled = int((current_hp / max_hp) * bar_width) if max_hp > 0 else 0
        hp_bar = '█' * filled + '░' * (bar_width - filled)

        # Get inventory stats
        inventory = self.player.get_component(InventoryComponent)
        item_count = inventory.count_items() if inventory else 0
        max_items = inventory.max_capacity if inventory else 0

        # Count visible enemies
        enemy_count = sum(1 for e in self.entities if e.has_tag("enemy") and e.has_component(HealthComponent))

        # Display stats
        print("\n" + "═" * 80)
        print(f"HP: [{hp_bar}] {current_hp}/{max_hp} ({hp_percentage:.0f}%)  |  " +
              f"Items: {item_count}/{max_items}  |  " +
              f"Enemies: {enemy_count}  |  " +
              f"Turn: {self.turn_count}")

        # Display recent messages (last 5)
        print("\n" + "─" * 80)
        print("Messages:")
        for msg in self.message_log[-5:]:
            print(f"  {msg}")
        print("─" * 80)
        print("  [WASD/Arrows: Move] [.: Wait] [Q: Quit] [?: Help]")

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
            # Calculate target position
            player_pos = self.player.get_component(PositionComponent)
            if not player_pos:
                return

            target_x = player_pos.x + command.dx
            target_y = player_pos.y + command.dy

            # Check if there's an entity at target position
            target_entity = self.combat_system.get_entity_at_position(
                target_x, target_y, self.entities, exclude=self.player
            )

            if target_entity:
                # There's an entity at target - check if it's alive and attackable
                target_health = target_entity.get_component(HealthComponent)
                if target_health and target_health.is_alive():
                    # Attack the entity
                    self.combat_system.melee_attack(
                        self.player, target_entity, self.message_log
                    )
                    self.end_turn()
                    return

            # No entity or entity is dead - try to move
            success = self.movement_system.try_move(self.player, command.dx, command.dy)

            if success:
                # Movement succeeded - check for auto-pickup
                self.try_auto_pickup()
                self.end_turn()
            else:
                # Movement failed (wall, etc.)
                self.add_message("You can't move there!")
                # Don't end turn - let player try again

    def try_auto_pickup(self) -> None:
        """
        Attempt to automatically pick up items at player's position.

        Educational Note:
            Auto-pickup happens after successful movement. Items at the
            player's new position are automatically picked up if there's
            inventory space.

            Alternative designs:
            - Manual pickup only (press 'g' to get items)
            - Prompt before picking up
            - Pick up only specific item types (auto-pickup gold)
        """
        player_pos = self.player.get_component(PositionComponent)
        inventory = self.player.get_component(InventoryComponent)

        if not player_pos or not inventory:
            return

        # Find items at player position
        items_at_position = []
        for entity in self.entities:
            if entity == self.player:
                continue

            # Check if entity is an item
            if not entity.has_tag("item"):
                continue

            pos = entity.get_component(PositionComponent)
            if pos and pos.x == player_pos.x and pos.y == player_pos.y:
                items_at_position.append(entity)

        # Try to pick up each item
        for item in items_at_position:
            if inventory.is_full():
                self.add_message("Your inventory is full!")
                break

            # Add item to inventory
            if inventory.add_item(item):
                # Remove from world
                self.entities.remove(item)

                # Get item name
                name_comp = item.get_component(NameComponent)
                item_name = name_comp.name if name_comp else "item"

                self.add_message(f"Picked up {item_name}.")

    def end_turn(self) -> None:
        """
        End the current turn and update game state.

        Educational Note:
            Ending a turn triggers all time-based updates:
            - Increment turn counter
            - Process enemy turns
            - Remove dead entities
            - Apply status effects (future)
            - Regeneration (future)
            - etc.
        """
        self.turn_count += 1

        # Process enemy turns
        for entity in self.entities:
            if entity != self.player and entity.has_component(AIComponent):
                self.ai_system.process(entity, self.player, self.entities, self.combat_system, self.message_log)

        # Remove dead entities
        living_entities, dead_entities = self.combat_system.remove_dead_entities(self.entities)

        # Process dead entities - transfer signals to player
        player_signals = self.player.get_component(SignalComponent)
        if player_signals:
            for dead_entity in dead_entities:
                # Get entity signals
                entity_signals = dead_entity.get_component(SignalComponent)
                if entity_signals:
                    # Transfer each signal type
                    for signal_type in entity_signals.get_all_signal_types():
                        quantity = entity_signals.get_signal_count(signal_type)
                        if quantity > 0:
                            # Try to add to player signals
                            added = player_signals.add_signal(signal_type, quantity)
                            if added > 0:
                                self.add_message(f"Collected {added}x {signal_type} signal(s)!")

        self.entities = living_entities

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
