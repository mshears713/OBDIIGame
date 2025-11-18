# Signal-Crafting Recipe Schema Documentation

## Overview

Signal-crafting is a core mechanic in the OBDII Game where players combine diagnostic signals to create new effects, tools, or abilities. This document defines the JSON schema for crafting recipes.

## Educational Context

In automotive ECU systems, signals are the fundamental units of communication:
- **CAN Bus Signals:** Messages exchanged between vehicle subsystems
- **Diagnostic Trouble Codes (DTCs):** Error signals indicating system faults
- **Sensor Signals:** Real-time data from O2 sensors, MAF sensors, etc.
- **Control Signals:** Commands to actuators, fuel injectors, etc.

Crafting recipes simulate the process of analyzing and combining these signals to understand, diagnose, or manipulate vehicle systems.

## Schema Structure

```json
{
  "recipe_id": "string (unique identifier)",
  "name": "string (human-readable name)",
  "description": "string (what this recipe creates and why)",

  "category": "string (diagnostic|offensive|defensive|utility)",

  "inputs": [
    {
      "signal_type": "string (type of signal required)",
      "quantity": "number (how many of this signal)",
      "consumed": "boolean (whether signal is consumed in crafting)"
    }
  ],

  "outputs": [
    {
      "signal_type": "string (type of signal produced)",
      "quantity": "number (how many produced)",
      "properties": {
        "duration": "number (turns, if temporary)",
        "power": "number (strength/effectiveness)"
      }
    }
  ],

  "requirements": {
    "min_floor": "number (minimum floor level)",
    "special_item": "string|null (special tool required)",
    "skill_check": "number|null (difficulty check 0-100)"
  },

  "effects": {
    "on_craft": [
      {
        "effect_type": "string (type of effect)",
        "parameters": "object (effect-specific params)"
      }
    ]
  },

  "metadata": {
    "difficulty": "string (easy|medium|hard|expert)",
    "discoverable": "boolean (can player find this recipe)",
    "hint": "string (clue for discovering recipe)",
    "tags": ["array", "of", "strings"]
  }
}
```

## Field Descriptions

### Basic Information

- **recipe_id**: Unique identifier for this recipe (kebab-case)
- **name**: Display name shown to player
- **description**: Detailed explanation of what the recipe creates and its purpose
- **category**: Recipe category:
  - `diagnostic`: Reveals information about enemies or environment
  - `offensive`: Creates attack signals or damage effects
  - `defensive`: Protective signals or healing
  - `utility`: Movement, detection, or other non-combat effects

### Inputs Array

Defines what signals/items are required:
- **signal_type**: Type identifier matching SignalComponent types
- **quantity**: Number of this signal required (default: 1)
- **consumed**: Whether the signal is used up (true) or reusable (false)

### Outputs Array

Defines what the recipe produces:
- **signal_type**: Type of signal created
- **quantity**: Number produced
- **properties**: Signal-specific attributes
  - **duration**: How many turns the signal lasts (0 = permanent)
  - **power**: Signal strength/effectiveness

### Requirements Object

Prerequisites for using this recipe:
- **min_floor**: Minimum dungeon floor level (1-based)
- **special_item**: Item_id of required tool, or null
- **skill_check**: Random chance roll (0-100), or null for guaranteed success

### Effects Object

Actions triggered when recipe is crafted:
- **on_craft**: Array of effect objects applied immediately
  - Common effect types: `damage`, `heal`, `status`, `spawn`, `reveal`, `message`

### Metadata Object

Recipe discovery and classification:
- **difficulty**: Player-facing difficulty indicator
- **discoverable**: Whether recipe can be found in-game vs pre-known
- **hint**: Clue text shown when player finds partial information
- **tags**: Searchable/filterable keywords

## Signal Types Reference

### Diagnostic Signals
- `dtc_code`: Diagnostic Trouble Code fragments
- `sensor_reading`: Raw sensor data
- `ecu_query`: System interrogation signal

### Attack Signals
- `corrupted_packet`: Malformed data causing damage
- `denial_signal`: Blocks or disrupts enemy signals
- `overload_pulse`: High-intensity burst

### Defensive Signals
- `error_correction`: Repairs corrupted data
- `firewall_rule`: Blocks incoming attacks
- `backup_signal`: System restoration

### Utility Signals
- `scanner_pulse`: Reveals hidden information
- `bridge_signal`: Connects disconnected systems
- `stealth_mode`: Reduces enemy detection

## Example Recipes

See individual JSON files in this directory:
- `basic_heal.json`: Simple healing recipe
- `diagnostic_scan.json`: Enemy analysis
- `firewall_shield.json`: Defensive barrier
- `exploit_injection.json`: Advanced attack

## Extending the System

To add new signal types:
1. Define signal properties in SignalComponent
2. Create recipes using the new signal type
3. Implement signal behavior in crafting system
4. Add to this reference documentation

## Design Philosophy

Recipes should:
- Reflect automotive diagnostic concepts when possible
- Balance accessibility (easy recipes) with depth (complex combinations)
- Reward exploration and experimentation
- Provide clear educational value about ECU systems
