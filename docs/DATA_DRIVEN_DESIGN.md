# Data-Driven Floor and Content Design Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Configuration Structure](#configuration-structure)
3. [Floor Definitions](#floor-definitions)
4. [Enemy Definitions](#enemy-definitions)
5. [Item Definitions](#item-definitions)
6. [Recipe Definitions](#recipe-definitions)
7. [Creating New Content](#creating-new-content)
8. [Schema Reference](#schema-reference)
9. [Best Practices](#best-practices)
10. [Validation and Testing](#validation-and-testing)

---

## Introduction

### What is Data-Driven Design?

**Data-driven design** separates game **content** (floors, enemies, items) from game **code** (systems, logic). Instead of hardcoding entities in Python, we define them in JSON configuration files that are loaded at runtime.

### Benefits

✅ **Non-programmers can create content** - No Python knowledge required
✅ **Rapid iteration** - Change content without recompiling
✅ **Modding support** - Community can add content
✅ **Version control friendly** - Easy to track content changes
✅ **Reduced bugs** - Content bugs don't affect code
✅ **Easier balancing** - Tweak numbers in JSON files

### How It Works

```
JSON Config File → JSONLoader → FloorBuilder/EntityFactory → Game Objects
```

**Example Flow:**
1. Designer creates `config/enemies/super_goblin.json`
2. Game loads JSON using `JSONLoader`
3. `EntityFactory` converts JSON to Entity with components
4. Entity appears in game with specified stats

---

## Configuration Structure

### Directory Layout

```
config/
├── floors/          # Dungeon floor definitions
│   ├── floor_1.json
│   ├── floor_2.json
│   └── ...
├── enemies/         # Enemy type definitions
│   ├── corrupted_packet.json
│   ├── signal_glitch.json
│   └── ...
├── items/           # Item definitions
│   ├── signal_boost.json
│   ├── diagnostic_tool.json
│   └── ...
└── recipes/         # Crafting recipe definitions
    ├── basic_heal.json
    ├── firewall_shield.json
    └── ...
```

### File Naming Conventions

**✅ Good Names:**
- `floor_1.json` - Numbered floors
- `corrupted_packet.json` - Snake_case, descriptive
- `signal_boost.json` - Clear, concise
- `basic_heal.json` - Indicates difficulty

**❌ Bad Names:**
- `f1.json` - Too abbreviated
- `Corrupted Packet.json` - Spaces in filename
- `newenemy123.json` - Not descriptive
- `test.json` - Too generic

### JSON Conventions

**Comments:**
Use `_comment` fields for documentation (they're stripped during loading):

```json
{
  "_comment": "This is a comment explaining the config",
  "_educational_note": "This field teaches about the design",
  "actual_field": "actual value"
}
```

**Field Ordering:**
1. Comments first
2. Core IDs and names
3. Main configuration
4. Metadata last

---

## Floor Definitions

### Purpose

Floor definitions describe dungeon levels: size, generation parameters, enemy spawns, item spawns, and difficulty.

### Location

`config/floors/*.json`

### Complete Schema

```json
{
  "_comment": "Floor description and purpose",
  "_educational_note": "Teaching notes about this floor",

  "floor_id": 1,
  "name": "Floor Display Name",
  "description": "Flavor text describing this floor",
  "theme": "visual_theme_identifier",

  "dimensions": {
    "_comment": "Map size in tiles",
    "width": 40,
    "height": 25
  },

  "generation": {
    "_comment": "Procedural generation parameters",
    "algorithm": "bsp",
    "room_count_min": 5,
    "room_count_max": 8,
    "room_size_min": 4,
    "room_size_max": 10,
    "corridor_width": 1
  },

  "tile_distribution": {
    "_comment": "Special tile placement percentages (0.0-1.0)",
    "hazard_tiles": 0.03,
    "door_tiles": 0.02
  },

  "enemy_spawns": [
    {
      "_comment": "Enemy spawn definition",
      "enemy_type": "enemy_id_from_enemies_folder",
      "count_min": 3,
      "count_max": 5,
      "spawn_weight": 70
    }
  ],

  "item_spawns": [
    {
      "_comment": "Item spawn definition",
      "item_type": "item_id_from_items_folder",
      "count_min": 1,
      "count_max": 2,
      "spawn_weight": 50
    }
  ],

  "stairs": {
    "_comment": "Stair placement",
    "stairs_down": {
      "enabled": true,
      "placement": "random_room"
    },
    "stairs_up": {
      "enabled": false
    }
  },

  "difficulty": {
    "_comment": "Difficulty modifiers",
    "level": 1,
    "enemy_health_multiplier": 1.0,
    "enemy_damage_multiplier": 1.0
  },

  "metadata": {
    "_comment": "Optional metadata",
    "author": "Designer Name",
    "version": "1.0",
    "tags": ["tutorial", "beginner"]
  }
}
```

### Field Reference

#### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `floor_id` | integer | ✅ | Unique floor identifier (1, 2, 3...) |
| `name` | string | ✅ | Display name shown to player |
| `description` | string | ✅ | Flavor text describing the floor |
| `theme` | string | ✅ | Visual theme identifier |

#### Dimensions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `width` | integer | ✅ | Map width in tiles (20-100 recommended) |
| `height` | integer | ✅ | Map height in tiles (15-50 recommended) |

#### Generation Parameters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `algorithm` | string | `"bsp"` | Generation algorithm ("bsp", "cellular", "rooms") |
| `room_count_min` | integer | `5` | Minimum number of rooms |
| `room_count_max` | integer | `8` | Maximum number of rooms |
| `room_size_min` | integer | `4` | Minimum room dimension |
| `room_size_max` | integer | `10` | Maximum room dimension |
| `corridor_width` | integer | `1` | Corridor width (1-3) |

#### Enemy Spawns

Each enemy spawn entry:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enemy_type` | string | ✅ | Enemy ID from `config/enemies/` |
| `count_min` | integer | ✅ | Minimum spawn count |
| `count_max` | integer | ✅ | Maximum spawn count |
| `spawn_weight` | integer | ✅ | Relative spawn probability (0-100) |

**Spawn Weight Example:**
```json
{
  "enemy_spawns": [
    {"enemy_type": "goblin", "spawn_weight": 70},  // 70% chance
    {"enemy_type": "orc", "spawn_weight": 30}      // 30% chance
  ]
}
```

#### Difficulty

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `level` | integer | `1` | Floor difficulty level |
| `enemy_health_multiplier` | float | `1.0` | Multiply enemy HP (1.0 = normal) |
| `enemy_damage_multiplier` | float | `1.0` | Multiply enemy damage (1.0 = normal) |

**Difficulty Curve Example:**
- Floor 1: `1.0x` HP, `1.0x` damage
- Floor 5: `1.5x` HP, `1.2x` damage
- Floor 10: `2.0x` HP, `1.5x` damage

### Example: Tutorial Floor

```json
{
  "_comment": "Floor 1: Tutorial level with weak enemies",

  "floor_id": 1,
  "name": "CAN Bus Level",
  "description": "Entry point to the ECU system. Weak corrupted packets wander here.",
  "theme": "can_bus",

  "dimensions": {
    "width": 30,
    "height": 20
  },

  "generation": {
    "algorithm": "bsp",
    "room_count_min": 4,
    "room_count_max": 6,
    "room_size_min": 5,
    "room_size_max": 8
  },

  "enemy_spawns": [
    {
      "enemy_type": "corrupted_packet",
      "count_min": 2,
      "count_max": 4,
      "spawn_weight": 100
    }
  ],

  "item_spawns": [
    {
      "item_type": "signal_boost",
      "count_min": 2,
      "count_max": 3,
      "spawn_weight": 100
    }
  ],

  "stairs": {
    "stairs_down": {"enabled": true, "placement": "random_room"},
    "stairs_up": {"enabled": false}
  },

  "difficulty": {
    "level": 1,
    "enemy_health_multiplier": 0.8,
    "enemy_damage_multiplier": 0.8
  },

  "metadata": {
    "author": "Tutorial Designer",
    "tags": ["tutorial", "easy", "starter"]
  }
}
```

### Example: Boss Floor

```json
{
  "_comment": "Floor 10: Boss level with challenging enemies",

  "floor_id": 10,
  "name": "Core Processing Unit",
  "description": "The heart of the ECU. A powerful entity controls this domain.",
  "theme": "cpu_core",

  "dimensions": {
    "width": 50,
    "height": 30
  },

  "generation": {
    "algorithm": "bsp",
    "room_count_min": 8,
    "room_count_max": 12,
    "room_size_min": 6,
    "room_size_max": 12
  },

  "enemy_spawns": [
    {
      "_comment": "Boss enemy - only one spawns",
      "enemy_type": "corrupted_kernel",
      "count_min": 1,
      "count_max": 1,
      "spawn_weight": 20
    },
    {
      "_comment": "Elite guards",
      "enemy_type": "firewall_guardian",
      "count_min": 2,
      "count_max": 4,
      "spawn_weight": 40
    },
    {
      "_comment": "Regular enemies",
      "enemy_type": "data_anomaly",
      "count_min": 5,
      "count_max": 8,
      "spawn_weight": 40
    }
  ],

  "item_spawns": [
    {
      "item_type": "mega_heal",
      "count_min": 1,
      "count_max": 2,
      "spawn_weight": 60
    },
    {
      "item_type": "legendary_signal",
      "count_min": 0,
      "count_max": 1,
      "spawn_weight": 40
    }
  ],

  "difficulty": {
    "level": 10,
    "enemy_health_multiplier": 2.0,
    "enemy_damage_multiplier": 1.5
  },

  "metadata": {
    "author": "Boss Designer",
    "tags": ["boss", "hard", "endgame"]
  }
}
```

---

## Enemy Definitions

### Purpose

Enemy definitions specify NPC stats, behavior, visual appearance, and drops.

### Location

`config/enemies/*.json`

### Complete Schema

```json
{
  "_comment": "Enemy description",

  "enemy_id": "unique_enemy_identifier",
  "name": "Enemy Display Name",
  "description": "Flavor text describing this enemy",

  "visual": {
    "ascii_char": "e",
    "color": "red",
    "render_order": 3
  },

  "components": {
    "_comment": "Component data for entity creation",

    "health": {
      "current_hp": 20,
      "max_hp": 20
    },

    "combat": {
      "damage": 5,
      "defense": 2,
      "attack_range": 1,
      "accuracy": 0.75,
      "crit_chance": 0.1,
      "crit_multiplier": 2.0
    },

    "ai": {
      "behavior": "chase",
      "aggro_range": 5,
      "chase_range": 10,
      "intelligence": "medium"
    }
  },

  "metadata": {
    "difficulty_tier": 2,
    "xp_reward": 10,
    "hp_scaling": 1.2,
    "tags": ["common", "aggressive"],
    "signal_drops": [
      {"signal_type": "corrupted_data", "quantity": 1}
    ]
  }
}
```

### Field Reference

#### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enemy_id` | string | ✅ | Unique identifier (used in floor configs) |
| `name` | string | ✅ | Display name |
| `description` | string | ✅ | Flavor text |

#### Visual

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ascii_char` | string | ✅ | Single ASCII character ('g', 'o', 'D') |
| `color` | string | ✅ | Color name (red, green, blue, etc.) |
| `render_order` | integer | ✅ | Drawing priority (1-10) |

#### Components - Health

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `current_hp` | integer | ✅ | Starting HP |
| `max_hp` | integer | ✅ | Maximum HP |

#### Components - Combat

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `damage` | integer | ✅ | - | Base damage per attack |
| `defense` | integer | ✅ | - | Damage reduction |
| `attack_range` | integer | ✅ | `1` | Attack range (1=melee) |
| `accuracy` | float | ❌ | `0.85` | Hit chance (0.0-1.0) |
| `crit_chance` | float | ❌ | `0.15` | Critical hit chance (0.0-1.0) |
| `crit_multiplier` | float | ❌ | `2.0` | Critical damage multiplier |

#### Components - AI

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `behavior` | string | ✅ | - | AI type: wander, chase, guard, flee, patrol |
| `aggro_range` | integer | ❌ | `5` | Detection range |
| `chase_range` | integer | ❌ | `10` | How far to chase |
| `intelligence` | string | ❌ | `"medium"` | AI quality: low, medium, high |

#### Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `difficulty_tier` | integer | ✅ | Difficulty (1=easy, 5=boss) |
| `xp_reward` | integer | ✅ | Experience points for killing |
| `hp_scaling` | float | ❌ | HP multiplier per floor level |
| `tags` | array | ❌ | Tags for filtering/categorization |
| `signal_drops` | array | ❌ | Signals dropped on death |

### Example: Weak Enemy

```json
{
  "_comment": "Corrupted Packet - Tutorial enemy",

  "enemy_id": "corrupted_packet",
  "name": "Corrupted Data Packet",
  "description": "A damaged data packet wandering aimlessly.",

  "visual": {
    "ascii_char": "p",
    "color": "red",
    "render_order": 3
  },

  "components": {
    "health": {
      "current_hp": 10,
      "max_hp": 10
    },
    "combat": {
      "damage": 2,
      "defense": 0,
      "attack_range": 1
    },
    "ai": {
      "behavior": "wander",
      "aggro_range": 3,
      "intelligence": "low"
    }
  },

  "metadata": {
    "difficulty_tier": 1,
    "xp_reward": 5,
    "hp_scaling": 1.1,
    "tags": ["weak", "common", "tutorial"],
    "signal_drops": [
      {"signal_type": "corrupted_data", "quantity": 1}
    ]
  }
}
```

### Example: Boss Enemy

```json
{
  "_comment": "Corrupted Kernel - Boss enemy",

  "enemy_id": "corrupted_kernel",
  "name": "Corrupted Kernel Process",
  "description": "A powerful entity that has taken control of the system core.",

  "visual": {
    "ascii_char": "K",
    "color": "red",
    "render_order": 8
  },

  "components": {
    "health": {
      "current_hp": 200,
      "max_hp": 200
    },
    "combat": {
      "damage": 20,
      "defense": 10,
      "attack_range": 2,
      "accuracy": 0.9,
      "crit_chance": 0.25,
      "crit_multiplier": 2.5
    },
    "ai": {
      "behavior": "guard",
      "aggro_range": 15,
      "chase_range": 20,
      "intelligence": "high"
    }
  },

  "metadata": {
    "difficulty_tier": 5,
    "xp_reward": 500,
    "hp_scaling": 1.0,
    "tags": ["boss", "unique", "endgame"],
    "signal_drops": [
      {"signal_type": "kernel_signature", "quantity": 1},
      {"signal_type": "power_core", "quantity": 1}
    ]
  }
}
```

### Example: Ranged Enemy

```json
{
  "_comment": "Signal Sniper - Ranged attacker",

  "enemy_id": "signal_sniper",
  "name": "Signal Sniper",
  "description": "Attacks from distance with high-frequency signals.",

  "visual": {
    "ascii_char": "s",
    "color": "cyan",
    "render_order": 4
  },

  "components": {
    "health": {
      "current_hp": 15,
      "max_hp": 15
    },
    "combat": {
      "damage": 8,
      "defense": 1,
      "attack_range": 6,
      "accuracy": 0.7
    },
    "ai": {
      "behavior": "flee",
      "aggro_range": 8,
      "intelligence": "medium"
    }
  },

  "metadata": {
    "difficulty_tier": 2,
    "xp_reward": 15,
    "tags": ["ranged", "tactical"]
  }
}
```

---

## Item Definitions

### Purpose

Item definitions specify consumables, equipment, and their effects.

### Location

`config/items/*.json`

### Complete Schema

```json
{
  "_comment": "Item description",

  "item_id": "unique_item_identifier",
  "name": "Item Display Name",
  "description": "What this item does",

  "visual": {
    "ascii_char": "!",
    "color": "yellow",
    "render_order": 1
  },

  "properties": {
    "item_type": "consumable",
    "stackable": true,
    "max_stack": 5,
    "usable": true
  },

  "effects": {
    "_comment": "Effects when used",
    "on_use": [
      {
        "effect_type": "heal",
        "value": 20,
        "target": "self"
      },
      {
        "effect_type": "message",
        "text": "You feel better!"
      }
    ]
  },

  "signals": {
    "_comment": "Signals contained (for crafting)",
    "healing_data": 1,
    "error_correction": 1
  },

  "metadata": {
    "rarity": "common",
    "value": 10,
    "tags": ["healing", "consumable"]
  }
}
```

### Field Reference

#### Properties

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `item_type` | string | ✅ | Type: consumable, equipment, quest, signal |
| `stackable` | boolean | ✅ | Can multiple stack in one slot? |
| `max_stack` | integer | ✅ | Maximum stack size |
| `usable` | boolean | ✅ | Can be used/consumed? |

#### Effects - On Use

| Effect Type | Parameters | Description |
|-------------|------------|-------------|
| `heal` | `value`, `target` | Restore HP |
| `damage` | `value`, `target` | Deal damage |
| `apply_status` | `status`, `duration` | Apply status effect |
| `message` | `text`, `color` | Show message to player |
| `teleport` | `floor_id` | Teleport to floor |

#### Metadata

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `rarity` | string | common, uncommon, rare, legendary | Rarity tier |
| `value` | integer | - | Gold value |
| `tags` | array | - | Categorization tags |

### Example: Healing Potion

```json
{
  "_comment": "Signal Boost - Basic healing item",

  "item_id": "signal_boost",
  "name": "Signal Boost",
  "description": "Restores system integrity. Heals 20 HP.",

  "visual": {
    "ascii_char": "!",
    "color": "cyan",
    "render_order": 1
  },

  "properties": {
    "item_type": "consumable",
    "stackable": true,
    "max_stack": 5,
    "usable": true
  },

  "effects": {
    "on_use": [
      {
        "effect_type": "heal",
        "value": 20,
        "target": "self"
      },
      {
        "effect_type": "message",
        "text": "The signal boost restores your system integrity."
      }
    ]
  },

  "signals": {
    "error_correction": 1
  },

  "metadata": {
    "rarity": "common",
    "value": 10,
    "tags": ["healing", "consumable", "starter"]
  }
}
```

### Example: Buff Potion

```json
{
  "_comment": "Overclocking Module - Damage buff",

  "item_id": "overclock_module",
  "name": "Overclocking Module",
  "description": "Temporarily increases processing power. +5 damage for 10 turns.",

  "visual": {
    "ascii_char": "*",
    "color": "red",
    "render_order": 1
  },

  "properties": {
    "item_type": "consumable",
    "stackable": true,
    "max_stack": 3,
    "usable": true
  },

  "effects": {
    "on_use": [
      {
        "effect_type": "apply_status",
        "status": "strength",
        "duration": 10,
        "modifier": {"damage": 5}
      },
      {
        "effect_type": "message",
        "text": "Your processing power increases!",
        "color": "red"
      }
    ]
  },

  "metadata": {
    "rarity": "uncommon",
    "value": 50,
    "tags": ["buff", "combat", "temporary"]
  }
}
```

### Example: Equipment

```json
{
  "_comment": "Firewall Protocol - Defensive equipment",

  "item_id": "firewall_protocol",
  "name": "Firewall Protocol",
  "description": "A defensive algorithm that reduces incoming damage. +3 defense.",

  "visual": {
    "ascii_char": "[",
    "color": "blue",
    "render_order": 1
  },

  "properties": {
    "item_type": "equipment",
    "stackable": false,
    "max_stack": 1,
    "usable": false,
    "equipment_slot": "defense"
  },

  "stat_modifiers": {
    "defense": 3,
    "max_hp": 10
  },

  "metadata": {
    "rarity": "rare",
    "value": 150,
    "tags": ["equipment", "defense", "permanent"]
  }
}
```

---

## Recipe Definitions

### Purpose

Recipe definitions specify signal-crafting combinations for creating effects.

### Location

`config/recipes/*.json`

### Complete Schema

```json
{
  "_comment": "Recipe description",
  "_educational_note": "Teaching notes",

  "recipe_id": "unique_recipe_identifier",
  "name": "Recipe Display Name",
  "description": "What this recipe creates",
  "category": "offensive|defensive|utility",

  "inputs": [
    {
      "_comment": "Required signal",
      "signal_type": "signal_name",
      "quantity": 2,
      "consumed": true
    }
  ],

  "outputs": [
    {
      "_comment": "Produced signal/effect",
      "signal_type": "output_signal",
      "quantity": 1,
      "properties": {
        "duration": 0,
        "power": 15
      }
    }
  ],

  "requirements": {
    "_comment": "Unlock requirements",
    "min_floor": 1,
    "special_item": null,
    "skill_check": null
  },

  "effects": {
    "on_craft": [
      {
        "effect_type": "heal",
        "target": "self",
        "value": 15
      }
    ]
  },

  "metadata": {
    "difficulty": "easy",
    "discoverable": true,
    "hint": "Combine sensors with error correction...",
    "tags": ["healing", "starter"]
  }
}
```

### Field Reference

#### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `recipe_id` | string | ✅ | Unique identifier |
| `name` | string | ✅ | Display name |
| `description` | string | ✅ | What it does |
| `category` | string | ✅ | offensive, defensive, utility |

#### Inputs

| Field | Type | Description |
|-------|------|-------------|
| `signal_type` | string | Signal identifier |
| `quantity` | integer | How many required |
| `consumed` | boolean | Is signal used up? |

#### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `signal_type` | string | Produced signal |
| `quantity` | integer | How many produced |
| `properties` | object | Signal properties |

#### Requirements

| Field | Type | Description |
|-------|------|-------------|
| `min_floor` | integer | Minimum floor level |
| `special_item` | string | Required item (or null) |
| `skill_check` | string | Required skill (or null) |

### Example: Healing Recipe

```json
{
  "_comment": "Basic Error Correction - Starter healing recipe",

  "recipe_id": "basic_heal",
  "name": "Error Correction Routine",
  "description": "Combines sensor data with error correction to heal.",
  "category": "defensive",

  "inputs": [
    {
      "signal_type": "sensor_reading",
      "quantity": 2,
      "consumed": true
    },
    {
      "signal_type": "error_correction",
      "quantity": 1,
      "consumed": false
    }
  ],

  "outputs": [
    {
      "signal_type": "healing_pulse",
      "quantity": 1,
      "properties": {
        "duration": 0,
        "power": 15
      }
    }
  ],

  "requirements": {
    "min_floor": 1,
    "special_item": null,
    "skill_check": null
  },

  "effects": {
    "on_craft": [
      {
        "effect_type": "heal",
        "target": "self",
        "value": 15
      },
      {
        "effect_type": "message",
        "text": "Error correction signal synthesized!",
        "color": "green"
      }
    ]
  },

  "metadata": {
    "difficulty": "easy",
    "discoverable": true,
    "hint": "Sensor data can correct system errors...",
    "tags": ["healing", "starter", "tutorial"]
  }
}
```

### Example: Offensive Recipe

```json
{
  "_comment": "Exploit Injection - Attack recipe",

  "recipe_id": "exploit_injection",
  "name": "Exploit Injection",
  "description": "Creates a malicious signal that damages enemies in range.",
  "category": "offensive",

  "inputs": [
    {
      "signal_type": "corrupted_data",
      "quantity": 3,
      "consumed": true
    },
    {
      "signal_type": "malware_signature",
      "quantity": 1,
      "consumed": true
    }
  ],

  "outputs": [
    {
      "signal_type": "exploit_payload",
      "quantity": 1,
      "properties": {
        "damage": 25,
        "aoe_range": 3
      }
    }
  ],

  "requirements": {
    "min_floor": 3,
    "special_item": null,
    "skill_check": null
  },

  "effects": {
    "on_craft": [
      {
        "effect_type": "damage_aoe",
        "target": "enemies",
        "value": 25,
        "range": 3
      },
      {
        "effect_type": "message",
        "text": "Exploit signal deployed!",
        "color": "red"
      }
    ]
  },

  "metadata": {
    "difficulty": "medium",
    "discoverable": true,
    "hint": "Corrupted data can be weaponized...",
    "tags": ["offensive", "aoe", "crafting"]
  }
}
```

---

## Creating New Content

### Workflow

1. **Plan:** Decide what you want to create
2. **Copy:** Use existing file as template
3. **Edit:** Modify fields for your content
4. **Validate:** Check JSON syntax
5. **Test:** Load in game and verify
6. **Balance:** Adjust stats as needed

### Creating a New Enemy

**Step 1:** Copy template
```bash
cp config/enemies/corrupted_packet.json config/enemies/my_enemy.json
```

**Step 2:** Edit fields
```json
{
  "enemy_id": "toxic_slime",
  "name": "Toxic Slime",
  "description": "A gelatinous creature that poisons on hit.",

  "visual": {
    "ascii_char": "s",
    "color": "green",
    "render_order": 3
  },

  "components": {
    "health": {"current_hp": 25, "max_hp": 25},
    "combat": {"damage": 4, "defense": 1, "attack_range": 1},
    "ai": {"behavior": "chase", "aggro_range": 5}
  },

  "metadata": {
    "difficulty_tier": 2,
    "xp_reward": 12,
    "tags": ["poison", "slow"]
  }
}
```

**Step 3:** Add to floor spawn
```json
{
  "enemy_spawns": [
    {
      "enemy_type": "toxic_slime",
      "count_min": 1,
      "count_max": 3,
      "spawn_weight": 50
    }
  ]
}
```

**Step 4:** Test in game
```bash
python main.py
# Navigate to floor with toxic slime
# Verify appearance, stats, behavior
```

### Creating a New Floor

**Step 1:** Copy template
```bash
cp config/floors/floor_1.json config/floors/floor_11.json
```

**Step 2:** Edit core fields
```json
{
  "floor_id": 11,
  "name": "Deep Memory Buffer",
  "description": "A dangerous area filled with memory corruption.",
  "theme": "memory_buffer"
}
```

**Step 3:** Adjust difficulty
```json
{
  "difficulty": {
    "level": 11,
    "enemy_health_multiplier": 2.2,
    "enemy_damage_multiplier": 1.6
  }
}
```

**Step 4:** Configure spawns
```json
{
  "enemy_spawns": [
    {
      "enemy_type": "memory_leak",
      "count_min": 5,
      "count_max": 8,
      "spawn_weight": 60
    },
    {
      "enemy_type": "buffer_overflow",
      "count_min": 2,
      "count_max": 4,
      "spawn_weight": 40
    }
  ]
}
```

### Creating a New Item

**Step 1:** Create file
```bash
touch config/items/mega_heal.json
```

**Step 2:** Define item
```json
{
  "item_id": "mega_heal",
  "name": "Mega Signal Boost",
  "description": "Fully restores system integrity.",

  "visual": {
    "ascii_char": "!",
    "color": "gold",
    "render_order": 1
  },

  "properties": {
    "item_type": "consumable",
    "stackable": true,
    "max_stack": 3,
    "usable": true
  },

  "effects": {
    "on_use": [
      {
        "effect_type": "heal",
        "value": 9999,
        "target": "self"
      }
    ]
  },

  "metadata": {
    "rarity": "rare",
    "value": 200,
    "tags": ["healing", "rare", "emergency"]
  }
}
```

### Creating a New Recipe

**Step 1:** Create file
```bash
touch config/recipes/advanced_shield.json
```

**Step 2:** Define recipe
```json
{
  "recipe_id": "advanced_shield",
  "name": "Advanced Firewall",
  "description": "Creates a powerful defensive barrier.",
  "category": "defensive",

  "inputs": [
    {"signal_type": "firewall_data", "quantity": 2, "consumed": true},
    {"signal_type": "encryption_key", "quantity": 1, "consumed": true}
  ],

  "outputs": [
    {
      "signal_type": "shield_barrier",
      "quantity": 1,
      "properties": {"duration": 5, "absorption": 30}
    }
  ],

  "requirements": {
    "min_floor": 5,
    "special_item": null
  },

  "effects": {
    "on_craft": [
      {
        "effect_type": "apply_status",
        "status": "shield",
        "duration": 5,
        "modifier": {"damage_reduction": 30}
      }
    ]
  },

  "metadata": {
    "difficulty": "hard",
    "discoverable": false,
    "hint": "Encryption strengthens firewalls..."
  }
}
```

---

## Schema Reference

### Color Values

Valid color strings:
- `"white"`, `"black"`, `"gray"`
- `"red"`, `"green"`, `"blue"`
- `"yellow"`, `"cyan"`, `"magenta"`
- `"orange"`, `"purple"`, `"pink"`

### AI Behaviors

| Behavior | Description |
|----------|-------------|
| `wander` | Random movement, attacks if adjacent |
| `chase` | Pursue target when in aggro range |
| `guard` | Stay in area, attack intruders |
| `flee` | Run away from target |
| `patrol` | Follow waypoint route |

### Item Types

| Type | Description |
|------|-------------|
| `consumable` | Single-use items (potions, scrolls) |
| `equipment` | Wearable items (armor, weapons) |
| `quest` | Quest-related items |
| `signal` | Crafting materials |

### Effect Types

| Effect | Parameters | Description |
|--------|------------|-------------|
| `heal` | `value`, `target` | Restore HP |
| `damage` | `value`, `target` | Deal damage |
| `damage_aoe` | `value`, `range`, `target` | Area damage |
| `apply_status` | `status`, `duration`, `modifier` | Apply buff/debuff |
| `remove_status` | `status` | Remove effect |
| `teleport` | `x`, `y` or `floor_id` | Teleport entity |
| `message` | `text`, `color` | Show message |

---

## Best Practices

### 1. Use Descriptive IDs

**✅ Good:**
```json
{
  "enemy_id": "corrupted_kernel_process",
  "item_id": "advanced_firewall_shield",
  "recipe_id": "emergency_system_reboot"
}
```

**❌ Bad:**
```json
{
  "enemy_id": "e1",
  "item_id": "item123",
  "recipe_id": "r_heal"
}
```

### 2. Balance Carefully

**Damage Scaling:**
- Floor 1: 2-5 damage
- Floor 5: 8-15 damage
- Floor 10: 15-30 damage

**Health Scaling:**
- Floor 1: 10-20 HP
- Floor 5: 30-60 HP
- Floor 10: 80-200 HP

**Healing Values:**
- Small: 10-20 HP
- Medium: 30-50 HP
- Large: 60-100 HP
- Full: 9999 HP

### 3. Use Comments Liberally

```json
{
  "_comment": "Boss enemy for floor 10",
  "_design_note": "Intended to be challenging solo encounter",
  "_balance_note": "HP increased from 150 to 200 after playtesting",

  "enemy_id": "boss_corrupted_kernel"
}
```

### 4. Version Your Content

```json
{
  "metadata": {
    "version": "2.1",
    "changelog": [
      "v2.1: Reduced HP from 250 to 200",
      "v2.0: Added ranged attack",
      "v1.0: Initial version"
    ]
  }
}
```

### 5. Tag Appropriately

```json
{
  "metadata": {
    "tags": [
      "boss",           // Entity type
      "fire_theme",     // Visual theme
      "endgame",        // Difficulty
      "unique",         // Rarity
      "aggressive"      // Behavior
    ]
  }
}
```

### 6. Test Iteratively

1. Create content
2. Load in game
3. Test thoroughly
4. Adjust values
5. Repeat

### 7. Document Your Intent

```json
{
  "_comment": "Designed to teach players about ranged combat",
  "_gameplay_intent": "Forces player to close distance or use cover",
  "_difficulty_target": "Should be beatable at level 3 with basic gear"
}
```

---

## Validation and Testing

### JSON Syntax Validation

**Online Tools:**
- https://jsonlint.com/
- https://jsonformatter.org/

**Command Line:**
```bash
# Python built-in
python -m json.tool config/enemies/my_enemy.json

# jq
jq . config/enemies/my_enemy.json
```

### Testing New Content

**1. Syntax Check:**
```python
import json

with open('config/enemies/my_enemy.json') as f:
    try:
        data = json.load(f)
        print("✅ Valid JSON")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
```

**2. Load Test:**
```python
from src.data_loader.json_loader import JSONLoader

loader = JSONLoader()
enemy_data = loader.load_enemy('my_enemy')
print(f"Loaded: {enemy_data['name']}")
```

**3. In-Game Test:**
```bash
python main.py
# Navigate to test floor
# Verify:
# - Enemy appears
# - Stats are correct
# - Behavior works
# - Visual looks good
```

### Common Errors

**Missing Comma:**
```json
{
  "enemy_id": "test"
  "name": "Test Enemy"  // ❌ Missing comma
}
```

**Extra Comma:**
```json
{
  "name": "Test",
  "hp": 10,  // ❌ Trailing comma before }
}
```

**Wrong Quotes:**
```json
{
  'enemy_id': 'test'  // ❌ Use double quotes
}
```

**Invalid Numbers:**
```json
{
  "hp": 10.5  // ✅ Float OK
  "damage": 05  // ❌ No leading zeros
}
```

---

## Advanced Topics

### Dynamic Difficulty

Adjust enemy stats based on floor:

```python
base_hp = enemy_config['components']['health']['max_hp']
floor_multiplier = floor_config['difficulty']['enemy_health_multiplier']
final_hp = int(base_hp * floor_multiplier)
```

### Procedural Variation

Add randomness within ranges:

```json
{
  "components": {
    "health": {
      "max_hp_min": 15,
      "max_hp_max": 25
    }
  }
}
```

### Conditional Spawns

Spawn based on conditions:

```json
{
  "enemy_spawns": [
    {
      "enemy_type": "boss",
      "condition": "player_level >= 10",
      "count_min": 1,
      "count_max": 1
    }
  ]
}
```

---

## Conclusion

Data-driven design empowers **anyone** to create content for the game without touching Python code. By following the schemas and best practices in this guide, you can:

- ✅ Create balanced, engaging enemies
- ✅ Design challenging floor layouts
- ✅ Add useful items and equipment
- ✅ Craft interesting signal recipes
- ✅ Iterate rapidly on game balance
- ✅ Support community modding

### Quick Reference Checklist

When creating new content:

- [ ] Copy appropriate template
- [ ] Use unique, descriptive ID
- [ ] Fill all required fields
- [ ] Add helpful comments
- [ ] Use appropriate tags
- [ ] Balance stats carefully
- [ ] Validate JSON syntax
- [ ] Test in-game
- [ ] Document changes
- [ ] Iterate based on testing

---

**Happy content creation! Build amazing dungeon floors and enemies! 🎮**
