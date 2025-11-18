"""
Entity Class for Entity-Component-System Architecture

This module defines the Entity class, which serves as a container for components.

Educational Notes:
------------------
In ECS architecture, entities are lightweight containers that hold components.
An entity by itself has no behavior - it's just an ID and a collection of
components. All behavior comes from systems that operate on entities based on
their components.

Think of an entity as a bag of components:
    Entity #1: [PositionComponent, RenderComponent, HealthComponent]
    Entity #2: [PositionComponent, RenderComponent, AIComponent]

Systems then process entities:
    - RenderSystem: Processes entities with PositionComponent + RenderComponent
    - CombatSystem: Processes entities with HealthComponent
    - MovementSystem: Processes entities with PositionComponent
"""

from typing import Dict, Optional, Type, Any, List
from src.components.base import Component


class Entity:
    """
    A container for components representing a game object.

    Entities are identified by a unique ID and contain a collection of
    components that define their properties and capabilities.

    Attributes:
        entity_id: Unique identifier for this entity
        components: Dictionary mapping component types to component instances
        tags: List of string tags for categorizing entities (e.g., "enemy", "item")

    Educational Note:
        Entities are intentionally simple - they're just data structures.
        Complex behavior is handled by systems that process components.
        This separation makes testing and debugging much easier.

    Example:
        >>> player = Entity(entity_id=1)
        >>> player.add_component(PositionComponent(x=5, y=10))
        >>> player.add_component(RenderComponent(char='@', color='white'))
        >>> pos = player.get_component(PositionComponent)
        >>> print(f"Player at ({pos.x}, {pos.y})")
    """

    # Class variable for auto-incrementing entity IDs
    # Educational Note: Class variables are shared across all instances
    _next_id: int = 1

    def __init__(self, entity_id: Optional[int] = None, tags: Optional[List[str]] = None):
        """
        Initialize an entity.

        Args:
            entity_id: Unique ID (auto-generated if not provided)
            tags: Optional list of tags for categorization

        Educational Note:
            Auto-generating IDs prevents ID conflicts and simplifies entity
            creation. The _next_id class variable ensures uniqueness.
        """
        if entity_id is None:
            # Auto-generate ID and increment counter
            self.entity_id = Entity._next_id
            Entity._next_id += 1
        else:
            self.entity_id = entity_id
            # Update counter if provided ID is larger
            if entity_id >= Entity._next_id:
                Entity._next_id = entity_id + 1

        # Dictionary to store components by their type name
        # e.g., {'PositionComponent': <PositionComponent instance>}
        self.components: Dict[str, Component] = {}

        # Tags for categorizing entities
        self.tags: List[str] = tags if tags is not None else []

    def add_component(self, component: Component) -> None:
        """
        Add a component to this entity.

        Args:
            component: The component instance to add

        Educational Note:
            Using component_type as the dictionary key allows O(1) lookup
            by component type. We store one component of each type per entity.

            If you need multiple components of the same type, consider
            creating wrapper components or using a list-based approach.

        Example:
            >>> entity.add_component(PositionComponent(x=10, y=20))
            >>> entity.add_component(HealthComponent(current_hp=100, max_hp=100))
        """
        self.components[component.component_type] = component

    def remove_component(self, component_type: Type[Component]) -> bool:
        """
        Remove a component from this entity.

        Args:
            component_type: The component class to remove

        Returns:
            True if component was removed, False if it didn't exist

        Educational Note:
            Returning a boolean success indicator helps callers handle the
            case where a component wasn't present without raising exceptions.

        Example:
            >>> success = entity.remove_component(PositionComponent)
            >>> if success:
            >>>     print("Position component removed")
        """
        component_name = component_type.__name__
        if component_name in self.components:
            del self.components[component_name]
            return True
        return False

    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        """
        Retrieve a component from this entity.

        Args:
            component_type: The component class to retrieve

        Returns:
            The component instance, or None if not present

        Educational Note:
            Returning None for missing components allows simple existence checks:
                if entity.get_component(HealthComponent):
                    # Entity has health
                    pass

        Example:
            >>> position = entity.get_component(PositionComponent)
            >>> if position:
            >>>     print(f"Entity at ({position.x}, {position.y})")
        """
        component_name = component_type.__name__
        return self.components.get(component_name)

    def has_component(self, component_type: Type[Component]) -> bool:
        """
        Check if entity has a specific component type.

        Args:
            component_type: The component class to check for

        Returns:
            True if entity has this component type, False otherwise

        Educational Note:
            This is a convenience method that's more readable than:
                if entity.get_component(SomeComponent) is not None:

            Instead, you can write:
                if entity.has_component(SomeComponent):

        Example:
            >>> if entity.has_component(HealthComponent):
            >>>     health = entity.get_component(HealthComponent)
            >>>     print(f"HP: {health.current_hp}/{health.max_hp}")
        """
        component_name = component_type.__name__
        return component_name in self.components

    def has_components(self, *component_types: Type[Component]) -> bool:
        """
        Check if entity has all specified component types.

        Args:
            *component_types: Variable number of component classes to check

        Returns:
            True if entity has ALL specified components, False otherwise

        Educational Note:
            This method uses *args to accept any number of component types.
            It's particularly useful for systems that need entities with
            specific component combinations.

            The all() function is a Python built-in that returns True only
            if all elements in an iterable are True.

        Example:
            >>> # Check if entity can be rendered (needs position + render)
            >>> if entity.has_components(PositionComponent, RenderComponent):
            >>>     render_system.draw(entity)
        """
        return all(self.has_component(comp_type) for comp_type in component_types)

    def add_tag(self, tag: str) -> None:
        """
        Add a tag to this entity for categorization.

        Args:
            tag: String tag to add (e.g., "enemy", "item", "player")

        Educational Note:
            Tags provide a simple way to categorize entities without creating
            component types for every category. Use tags for broad classifications
            and components for specific data/behavior.

        Example:
            >>> entity.add_tag("enemy")
            >>> entity.add_tag("aggressive")
        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> bool:
        """
        Remove a tag from this entity.

        Args:
            tag: String tag to remove

        Returns:
            True if tag was removed, False if it wasn't present

        Example:
            >>> entity.remove_tag("aggressive")
        """
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False

    def has_tag(self, tag: str) -> bool:
        """
        Check if entity has a specific tag.

        Args:
            tag: String tag to check for

        Returns:
            True if entity has this tag, False otherwise

        Example:
            >>> if entity.has_tag("enemy"):
            >>>     ai_system.process(entity)
        """
        return tag in self.tags

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize entity to dictionary for saving.

        Returns:
            Dictionary representation of entity and all components

        Educational Note:
            Serialization converts Python objects to simple data structures
            (dicts, lists, primitives) that can be saved to JSON or other
            formats. This enables save/load functionality.

        Example:
            >>> data = entity.to_dict()
            >>> json.dump(data, file)
        """
        return {
            'entity_id': self.entity_id,
            'tags': self.tags,
            'components': {
                name: component.to_dict()
                for name, component in self.components.items()
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any],
                  component_registry: Dict[str, Type[Component]]) -> 'Entity':
        """
        Deserialize entity from dictionary.

        Args:
            data: Dictionary containing entity data
            component_registry: Mapping of component type names to classes

        Returns:
            New Entity instance with components restored

        Educational Note:
            Deserialization requires a component registry to know which class
            to instantiate for each component type. This is a common pattern
            in save/load systems.

            The registry maps component names to their classes:
                {'PositionComponent': PositionComponent, ...}

        Example:
            >>> registry = {
            >>>     'PositionComponent': PositionComponent,
            >>>     'RenderComponent': RenderComponent
            >>> }
            >>> entity = Entity.from_dict(saved_data, registry)
        """
        entity = cls(
            entity_id=data.get('entity_id'),
            tags=data.get('tags', [])
        )

        # Restore components
        for component_data in data.get('components', {}).values():
            component_type_name = component_data.get('component_type')
            if component_type_name in component_registry:
                component_class = component_registry[component_type_name]
                component = component_class.from_dict(component_data)
                entity.add_component(component)

        return entity

    def __repr__(self) -> str:
        """
        Return string representation of entity for debugging.

        Educational Note:
            Providing a useful __repr__ makes debugging much easier.
            You can print entities during development to see their state.

        Returns:
            String showing entity ID, tags, and component types
        """
        component_names = ', '.join(self.components.keys())
        tags_str = ', '.join(self.tags) if self.tags else 'no tags'
        return (f"Entity(id={self.entity_id}, "
                f"tags=[{tags_str}], "
                f"components=[{component_names}])")

    @classmethod
    def reset_id_counter(cls, start_id: int = 1) -> None:
        """
        Reset the entity ID counter.

        Args:
            start_id: The ID to start counting from

        Educational Note:
            This method is primarily useful for testing, allowing tests to
            start with predictable entity IDs. In production code, you rarely
            need to reset the counter.

        Example:
            >>> Entity.reset_id_counter(1)  # Reset to 1 before tests
        """
        cls._next_id = start_id
