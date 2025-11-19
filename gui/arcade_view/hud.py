"""
HUD (Heads-Up Display) System

Renders UI elements including health bars, meters, status indicators,
message log, and mini-map.
"""

import arcade
from typing import List, Optional
from src.entities.entity import Entity
from src.components import HealthComponent, InventoryComponent, SignalComponent
from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, HUD_MARGIN, HUD_BAR_WIDTH, HUD_BAR_HEIGHT,
    HUD_FONT_SIZE, HUD_MESSAGE_COUNT, COLOR_HEALTH_BAR_GOOD,
    COLOR_HEALTH_BAR_WARNING, COLOR_HEALTH_BAR_CRITICAL
)


class HUD:
    """
    Heads-Up Display for game information.

    Renders:
    - Player health bar
    - Subsystem meters (fuel, voltage, etc.)
    - Status indicators
    - Message log
    - Mini-map
    - Turn counter
    """

    def __init__(self):
        """Initialize the HUD."""
        self.message_log: List[str] = []
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self, player: Entity, turn_count: int, message_log: List[str]):
        """
        Update HUD state.

        Args:
            player: The player entity
            turn_count: Current turn number
            message_log: List of game messages
        """
        self.message_log = message_log[-HUD_MESSAGE_COUNT:]

    def draw(self, player: Entity, turn_count: int, enemy_count: int = 0):
        """
        Draw all HUD elements.

        Args:
            player: The player entity
            turn_count: Current turn number
            enemy_count: Number of visible enemies
        """
        # Use HUD camera (screen-space coordinates)
        self.camera.use()

        # Draw semi-transparent background panel
        self._draw_hud_background()

        # Draw player stats
        self._draw_health_bar(player)
        self._draw_inventory_info(player)
        self._draw_signal_info(player)

        # Draw game info
        self._draw_turn_counter(turn_count, enemy_count)

        # Draw message log
        self._draw_message_log()

        # Draw controls reminder
        self._draw_controls()

    def _draw_hud_background(self):
        """Draw semi-transparent background panel for HUD."""
        # Top panel for stats
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 60,
            SCREEN_WIDTH,
            120,
            (20, 20, 30, 200)
        )

        # Bottom panel for messages and controls
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            80,
            SCREEN_WIDTH,
            160,
            (20, 20, 30, 200)
        )

    def _draw_health_bar(self, player: Entity):
        """
        Draw player health bar.

        Args:
            player: The player entity
        """
        health_comp = player.get_component(HealthComponent)
        if not health_comp:
            return

        # Calculate health percentage
        health_pct = health_comp.current_hp / health_comp.max_hp if health_comp.max_hp > 0 else 0

        # Choose color based on health
        if health_pct > 0.6:
            bar_color = COLOR_HEALTH_BAR_GOOD
        elif health_pct > 0.3:
            bar_color = COLOR_HEALTH_BAR_WARNING
        else:
            bar_color = COLOR_HEALTH_BAR_CRITICAL

        # Position
        x = HUD_MARGIN + 80
        y = SCREEN_HEIGHT - HUD_MARGIN - 20

        # Draw label
        arcade.draw_text(
            "HP:",
            HUD_MARGIN,
            y - 5,
            arcade.color.WHITE,
            HUD_FONT_SIZE,
            bold=True
        )

        # Draw background bar
        arcade.draw_rectangle_filled(
            x + HUD_BAR_WIDTH / 2,
            y,
            HUD_BAR_WIDTH,
            HUD_BAR_HEIGHT,
            (50, 50, 50)
        )

        # Draw health bar
        if health_pct > 0:
            arcade.draw_rectangle_filled(
                x + (HUD_BAR_WIDTH * health_pct) / 2,
                y,
                HUD_BAR_WIDTH * health_pct,
                HUD_BAR_HEIGHT,
                bar_color
            )

        # Draw text
        arcade.draw_text(
            f"{health_comp.current_hp}/{health_comp.max_hp}",
            x + HUD_BAR_WIDTH + 10,
            y - 5,
            arcade.color.WHITE,
            HUD_FONT_SIZE
        )

    def _draw_inventory_info(self, player: Entity):
        """
        Draw inventory information.

        Args:
            player: The player entity
        """
        inventory = player.get_component(InventoryComponent)
        if not inventory:
            return

        x = HUD_MARGIN
        y = SCREEN_HEIGHT - HUD_MARGIN - 50

        item_count = inventory.count_items()
        max_items = inventory.max_capacity

        arcade.draw_text(
            f"Items: {item_count}/{max_items}",
            x,
            y,
            arcade.color.WHITE,
            HUD_FONT_SIZE
        )

    def _draw_signal_info(self, player: Entity):
        """
        Draw signal/data information.

        Args:
            player: The player entity
        """
        signal_comp = player.get_component(SignalComponent)
        if not signal_comp:
            return

        x = HUD_MARGIN + 200
        y = SCREEN_HEIGHT - HUD_MARGIN - 50

        # Get all signal types and counts
        signal_types = signal_comp.get_all_signal_types()
        if signal_types:
            total_signals = sum(signal_comp.get_signal_count(st) for st in signal_types)
            arcade.draw_text(
                f"Signals: {total_signals}",
                x,
                y,
                arcade.color.CYAN,
                HUD_FONT_SIZE
            )

    def _draw_turn_counter(self, turn_count: int, enemy_count: int):
        """
        Draw turn counter and enemy count.

        Args:
            turn_count: Current turn number
            enemy_count: Number of visible enemies
        """
        x = SCREEN_WIDTH - HUD_MARGIN - 150
        y = SCREEN_HEIGHT - HUD_MARGIN - 20

        arcade.draw_text(
            f"Turn: {turn_count}",
            x,
            y,
            arcade.color.WHITE,
            HUD_FONT_SIZE
        )

        # Enemy count
        y -= 25
        color = arcade.color.RED if enemy_count > 0 else arcade.color.GRAY
        arcade.draw_text(
            f"Enemies: {enemy_count}",
            x,
            y,
            color,
            HUD_FONT_SIZE
        )

    def _draw_message_log(self):
        """Draw recent game messages."""
        x = HUD_MARGIN
        y = 120

        arcade.draw_text(
            "Messages:",
            x,
            y,
            arcade.color.WHITE,
            HUD_FONT_SIZE,
            bold=True
        )

        # Draw messages (most recent at bottom)
        for i, message in enumerate(self.message_log):
            arcade.draw_text(
                f"> {message}",
                x + 10,
                y - (i + 1) * 20,
                arcade.color.LIGHT_GRAY,
                HUD_FONT_SIZE - 2
            )

    def _draw_controls(self):
        """Draw control hints."""
        controls = [
            "WASD/Arrows: Move",
            "Space: Wait",
            "I: Inventory",
            "Q: Quit"
        ]

        x = SCREEN_WIDTH - HUD_MARGIN - 400
        y = HUD_MARGIN + 10

        control_text = "  |  ".join(controls)
        arcade.draw_text(
            control_text,
            x,
            y,
            arcade.color.DARK_GRAY,
            HUD_FONT_SIZE - 3
        )

    def add_message(self, message: str):
        """
        Add a message to the message log.

        Args:
            message: The message text
        """
        self.message_log.append(message)
        # Keep only recent messages
        if len(self.message_log) > HUD_MESSAGE_COUNT:
            self.message_log = self.message_log[-HUD_MESSAGE_COUNT:]
