"""
InventoryComponent - Manages entity item storage

This component tracks items carried by an entity, with capacity limits and
item management methods.

Educational Notes:
------------------
Inventory systems are core to RPGs and roguelikes. They handle:
- Item storage (what items does entity have?)
- Capacity limits (max items or weight)
- Item access (adding, removing, searching)
- Organization (stacking, sorting, categories)

Design Considerations:
1. **Capacity System:**
   - Slot-based: Limited number of item slots
   - Weight-based: Limited total weight
   - Hybrid: Both slots and weight

2. **Stacking:**
   - Should identical items stack? (3x Health Potion)
   - Max stack size?

3. **Equipment:**
   - Separate inventory from equipped items?
   - Equipment slots (weapon, armor, etc.)?

This implementation uses a simple slot-based system with entity references.
"""

from typing import List, Optional, Dict, Any, TYPE_CHECKING
from src.components.base import Component

if TYPE_CHECKING:
    from src.entities.entity import Entity


class InventoryComponent(Component):
    """
    Component for storing and managing items.

    Attributes:
        items: List of item entities in inventory
        max_capacity: Maximum number of items that can be carried
        gold: Amount of currency (future use)

    Educational Note:
        Inventory items are entities too! An item is just an entity with:
        - PositionComponent (where it is)
        - RenderComponent (how it looks)
        - SignalComponent (what it contains)
        - Maybe other components (consumable, equippable, etc.)

        When picked up, the item entity is:
        1. Removed from the world entity list
        2. Added to inventory items list
        3. Position becomes irrelevant (it's "in inventory")

    Example:
        >>> inventory = InventoryComponent(max_capacity=20)
        >>> # Pick up an item
        >>> item = create_item("health_potion", x=0, y=0)
        >>> if inventory.add_item(item):
        ...     print("Picked up item!")
        >>>
        >>> # Check if full
        >>> if inventory.is_full():
        ...     print("Inventory full!")
        >>>
        >>> # Drop an item
        >>> dropped = inventory.remove_item(0)
    """

    def __init__(self, max_capacity: int = 20, gold: int = 0):
        """
        Initialize inventory component.

        Args:
            max_capacity: Maximum number of items (default 20)
            gold: Starting gold amount (default 0)

        Educational Note:
            max_capacity of 20 is common in roguelikes - enough to be
            useful but not unlimited. Forces interesting decisions about
            what to keep and what to drop.
        """
        super().__init__()
        self.items: List['Entity'] = []
        self.max_capacity = max_capacity
        self.gold = gold

    def add_item(self, item: 'Entity') -> bool:
        """
        Add an item to inventory.

        Args:
            item: Item entity to add

        Returns:
            True if item added successfully, False if inventory full

        Educational Note:
            Returns boolean so caller knows if pickup succeeded.
            Useful for feedback: "Inventory full!" vs "Picked up sword"

        Example:
            >>> inventory = InventoryComponent(max_capacity=5)
            >>> item = Entity()  # Some item
            >>> if inventory.add_item(item):
            ...     print("Item added!")
            ... else:
            ...     print("Inventory full!")
        """
        if self.is_full():
            return False

        self.items.append(item)
        return True

    def remove_item(self, index: int) -> Optional['Entity']:
        """
        Remove item at given index.

        Args:
            index: Index of item to remove (0-based)

        Returns:
            Removed item entity, or None if index invalid

        Educational Note:
            Returns the removed item so it can be:
            - Dropped in the world (placed at player position)
            - Used/consumed (apply effects, then destroy)
            - Thrown (place in throw trajectory)

        Example:
            >>> inventory = InventoryComponent()
            >>> # ... add some items ...
            >>> dropped = inventory.remove_item(2)  # Remove 3rd item
            >>> if dropped:
            ...     # Place item in world at player position
            ...     place_in_world(dropped, player_x, player_y)
        """
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def remove_item_by_entity(self, item: 'Entity') -> bool:
        """
        Remove specific item entity from inventory.

        Args:
            item: Item entity to remove

        Returns:
            True if item was removed, False if not found

        Educational Note:
            Useful when you have reference to item entity but not its
            index. For example, when using an item.

        Example:
            >>> health_potion = find_item("health_potion")
            >>> if health_potion:
            ...     inventory.remove_item_by_entity(health_potion)
            ...     # Apply healing effect
            ...     player.heal(20)
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_item(self, index: int) -> Optional['Entity']:
        """
        Get item at index without removing it.

        Args:
            index: Index of item to get (0-based)

        Returns:
            Item entity at index, or None if invalid index

        Example:
            >>> item = inventory.get_item(0)  # Look at first item
            >>> if item:
            ...     name = item.get_component(NameComponent).name
            ...     print(f"First item: {name}")
        """
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def find_item_by_name(self, name: str) -> Optional['Entity']:
        """
        Find first item matching name.

        Args:
            name: Name to search for (case-insensitive)

        Returns:
            First matching item entity, or None if not found

        Educational Note:
            Useful for scripting/commands:
            - "use health potion" -> find by name -> use item
            - "drop sword" -> find by name -> drop item

        Example:
            >>> potion = inventory.find_item_by_name("health potion")
            >>> if potion:
            ...     use_item(potion)
        """
        from src.components import NameComponent

        name_lower = name.lower()
        for item in self.items:
            name_comp = item.get_component(NameComponent)
            if name_comp and name_lower in name_comp.name.lower():
                return item
        return None

    def count_items(self) -> int:
        """
        Get number of items in inventory.

        Returns:
            Number of items currently in inventory

        Example:
            >>> count = inventory.count_items()
            >>> print(f"You have {count} items")
        """
        return len(self.items)

    def is_full(self) -> bool:
        """
        Check if inventory is at capacity.

        Returns:
            True if inventory full, False otherwise

        Example:
            >>> if not inventory.is_full():
            ...     inventory.add_item(new_item)
        """
        return len(self.items) >= self.max_capacity

    def is_empty(self) -> bool:
        """
        Check if inventory has no items.

        Returns:
            True if empty, False otherwise

        Example:
            >>> if inventory.is_empty():
            ...     print("Your inventory is empty")
        """
        return len(self.items) == 0

    def get_remaining_capacity(self) -> int:
        """
        Get number of free inventory slots.

        Returns:
            Number of items that can still be added

        Example:
            >>> free = inventory.get_remaining_capacity()
            >>> print(f"You can carry {free} more items")
        """
        return self.max_capacity - len(self.items)

    def clear(self) -> List['Entity']:
        """
        Remove all items from inventory.

        Returns:
            List of all removed items

        Educational Note:
            Useful for death handling - drop all items on death.

        Example:
            >>> # Player dies, drop everything
            >>> dropped_items = inventory.clear()
            >>> for item in dropped_items:
            ...     place_at_position(item, player_x, player_y)
        """
        items = self.items.copy()
        self.items.clear()
        return items

    def add_gold(self, amount: int) -> None:
        """
        Add gold to inventory.

        Args:
            amount: Amount of gold to add

        Example:
            >>> inventory.add_gold(50)
            >>> print(f"Gold: {inventory.gold}")
        """
        self.gold = max(0, self.gold + amount)

    def remove_gold(self, amount: int) -> bool:
        """
        Remove gold from inventory.

        Args:
            amount: Amount of gold to remove

        Returns:
            True if enough gold, False if insufficient

        Example:
            >>> if inventory.remove_gold(100):
            ...     print("Purchased item!")
            ... else:
            ...     print("Not enough gold!")
        """
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize inventory component to dictionary."""
        return {
            'component_type': self.component_type,
            'item_ids': [item.entity_id for item in self.items],
            'max_capacity': self.max_capacity,
            'gold': self.gold
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryComponent':
        """
        Deserialize inventory component from dictionary.

        Args:
            data: Dictionary containing inventory data

        Returns:
            New InventoryComponent instance

        Educational Note:
            Item entities are referenced by ID during serialization.
            During loading, these IDs are used to reconnect inventory
            with item entities after all entities are loaded.
        """
        inventory = cls(
            max_capacity=data.get('max_capacity', 20),
            gold=data.get('gold', 0)
        )
        # Note: items are restored by entity ID references
        # The actual item entities are reconnected during world loading
        return inventory
