# Entity-Component-System Developer Guide

## Table of Contents

1. [Introduction to ECS](#introduction-to-ecs)
2. [Core Concepts](#core-concepts)
3. [Components Reference](#components-reference)
4. [Systems Reference](#systems-reference)
5. [Entity Management](#entity-management)
6. [Practical Examples](#practical-examples)
7. [Best Practices](#best-practices)
8. [Common Patterns](#common-patterns)
9. [Extension Guide](#extension-guide)
10. [Troubleshooting](#troubleshooting)

---

## Introduction to ECS

### What is Entity-Component-System?

**Entity-Component-System (ECS)** is an architectural pattern that favors **composition over inheritance**. Instead of creating complex class hierarchies (e.g., `Player extends Character extends GameObject`), ECS composes game objects (entities) from small, reusable data containers (components) that are processed by specialized logic modules (systems).

### The Three Pillars

#### 1. Entities
- **Lightweight containers** with unique IDs
- Hold a collection of components
- No behavior - just data aggregation
- Think of them as "bags of components"

#### 2. Components
- **Pure data containers** with minimal logic
- Represent specific aspects (position, health, rendering, etc.)
- Independent and reusable
- Can be mixed and matched freely

#### 3. Systems
- **Logic processors** that operate on entities
- Process entities based on required components
- Implement all game behavior
- Stateless when possible

### Why ECS?

**Traditional Inheritance Approach:**
```
GameObject
├── Character
│   ├── Player (position, render, health, inventory, input)
│   └── Enemy (position, render, health, AI)
├── Item (position, render, inventory item)
└── Trap (position, render, tile effect)
```

**Problems:**
- Rigid hierarchies
- Code duplication
- Difficult to add cross-cutting features
- Complex multiple inheritance issues

**ECS Approach:**
```
Entity #1 (Player):    [Position, Render, Health, Inventory, Input, Name]
Entity #2 (Enemy):     [Position, Render, Health, Combat, AI, Name]
Entity #3 (Item):      [Position, Render, Inventory]
Entity #4 (Trap):      [Position, Render, TileEffect]
```

**Benefits:**
- ✅ **Modularity:** Components are independent units
- ✅ **Flexibility:** Add/remove capabilities dynamically
- ✅ **Reusability:** Components work across entity types
- ✅ **Testability:** Test components in isolation
- ✅ **Data-driven:** Easy to define entities in JSON
- ✅ **Performance:** Cache-friendly data layouts (advanced)

---

## Core Concepts

### Component Base Class

All components inherit from the abstract `Component` base class:

**Location:** `src/components/base.py`

```python
from src.components.base import Component

class Component(ABC):
    def __init__(self):
        self.component_type = self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for save/load"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Component':
        """Deserialize from save data"""
```

**Key Features:**
- Automatic type identification (`component_type`)
- Serialization support for save/load
- Minimal interface - maximum flexibility

### Entity Class

Entities are component containers with unique IDs:

**Location:** `src/entities/entity.py`

```python
from src.entities.entity import Entity

# Create entity
player = Entity(tags=['player'])

# Add components
player.add_component(PositionComponent(x=10, y=5))
player.add_component(RenderComponent(char='@', color='white'))
player.add_component(HealthComponent(current_hp=100, max_hp=100))

# Query components
if player.has_component(HealthComponent):
    health = player.get_component(HealthComponent)
    print(f"HP: {health.current_hp}/{health.max_hp}")

# Check multiple components
if player.has_components(PositionComponent, RenderComponent):
    render_system.draw(player)
```

**Key Methods:**
- `add_component(component)` - Add a component
- `remove_component(ComponentType)` - Remove a component
- `get_component(ComponentType)` - Retrieve a component
- `has_component(ComponentType)` - Check existence
- `has_components(*types)` - Check multiple components
- `add_tag(tag)` / `has_tag(tag)` - Tag management
- `to_dict()` / `from_dict()` - Serialization

### System Pattern

Systems process entities with specific component requirements:

```python
class MovementSystem:
    def process(self, entity, dx, dy, dungeon_map):
        # Require PositionComponent
        if not entity.has_component(PositionComponent):
            return False

        position = entity.get_component(PositionComponent)
        new_x = position.x + dx
        new_y = position.y + dy

        if dungeon_map.is_walkable(new_x, new_y):
            position.set_position(new_x, new_y)
            return True
        return False
```

---

## Components Reference

### 1. PositionComponent

**Purpose:** Spatial location in 2D space

**Location:** `src/components/position.py`

**Attributes:**
- `x: int` - X coordinate
- `y: int` - Y coordinate

**Methods:**
- `set_position(x, y)` - Update position
- `distance_to(other)` - Calculate distance to another position
- `is_adjacent_to(other)` - Check if adjacent (within 1 tile)

**Usage:**
```python
from src.components import PositionComponent

pos = PositionComponent(x=10, y=20)
pos.set_position(11, 20)  # Move right

# Check distance
enemy_pos = PositionComponent(x=12, y=20)
distance = pos.distance_to(enemy_pos)  # 1.0

# Check adjacency for melee combat
if pos.is_adjacent_to(enemy_pos):
    combat_system.attack(player, enemy)
```

**When to Use:**
- Any entity that exists in the dungeon
- Required for: rendering, movement, combat, collision

---

### 2. RenderComponent

**Purpose:** Visual representation on screen

**Location:** `src/components/render.py`

**Attributes:**
- `char: str` - ASCII character to display
- `color: str` - Color name (white, red, green, etc.)
- `render_order: int` - Drawing priority (higher = drawn on top)
- `visible: bool` - Whether entity is currently visible

**Methods:**
- `set_visibility(visible)` - Show/hide entity
- `set_char(char)` - Change display character
- `set_color(color)` - Change color

**Usage:**
```python
from src.components import RenderComponent

# Player: white @ at high priority
player_render = RenderComponent(char='@', color='white', render_order=10)

# Enemy: red 'g' at medium priority
enemy_render = RenderComponent(char='g', color='red', render_order=5)

# Item: yellow '*' at low priority
item_render = RenderComponent(char='*', color='yellow', render_order=1)

# Hide entity temporarily
player_render.set_visibility(False)
```

**Render Order Convention:**
- 1-3: Items, floor effects
- 4-6: Enemies, NPCs
- 7-10: Player, important entities

---

### 3. HealthComponent

**Purpose:** Hit points and death state

**Location:** `src/components/health.py`

**Attributes:**
- `current_hp: int` - Current hit points
- `max_hp: int` - Maximum hit points
- `is_dead: bool` - Death state (cached)

**Methods:**
- `take_damage(amount)` - Reduce HP by amount
- `heal(amount)` - Restore HP (capped at max)
- `set_max_hp(new_max)` - Change max HP
- `is_alive()` - Check if entity is alive
- `get_hp_percentage()` - Get HP as percentage (0.0-1.0)

**Usage:**
```python
from src.components import HealthComponent

health = HealthComponent(current_hp=100, max_hp=100)

# Take damage
health.take_damage(30)
print(f"HP: {health.current_hp}/{health.max_hp}")  # HP: 70/100

# Check if alive
if health.is_alive():
    print("Still fighting!")

# Heal
health.heal(20)  # Now at 90/100

# Level up - increase max HP
health.set_max_hp(120)
health.heal(30)  # Now at 120/120

# Check death
health.take_damage(150)
assert health.is_dead
```

---

### 4. CombatComponent

**Purpose:** Combat statistics and damage calculation

**Location:** `src/components/combat.py`

**Attributes:**
- `base_damage: int` - Base attack damage
- `defense: int` - Damage reduction
- `accuracy: float` - Hit chance (0.0-1.0)
- `crit_chance: float` - Critical hit chance (0.0-1.0)
- `crit_multiplier: float` - Critical damage multiplier (default 2.0)
- `attack_range: int` - Attack range in tiles (1 = melee)

**Methods:**
- `calculate_damage()` - Roll damage with crits
- `apply_defense(damage)` - Reduce damage by defense
- `modify_damage(amount)` - Adjust base damage
- `modify_defense(amount)` - Adjust defense

**Usage:**
```python
from src.components import CombatComponent

# Warrior: high damage, medium defense
warrior = CombatComponent(
    base_damage=15,
    defense=5,
    accuracy=0.85,
    crit_chance=0.2,
    attack_range=1
)

# Archer: lower damage, long range
archer = CombatComponent(
    base_damage=8,
    defense=2,
    accuracy=0.75,
    crit_chance=0.15,
    attack_range=5
)

# Calculate damage
damage = warrior.calculate_damage()  # 15 or 30 (if crit)

# Apply defense
actual_damage = archer.apply_defense(damage)  # damage - 2
```

---

### 5. InventoryComponent

**Purpose:** Item storage and management

**Location:** `src/components/inventory.py`

**Attributes:**
- `items: List[Entity]` - List of item entities
- `capacity: int` - Maximum items allowed
- `gold: int` - Currency amount

**Methods:**
- `add_item(item)` - Add item to inventory
- `remove_item(item)` - Remove item from inventory
- `has_item(item)` - Check if item exists
- `is_full()` - Check if at capacity
- `find_item_by_name(name)` - Search for item
- `add_gold(amount)` / `remove_gold(amount)` - Gold management

**Usage:**
```python
from src.components import InventoryComponent

inventory = InventoryComponent(capacity=10)

# Add item
potion = Entity(tags=['item', 'consumable'])
# ... add components to potion ...
if inventory.add_item(potion):
    print("Picked up potion!")

# Check capacity
if inventory.is_full():
    print(f"Inventory full! ({len(inventory.items)}/{inventory.capacity})")

# Search for item
health_potion = inventory.find_item_by_name("Health Potion")

# Gold management
inventory.add_gold(50)
if inventory.gold >= 100:
    inventory.remove_gold(100)
    print("Purchased item!")
```

---

### 6. AIComponent

**Purpose:** NPC/enemy behavior control

**Location:** `src/components/ai.py`

**Attributes:**
- `behavior: str` - Behavior type (wander, chase, guard, flee, patrol)
- `target: Optional[Entity]` - Current target entity
- `patrol_route: List[Tuple[int, int]]` - Patrol waypoints
- `patrol_index: int` - Current waypoint index
- `state_data: Dict` - Arbitrary state storage

**Methods:**
- `set_behavior(behavior)` - Change behavior type
- `set_target(entity)` - Set target entity
- `clear_target()` - Remove target
- `set_patrol_route(waypoints)` - Define patrol path
- `get_next_patrol_point()` - Get next waypoint

**Behaviors:**
- **wander:** Random movement
- **chase:** Follow target entity
- **guard:** Stay in area, attack intruders
- **flee:** Run away from target
- **patrol:** Follow waypoint route

**Usage:**
```python
from src.components import AIComponent

# Wandering enemy
ai = AIComponent(behavior='wander')

# Guard with patrol route
guard = AIComponent(behavior='patrol')
guard.set_patrol_route([
    (10, 5), (20, 5), (20, 15), (10, 15)
])

# Chase player when spotted
if player_spotted:
    ai.set_behavior('chase')
    ai.set_target(player)

# Process AI in game loop
ai_system.process(enemy, dungeon_map, entities)
```

---

### 7. SignalComponent

**Purpose:** Signal crafting and combination

**Location:** `src/components/signal.py`

**Attributes:**
- `signal_type: str` - Type of signal (voltage, current, frequency)
- `strength: float` - Signal strength (0.0-1.0)
- `modulation: Optional[str]` - Signal modulation

**Methods:**
- `set_strength(strength)` - Adjust signal strength
- `set_modulation(mod)` - Change modulation
- `combine_with(other)` - Combine two signals

**Usage:**
```python
from src.components import SignalComponent

# Create voltage signal
signal = SignalComponent(
    signal_type='voltage',
    strength=0.8,
    modulation='PWM'
)

# Combine signals for crafting
signal2 = SignalComponent(signal_type='current', strength=0.6)
result = signal.combine_with(signal2)
```

---

### 8. StatusEffectComponent

**Purpose:** Temporary buffs/debuffs

**Location:** `src/components/status_effect.py`

**Attributes:**
- `effects: Dict[str, StatusEffect]` - Active effects by name
- `StatusEffect` includes: duration, stat_modifier, effect_type

**Methods:**
- `add_effect(name, duration, modifier, effect_type)` - Apply effect
- `remove_effect(name)` - Remove effect
- `has_effect(name)` - Check for effect
- `tick_effects()` - Decrease durations by 1 turn
- `get_stat_modifier(stat_name)` - Get total modifier for stat

**Effect Types:**
- **buff:** Positive effect
- **debuff:** Negative effect
- **damage_over_time:** Deal damage each turn
- **heal_over_time:** Heal each turn

**Usage:**
```python
from src.components import StatusEffectComponent

status = StatusEffectComponent()

# Apply poison (3 damage per turn for 5 turns)
status.add_effect(
    name='poison',
    duration=5,
    modifier={'damage_per_turn': 3},
    effect_type='damage_over_time'
)

# Apply strength buff (+5 damage for 10 turns)
status.add_effect(
    name='strength',
    duration=10,
    modifier={'damage': 5},
    effect_type='buff'
)

# Check for effect
if status.has_effect('poison'):
    print("Poisoned!")

# Process effects each turn
status.tick_effects()
damage_bonus = status.get_stat_modifier('damage')  # +5 from strength
```

---

### 9. TileEffectComponent

**Purpose:** Effects triggered by standing on tiles

**Location:** `src/components/tile_effect.py`

**Attributes:**
- `effect_type: str` - Effect type (damage, heal, apply_status)
- `trigger: str` - When to trigger (on_enter, on_exit, per_turn)
- `properties: Dict` - Effect-specific properties

**Methods:**
- `set_effect_type(effect_type)` - Change effect type
- `set_trigger(trigger)` - Change trigger timing
- `get_property(key)` - Get effect property
- `set_property(key, value)` - Set effect property

**Usage:**
```python
from src.components import TileEffectComponent

# Lava tile: 10 damage per turn
lava = TileEffectComponent(
    effect_type='damage',
    trigger='per_turn',
    properties={'amount': 10, 'damage_type': 'fire'}
)

# Healing fountain: 5 HP on entry
fountain = TileEffectComponent(
    effect_type='heal',
    trigger='on_enter',
    properties={'amount': 5}
)

# Poison cloud: apply poison status
poison_cloud = TileEffectComponent(
    effect_type='apply_status',
    trigger='on_enter',
    properties={'status': 'poison', 'duration': 5}
)
```

---

### 10. InputComponent

**Purpose:** Control input acceptance

**Location:** `src/components/input.py`

**Attributes:**
- `accepts_input: bool` - Whether entity can receive input

**Methods:**
- `enable_input()` - Allow input
- `disable_input()` - Block input
- `can_act()` - Check if can receive input

**Usage:**
```python
from src.components import InputComponent

input_comp = InputComponent()

# Disable during cutscene
input_comp.disable_input()

# Re-enable after cutscene
input_comp.enable_input()

# Check before processing input
if player.get_component(InputComponent).can_act():
    process_player_command(command)
```

---

### 11. NameComponent

**Purpose:** Entity identification and display names

**Location:** `src/components/name.py`

**Attributes:**
- `name: str` - Display name
- `description: str` - Detailed description

**Methods:**
- `set_name(name)` - Change name
- `set_description(desc)` - Change description

**Usage:**
```python
from src.components import NameComponent

name = NameComponent(
    name="Corrupted Data Packet",
    description="A hostile entity born from corrupted data transmission."
)

# Display in UI
print(f"You see: {name.name}")
print(f"  {name.description}")
```

---

## Systems Reference

### 1. RenderSystem (ASCIIRenderer)

**Purpose:** Convert game state to terminal output

**Location:** `src/systems/renderer.py`

**Requirements:** Entities with `PositionComponent + RenderComponent`

**Key Methods:**
```python
renderer = ASCIIRenderer(width=80, height=24)

# Basic render
output = renderer.render(dungeon_map, entities)

# Render with camera offset
output = renderer.render(dungeon_map, entities, camera_x=10, camera_y=5)

# Render directly to console
renderer.render_to_console(dungeon_map, entities)

# Render with border
output = renderer.render_with_border(dungeon_map, entities, title="Floor 1")
```

**Process:**
1. Render base map tiles
2. Sort entities by `render_order`
3. Overlay visible entities
4. Convert to string output

---

### 2. MovementSystem

**Purpose:** Handle entity movement and collision

**Location:** `src/systems/movement.py`

**Requirements:** Entities with `PositionComponent`

**Key Methods:**
```python
movement_system = MovementSystem()

# Move entity
success = movement_system.move_entity(
    entity=player,
    dx=1, dy=0,  # Move right
    dungeon_map=dungeon_map
)

# Check if position is blocked
blocked = movement_system.is_position_blocked(
    x=10, y=5,
    dungeon_map=dungeon_map,
    entities=entities
)
```

---

### 3. CombatSystem

**Purpose:** Resolve combat between entities

**Location:** `src/systems/combat.py`

**Requirements:** Entities with `CombatComponent + HealthComponent + PositionComponent`

**Key Methods:**
```python
combat_system = CombatSystem()

# Execute attack
success, messages = combat_system.attack(
    attacker=player,
    defender=enemy,
    entities=entities
)

for msg in messages:
    print(msg)  # "Player attacks Goblin for 15 damage!"
```

**Combat Flow:**
1. Check range (must be within `attack_range`)
2. Roll accuracy (hit/miss)
3. Calculate damage (with crit chance)
4. Apply defense
5. Apply damage to health
6. Check for death
7. Generate messages

---

### 4. AISystem

**Purpose:** Process NPC/enemy behaviors

**Location:** `src/systems/ai.py`

**Requirements:** Entities with `AIComponent + PositionComponent`

**Key Methods:**
```python
ai_system = AISystem()

# Process single entity AI
ai_system.process_entity(
    entity=enemy,
    dungeon_map=dungeon_map,
    entities=entities,
    player=player
)

# Process all AI entities
ai_system.process_all(entities, dungeon_map, player)
```

**Behaviors:**
- **wander:** Random walk
- **chase:** Pathfind toward target
- **guard:** Attack nearby enemies
- **flee:** Move away from target
- **patrol:** Follow waypoint route

---

### 5. CraftingSystem

**Purpose:** Combine signals using recipes

**Location:** `src/systems/crafting.py`

**Requirements:** Entities with `SignalComponent + InventoryComponent`

**Key Methods:**
```python
crafting_system = CraftingSystem()

# Attempt craft
success, result = crafting_system.craft(
    entity=player,
    recipe_id="voltage_boost",
    ingredients=[signal1, signal2]
)

if success:
    print(f"Crafted: {result.name}")
```

---

### 6. SaveLoadSystem

**Purpose:** Persist and restore game state

**Location:** `src/systems/save_load.py`

**Key Methods:**
```python
save_system = SaveLoadSystem()

# Save game
save_system.save_game(
    filename="savegame.json",
    player=player,
    entities=entities,
    dungeon_map=dungeon_map,
    game_state=game_state
)

# Load game
player, entities, dungeon_map, game_state = save_system.load_game(
    filename="savegame.json"
)
```

---

### 7. InputHandler

**Purpose:** Parse and process player input

**Location:** `src/systems/input_handler.py`

**Key Methods:**
```python
input_handler = InputHandler()

# Process command
command = input_handler.parse_input("move north")

if command['action'] == 'move':
    dx, dy = command['direction']
    movement_system.move_entity(player, dx, dy, dungeon_map)
```

---

### 8. LoggingSystem

**Purpose:** Track game events for debugging

**Location:** `src/systems/logging_system.py`

**Key Methods:**
```python
from src.systems.logging_system import get_logger, log_event

logger = get_logger()

# Log events
log_event("combat", "Player attacked Goblin", {"damage": 15})
log_event("movement", "Player moved to (10, 5)")

# Log performance
logger.log_performance("dungeon_generation", 0.245)
```

---

## Entity Management

### Creating Entities

**Basic Entity Creation:**
```python
from src.entities.entity import Entity
from src.components import *

# Create player entity
player = Entity(tags=['player'])
player.add_component(PositionComponent(x=10, y=10))
player.add_component(RenderComponent(char='@', color='white', render_order=10))
player.add_component(HealthComponent(current_hp=100, max_hp=100))
player.add_component(CombatComponent(base_damage=10, defense=3, accuracy=0.85))
player.add_component(InventoryComponent(capacity=20))
player.add_component(InputComponent())
player.add_component(NameComponent(name="Player", description="That's you!"))
```

**Enemy Entity:**
```python
enemy = Entity(tags=['enemy', 'hostile'])
enemy.add_component(PositionComponent(x=15, y=12))
enemy.add_component(RenderComponent(char='g', color='red', render_order=5))
enemy.add_component(HealthComponent(current_hp=30, max_hp=30))
enemy.add_component(CombatComponent(base_damage=5, defense=1, accuracy=0.75))
enemy.add_component(AIComponent(behavior='chase'))
enemy.add_component(NameComponent(name="Goblin", description="A hostile creature"))
```

**Item Entity:**
```python
potion = Entity(tags=['item', 'consumable'])
potion.add_component(PositionComponent(x=12, y=8))
potion.add_component(RenderComponent(char='!', color='yellow', render_order=1))
potion.add_component(NameComponent(name="Health Potion", description="Restores 50 HP"))
# Store healing amount in a custom attribute or use a custom component
```

### Data-Driven Entity Creation

**From JSON Configuration:**
```python
from src.data_loader.json_loader import JSONLoader

loader = JSONLoader()

# Load enemy config
enemy_config = loader.load_enemy("corrupted_packet")

# Build entity from config
enemy = Entity(tags=['enemy'])
enemy.add_component(PositionComponent(x=10, y=10))
enemy.add_component(RenderComponent(
    char=enemy_config['visual']['ascii_char'],
    color=enemy_config['visual']['color'],
    render_order=5
))

# Add components from config
if 'health' in enemy_config['components']:
    health_data = enemy_config['components']['health']
    enemy.add_component(HealthComponent(
        current_hp=health_data['current_hp'],
        max_hp=health_data['max_hp']
    ))
```

### Entity Querying

**Find Entities by Component:**
```python
# Find all entities with health
living_entities = [e for e in entities if e.has_component(HealthComponent)]

# Find all enemies
enemies = [e for e in entities if e.has_tag('enemy')]

# Find renderable entities
renderable = [e for e in entities
              if e.has_components(PositionComponent, RenderComponent)]

# Find entities at position
entities_at_pos = [e for e in entities
                   if e.has_component(PositionComponent) and
                   e.get_component(PositionComponent).x == target_x and
                   e.get_component(PositionComponent).y == target_y]
```

### Entity Destruction

**Remove Dead Entities:**
```python
# Mark for removal
dead_entities = [e for e in entities
                 if e.has_component(HealthComponent) and
                 e.get_component(HealthComponent).is_dead]

# Remove from entity list
for dead in dead_entities:
    entities.remove(dead)

    # Optional: Drop items
    if dead.has_component(InventoryComponent):
        inventory = dead.get_component(InventoryComponent)
        position = dead.get_component(PositionComponent)
        for item in inventory.items:
            # Move items to ground
            item.get_component(PositionComponent).set_position(position.x, position.y)
```

---

## Practical Examples

### Example 1: Creating a Custom Enemy Type

**Goal:** Create a "Toxic Slime" enemy that poisons on hit

```python
from src.entities.entity import Entity
from src.components import *

def create_toxic_slime(x, y):
    """Factory function for Toxic Slime enemy"""
    slime = Entity(tags=['enemy', 'poison'])

    # Core components
    slime.add_component(PositionComponent(x=x, y=y))
    slime.add_component(RenderComponent(char='s', color='green', render_order=5))
    slime.add_component(NameComponent(
        name="Toxic Slime",
        description="A gelatinous creature that secretes poison"
    ))

    # Combat stats
    slime.add_component(HealthComponent(current_hp=20, max_hp=20))
    slime.add_component(CombatComponent(
        base_damage=3,
        defense=1,
        accuracy=0.7,
        attack_range=1
    ))

    # AI behavior
    slime.add_component(AIComponent(behavior='chase'))

    return slime

# Use in combat system to apply poison on hit
def on_successful_hit(attacker, defender):
    if attacker.has_tag('poison'):
        if defender.has_component(StatusEffectComponent):
            status = defender.get_component(StatusEffectComponent)
        else:
            status = StatusEffectComponent()
            defender.add_component(status)

        status.add_effect(
            name='poison',
            duration=3,
            modifier={'damage_per_turn': 2},
            effect_type='damage_over_time'
        )
```

### Example 2: Implementing a Teleport Trap

**Goal:** Create a trap tile that teleports player to random location

```python
def create_teleport_trap(x, y):
    """Create a teleport trap entity"""
    trap = Entity(tags=['trap', 'hazard'])

    trap.add_component(PositionComponent(x=x, y=y))
    trap.add_component(RenderComponent(char='^', color='cyan', render_order=1))
    trap.add_component(NameComponent(
        name="Teleport Trap",
        description="A magical trap that teleports unwary adventurers"
    ))
    trap.add_component(TileEffectComponent(
        effect_type='teleport',
        trigger='on_enter',
        properties={'random': True}
    ))

    return trap

# In game loop, check for tile effects
def process_tile_effects(entity, entities, dungeon_map):
    if not entity.has_component(PositionComponent):
        return

    pos = entity.get_component(PositionComponent)

    # Find entities at same position with tile effects
    for other in entities:
        if not other.has_components(PositionComponent, TileEffectComponent):
            continue

        other_pos = other.get_component(PositionComponent)
        if other_pos.x == pos.x and other_pos.y == pos.y:
            effect = other.get_component(TileEffectComponent)

            if effect.effect_type == 'teleport' and effect.trigger == 'on_enter':
                # Teleport to random walkable tile
                import random
                while True:
                    new_x = random.randint(0, dungeon_map.width - 1)
                    new_y = random.randint(0, dungeon_map.height - 1)
                    if dungeon_map.is_walkable(new_x, new_y):
                        pos.set_position(new_x, new_y)
                        print("You've been teleported!")
                        break
```

### Example 3: Implementing a Buff Potion

**Goal:** Create a strength potion that boosts damage

```python
def create_strength_potion(x, y):
    """Create a strength potion item"""
    potion = Entity(tags=['item', 'consumable', 'potion'])

    potion.add_component(PositionComponent(x=x, y=y))
    potion.add_component(RenderComponent(char='!', color='red', render_order=1))
    potion.add_component(NameComponent(
        name="Strength Potion",
        description="Increases damage by 5 for 10 turns"
    ))

    return potion

# In use_item function
def use_strength_potion(user_entity, potion):
    """Apply strength buff to user"""
    if not user_entity.has_component(StatusEffectComponent):
        status = StatusEffectComponent()
        user_entity.add_component(status)
    else:
        status = user_entity.get_component(StatusEffectComponent)

    status.add_effect(
        name='strength',
        duration=10,
        modifier={'damage': 5},
        effect_type='buff'
    )

    print("You feel stronger!")
    return True  # Consumed successfully

# In combat system, apply buffs
def calculate_total_damage(attacker):
    combat = attacker.get_component(CombatComponent)
    base_damage = combat.calculate_damage()

    # Add status effect modifiers
    if attacker.has_component(StatusEffectComponent):
        status = attacker.get_component(StatusEffectComponent)
        damage_bonus = status.get_stat_modifier('damage')
        base_damage += damage_bonus

    return base_damage
```

### Example 4: Implementing Fog of War

**Goal:** Only render entities the player can see

```python
class VisibilityComponent(Component):
    """Component for field of view calculation"""
    def __init__(self, vision_range=10):
        super().__init__()
        self.vision_range = vision_range
        self.visible_tiles = set()  # Set of (x, y) tuples

    def update_visibility(self, dungeon_map, position):
        """Calculate visible tiles from position"""
        self.visible_tiles.clear()

        # Simple circular vision (can be replaced with proper FOV algorithm)
        for dx in range(-self.vision_range, self.vision_range + 1):
            for dy in range(-self.vision_range, self.vision_range + 1):
                if dx*dx + dy*dy <= self.vision_range * self.vision_range:
                    x, y = position.x + dx, position.y + dy
                    if 0 <= x < dungeon_map.width and 0 <= y < dungeon_map.height:
                        if not dungeon_map.blocks_sight(x, y):
                            self.visible_tiles.add((x, y))

# Add to player
player.add_component(VisibilityComponent(vision_range=8))

# Before rendering
if player.has_component(VisibilityComponent):
    visibility = player.get_component(VisibilityComponent)
    position = player.get_component(PositionComponent)
    visibility.update_visibility(dungeon_map, position)

    # Hide entities outside vision
    for entity in entities:
        if entity.has_components(PositionComponent, RenderComponent):
            pos = entity.get_component(PositionComponent)
            render = entity.get_component(RenderComponent)

            if (pos.x, pos.y) in visibility.visible_tiles:
                render.set_visibility(True)
            else:
                render.set_visibility(False)
```

---

## Best Practices

### 1. Keep Components Pure Data

**❌ Bad - Logic in component:**
```python
class HealthComponent(Component):
    def __init__(self, hp, max_hp):
        self.hp = hp
        self.max_hp = max_hp

    def attack_enemy(self, enemy, damage):  # ❌ Don't do this!
        enemy.get_component(HealthComponent).take_damage(damage)
```

**✅ Good - Logic in system:**
```python
class HealthComponent(Component):
    def __init__(self, hp, max_hp):
        self.hp = hp
        self.max_hp = max_hp

    def take_damage(self, amount):  # ✅ Simple data manipulation OK
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

class CombatSystem:
    def attack(self, attacker, defender):  # ✅ Logic in system
        # ... combat logic ...
```

### 2. Use Factory Functions

**✅ Create reusable entity templates:**
```python
def create_player(x, y):
    """Factory for player entity"""
    player = Entity(tags=['player'])
    player.add_component(PositionComponent(x=x, y=y))
    player.add_component(RenderComponent(char='@', color='white', render_order=10))
    player.add_component(HealthComponent(current_hp=100, max_hp=100))
    player.add_component(InventoryComponent(capacity=20))
    player.add_component(InputComponent())
    return player

def create_enemy(enemy_type, x, y):
    """Factory for enemies from templates"""
    templates = {
        'goblin': {
            'char': 'g', 'color': 'red',
            'hp': 20, 'damage': 5, 'defense': 1
        },
        'orc': {
            'char': 'o', 'color': 'green',
            'hp': 40, 'damage': 8, 'defense': 3
        }
    }

    template = templates[enemy_type]
    enemy = Entity(tags=['enemy'])
    enemy.add_component(PositionComponent(x=x, y=y))
    enemy.add_component(RenderComponent(
        char=template['char'],
        color=template['color'],
        render_order=5
    ))
    enemy.add_component(HealthComponent(
        current_hp=template['hp'],
        max_hp=template['hp']
    ))
    enemy.add_component(CombatComponent(
        base_damage=template['damage'],
        defense=template['defense'],
        accuracy=0.75
    ))
    enemy.add_component(AIComponent(behavior='chase'))
    return enemy
```

### 3. Check Component Existence

**✅ Always check before getting components:**
```python
# ✅ Safe
if entity.has_component(HealthComponent):
    health = entity.get_component(HealthComponent)
    health.take_damage(10)

# ✅ Also safe
health = entity.get_component(HealthComponent)
if health:
    health.take_damage(10)

# ❌ Unsafe - might be None
health = entity.get_component(HealthComponent)
health.take_damage(10)  # Crashes if no HealthComponent!
```

### 4. Use Tags for Categories

**✅ Tags for broad classification:**
```python
entity.add_tag('enemy')
entity.add_tag('hostile')
entity.add_tag('undead')

# Easy filtering
enemies = [e for e in entities if e.has_tag('enemy')]
undead = [e for e in entities if e.has_tag('undead')]
```

### 5. Implement Serialization

**✅ Override to_dict/from_dict for custom components:**
```python
class CustomComponent(Component):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def to_dict(self):
        return {
            'component_type': self.component_type,
            'data': self.data
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data=data.get('data'))
```

### 6. System Processing Patterns

**✅ Clear system interfaces:**
```python
class MySystem:
    def process_entity(self, entity, *args):
        """Process single entity"""
        if not entity.has_components(RequiredComponent1, RequiredComponent2):
            return False

        # Process entity
        return True

    def process_all(self, entities, *args):
        """Process all valid entities"""
        results = []
        for entity in entities:
            if self.process_entity(entity, *args):
                results.append(entity)
        return results
```

---

## Common Patterns

### Pattern 1: State Machine via Components

Use components and tags to implement state machines:

```python
# States via tags
entity.add_tag('idle')

# Transition to attacking
if target_found:
    entity.remove_tag('idle')
    entity.add_tag('attacking')
    entity.get_component(AIComponent).set_target(player)

# Transition to fleeing
if low_health:
    entity.remove_tag('attacking')
    entity.add_tag('fleeing')
    entity.get_component(AIComponent).set_behavior('flee')
```

### Pattern 2: Event Messaging

Generate messages for player feedback:

```python
def attack(attacker, defender):
    messages = []

    # Calculate and apply damage
    damage = calculate_damage(attacker, defender)
    defender.get_component(HealthComponent).take_damage(damage)

    # Generate message
    attacker_name = attacker.get_component(NameComponent).name
    defender_name = defender.get_component(NameComponent).name
    messages.append(f"{attacker_name} attacks {defender_name} for {damage} damage!")

    # Check for death
    if defender.get_component(HealthComponent).is_dead:
        messages.append(f"{defender_name} has been defeated!")

    return messages
```

### Pattern 3: Component Composition

Build complex behaviors through component combinations:

```python
# Boss enemy with multiple components
boss = Entity(tags=['enemy', 'boss'])
boss.add_component(PositionComponent(x=40, y=20))
boss.add_component(RenderComponent(char='D', color='red', render_order=8))
boss.add_component(HealthComponent(current_hp=200, max_hp=200))
boss.add_component(CombatComponent(base_damage=20, defense=10, accuracy=0.9))
boss.add_component(AIComponent(behavior='chase'))
boss.add_component(StatusEffectComponent())  # Can be buffed/debuffed
boss.add_component(InventoryComponent(capacity=5))  # Drops loot
boss.add_component(NameComponent(name="Dragon", description="A fearsome dragon"))

# The combination of components defines complex behavior:
# - Chases player (AI + Position)
# - Tough combat (Health + Combat)
# - Can be affected by spells (StatusEffect)
# - Drops valuable loot (Inventory)
```

### Pattern 4: Prototype Cloning

Clone entities for spawning:

```python
def clone_entity(source, new_x, new_y):
    """Create a copy of an entity at a new position"""
    clone = Entity(tags=source.tags.copy())

    for component_name, component in source.components.items():
        # Clone component
        cloned_component = type(component).from_dict(component.to_dict())
        clone.add_component(cloned_component)

    # Update position
    if clone.has_component(PositionComponent):
        clone.get_component(PositionComponent).set_position(new_x, new_y)

    return clone

# Use for spawning
template_goblin = create_enemy('goblin', 0, 0)

# Spawn 10 goblins at random positions
for i in range(10):
    x, y = get_random_spawn_position()
    goblin = clone_entity(template_goblin, x, y)
    entities.append(goblin)
```

---

## Extension Guide

### Adding a New Component

**1. Create component file:**

`src/components/my_component.py`:
```python
from src.components.base import Component
from typing import Dict, Any

class MyComponent(Component):
    """
    Brief description of component purpose.

    Attributes:
        my_attribute: Description
    """
    def __init__(self, my_attribute: int):
        super().__init__()
        self.my_attribute = my_attribute

    def to_dict(self) -> Dict[str, Any]:
        return {
            'component_type': self.component_type,
            'my_attribute': self.my_attribute
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MyComponent':
        return cls(my_attribute=data.get('my_attribute', 0))
```

**2. Add to `src/components/__init__.py`:**
```python
from src.components.my_component import MyComponent

__all__ = [
    # ... existing components ...
    'MyComponent',
]
```

**3. Register for serialization:**

In save/load system, add to component registry:
```python
COMPONENT_REGISTRY = {
    # ... existing components ...
    'MyComponent': MyComponent,
}
```

**4. Create tests:**

`tests/components/test_my_component.py`:
```python
import pytest
from src.components.my_component import MyComponent

def test_my_component_creation():
    comp = MyComponent(my_attribute=42)
    assert comp.my_attribute == 42

def test_serialization():
    comp = MyComponent(my_attribute=42)
    data = comp.to_dict()
    restored = MyComponent.from_dict(data)
    assert restored.my_attribute == comp.my_attribute
```

### Adding a New System

**1. Create system file:**

`src/systems/my_system.py`:
```python
from src.entities.entity import Entity
from src.components import MyComponent, PositionComponent
from typing import List

class MySystem:
    """
    Brief description of system purpose.

    This system processes entities with MyComponent.
    """

    def __init__(self):
        """Initialize system state if needed"""
        pass

    def process_entity(self, entity: Entity, *args) -> bool:
        """
        Process a single entity.

        Args:
            entity: Entity to process
            *args: Additional arguments

        Returns:
            True if processing succeeded, False otherwise
        """
        if not entity.has_component(MyComponent):
            return False

        my_comp = entity.get_component(MyComponent)
        # Process logic here

        return True

    def process_all(self, entities: List[Entity], *args) -> List[Entity]:
        """
        Process all valid entities.

        Args:
            entities: List of entities
            *args: Additional arguments

        Returns:
            List of successfully processed entities
        """
        processed = []
        for entity in entities:
            if self.process_entity(entity, *args):
                processed.append(entity)
        return processed
```

**2. Add to `src/systems/__init__.py`:**
```python
from src.systems.my_system import MySystem

__all__ = [
    # ... existing systems ...
    'MySystem',
]
```

**3. Integrate into game loop:**

`main.py`:
```python
from src.systems import MySystem

# Initialize
my_system = MySystem()

# In game loop
my_system.process_all(entities, additional_args)
```

**4. Create tests:**

`tests/systems/test_my_system.py`:
```python
import pytest
from src.systems.my_system import MySystem
from src.entities.entity import Entity
from src.components import MyComponent

def test_my_system_processes_valid_entity():
    entity = Entity()
    entity.add_component(MyComponent(my_attribute=10))

    system = MySystem()
    result = system.process_entity(entity)

    assert result is True

def test_my_system_ignores_invalid_entity():
    entity = Entity()  # No MyComponent

    system = MySystem()
    result = system.process_entity(entity)

    assert result is False
```

---

## Troubleshooting

### Issue: Component Not Found

**Symptom:**
```python
AttributeError: 'NoneType' object has no attribute 'take_damage'
```

**Cause:** Trying to use a component that doesn't exist on entity

**Solution:**
```python
# ❌ Don't do this
health = entity.get_component(HealthComponent)
health.take_damage(10)  # Crashes if no HealthComponent

# ✅ Do this
if entity.has_component(HealthComponent):
    health = entity.get_component(HealthComponent)
    health.take_damage(10)

# ✅ Or this
health = entity.get_component(HealthComponent)
if health:
    health.take_damage(10)
```

### Issue: Serialization Fails

**Symptom:**
```python
KeyError: 'MyComponent'
```

**Cause:** Component not registered in component registry

**Solution:** Add to `COMPONENT_REGISTRY` in save/load system:
```python
COMPONENT_REGISTRY = {
    'PositionComponent': PositionComponent,
    'RenderComponent': RenderComponent,
    'MyComponent': MyComponent,  # ← Add your component
    # ...
}
```

### Issue: System Doesn't Process Entity

**Symptom:** System skips entity silently

**Cause:** Missing required components

**Solution:** Check component requirements:
```python
def process_entity(self, entity):
    # Add debug logging
    required = [PositionComponent, MyComponent]
    for comp_type in required:
        if not entity.has_component(comp_type):
            print(f"Entity {entity.entity_id} missing {comp_type.__name__}")
            return False

    # Process...
```

### Issue: Entities Not Rendering

**Symptom:** Entity exists but doesn't appear

**Possible Causes:**
1. Missing `PositionComponent` or `RenderComponent`
2. `visible` flag set to False
3. `render_order` too low (hidden behind other entities)
4. Position outside camera view

**Solution:**
```python
# Check all requirements
assert entity.has_components(PositionComponent, RenderComponent)

render = entity.get_component(RenderComponent)
assert render.visible is True

pos = entity.get_component(PositionComponent)
print(f"Entity at ({pos.x}, {pos.y})")
```

### Issue: Save/Load Breaks After Adding Component

**Symptom:** Old save files won't load

**Solution:** Handle missing components gracefully:
```python
@classmethod
def from_dict(cls, data, component_registry):
    entity = cls(entity_id=data.get('entity_id'))

    for component_data in data.get('components', {}).values():
        component_type = component_data.get('component_type')

        if component_type not in component_registry:
            print(f"Warning: Unknown component type {component_type}")
            continue  # Skip unknown components

        component_class = component_registry[component_type]
        component = component_class.from_dict(component_data)
        entity.add_component(component)

    return entity
```

---

## Performance Optimization

### Component Queries

**❌ Inefficient:**
```python
# Checks components multiple times
for entity in entities:
    if entity.has_component(PositionComponent):
        pos = entity.get_component(PositionComponent)
        if entity.has_component(RenderComponent):
            render = entity.get_component(RenderComponent)
            # Process...
```

**✅ Efficient:**
```python
# Single check, cache components
for entity in entities:
    if not entity.has_components(PositionComponent, RenderComponent):
        continue

    pos = entity.get_component(PositionComponent)
    render = entity.get_component(RenderComponent)
    # Process...
```

### Entity Filtering

**❌ Inefficient:**
```python
# Filters entire list every frame
enemies = [e for e in entities if e.has_tag('enemy')]
for enemy in enemies:
    ai_system.process(enemy)
```

**✅ Efficient:**
```python
# Maintain separate lists
class EntityManager:
    def __init__(self):
        self.all_entities = []
        self.enemies = []
        self.items = []

    def add_entity(self, entity):
        self.all_entities.append(entity)
        if entity.has_tag('enemy'):
            self.enemies.append(entity)
        elif entity.has_tag('item'):
            self.items.append(entity)

    def remove_entity(self, entity):
        self.all_entities.remove(entity)
        if entity in self.enemies:
            self.enemies.remove(entity)
        elif entity in self.items:
            self.items.remove(entity)

# Use in game loop
for enemy in entity_manager.enemies:
    ai_system.process(enemy)
```

---

## Conclusion

This ECS architecture provides a **flexible, modular foundation** for building complex game systems. By separating data (components) from logic (systems) and using composition over inheritance, the codebase remains maintainable and extensible.

### Key Takeaways:

1. **Components are data** - Keep logic in systems
2. **Entities are containers** - Just IDs and component collections
3. **Systems are processors** - Implement all behavior
4. **Composition over inheritance** - Mix components freely
5. **Check before accessing** - Always verify components exist
6. **Use factory functions** - Create reusable entity templates
7. **Serialize everything** - Enable save/load from the start

### Next Steps:

- Read `docs/DATA_DRIVEN_DESIGN.md` for JSON content management
- Explore `docs/EXTENDING_SYSTEMS.md` for advanced system patterns
- Review `tests/` for comprehensive examples
- Check `config/` for data-driven entity definitions

---

**Happy coding! Build amazing roguelike systems with ECS! 🎮**
