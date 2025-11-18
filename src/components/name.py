"""
NameComponent - Entity identification and description

This component stores an entity's name and description for display.

Educational Notes:
------------------
Names are essential for:
- Displaying entity information to the player
- Combat messages ("Player attacks Goblin")
- Item descriptions ("Iron Sword: +5 damage")
- Save file readability

Separating names into a component allows:
- Easy localization (translate names)
- Dynamic name generation (procedural enemy names)
- Name changes (shapeshifters, disguises)
"""

from src.components.base import Component
from typing import Dict, Any, Optional


class NameComponent(Component):
    """
    Component storing entity name and description.

    Attributes:
        name: Entity's display name
        description: Longer description or flavor text

    Educational Note:
        Names should be short and readable (max ~30 characters).
        Descriptions can be longer and provide backstory or details.

    Example:
        >>> # Player name
        >>> player_name = NameComponent(
        ...     name="Hero",
        ...     description="A brave adventurer exploring the ECU"
        ... )
        >>>
        >>> # Enemy name
        >>> enemy_name = NameComponent(
        ...     name="Corrupted Packet",
        ...     description="A damaged data packet wandering the CAN Bus"
        ... )
    """

    def __init__(self, name: str = "Unknown", description: str = ""):
        """
        Initialize name component.

        Args:
            name: Entity's name (default "Unknown")
            description: Entity's description (default empty)

        Educational Note:
            Default "Unknown" helps identify entities that haven't been
            properly configured during testing.
        """
        super().__init__()
        self.name = name
        self.description = description

    def get_name(self) -> str:
        """
        Get the entity's name.

        Returns:
            Entity name string

        Example:
            >>> name_comp = NameComponent(name="Goblin")
            >>> print(f"You encounter a {name_comp.get_name()}")
            You encounter a Goblin
        """
        return self.name

    def set_name(self, new_name: str) -> None:
        """
        Change the entity's name.

        Args:
            new_name: New name for the entity

        Educational Note:
            Useful for:
            - Shapeshifting (Doppelganger becomes "John Smith")
            - Identification (Unidentified Potion becomes "Healing Potion")
            - Story events (NPC name reveals)

        Example:
            >>> name_comp = NameComponent(name="???")
            >>> # After identification
            >>> name_comp.set_name("Potion of Healing")
        """
        self.name = new_name

    def get_description(self) -> str:
        """
        Get the entity's description.

        Returns:
            Description string

        Example:
            >>> enemy = NameComponent(
            ...     name="Dragon",
            ...     description="An ancient fire-breathing dragon"
            ... )
            >>> print(enemy.get_description())
            An ancient fire-breathing dragon
        """
        return self.description

    def set_description(self, new_description: str) -> None:
        """
        Change the entity's description.

        Args:
            new_description: New description text
        """
        self.description = new_description

    def to_dict(self) -> Dict[str, Any]:
        """Serialize name component to dictionary."""
        return {
            'component_type': self.component_type,
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NameComponent':
        """
        Deserialize name component from dictionary.

        Args:
            data: Dictionary containing name data

        Returns:
            New NameComponent instance
        """
        return cls(
            name=data.get('name', 'Unknown'),
            description=data.get('description', '')
        )
