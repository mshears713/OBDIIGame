# Edge Case Handling - Step 30 Documentation

## Overview
This document details how edge cases and error conditions are handled throughout the OBDII Game codebase. Step 30 focuses on ensuring robust handling of invalid inputs, empty states, and boundary conditions.

## Input Validation

### Invalid Movement Commands
**Location:** `src/systems/movement.py`
- **Edge Case:** Player attempts to move out of bounds
- **Handling:** `MovementSystem.try_move()` validates coordinates with `map.is_in_bounds()`
- **Result:** Movement rejected, player stays in place, no error message spam

### Invalid Input Commands
**Location:** `src/systems/input_handler.py`
- **Edge Case:** Player enters unrecognized command
- **Handling:** `InputHandler.parse_input()` returns None for invalid commands
- **Result:** Game loop ignores invalid input, prompts for valid command

## Inventory & Signal Management

### Empty Inventory Access
**Location:** `src/components/signal.py`
- **Edge Case:** Attempting to remove signals when inventory is empty
- **Handling:**
  ```python
  def remove_signal(self, signal_type, quantity):
      if signal_type not in self.signals:
          return 0  # Safe return, no crash
  ```
- **Result:** Returns 0 signals removed, no exception

### Insufficient Signals for Crafting
**Location:** `src/systems/crafting.py`
- **Edge Case:** Player attempts to craft without required signals
- **Handling:**
  ```python
  def craft(self, recipe, signal_component, entity):
      if not signal_component.can_afford_recipe(recipe.inputs):
          return False, "Insufficient signals..."
  ```
- **Result:** Craft fails gracefully, clear error message, no partial consumption

### Signal Capacity Limits
**Location:** `src/components/signal.py`
- **Edge Case:** Adding signals beyond capacity limit
- **Handling:**
  ```python
  def add_signal(self, signal_type, quantity):
      max_addable = self.max_per_signal - current_count
      actual_added = min(quantity, max_addable)
      # Only add what fits
  ```
- **Result:** Adds maximum possible, returns actual amount added

## Recipe & Crafting Edge Cases

### Missing Recipe Files
**Location:** `src/systems/crafting.py`
- **Edge Case:** Recipe JSON file not found or malformed
- **Handling:**
  ```python
  try:
      with open(recipe_file, 'r') as f:
          recipe_data = json.load(f)
  except json.JSONDecodeError as e:
      print(f"Warning: Failed to parse recipe {recipe_file}")
      continue  # Skip this recipe, load others
  ```
- **Result:** System continues with valid recipes, logs warning

### No Craftable Recipes
**Location:** `src/systems/crafting.py`
- **Edge Case:** Player has no materials to craft any recipe
- **Handling:** `get_craftable_recipes()` returns empty list
- **Result:** UI shows "No craftable recipes" message (in future UI implementation)

### Recipe Skill Check Failure
**Location:** `src/systems/crafting.py`
- **Edge Case:** Player fails probabilistic skill check
- **Handling:**
  ```python
  if roll > skill_check:
      return False, f"Crafting failed (Required {skill_check}, rolled {roll})"
  ```
- **Result:** No signals consumed on failure (transaction-safe)

## Entity Factory Edge Cases

### Nonexistent Enemy/Item IDs
**Location:** `src/data_loader/entity_factory.py`
- **Edge Case:** Attempting to create entity with invalid ID
- **Handling:**
  ```python
  enemy_data = self.loader.load_enemy(enemy_id)
  if enemy_data is None:
      return None  # Safe None return
  ```
- **Result:** Returns None, caller handles gracefully

### Missing JSON Fields
**Location:** `src/data_loader/entity_factory.py`
- **Edge Case:** Entity JSON missing required fields
- **Handling:** Uses `.get()` with defaults:
  ```python
  name=enemy_data.get("name", "Unknown Enemy")
  char=visual.get("ascii_char", "?")
  ```
- **Result:** Entity created with sensible defaults

## Save/Load Edge Cases

### Save File Not Found
**Location:** `src/systems/save_load.py`
- **Edge Case:** Loading from nonexistent save slot
- **Handling:**
  ```python
  if not save_path.exists():
      print(f"Save file not found: {save_path}")
      return None
  ```
- **Result:** Returns None, caller handles (e.g., show "No save found")

### Corrupted Save Data
**Location:** `src/systems/save_load.py`
- **Edge Case:** Save file has invalid JSON or missing fields
- **Handling:**
  ```python
  try:
      with open(save_path, 'r') as f:
          save_data = json.load(f)
  except Exception as e:
      print(f"Load failed: {e}")
      return None
  ```
- **Result:** Load fails safely, game state unchanged

### Missing Component in Save Data
**Location:** `src/entities/entity.py`
- **Edge Case:** Save data references component type not in registry
- **Handling:**
  ```python
  if component_type_name in component_registry:
      component_class = component_registry[component_type_name]
      component = component_class.from_dict(component_data)
      entity.add_component(component)
  # Silently skip unknown components
  ```
- **Result:** Entity loaded without unknown component, game continues

## Boundary Conditions

### Zero or Negative Values
**Locations:** Multiple components
- **Edge Cases:**
  - Adding zero signals
  - Removing negative quantities
  - Healing zero HP
  - Damage of zero
- **Handling:** All methods check for valid ranges:
  ```python
  if quantity <= 0:
      return 0
  ```
- **Result:** No-op, returns zero, no errors

### Maximum Value Overflow
**Location:** `src/components/health.py`, `src/components/signal.py`
- **Edge Case:** Healing beyond max HP, adding signals beyond limit
- **Handling:**
  ```python
  actual_healing = min(amount, self.max_hp - self.current_hp)
  self.current_hp = min(self.current_hp + amount, self.max_hp)
  ```
- **Result:** Capped at maximum, no overflow

### Empty Collections
**Multiple locations**
- **Edge Cases:**
  - Iterating over empty signal dictionary
  - Processing empty entity list
  - Empty recipe inputs
- **Handling:** Python's iteration safely handles empty collections
- **Result:** Loops execute zero times, no errors

## Data Loading Edge Cases

### Missing Configuration Directories
**Location:** `src/data_loader/json_loader.py`
- **Edge Case:** config/recipes, config/enemies, etc. don't exist
- **Handling:**
  ```python
  if not self.recipes_dir.exists():
      print(f"Warning: Recipes directory not found")
      return  # Continue with empty recipes
  ```
- **Result:** System continues with empty content, logs warning

### Malformed JSON
**Location:** All JSON loading code
- **Edge Case:** Invalid JSON syntax in configuration files
- **Handling:** `try/except json.JSONDecodeError`
- **Result:** File skipped, warning logged, other files processed

### ID Mismatches
**Location:** `src/data_loader/json_loader.py`
- **Edge Case:** File named "floor_1.json" but floor_id is 2
- **Handling:**
  ```python
  if data.get('floor_id') != floor_id:
      logger.warning(f"Floor ID mismatch: expected {floor_id}")
  # Return data anyway, log warning
  ```
- **Result:** Warning logged, data still usable

## Component Edge Cases

### Component Not Present
**Location:** `src/entities/entity.py`
- **Edge Case:** Trying to get component entity doesn't have
- **Handling:**
  ```python
  def get_component(self, component_type):
      return self.components.get(component_name)  # Returns None
  ```
- **Result:** Returns None, caller checks before using

### Duplicate Component Addition
**Location:** `src/entities/entity.py`
- **Edge Case:** Adding same component type twice
- **Handling:** Dictionary overwrites previous:
  ```python
  self.components[component.component_type] = component
  ```
- **Result:** Latest component replaces old one (intended behavior)

## Status Effects Edge Cases

### Effect Duration Edge Cases
**Location:** `src/components/status_effect.py`
- **Edge Cases:**
  - Permanent effects (duration = -1)
  - Instant effects (duration = 0)
  - Effects expiring mid-tick
- **Handling:**
  ```python
  def tick(self):
      if self.duration > 0:
          self.duration -= 1
      return self.duration != 0  # -1 never expires
  ```
- **Result:** Permanent effects never expire, instant effects clean up

### Effect Stacking Limits
**Location:** `src/components/status_effect.py`
- **Edge Case:** Adding effect beyond max stacks
- **Handling:**
  ```python
  if existing.stacks < max_stacks:
      existing.stacks += 1
  # Else don't stack further
  ```
- **Result:** Stacks capped at maximum

## Best Practices Implemented

### 1. Defensive Returns
- Functions return safe default values (None, 0, False, []) rather than raising exceptions
- Callers always check return values

### 2. Transaction Safety
- Crafting is all-or-nothing (validation before consumption)
- Signal transfers are atomic (add to target, then remove from source)

### 3. Clear Error Messages
- User-facing errors are descriptive
- Debug logs provide technical details
- No cryptic error codes

### 4. Graceful Degradation
- Missing content files don't crash the game
- Unknown components skipped during deserialization
- Malformed data logged but doesn't stop loading

### 5. Input Sanitization
- All user input validated before use
- Numeric inputs clamped to valid ranges
- String inputs checked against allowed values

## Testing Coverage

Each edge case has corresponding unit tests in:
- `tests/components/test_signal.py` - Signal edge cases
- `tests/systems/test_crafting.py` - Crafting edge cases
- `tests/data_loader/test_entity_factory.py` - Entity creation edge cases

Example test patterns:
```python
def test_remove_more_than_available(self):
    """Test removing more signals than exist."""
    signals.add_signal("type_a", 5)
    removed = signals.remove_signal("type_a", 10)
    assert removed == 5  # Only removed available
    assert signals.get_signal_count("type_a") == 0

def test_craft_without_signals(self):
    """Test crafting without required signals."""
    success, message = crafting.craft(recipe, empty_signals, entity)
    assert success is False
    assert "Insufficient" in message
```

## Future Enhancements

While current edge case handling is robust, future improvements could include:

1. **User-Facing Error UI**
   - Visual indicators for failed actions
   - Tooltip explanations of why action failed
   - Suggested alternatives

2. **Undo System**
   - Allow reverting accidental actions
   - Especially useful for crafting

3. **Confirmation Dialogs**
   - Confirm destructive actions (delete save, consume rare item)
   - Optional for experienced players

4. **Input Autocomplete**
   - Suggest valid commands
   - Reduce invalid input attempts

5. **Debug Mode**
   - More verbose error logging
   - Stack traces for developers
   - Validation warnings

## Conclusion

Step 30's edge case handling is comprehensively implemented throughout the codebase via:
- Defensive programming practices
- Validation at system boundaries
- Graceful error handling
- Transaction-safe operations
- Clear error feedback
- Extensive test coverage

The game handles edge cases robustly without crashes, data corruption, or poor user experience.
