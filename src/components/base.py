"""
Base Component Class for Entity-Component-System Architecture

This module defines the abstract base class for all game components.

Educational Notes on Entity-Component-System (ECS):
----------------------------------------------------
ECS is an architectural pattern that favors composition over inheritance.
Instead of creating complex class hierarchies (e.g., Player extends Character
extends GameObject), we compose entities from small, reusable components.

Benefits of ECS:
1. **Modularity:** Components are independent, self-contained units
2. **Reusability:** Components can be mixed and matched across entity types
3. **Flexibility:** Add/remove capabilities by adding/removing components
4. **Maintainability:** Changes to one component don't affect others
5. **Performance:** Data-oriented design can be cache-friendly (advanced)

Example:
    A player entity might have: PositionComponent, RenderComponent,
    HealthComponent, InventoryComponent, InputComponent

    An enemy might have: PositionComponent, RenderComponent,
    HealthComponent, AIComponent

    Both share position, render, and health behaviors without inheritance!
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class Component(ABC):
    """
    Abstract base class for all entity components.

    Components are data containers with minimal logic. They represent specific
    aspects or capabilities of an entity (position, health, inventory, etc.).

    Educational Note:
        ABC (Abstract Base Class) prevents instantiation of this base class
        directly. All components must inherit from this class, ensuring
        consistency across the component system.

        The @abstractmethod decorator (if used) would enforce that child classes
        implement specific methods. For now, we keep Component simple to allow
        maximum flexibility in component design.

    Design Principles:
        1. Components should store data, not complex logic
        2. Systems operate on components to implement behavior
        3. Components should be as small and focused as possible
        4. Avoid dependencies between components

    Attributes:
        component_type: Unique identifier for this component type (auto-set)
    """

    def __init__(self):
        """
        Initialize the component.

        Educational Note:
            __init__ sets the component_type based on the class name.
            This allows runtime type checking and component lookups.
        """
        # Automatically set component type based on class name
        # e.g., PositionComponent -> "PositionComponent"
        self.component_type: str = self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize component to a dictionary for saving/loading.

        Returns:
            Dictionary representation of component data

        Educational Note:
            This method enables save/load functionality. Override in child
            classes to customize serialization. The default implementation
            uses __dict__ which works for simple data components.

        Example:
            >>> position = PositionComponent(x=5, y=10)
            >>> data = position.to_dict()
            >>> # {'component_type': 'PositionComponent', 'x': 5, 'y': 10}
        """
        return {
            'component_type': self.component_type,
            **self.__dict__
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Component':
        """
        Deserialize component from a dictionary.

        Args:
            data: Dictionary containing component data

        Returns:
            New component instance created from data

        Educational Note:
            This class method enables loading saved games. Override in child
            classes for custom deserialization logic.

            @classmethod receives the class itself as first argument (cls)
            instead of an instance (self), allowing factory-style creation.

        Example:
            >>> data = {'x': 5, 'y': 10}
            >>> position = PositionComponent.from_dict(data)
        """
        # Remove component_type from data if present
        component_data = {k: v for k, v in data.items()
                         if k != 'component_type'}

        # Create instance using remaining data as keyword arguments
        return cls(**component_data)

    def __repr__(self) -> str:
        """
        Return string representation of component for debugging.

        Educational Note:
            __repr__ provides a developer-friendly string representation.
            Useful for debugging and logging.

        Returns:
            String representation showing component type and attributes
        """
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items()
                         if k != 'component_type')
        return f"{self.component_type}({attrs})"
