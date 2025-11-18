"""
SignalComponent - Manages entity signal inventory for crafting

This component tracks the diagnostic signals an entity possesses, which can be
combined through crafting recipes to create powerful effects.

Educational Notes on Signal-Crafting Mechanic:
-----------------------------------------------
In automotive ECU systems, signals are the fundamental units of communication:
- CAN bus messages carry sensor data and control commands
- Diagnostic Trouble Codes (DTCs) indicate system faults
- Protocol signals enable inter-module communication

This game mechanic simulates collecting, managing, and combining these signals
to create diagnostic tools, attacks, defenses, and utilities. Think of it as
analyzing and manipulating the "language" of the vehicle's computer network.

Signal Types Explained:
    - sensor_reading: Raw data from sensors (O2, MAF, temperature, etc.)
    - dtc_code: Diagnostic codes indicating specific faults
    - ecu_query: Interrogation signals to probe system status
    - corrupted_packet: Malformed data that can damage systems
    - error_correction: Protocols for fixing corrupted data
    - firewall_rule: Security policies to block threats
    - scanner_pulse: Broadcast signals for detection
    - And many more defined in recipes...

Design Philosophy:
    Signals are resources that players collect from:
    - Defeated enemies (drop signals)
    - Found items (contain signals)
    - Environmental sources (signal nodes)
    - Crafting (recipes produce new signals)
"""

from src.components.base import Component
from typing import Dict, Any, List, Optional
from collections import defaultdict


class SignalComponent(Component):
    """
    Component managing an entity's collection of diagnostic signals.

    Signals are the crafting materials of the game. Players collect different
    signal types and combine them using recipes to create powerful effects.

    Attributes:
        signals: Dictionary mapping signal_type (str) to quantity (int)
        max_signal_types: Maximum number of different signal types (0 = unlimited)
        max_per_signal: Maximum quantity per signal type (0 = unlimited)

    Educational Note:
        Using a dictionary to store signals allows:
        - Fast lookup: O(1) to check if signal exists
        - Easy quantity tracking: signals["sensor_reading"] = 5
        - Flexible signal types: Add new types without code changes
        - Efficient serialization: Convert directly to JSON

        The defaultdict with int factory means accessing non-existent signals
        returns 0 instead of raising KeyError, simplifying signal checks.

    Example:
        >>> # Create signal component for player
        >>> signals = SignalComponent()
        >>>
        >>> # Add some signals
        >>> signals.add_signal("sensor_reading", 3)
        >>> signals.add_signal("dtc_code", 2)
        >>>
        >>> # Check signal quantity
        >>> assert signals.get_signal_count("sensor_reading") == 3
        >>> assert signals.has_signal("dtc_code", 2) is True
        >>>
        >>> # Remove signals for crafting
        >>> signals.remove_signal("sensor_reading", 2)
        >>> assert signals.get_signal_count("sensor_reading") == 1
        >>>
        >>> # List all signals
        >>> all_signals = signals.get_all_signals()
        >>> # {'sensor_reading': 1, 'dtc_code': 2}
    """

    def __init__(
        self,
        max_signal_types: int = 0,
        max_per_signal: int = 999
    ):
        """
        Initialize signal component.

        Args:
            max_signal_types: Maximum different signal types (0 = unlimited)
            max_per_signal: Maximum quantity per type (default 999)

        Educational Note:
            Different entities might have different signal capacities:
            - Player: Large capacity, many types (for crafting)
            - Enemies: Small capacity, specific types (for drops)
            - Items: Fixed signals (consumed when picked up)

            Setting max_signal_types = 0 means unlimited types, useful for
            player inventory. Setting a limit creates strategic choices about
            which signals to keep.
        """
        super().__init__()
        # Use defaultdict so missing signals return 0
        self.signals: Dict[str, int] = defaultdict(int)
        self.max_signal_types = max_signal_types
        self.max_per_signal = max_per_signal

    def add_signal(self, signal_type: str, quantity: int = 1) -> int:
        """
        Add signals of a specific type.

        Args:
            signal_type: Type identifier of the signal
            quantity: Number of signals to add (default 1)

        Returns:
            Actual quantity added (may be less due to capacity limits)

        Educational Note:
            Returns actual quantity added to handle:
            - Capacity limits (can't add more than max_per_signal)
            - Signal type limits (can't add new type if at max types)
            - Feedback to player ("picked up 3 of 5 signals - inventory full")

        Example:
            >>> signals = SignalComponent(max_per_signal=10)
            >>> signals.add_signal("sensor_reading", 8)
            >>> actual = signals.add_signal("sensor_reading", 5)
            >>> assert actual == 2  # Only added 2 to reach max of 10
            >>> assert signals.get_signal_count("sensor_reading") == 10
        """
        if quantity <= 0:
            return 0

        # Check if adding a new signal type would exceed type limit
        if (self.max_signal_types > 0 and
            signal_type not in self.signals and
            len(self.signals) >= self.max_signal_types):
            return 0  # Can't add new type - at capacity

        current_count = self.signals[signal_type]

        # Calculate how much can be added considering per-signal limit
        if self.max_per_signal > 0:
            max_addable = self.max_per_signal - current_count
            actual_added = min(quantity, max_addable)
        else:
            actual_added = quantity

        if actual_added > 0:
            self.signals[signal_type] += actual_added

        return actual_added

    def remove_signal(self, signal_type: str, quantity: int = 1) -> int:
        """
        Remove signals of a specific type.

        Args:
            signal_type: Type identifier of the signal
            quantity: Number of signals to remove (default 1)

        Returns:
            Actual quantity removed (may be less if insufficient signals)

        Educational Note:
            Used when:
            - Crafting recipes (consume input signals)
            - Trading signals
            - Signal degradation/corruption over time
            - Ability costs

            Returns actual removed for feedback and validation.

        Example:
            >>> signals = SignalComponent()
            >>> signals.add_signal("dtc_code", 5)
            >>> actual = signals.remove_signal("dtc_code", 3)
            >>> assert actual == 3
            >>> assert signals.get_signal_count("dtc_code") == 2
            >>>
            >>> # Try to remove more than available
            >>> actual = signals.remove_signal("dtc_code", 10)
            >>> assert actual == 2  # Only removed remaining 2
            >>> assert signals.get_signal_count("dtc_code") == 0
        """
        if quantity <= 0 or signal_type not in self.signals:
            return 0

        current_count = self.signals[signal_type]
        actual_removed = min(quantity, current_count)

        self.signals[signal_type] -= actual_removed

        # Clean up if count reaches 0
        if self.signals[signal_type] <= 0:
            del self.signals[signal_type]

        return actual_removed

    def has_signal(self, signal_type: str, quantity: int = 1) -> bool:
        """
        Check if entity has sufficient signals of a type.

        Args:
            signal_type: Type identifier to check
            quantity: Minimum quantity required (default 1)

        Returns:
            True if entity has >= quantity of signal_type

        Educational Note:
            Primary method for checking crafting requirements:
            - Does player have materials for recipe?
            - Can ability be activated?
            - Is quest item signal present?

        Example:
            >>> signals = SignalComponent()
            >>> signals.add_signal("sensor_reading", 5)
            >>> assert signals.has_signal("sensor_reading", 3) is True
            >>> assert signals.has_signal("sensor_reading", 10) is False
            >>> assert signals.has_signal("nonexistent") is False
        """
        return self.signals.get(signal_type, 0) >= quantity

    def get_signal_count(self, signal_type: str) -> int:
        """
        Get the quantity of a specific signal type.

        Args:
            signal_type: Type identifier to query

        Returns:
            Quantity of this signal (0 if not present)

        Example:
            >>> signals = SignalComponent()
            >>> signals.add_signal("ecu_query", 7)
            >>> assert signals.get_signal_count("ecu_query") == 7
            >>> assert signals.get_signal_count("missing") == 0
        """
        return self.signals.get(signal_type, 0)

    def get_all_signals(self) -> Dict[str, int]:
        """
        Get a copy of all signals.

        Returns:
            Dictionary mapping signal_type to quantity

        Educational Note:
            Returns a copy (dict()) to prevent external modification.
            This is defensive programming - callers can't accidentally
            modify the internal signals dictionary.

            Use for:
            - Displaying inventory UI
            - Checking crafting possibilities
            - Save/load operations
            - AI decision making

        Example:
            >>> signals = SignalComponent()
            >>> signals.add_signal("corrupted_packet", 3)
            >>> signals.add_signal("error_correction", 1)
            >>> all_sigs = signals.get_all_signals()
            >>> # {'corrupted_packet': 3, 'error_correction': 1}
        """
        return dict(self.signals)

    def get_signal_types(self) -> List[str]:
        """
        Get list of all signal types currently held.

        Returns:
            List of signal type identifiers

        Example:
            >>> signals = SignalComponent()
            >>> signals.add_signal("dtc_code", 2)
            >>> signals.add_signal("scanner_pulse", 1)
            >>> types = signals.get_signal_types()
            >>> assert "dtc_code" in types
            >>> assert "scanner_pulse" in types
        """
        return list(self.signals.keys())

    def get_total_signal_count(self) -> int:
        """
        Get total number of signals across all types.

        Returns:
            Sum of all signal quantities

        Educational Note:
            Useful for:
            - Weight/encumbrance systems
            - Achievement tracking ("collect 100 signals")
            - Resource scarcity indicators

        Example:
            >>> signals = SignalComponent()
            >>> signals.add_signal("type_a", 5)
            >>> signals.add_signal("type_b", 3)
            >>> signals.add_signal("type_c", 2)
            >>> assert signals.get_total_signal_count() == 10
        """
        return sum(self.signals.values())

    def clear_signals(self) -> None:
        """
        Remove all signals.

        Educational Note:
            Use cases:
            - Death penalty (lose all signals)
            - Trading all signals for something
            - Reset/debugging
            - Corruption effect (signals destroyed)
        """
        self.signals.clear()

    def transfer_signal(
        self,
        signal_type: str,
        quantity: int,
        target: 'SignalComponent'
    ) -> int:
        """
        Transfer signals from this component to another.

        Args:
            signal_type: Type of signal to transfer
            quantity: Amount to transfer
            target: Destination SignalComponent

        Returns:
            Actual quantity transferred

        Educational Note:
            Atomic transfer operation ensuring signals aren't lost or duplicated:
            1. Try to add to target
            2. Only remove from source if addition succeeded
            3. Return actual amount transferred

            Use for:
            - Trading between entities
            - Storing signals in containers
            - Party member signal sharing
            - Enemy signal drops on death

        Example:
            >>> player_signals = SignalComponent()
            >>> chest_signals = SignalComponent()
            >>> player_signals.add_signal("sensor_reading", 10)
            >>>
            >>> # Transfer 5 signals to chest
            >>> transferred = player_signals.transfer_signal(
            ...     "sensor_reading", 5, chest_signals
            ... )
            >>> assert transferred == 5
            >>> assert player_signals.get_signal_count("sensor_reading") == 5
            >>> assert chest_signals.get_signal_count("sensor_reading") == 5
        """
        if not self.has_signal(signal_type, quantity):
            quantity = self.get_signal_count(signal_type)

        # Try to add to target
        actually_added = target.add_signal(signal_type, quantity)

        # Only remove from source what was actually added to target
        if actually_added > 0:
            self.remove_signal(signal_type, actually_added)

        return actually_added

    def can_afford_recipe(self, recipe_inputs: List[Dict[str, Any]]) -> bool:
        """
        Check if entity has all signals required for a recipe.

        Args:
            recipe_inputs: List of input dictionaries from recipe JSON
                Each input has: signal_type, quantity, consumed

        Returns:
            True if all recipe requirements are met

        Educational Note:
            Recipe validation before crafting attempt. Prevents:
            - Partial crafting (consuming some but not all inputs)
            - Failed crafting attempts
            - Poor user experience

            Call this before showing "craftable" indicator in UI.

        Example:
            >>> signals = SignalComponent()
            >>> signals.add_signal("sensor_reading", 5)
            >>> signals.add_signal("error_correction", 2)
            >>>
            >>> recipe = [
            ...     {"signal_type": "sensor_reading", "quantity": 3, "consumed": True},
            ...     {"signal_type": "error_correction", "quantity": 1, "consumed": False}
            ... ]
            >>> assert signals.can_afford_recipe(recipe) is True
            >>>
            >>> impossible_recipe = [
            ...     {"signal_type": "sensor_reading", "quantity": 10, "consumed": True}
            ... ]
            >>> assert signals.can_afford_recipe(impossible_recipe) is False
        """
        for input_signal in recipe_inputs:
            signal_type = input_signal.get("signal_type")
            quantity = input_signal.get("quantity", 1)

            if not self.has_signal(signal_type, quantity):
                return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize signal component to dictionary.

        Returns:
            Dictionary representation for saving

        Educational Note:
            Convert defaultdict to regular dict for JSON serialization.
            JSON doesn't support defaultdict, so we use dict() conversion.
        """
        return {
            'component_type': self.component_type,
            'signals': dict(self.signals),  # Convert defaultdict to dict
            'max_signal_types': self.max_signal_types,
            'max_per_signal': self.max_per_signal
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SignalComponent':
        """
        Deserialize signal component from dictionary.

        Args:
            data: Dictionary containing signal component data

        Returns:
            New SignalComponent instance
        """
        component = cls(
            max_signal_types=data.get('max_signal_types', 0),
            max_per_signal=data.get('max_per_signal', 999)
        )

        # Restore signals
        signals_data = data.get('signals', {})
        for signal_type, quantity in signals_data.items():
            component.signals[signal_type] = quantity

        return component
