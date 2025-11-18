"""
Unit tests for InventoryComponent

Tests cover:
- Initialization
- Adding and removing items
- Capacity management
- Item searching
- Gold management
- Serialization and deserialization
"""

import pytest
from src.components.inventory import InventoryComponent
from src.components.name import NameComponent
from src.entities.entity import Entity


class TestInventoryComponent:
    """Test suite for InventoryComponent."""

    def test_initialization_with_defaults(self):
        """Test default initialization."""
        inventory = InventoryComponent()

        assert inventory.max_capacity == 20
        assert inventory.gold == 0
        assert inventory.count_items() == 0
        assert inventory.is_empty() is True

    def test_initialization_with_custom_values(self):
        """Test initialization with custom parameters."""
        inventory = InventoryComponent(max_capacity=10, gold=50)

        assert inventory.max_capacity == 10
        assert inventory.gold == 50

    def test_add_item(self):
        """Test adding an item."""
        inventory = InventoryComponent()
        item = Entity()

        result = inventory.add_item(item)

        assert result is True
        assert inventory.count_items() == 1
        assert inventory.is_empty() is False

    def test_add_multiple_items(self):
        """Test adding multiple items."""
        inventory = InventoryComponent()

        for i in range(5):
            item = Entity()
            inventory.add_item(item)

        assert inventory.count_items() == 5

    def test_add_item_when_full(self):
        """Test that adding item fails when inventory full."""
        inventory = InventoryComponent(max_capacity=2)

        item1 = Entity()
        item2 = Entity()
        item3 = Entity()

        assert inventory.add_item(item1) is True
        assert inventory.add_item(item2) is True
        assert inventory.add_item(item3) is False  # Inventory full

        assert inventory.count_items() == 2

    def test_remove_item_by_index(self):
        """Test removing item by index."""
        inventory = InventoryComponent()
        item1 = Entity()
        item2 = Entity()

        inventory.add_item(item1)
        inventory.add_item(item2)

        removed = inventory.remove_item(0)

        assert removed == item1
        assert inventory.count_items() == 1

    def test_remove_item_invalid_index(self):
        """Test removing item with invalid index."""
        inventory = InventoryComponent()
        item = Entity()
        inventory.add_item(item)

        # Negative index
        result = inventory.remove_item(-1)
        assert result is None

        # Index too high
        result = inventory.remove_item(5)
        assert result is None

    def test_remove_item_by_entity(self):
        """Test removing specific item entity."""
        inventory = InventoryComponent()
        item1 = Entity()
        item2 = Entity()

        inventory.add_item(item1)
        inventory.add_item(item2)

        result = inventory.remove_item_by_entity(item1)

        assert result is True
        assert inventory.count_items() == 1
        assert item1 not in inventory.items
        assert item2 in inventory.items

    def test_remove_item_by_entity_not_found(self):
        """Test removing item that's not in inventory."""
        inventory = InventoryComponent()
        item1 = Entity()
        item2 = Entity()

        inventory.add_item(item1)

        result = inventory.remove_item_by_entity(item2)

        assert result is False
        assert inventory.count_items() == 1

    def test_get_item(self):
        """Test getting item without removing it."""
        inventory = InventoryComponent()
        item1 = Entity()
        item2 = Entity()

        inventory.add_item(item1)
        inventory.add_item(item2)

        retrieved = inventory.get_item(1)

        assert retrieved == item2
        assert inventory.count_items() == 2  # Not removed

    def test_get_item_invalid_index(self):
        """Test getting item with invalid index."""
        inventory = InventoryComponent()

        result = inventory.get_item(0)
        assert result is None

        result = inventory.get_item(-1)
        assert result is None

    def test_find_item_by_name(self):
        """Test finding item by name."""
        inventory = InventoryComponent()

        item1 = Entity()
        item1.add_component(NameComponent(name="Health Potion"))

        item2 = Entity()
        item2.add_component(NameComponent(name="Mana Potion"))

        inventory.add_item(item1)
        inventory.add_item(item2)

        found = inventory.find_item_by_name("health")

        assert found == item1

    def test_find_item_by_name_case_insensitive(self):
        """Test that name search is case-insensitive."""
        inventory = InventoryComponent()

        item = Entity()
        item.add_component(NameComponent(name="Sword of Power"))
        inventory.add_item(item)

        found = inventory.find_item_by_name("SWORD")

        assert found == item

    def test_find_item_by_name_not_found(self):
        """Test finding item that doesn't exist."""
        inventory = InventoryComponent()

        item = Entity()
        item.add_component(NameComponent(name="Shield"))
        inventory.add_item(item)

        found = inventory.find_item_by_name("Sword")

        assert found is None

    def test_count_items(self):
        """Test counting items."""
        inventory = InventoryComponent()

        assert inventory.count_items() == 0

        for i in range(3):
            inventory.add_item(Entity())

        assert inventory.count_items() == 3

    def test_is_full(self):
        """Test is_full check."""
        inventory = InventoryComponent(max_capacity=2)

        assert inventory.is_full() is False

        inventory.add_item(Entity())
        assert inventory.is_full() is False

        inventory.add_item(Entity())
        assert inventory.is_full() is True

    def test_is_empty(self):
        """Test is_empty check."""
        inventory = InventoryComponent()

        assert inventory.is_empty() is True

        inventory.add_item(Entity())
        assert inventory.is_empty() is False

        inventory.remove_item(0)
        assert inventory.is_empty() is True

    def test_get_remaining_capacity(self):
        """Test calculating remaining capacity."""
        inventory = InventoryComponent(max_capacity=5)

        assert inventory.get_remaining_capacity() == 5

        inventory.add_item(Entity())
        inventory.add_item(Entity())

        assert inventory.get_remaining_capacity() == 3

    def test_clear(self):
        """Test clearing all items."""
        inventory = InventoryComponent()

        item1 = Entity()
        item2 = Entity()
        item3 = Entity()

        inventory.add_item(item1)
        inventory.add_item(item2)
        inventory.add_item(item3)

        dropped = inventory.clear()

        assert len(dropped) == 3
        assert item1 in dropped
        assert item2 in dropped
        assert item3 in dropped
        assert inventory.is_empty() is True

    def test_add_gold(self):
        """Test adding gold."""
        inventory = InventoryComponent(gold=10)

        inventory.add_gold(50)
        assert inventory.gold == 60

        inventory.add_gold(5)
        assert inventory.gold == 65

    def test_add_negative_gold(self):
        """Test that negative gold doesn't reduce total."""
        inventory = InventoryComponent(gold=100)

        inventory.add_gold(-50)
        assert inventory.gold == 50

        inventory.add_gold(-100)
        assert inventory.gold == 0

    def test_remove_gold_success(self):
        """Test removing gold when sufficient."""
        inventory = InventoryComponent(gold=100)

        result = inventory.remove_gold(50)

        assert result is True
        assert inventory.gold == 50

    def test_remove_gold_insufficient(self):
        """Test removing gold when insufficient."""
        inventory = InventoryComponent(gold=30)

        result = inventory.remove_gold(50)

        assert result is False
        assert inventory.gold == 30  # Unchanged

    def test_remove_gold_exact_amount(self):
        """Test removing exact gold amount."""
        inventory = InventoryComponent(gold=100)

        result = inventory.remove_gold(100)

        assert result is True
        assert inventory.gold == 0

    def test_to_dict(self):
        """Test serialization to dictionary."""
        inventory = InventoryComponent(max_capacity=15, gold=75)

        item1 = Entity()
        item1.entity_id = 101
        item2 = Entity()
        item2.entity_id = 102

        inventory.add_item(item1)
        inventory.add_item(item2)

        data = inventory.to_dict()

        assert data['component_type'] == 'InventoryComponent'
        assert data['max_capacity'] == 15
        assert data['gold'] == 75
        assert data['item_ids'] == [101, 102]

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'component_type': 'InventoryComponent',
            'max_capacity': 25,
            'gold': 150
        }

        inventory = InventoryComponent.from_dict(data)

        assert inventory.max_capacity == 25
        assert inventory.gold == 150

    def test_from_dict_with_defaults(self):
        """Test deserialization with missing fields."""
        data = {'component_type': 'InventoryComponent'}

        inventory = InventoryComponent.from_dict(data)

        assert inventory.max_capacity == 20
        assert inventory.gold == 0

    def test_serialization_round_trip(self):
        """Test that serialization preserves data."""
        original = InventoryComponent(max_capacity=30, gold=200)

        data = original.to_dict()
        restored = InventoryComponent.from_dict(data)

        assert restored.max_capacity == original.max_capacity
        assert restored.gold == original.gold

    def test_inventory_workflow(self):
        """Test complete inventory workflow."""
        inventory = InventoryComponent(max_capacity=3)

        # Pick up items
        sword = Entity()
        sword.add_component(NameComponent(name="Sword"))

        shield = Entity()
        shield.add_component(NameComponent(name="Shield"))

        potion = Entity()
        potion.add_component(NameComponent(name="Potion"))

        inventory.add_item(sword)
        inventory.add_item(shield)
        inventory.add_item(potion)

        # Inventory full
        assert inventory.is_full()

        # Use potion (remove it)
        found_potion = inventory.find_item_by_name("Potion")
        inventory.remove_item_by_entity(found_potion)

        # Now have space
        assert not inventory.is_full()
        assert inventory.count_items() == 2

    def test_gold_transactions(self):
        """Test gold buying/selling workflow."""
        inventory = InventoryComponent(gold=100)

        # Buy item for 60 gold
        if inventory.remove_gold(60):
            # Add item to inventory
            item = Entity()
            inventory.add_item(item)

        assert inventory.gold == 40
        assert inventory.count_items() == 1

        # Try to buy expensive item (120 gold)
        can_afford = inventory.remove_gold(120)
        assert can_afford is False
        assert inventory.gold == 40  # Unchanged

        # Sell item for 30 gold
        inventory.add_gold(30)
        assert inventory.gold == 70
