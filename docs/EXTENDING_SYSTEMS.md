# Extending Core Systems - Developer Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Adding New Components](#adding-new-components)
3. [Creating New Systems](#creating-new-systems)
4. [Extending Existing Systems](#extending-existing-systems)
5. [Adding New Game Mechanics](#adding-new-game-mechanics)
6. [Advanced Patterns](#advanced-patterns)
7. [Performance Considerations](#performance-considerations)
8. [Testing Extensions](#testing-extensions)

---

## Introduction

This guide covers how to extend the game's core systems to add new mechanics, features, and capabilities. It assumes familiarity with the ECS architecture (see `ECS_DEVELOPER_GUIDE.md`).

### Extension Philosophy

The game is designed for extensibility:
- **Components** are pure data - easy to add
- **Systems** are loosely coupled - easy to modify
- **Data-driven** content - easy to create
- **Modular architecture** - easy to understand

### Before You Start

1. Read `ECS_DEVELOPER_GUIDE.md`
2. Understand the existing codebase structure
3. Run all tests to ensure baseline functionality
4. Create a new branch for your changes

---

## Adding New Components

### Component Template

```python
# src/components/my_new_component.py

from src.components.base import Component
from typing import Dict, Any

class MyNewComponent(Component):
    """
    Brief description of what this component does.

    Attributes:
        attribute_name: Description of attribute
        another_attribute: Description of another attribute

    Educational Note:
        Explain the design rationale and use cases.
    """

    def __init__(self, attribute_value: int, another_value: str = "default"):
        """
        Initialize the component.

        Args:
            attribute_value: Description
            another_value: Description with default

        Educational Note:
            Explain parameter choices.
        """
        super().__init__()
        self.attribute_value = attribute_value
        self.another_value = another_value

    def to_dict(self) -> Dict[str, Any]:
        """Serialize component for save/load."""
        return {
            'component_type': self.component_type,
            'attribute_value': self.attribute_value,
            'another_value': self.another_value
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MyNewComponent':
        """Deserialize component from save data."""
        return cls(
            attribute_value=data.get('attribute_value', 0),
            another_value=data.get('another_value', 'default')
        )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"MyNewComponent(attribute_value={self.attribute_value}, "
                f"another_value='{self.another_value}')")
```

### Register Component

**1. Add to `src/components/__init__.py`:**
```python
from src.components.my_new_component import MyNewComponent

__all__ = [
    # ... existing components ...
    'MyNewComponent',
]
```

**2. Add to component registry (in save/load system):**
```python
# src/systems/save_load.py

COMPONENT_REGISTRY = {
    # ... existing components ...
    'MyNewComponent': MyNewComponent,
}
```

### Create Tests

**tests/components/test_my_new_component.py:**
```python
import pytest
from src.components.my_new_component import MyNewComponent

def test_initialization():
    """Test component creates correctly."""
    comp = MyNewComponent(attribute_value=42, another_value="test")
    assert comp.attribute_value == 42
    assert comp.another_value == "test"

def test_default_values():
    """Test default parameter values."""
    comp = MyNewComponent(attribute_value=10)
    assert comp.another_value == "default"

def test_serialization():
    """Test to_dict/from_dict round-trip."""
    original = MyNewComponent(attribute_value=99, another_value="data")
    data = original.to_dict()
    restored = MyNewComponent.from_dict(data)

    assert restored.attribute_value == original.attribute_value
    assert restored.another_value == original.another_value

def test_component_type():
    """Test component_type is set correctly."""
    comp = MyNewComponent(attribute_value=1)
    assert comp.component_type == "MyNewComponent"
```

### Example: Adding a Hunger Component

```python
# src/components/hunger.py

from src.components.base import Component
from typing import Dict, Any

class HungerComponent(Component):
    """
    Tracks entity hunger/satiation levels.

    Hunger increases over time and can cause damage if too high.
    Eating food reduces hunger.

    Attributes:
        current_hunger: Current hunger level (0-100, 100 = starving)
        hunger_rate: Hunger increase per turn
        damage_threshold: Hunger level that causes damage
        damage_per_turn: Damage taken when above threshold
    """

    def __init__(self,
                 current_hunger: int = 0,
                 hunger_rate: int = 1,
                 damage_threshold: int = 80,
                 damage_per_turn: int = 1):
        super().__init__()
        self.current_hunger = current_hunger
        self.hunger_rate = hunger_rate
        self.damage_threshold = damage_threshold
        self.damage_per_turn = damage_per_turn

    def increase_hunger(self):
        """Increase hunger by hunger_rate."""
        self.current_hunger = min(100, self.current_hunger + self.hunger_rate)

    def decrease_hunger(self, amount: int):
        """Decrease hunger by amount (eating food)."""
        self.current_hunger = max(0, self.current_hunger - amount)

    def is_starving(self) -> bool:
        """Check if entity is taking starvation damage."""
        return self.current_hunger >= self.damage_threshold

    def get_hunger_percentage(self) -> float:
        """Get hunger as percentage (0.0-1.0)."""
        return self.current_hunger / 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'component_type': self.component_type,
            'current_hunger': self.current_hunger,
            'hunger_rate': self.hunger_rate,
            'damage_threshold': self.damage_threshold,
            'damage_per_turn': self.damage_per_turn
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HungerComponent':
        return cls(
            current_hunger=data.get('current_hunger', 0),
            hunger_rate=data.get('hunger_rate', 1),
            damage_threshold=data.get('damage_threshold', 80),
            damage_per_turn=data.get('damage_per_turn', 1)
        )
```

---

## Creating New Systems

### System Template

```python
# src/systems/my_new_system.py

from typing import List, Tuple, Optional
from src.entities.entity import Entity
from src.components import MyNewComponent, PositionComponent
from src.models import Map

class MyNewSystem:
    """
    Brief description of what this system does.

    This system processes entities with MyNewComponent and performs X.

    Educational Note:
        Explain the system's role in the game loop.
    """

    def __init__(self):
        """Initialize system state."""
        # Store any system-wide state here
        self.processed_count = 0

    def process_entity(self,
                      entity: Entity,
                      dungeon_map: Map,
                      *args) -> bool:
        """
        Process a single entity.

        Args:
            entity: Entity to process
            dungeon_map: Current dungeon map
            *args: Additional arguments

        Returns:
            True if processing succeeded, False otherwise

        Educational Note:
            Explain processing logic.
        """
        # Check component requirements
        if not entity.has_component(MyNewComponent):
            return False

        # Get required components
        my_comp = entity.get_component(MyNewComponent)

        # Perform processing
        # ... system logic here ...

        self.processed_count += 1
        return True

    def process_all(self,
                   entities: List[Entity],
                   dungeon_map: Map,
                   *args) -> List[Entity]:
        """
        Process all valid entities.

        Args:
            entities: List of all entities
            dungeon_map: Current dungeon map
            *args: Additional arguments

        Returns:
            List of successfully processed entities
        """
        processed = []
        for entity in entities:
            if self.process_entity(entity, dungeon_map, *args):
                processed.append(entity)
        return processed

    def reset_stats(self):
        """Reset system statistics."""
        self.processed_count = 0
```

### Integrate Into Game Loop

```python
# main.py or game loop file

from src.systems.my_new_system import MyNewSystem

# Initialize system
my_system = MyNewSystem()

# In game loop
while game_running:
    # ... existing systems ...

    # Process new system
    my_system.process_all(entities, dungeon_map, additional_args)

    # ... continue game loop ...
```

### Example: Hunger System

```python
# src/systems/hunger_system.py

from typing import List
from src.entities.entity import Entity
from src.components import HungerComponent, HealthComponent, NameComponent

class HungerSystem:
    """
    Manages hunger mechanics for entities.

    Increases hunger each turn and applies starvation damage
    when hunger exceeds threshold.
    """

    def __init__(self):
        self.total_damage_dealt = 0

    def process_entity(self, entity: Entity) -> Tuple[bool, List[str]]:
        """
        Process hunger for one entity.

        Returns:
            (success, messages) tuple
        """
        messages = []

        if not entity.has_component(HungerComponent):
            return (False, messages)

        hunger = entity.get_component(HungerComponent)

        # Increase hunger
        hunger.increase_hunger()

        # Check for starvation
        if hunger.is_starving():
            if entity.has_component(HealthComponent):
                health = entity.get_component(HealthComponent)
                health.take_damage(hunger.damage_per_turn)
                self.total_damage_dealt += hunger.damage_per_turn

                # Generate message
                if entity.has_component(NameComponent):
                    name = entity.get_component(NameComponent).name
                else:
                    name = f"Entity {entity.entity_id}"

                messages.append(
                    f"{name} is starving! ({hunger.damage_per_turn} damage)"
                )

        return (True, messages)

    def process_all(self, entities: List[Entity]) -> List[str]:
        """Process all entities with hunger."""
        all_messages = []
        for entity in entities:
            success, messages = self.process_entity(entity)
            all_messages.extend(messages)
        return all_messages

    def feed_entity(self, entity: Entity, food_value: int) -> bool:
        """Feed an entity to reduce hunger."""
        if not entity.has_component(HungerComponent):
            return False

        hunger = entity.get_component(HungerComponent)
        hunger.decrease_hunger(food_value)
        return True
```

---

## Extending Existing Systems

### Pattern 1: Subclassing

```python
# src/systems/my_combat_system.py

from src.systems.combat import CombatSystem
from src.components import MyNewComponent

class ExtendedCombatSystem(CombatSystem):
    """Extended combat system with new mechanics."""

    def calculate_damage(self, attacker, defender):
        """Override damage calculation."""
        # Call parent method
        base_damage = super().calculate_damage(attacker, defender)

        # Add new mechanics
        if attacker.has_component(MyNewComponent):
            bonus = attacker.get_component(MyNewComponent).damage_bonus
            base_damage += bonus

        return base_damage
```

### Pattern 2: Composition

```python
# src/systems/enhanced_ai.py

from src.systems.ai import AISystem
from src.components import MyNewComponent

class EnhancedAISystem:
    """AI system with additional behavior handling."""

    def __init__(self):
        self.base_ai = AISystem()

    def process_entity(self, entity, *args):
        """Process with additional checks."""
        # Handle new component
        if entity.has_component(MyNewComponent):
            self._process_special_behavior(entity, *args)

        # Delegate to base AI
        return self.base_ai.process_entity(entity, *args)

    def _process_special_behavior(self, entity, *args):
        """Handle special AI behavior."""
        # ... custom logic ...
        pass
```

### Pattern 3: Hooks/Events

```python
# src/systems/combat_hooks.py

from typing import Callable, List
from src.systems.combat import CombatSystem

class HookableCombatSystem(CombatSystem):
    """Combat system with event hooks."""

    def __init__(self):
        super().__init__()
        self.on_attack_hooks: List[Callable] = []
        self.on_damage_hooks: List[Callable] = []
        self.on_death_hooks: List[Callable] = []

    def register_attack_hook(self, callback: Callable):
        """Register callback for attack events."""
        self.on_attack_hooks.append(callback)

    def attack(self, attacker, defender):
        """Attack with hook support."""
        # Call pre-attack hooks
        for hook in self.on_attack_hooks:
            hook(attacker, defender, "pre")

        # Execute attack
        result = super().attack(attacker, defender)

        # Call post-attack hooks
        for hook in self.on_attack_hooks:
            hook(attacker, defender, "post")

        return result

# Usage:
def poison_on_hit(attacker, defender, phase):
    """Apply poison effect on hit."""
    if phase == "post" and attacker.has_tag("poison"):
        # Apply poison to defender
        pass

combat_system = HookableCombatSystem()
combat_system.register_attack_hook(poison_on_hit)
```

---

## Adding New Game Mechanics

### Example 1: Magic/Spell System

**Step 1: Create Components**
```python
# src/components/magic.py

class ManaComponent(Component):
    """Tracks magical energy."""
    def __init__(self, current_mana: int, max_mana: int):
        super().__init__()
        self.current_mana = current_mana
        self.max_mana = max_mana

    def spend_mana(self, cost: int) -> bool:
        """Spend mana if available."""
        if self.current_mana >= cost:
            self.current_mana -= cost
            return True
        return False

class SpellComponent(Component):
    """Defines a castable spell."""
    def __init__(self, spell_id: str, mana_cost: int, effect: str):
        super().__init__()
        self.spell_id = spell_id
        self.mana_cost = mana_cost
        self.effect = effect
```

**Step 2: Create System**
```python
# src/systems/magic_system.py

class MagicSystem:
    """Handles spell casting."""

    def cast_spell(self, caster, spell, target):
        """Cast a spell from caster to target."""
        # Check mana
        if not caster.has_component(ManaComponent):
            return (False, "No mana!")

        mana = caster.get_component(ManaComponent)
        if not mana.spend_mana(spell.mana_cost):
            return (False, "Not enough mana!")

        # Apply spell effect
        self._apply_spell_effect(spell, target)
        return (True, f"Cast {spell.spell_id}!")

    def _apply_spell_effect(self, spell, target):
        """Apply spell effect to target."""
        # Implement spell effects
        pass
```

**Step 3: Add to Game Loop**
```python
# main.py

magic_system = MagicSystem()

# When player casts spell:
if command == 'cast':
    spell = player.get_spell(spell_id)
    success, message = magic_system.cast_spell(player, spell, target)
    print(message)
```

### Example 2: Weather System

```python
# src/systems/weather_system.py

from enum import Enum, auto

class Weather(Enum):
    CLEAR = auto()
    RAIN = auto()
    STORM = auto()
    FOG = auto()

class WeatherSystem:
    """Manages environmental weather effects."""

    def __init__(self):
        self.current_weather = Weather.CLEAR
        self.turns_until_change = 50

    def update(self, entities, dungeon_map):
        """Update weather each turn."""
        self.turns_until_change -= 1

        if self.turns_until_change <= 0:
            self._change_weather()
            self.turns_until_change = 50

        # Apply weather effects
        self._apply_weather_effects(entities, dungeon_map)

    def _change_weather(self):
        """Randomly change weather."""
        import random
        self.current_weather = random.choice(list(Weather))

    def _apply_weather_effects(self, entities, dungeon_map):
        """Apply current weather effects."""
        if self.current_weather == Weather.RAIN:
            # Reduce accuracy for all entities
            for entity in entities:
                if entity.has_component(CombatComponent):
                    combat = entity.get_component(CombatComponent)
                    # Temporary accuracy penalty
                    pass

        elif self.current_weather == Weather.FOG:
            # Reduce vision range
            for entity in entities:
                if entity.has_component(VisibilityComponent):
                    # Temporary vision penalty
                    pass
```

---

## Advanced Patterns

### Pattern 1: Event Queue

```python
# src/systems/event_queue.py

from dataclasses import dataclass
from typing import List, Callable, Any
from enum import Enum, auto

class EventType(Enum):
    ENTITY_DEATH = auto()
    ITEM_PICKUP = auto()
    COMBAT_HIT = auto()
    LEVEL_UP = auto()

@dataclass
class GameEvent:
    event_type: EventType
    data: dict

class EventQueue:
    """Central event queue for game events."""

    def __init__(self):
        self.events: List[GameEvent] = []
        self.listeners: dict = {}

    def emit(self, event_type: EventType, data: dict):
        """Add event to queue."""
        event = GameEvent(event_type=event_type, data=data)
        self.events.append(event)

    def register_listener(self, event_type: EventType, callback: Callable):
        """Register callback for event type."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def process_events(self):
        """Process all queued events."""
        while self.events:
            event = self.events.pop(0)
            if event.event_type in self.listeners:
                for callback in self.listeners[event.event_type]:
                    callback(event.data)

# Usage:
event_queue = EventQueue()

def on_entity_death(data):
    """Handle entity death."""
    entity = data['entity']
    print(f"{entity} died!")

event_queue.register_listener(EventType.ENTITY_DEATH, on_entity_death)

# In combat system:
if health.is_dead:
    event_queue.emit(EventType.ENTITY_DEATH, {'entity': defender})
```

### Pattern 2: Effect System

```python
# src/systems/effect_system.py

from abc import ABC, abstractmethod

class Effect(ABC):
    """Base class for game effects."""

    def __init__(self, duration: int):
        self.duration = duration

    @abstractmethod
    def apply(self, entity):
        """Apply effect to entity."""
        pass

    @abstractmethod
    def remove(self, entity):
        """Remove effect from entity."""
        pass

    def tick(self) -> bool:
        """Decrease duration. Returns True if expired."""
        self.duration -= 1
        return self.duration <= 0

class PoisonEffect(Effect):
    """Poison damage over time."""

    def __init__(self, duration: int, damage_per_turn: int):
        super().__init__(duration)
        self.damage_per_turn = damage_per_turn

    def apply(self, entity):
        """Apply poison damage."""
        if entity.has_component(HealthComponent):
            health = entity.get_component(HealthComponent)
            health.take_damage(self.damage_per_turn)

    def remove(self, entity):
        """No cleanup needed for poison."""
        pass

class EffectManager:
    """Manages active effects on entities."""

    def __init__(self):
        self.entity_effects: dict = {}  # entity_id -> [Effect]

    def add_effect(self, entity_id: int, effect: Effect):
        """Add effect to entity."""
        if entity_id not in self.entity_effects:
            self.entity_effects[entity_id] = []
        self.entity_effects[entity_id].append(effect)

    def update_effects(self, entities):
        """Update all effects each turn."""
        for entity in entities:
            if entity.entity_id in self.entity_effects:
                effects = self.entity_effects[entity.entity_id]
                remaining = []

                for effect in effects:
                    # Apply effect
                    effect.apply(entity)

                    # Check if expired
                    if not effect.tick():
                        remaining.append(effect)
                    else:
                        effect.remove(entity)

                self.entity_effects[entity.entity_id] = remaining
```

### Pattern 3: Command Pattern

```python
# src/systems/command_system.py

from abc import ABC, abstractmethod

class Command(ABC):
    """Base class for game commands."""

    @abstractmethod
    def execute(self, game_state):
        """Execute command."""
        pass

    @abstractmethod
    def undo(self, game_state):
        """Undo command (for replay/undo systems)."""
        pass

class MoveCommand(Command):
    """Command to move entity."""

    def __init__(self, entity, dx, dy):
        self.entity = entity
        self.dx = dx
        self.dy = dy
        self.old_x = None
        self.old_y = None

    def execute(self, game_state):
        """Move entity."""
        pos = self.entity.get_component(PositionComponent)
        self.old_x, self.old_y = pos.x, pos.y
        pos.set_position(pos.x + self.dx, pos.y + self.dy)

    def undo(self, game_state):
        """Undo move."""
        pos = self.entity.get_component(PositionComponent)
        pos.set_position(self.old_x, self.old_y)

class CommandQueue:
    """Queue of commands for execution."""

    def __init__(self):
        self.commands = []
        self.history = []

    def add_command(self, command: Command):
        """Add command to queue."""
        self.commands.append(command)

    def execute_all(self, game_state):
        """Execute all queued commands."""
        while self.commands:
            command = self.commands.pop(0)
            command.execute(game_state)
            self.history.append(command)

    def undo_last(self, game_state):
        """Undo last command."""
        if self.history:
            command = self.history.pop()
            command.undo(game_state)
```

---

## Performance Considerations

### Spatial Hashing for Large Maps

```python
# src/systems/spatial_hash.py

class SpatialHash:
    """Efficient entity lookups by position."""

    def __init__(self, cell_size: int = 10):
        self.cell_size = cell_size
        self.cells: dict = {}

    def _hash(self, x: int, y: int) -> tuple:
        """Convert position to cell coordinates."""
        return (x // self.cell_size, y // self.cell_size)

    def insert(self, entity, x: int, y: int):
        """Insert entity at position."""
        cell = self._hash(x, y)
        if cell not in self.cells:
            self.cells[cell] = []
        self.cells[cell].append(entity)

    def query_area(self, x: int, y: int, radius: int) -> List:
        """Get all entities in area."""
        entities = []
        cell_x, cell_y = self._hash(x, y)
        cell_radius = (radius // self.cell_size) + 1

        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                cell = (cell_x + dx, cell_y + dy)
                if cell in self.cells:
                    entities.extend(self.cells[cell])

        return entities
```

### Entity Pooling

```python
# src/entities/entity_pool.py

class EntityPool:
    """Reuse entity objects to reduce allocation."""

    def __init__(self, pool_size: int = 100):
        self.available = []
        self.in_use = []

        # Pre-allocate entities
        for _ in range(pool_size):
            self.available.append(Entity())

    def acquire(self, tags=None):
        """Get entity from pool."""
        if self.available:
            entity = self.available.pop()
            entity.tags = tags or []
            self.in_use.append(entity)
            return entity
        else:
            # Pool exhausted, create new
            entity = Entity(tags=tags)
            self.in_use.append(entity)
            return entity

    def release(self, entity):
        """Return entity to pool."""
        if entity in self.in_use:
            self.in_use.remove(entity)
            # Clear entity state
            entity.components.clear()
            entity.tags.clear()
            self.available.append(entity)
```

---

## Testing Extensions

### Test Template

```python
# tests/systems/test_my_new_system.py

import pytest
from src.systems.my_new_system import MyNewSystem
from src.entities.entity import Entity
from src.components import MyNewComponent

@pytest.fixture
def system():
    """Create system instance."""
    return MyNewSystem()

@pytest.fixture
def test_entity():
    """Create test entity with required components."""
    entity = Entity()
    entity.add_component(MyNewComponent(value=42))
    return entity

def test_system_initialization(system):
    """Test system initializes correctly."""
    assert system is not None
    assert system.processed_count == 0

def test_process_valid_entity(system, test_entity):
    """Test processing entity with required components."""
    result = system.process_entity(test_entity, None)
    assert result is True
    assert system.processed_count == 1

def test_process_invalid_entity(system):
    """Test processing entity without required components."""
    entity = Entity()  # No MyNewComponent
    result = system.process_entity(entity, None)
    assert result is False
    assert system.processed_count == 0

def test_process_all(system, test_entity):
    """Test processing multiple entities."""
    entities = [test_entity, Entity(), test_entity]
    processed = system.process_all(entities, None)
    assert len(processed) == 2  # Only 2 have required components
```

---

## Best Practices Summary

### Do:
✅ Keep components pure data
✅ Put logic in systems
✅ Write tests for new features
✅ Document design decisions
✅ Follow existing patterns
✅ Use type hints
✅ Handle edge cases
✅ Consider performance

### Don't:
❌ Put logic in components
❌ Create tightly coupled systems
❌ Skip testing
❌ Hardcode values
❌ Break existing functionality
❌ Ignore performance
❌ Forget documentation

---

## Conclusion

This guide provides patterns and examples for extending the game. Remember:

1. **Start small** - Add one feature at a time
2. **Test thoroughly** - Write tests before integrating
3. **Follow patterns** - Use existing code as examples
4. **Document well** - Explain your design decisions
5. **Ask for help** - Check documentation and community

**Happy extending! Build amazing new features!** 🚀
