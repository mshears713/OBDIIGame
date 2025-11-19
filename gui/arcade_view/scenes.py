"""
Scene Management

Handles transitions between different game scenes/subsystems with visual effects.
"""

import arcade
from enum import Enum, auto
from typing import Optional, Callable
from .config import SCREEN_WIDTH, SCREEN_HEIGHT


class SceneType(Enum):
    """Types of game scenes."""
    MAIN_MENU = auto()
    GAMEPLAY = auto()
    INVENTORY = auto()
    SUBSYSTEM_TRANSITION = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class SceneTransition:
    """
    Manages smooth transitions between scenes.

    Supports various transition effects:
    - Fade to black
    - Cross-fade
    - Wipe effects
    - Custom transitions
    """

    def __init__(self, duration: float = 1.0):
        """
        Initialize scene transition.

        Args:
            duration: Transition duration in seconds
        """
        self.duration = duration
        self.elapsed = 0.0
        self.active = False
        self.alpha = 0
        self.callback: Optional[Callable] = None

    def start(self, callback: Optional[Callable] = None):
        """
        Start the transition.

        Args:
            callback: Function to call when transition is halfway complete
        """
        self.active = True
        self.elapsed = 0.0
        self.alpha = 0
        self.callback = callback

    def update(self, delta_time: float) -> bool:
        """
        Update transition state.

        Args:
            delta_time: Time elapsed

        Returns:
            True if transition is complete
        """
        if not self.active:
            return True

        self.elapsed += delta_time

        # Fade out (first half)
        if self.elapsed < self.duration / 2:
            self.alpha = int((self.elapsed / (self.duration / 2)) * 255)

            # Call callback at halfway point
            if self.elapsed >= self.duration / 2 and self.callback:
                self.callback()
                self.callback = None

        # Fade in (second half)
        else:
            self.alpha = int((1.0 - (self.elapsed - self.duration / 2) / (self.duration / 2)) * 255)

        # Check if complete
        if self.elapsed >= self.duration:
            self.active = False
            self.alpha = 0
            return True

        return False

    def draw(self):
        """Draw the transition overlay."""
        if not self.active or self.alpha == 0:
            return

        # Draw black overlay with current alpha
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (0, 0, 0, self.alpha)
        )


class SubsystemTransition:
    """
    Specialized transition for moving between subsystems.

    Shows subsystem name and flavor text during transition.
    """

    def __init__(self):
        """Initialize subsystem transition."""
        self.transition = SceneTransition(duration=2.0)
        self.subsystem_name = ""
        self.subsystem_desc = ""
        self.show_text = False

    def start(self, subsystem_name: str, description: str, callback: Optional[Callable] = None):
        """
        Start subsystem transition.

        Args:
            subsystem_name: Name of the subsystem
            description: Flavor text description
            callback: Function to call during transition
        """
        self.subsystem_name = subsystem_name
        self.subsystem_desc = description

        def transition_callback():
            self.show_text = True
            if callback:
                callback()

        self.transition.start(transition_callback)

    def update(self, delta_time: float) -> bool:
        """
        Update transition.

        Args:
            delta_time: Time elapsed

        Returns:
            True if complete
        """
        complete = self.transition.update(delta_time)

        if complete:
            self.show_text = False

        return complete

    def draw(self):
        """Draw subsystem transition."""
        self.transition.draw()

        # Show subsystem name during transition
        if self.show_text and self.transition.alpha > 128:
            arcade.draw_text(
                self.subsystem_name,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 + 50,
                arcade.color.CYAN,
                36,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                self.subsystem_desc,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                18,
                anchor_x="center",
                width=SCREEN_WIDTH - 100,
                align="center",
                multiline=True
            )


# Subsystem names and descriptions
SUBSYSTEM_INFO = {
    'fuel_injection': {
        'name': 'FUEL INJECTION FOREST',
        'desc': 'A maze of high-pressure fuel lines and atomizing injectors.\nVoltage spikes lurk in the mist of vaporized fuel.'
    },
    'ignition': {
        'name': 'IGNITION SYSTEM',
        'desc': 'Sparks fly through darkness.\nCoils hum with deadly voltage.'
    },
    'can_bus': {
        'name': 'CAN-BUS CATACOMBS',
        'desc': 'Endless data streams flow through twisted pathways.\nCorrupted packets echo in the digital void.'
    },
    'transmission': {
        'name': 'TRANSMISSION ABYSS',
        'desc': 'Grinding gears and hydraulic pressure.\nSlip into the depths of mechanical chaos.'
    },
    'oxygen': {
        'name': 'O₂ SENSOR SANCTUARY',
        'desc': 'Thin air and chemical sensors.\nMonitor the balance between life and combustion.'
    },
    'ecu': {
        'name': 'ECU CORE',
        'desc': 'The heart of the system.\nRestore order to the central processor.'
    }
}
