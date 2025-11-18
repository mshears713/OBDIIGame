"""
InputComponent - Marks entities controlled by player input

This component identifies entities that should respond to player commands.

Educational Notes:
------------------
In a game with multiple entities, we need to identify which one is controlled
by the player. The InputComponent is a simple marker component - it has no
data, it just tags an entity as "player-controlled".

This enables:
- Input system finds entities with InputComponent
- Only those entities process keyboard/mouse input
- Easy switching between entities (remove from one, add to another)
- Spectator mode (remove InputComponent from player)

This is an example of a "tag component" or "marker component" - a component
whose existence is more important than any data it might contain.
"""

from src.components.base import Component
from typing import Dict, Any


class InputComponent(Component):
    """
    Component marking an entity as player-controlled.

    Attributes:
        accepts_input: Whether this entity currently accepts input

    Educational Note:
        The accepts_input flag allows temporarily disabling player control
        without removing the component entirely. Useful for:
        - Cutscenes (disable input during story moments)
        - Stun effects (player temporarily can't act)
        - Turn-based mechanics (not your turn)

    Example:
        >>> # Create player entity
        >>> player = Entity()
        >>> player.add_component(InputComponent())
        >>>
        >>> # Input system checks for this component
        >>> if player.has_component(InputComponent):
        >>>     process_player_command(player, user_input)
    """

    def __init__(self, accepts_input: bool = True):
        """
        Initialize input component.

        Args:
            accepts_input: Whether entity accepts input (default True)

        Educational Note:
            Usually entities with InputComponent start accepting input.
            Setting False allows pre-creating the component in a disabled state.
        """
        super().__init__()
        self.accepts_input = accepts_input

    def enable_input(self) -> None:
        """
        Enable input processing for this entity.

        Example:
            >>> input_comp = InputComponent(accepts_input=False)
            >>> # After cutscene ends
            >>> input_comp.enable_input()
            >>> assert input_comp.can_accept_input()
        """
        self.accepts_input = True

    def disable_input(self) -> None:
        """
        Disable input processing for this entity.

        Example:
            >>> input_comp = InputComponent()
            >>> # During stun effect
            >>> input_comp.disable_input()
            >>> assert not input_comp.can_accept_input()
        """
        self.accepts_input = False

    def can_accept_input(self) -> bool:
        """
        Check if this entity can currently accept input.

        Returns:
            True if entity accepts input, False otherwise

        Example:
            >>> input_comp = InputComponent()
            >>> if input_comp.can_accept_input():
            >>>     # Process player command
            >>>     handle_input(command)
        """
        return self.accepts_input

    def to_dict(self) -> Dict[str, Any]:
        """Serialize input component to dictionary."""
        return {
            'component_type': self.component_type,
            'accepts_input': self.accepts_input
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InputComponent':
        """
        Deserialize input component from dictionary.

        Args:
            data: Dictionary containing input data

        Returns:
            New InputComponent instance
        """
        return cls(accepts_input=data.get('accepts_input', True))
