# Claude AI Agent Guide for Modular Python Roguelike

## Project Overview

This is an educational Python roguelike game where players explore a dungeon-like representation of an automotive ECU (Engine Control Unit). The project is designed to teach intermediate Python developers about:

- Procedural generation algorithms
- Entity-Component-System (ECS) architecture
- Data-driven content management
- Turn-based game loop programming
- Save/load state persistence

**Target Completion:** 2-3 weeks
**Complexity:** Medium (intermediate Python developers)
**Educational Focus:** This project prioritizes learning and code clarity over production optimizations

## Core Architecture

### Entity-Component-System (ECS) Pattern

This project uses ECS architecture for maximum modularity and extensibility:

- **Entities:** Game objects (player, enemies, items) composed of multiple components
- **Components:** Modular units defining behavior/data (e.g., `PositionComponent`, `RenderComponent`, `SignalComponent`)
- **Systems:** Manage functionality (rendering, movement, combat) by operating on entities via components

**Key Principle:** Favor composition over inheritance. Add features by creating new components, not subclassing.

### Data-Driven Design

Game content is defined in JSON files, not hardcoded:
- Dungeon floor configurations (`/config`)
- Enemy definitions
- Item properties
- Crafting recipes

**When modifying gameplay:** Update JSON schemas first, then implement code to consume them.

## Technology Stack

- **Language:** Python 3.8+ (use type hints throughout)
- **Storage:** JSON files for configuration and save states
- **Testing:** `pytest` for all test files
- **UI:** CLI-only with ASCII rendering (no GUI frameworks)
- **Key Patterns:** Dataclasses for models, modular file structure

## Project Structure

```
/project-root
  /src                # All Python source modules
    /components       # Component classes (Position, Render, Inventory, etc.)
    /systems          # Game systems (Renderer, Combat, Movement)
    /entities         # Entity factories and definitions
    /procedural       # Dungeon generation algorithms
  /assets             # ASCII art and visual assets
  /config             # JSON configuration files
    /floors           # Floor definitions
    /enemies          # Enemy configurations
    /items            # Item definitions
    /recipes          # Signal-crafting recipes
  /tests              # pytest unit tests mirroring /src structure
  main.py             # Entry point
  requirements.txt    # Dependencies (currently just pytest)
  README.md           # Comprehensive project documentation
```

## Development Principles

### 1. Educational Code Quality

This project teaches programming concepts, so code must be:

- **Extensively commented:** Explain WHY, not just WHAT
- **Clear over clever:** Readable code > optimized code
- **Progressive complexity:** Build simple foundations first
- **Rich documentation:** Inline tooltips, help sections, examples

**Example of good commenting:**
```python
# Using dataclass to automatically generate __init__, __repr__, etc.
# This reduces boilerplate while maintaining type safety
@dataclass
class PositionComponent:
    x: int
    y: int
```

### 2. Modularity First

- Each module should have a single, clear responsibility
- Components should be reusable across different entity types
- Avoid tight coupling between systems
- Use dependency injection where appropriate

### 3. Test-Driven Development

- Write `pytest` tests as you develop features
- Test component behavior in isolation
- Validate procedural generation outputs
- Test JSON loading and schema validation
- Cover edge cases (invalid input, empty inventory, etc.)

### 4. Type Safety

Use Python type hints consistently:

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Entity:
    components: Dict[str, Component]

    def get_component(self, component_type: str) -> Optional[Component]:
        return self.components.get(component_type)
```

## Key Systems Guide

### Component System

**Location:** `/src/components/`

Components are data containers with minimal logic. When creating new components:

1. Inherit from base `Component` class
2. Use `@dataclass` decorator
3. Add type hints for all fields
4. Include docstring explaining purpose
5. Keep logic minimal—systems handle behavior

**Example:**
```python
from dataclasses import dataclass
from .base import Component

@dataclass
class HealthComponent(Component):
    """Tracks entity health and damage state.

    Used by both player and enemies to manage HP.
    Combat system modifies these values during attacks.
    """
    current_hp: int
    max_hp: int

    def is_alive(self) -> bool:
        return self.current_hp > 0
```

### Procedural Generation

**Location:** `/src/procedural/`

Dungeon generation creates randomized rooms and corridors:

- Use clear, documented algorithms (Binary Space Partitioning, etc.)
- Include visualization/debugging output
- Test for connectivity and playability
- Balance randomness with design constraints

**When modifying generation:**
1. Test outputs extensively
2. Add parameters to JSON configs where possible
3. Document algorithm choices in comments

### Game Loop

**Location:** `/src/game_loop.py` (likely)

Turn-based loop structure:

1. **Input Phase:** Parse player command
2. **Update Phase:** Process command, update game state
3. **AI Phase:** Execute enemy AI (stub for now)
4. **Render Phase:** Draw updated map and entities
5. **Feedback Phase:** Display messages to player

**Critical:** Each phase should be clearly separated for educational clarity.

### Save/Load System

**Location:** `/src/persistence/` (likely)

Serialization requirements:

- Serialize entire game state to JSON
- Handle circular references carefully
- Validate deserialized data
- Test with various game states
- Provide clear error messages on corruption

## Common Development Tasks

### Adding a New Component

1. Create file in `/src/components/new_component.py`
2. Define as `@dataclass` inheriting from `Component`
3. Add type hints and docstrings
4. Register in component factory if needed
5. Write unit tests in `/tests/components/test_new_component.py`
6. Update documentation

### Adding New Enemy Type

1. Define enemy properties in `/config/enemies/new_enemy.json`
2. Specify required components (Position, Render, Health, AI, etc.)
3. Add ASCII representation in `RenderComponent`
4. Configure spawn rules in floor definitions
5. Test spawning and behavior
6. Document in enemy guide

### Creating New Floor

1. Create `/config/floors/floor_N.json`
2. Define floor parameters (size, theme, difficulty)
3. Specify tile types and distribution
4. Configure enemy spawn tables
5. Add item placement rules
6. Test generation and playability

### Implementing New Game Mechanic

1. **Plan:** Break down into component/system responsibilities
2. **Data Schema:** Update JSON schemas if needed
3. **Components:** Create/modify components for new data
4. **Systems:** Implement logic in appropriate system
5. **Integration:** Connect to game loop
6. **Testing:** Write comprehensive tests
7. **Documentation:** Update guides and comments

## Code Style Conventions

### Python Style

- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter default)
- Use snake_case for functions and variables
- Use PascalCase for classes

### Import Organization

```python
# Standard library imports
import json
from typing import List, Dict

# Third-party imports
import pytest

# Local application imports
from src.components.base import Component
from src.entities.player import Player
```

### Documentation Style

Use Google-style docstrings:

```python
def generate_dungeon(width: int, height: int, room_count: int) -> Map:
    """Generate a procedural dungeon with rooms and corridors.

    Args:
        width: Dungeon width in tiles
        height: Dungeon height in tiles
        room_count: Target number of rooms to generate

    Returns:
        Map object containing generated dungeon

    Raises:
        ValueError: If dimensions are too small for room_count
    """
    pass
```

## Testing Guidelines

### Test File Organization

Mirror the `/src` structure in `/tests`:
- `/src/components/health.py` → `/tests/components/test_health.py`

### Test Naming Convention

```python
def test_health_component_initialization():
    """Test HealthComponent creates with correct values."""

def test_health_component_damage_reduces_hp():
    """Test damage application reduces current HP."""

def test_health_component_death_at_zero():
    """Test entity marked dead when HP reaches zero."""
```

### What to Test

- **Component behavior:** Initialization, state changes, edge cases
- **Procedural generation:** Valid outputs, connectivity, constraints
- **JSON loading:** Schema validation, error handling, data integrity
- **Game mechanics:** Combat calculations, movement rules, inventory operations
- **Save/load:** Serialization roundtrip, state preservation
- **Input handling:** Valid commands, invalid input, edge cases

## Automotive/ECU Theme Integration

The game uses automotive ECU concepts as flavor:

- **CAN Bus:** Communication between components (floor theme)
- **Fuel Injection:** Resource management mechanics
- **O2 Sensing:** Environmental hazard monitoring
- **Signal Crafting:** Combine diagnostic signals for effects

**Important:** Theme is educational flavor, not simulation. Prioritize fun gameplay over technical accuracy.

## Phase-Based Development

The README outlines 50 steps across 5 phases. When working on this project:

### Current Phase Awareness

- Check which phase you're in (Foundations, Core Systems, Features, Polish, Documentation)
- Respect dependencies between steps
- Don't jump ahead to advanced features before foundations are solid

### Educational Checkpoints

After each major step, ensure:
- Code is well-documented with teaching comments
- Tests are written and passing
- Examples/demos are included where appropriate
- Documentation is updated

## Common Pitfalls to Avoid

### 1. Over-Engineering Early

- Don't add complex features before basics work
- Start with simple implementations
- Refactor when patterns emerge

### 2. Tight Coupling

- Components shouldn't reference each other directly
- Systems coordinate component interactions
- Use message passing or event systems for communication

### 3. Hardcoded Content

- Game data belongs in JSON, not Python files
- Make systems data-driven from the start
- Facilitate easy content modification

### 4. Insufficient Testing

- Write tests as you develop, not after
- Test edge cases and error conditions
- Validate assumptions about procedural generation

### 5. Poor Error Handling

- Validate user input thoroughly
- Provide clear, helpful error messages
- Handle file I/O errors gracefully
- Never crash without explanation

## JSON Schema Examples

### Floor Definition

```json
{
  "floor_id": 1,
  "name": "CAN Bus Level",
  "theme": "can_bus",
  "dimensions": {"width": 50, "height": 30},
  "room_count": 8,
  "difficulty": 1,
  "enemy_spawns": [
    {"type": "corrupted_packet", "count": 5, "min_level": 1}
  ],
  "items": [
    {"type": "signal_boost", "count": 2}
  ],
  "tile_effects": {
    "hazard_tiles": 0.05
  }
}
```

### Enemy Definition

```json
{
  "enemy_id": "corrupted_packet",
  "name": "Corrupted Data Packet",
  "ascii_char": "P",
  "components": {
    "health": {"current_hp": 10, "max_hp": 10},
    "combat": {"damage": 2, "defense": 1},
    "ai": {"behavior": "patrol", "aggro_range": 5}
  },
  "description": "A damaged data packet wandering the bus."
}
```

## Performance Considerations

While education comes first, avoid obvious inefficiencies:

- **Rendering:** Don't redraw unchanged tiles (Phase 4, Step 36)
- **Entity lookup:** Use dictionaries for O(1) component access
- **Procedural generation:** Cache results where appropriate
- **Save/load:** Don't serialize more than necessary

## Debugging Tips

### Enable Logging

Implement logging early (Phase 4, Step 37):
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Player moved to position: {x}, {y}")
```

### Visualization Helpers

Add debug rendering modes:
- Show component data overlays
- Highlight specific tile types
- Display entity AI state
- Visualize pathfinding

### Test Utilities

Create helper functions for testing:
```python
def create_test_entity(components: Dict[str, Component]) -> Entity:
    """Factory for test entities with specified components."""

def create_test_dungeon(width: int, height: int) -> Map:
    """Generate deterministic dungeon for testing."""
```

## Working with This Project

### When Starting a New Task

1. Read the relevant README section
2. Check phase dependencies
3. Review existing related code
4. Plan component/system responsibilities
5. Write tests first (TDD approach)
6. Implement with extensive comments
7. Validate and document

### When Debugging Issues

1. Check test output first
2. Review relevant JSON schemas
3. Add logging to trace execution
4. Validate component state
5. Test with minimal reproduction case
6. Document the fix

### When Extending Features

1. Ensure core systems are solid
2. Design data schema additions
3. Create new components if needed
4. Implement in appropriate system
5. Write comprehensive tests
6. Update documentation and examples

## Questions to Ask

When uncertain about implementation:

- **Architecture:** Does this belong in a component or system?
- **Data:** Should this be configurable via JSON?
- **Testing:** How do I validate this behavior?
- **Education:** Is this code clear to an intermediate developer?
- **Modularity:** Can this be reused for other features?

## Success Criteria

You're on track if:

- ✅ Code is modular with clear single responsibilities
- ✅ Components are reusable across entity types
- ✅ Game content is data-driven via JSON
- ✅ Tests exist and pass for all features
- ✅ Documentation is extensive and educational
- ✅ Turn-based loop is clean and extensible
- ✅ Save/load preserves game state correctly
- ✅ Input handling is robust with validation
- ✅ Error messages are clear and helpful

## Resources

- **README.md:** Complete project specification with 50 implementation steps
- **Phase Documentation:** Each phase has detailed educational notes
- **Code Comments:** Inline teaching embedded throughout
- **Test Suite:** Examples of proper usage patterns

## Final Notes

Remember: This project's primary goal is **education**. When in doubt:

- **Clarity over cleverness**
- **Documentation over brevity**
- **Modularity over expedience**
- **Testing over "it works on my machine"**

Every line of code is an opportunity to teach. Make it count.
