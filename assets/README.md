# ASCII Art Assets

## Overview

This directory contains ASCII art assets used throughout the game for enhanced visual presentation, title screens, menus, and special effects.

## Directory Structure

```
assets/
├── characters/      # Player and NPC character art
├── enemies/         # Enemy character art and boss portraits
├── items/           # Item icons and descriptions
├── ui/              # User interface elements
├── tiles/           # Special tile patterns and decorations
└── README.md        # This file
```

## Asset Types

### 1. Characters

Player sprites, portraits, and status representations.

### 2. Enemies

Enemy portraits displayed during encounters, boss introduction screens.

### 3. Items

Enhanced item visualizations for inventory screens.

### 4. UI Elements

Title screens, borders, panels, and interface decorations.

### 5. Tiles

Special dungeon tile patterns and environmental art.

## Usage

Assets are loaded as text files and rendered in the terminal. They should:
- Use only ASCII characters (printable characters 32-126)
- Be monospaced-font compatible
- Avoid using tabs (use spaces for alignment)
- Include color codes if needed (ANSI escape codes)

## Creating New Assets

1. Create text file in appropriate subdirectory
2. Use ASCII characters to draw
3. Test in terminal to verify appearance
4. Document dimensions and usage

## Color Codes

Assets can include color using these markers:
- `{RED}text{/}` - Red text
- `{GREEN}text{/}` - Green text
- `{BLUE}text{/}` - Blue text
- `{YELLOW}text{/}` - Yellow text
- `{CYAN}text{/}` - Cyan text
- `{MAGENTA}text{/}` - Magenta text
- `{WHITE}text{/}` - White text

## Guidelines

✅ **Do:**
- Keep designs simple and recognizable
- Test in actual terminal
- Use consistent character widths
- Provide multiple size variations

❌ **Don't:**
- Use special Unicode characters (emoji, box-drawing)
- Exceed 80 character width
- Use tabs for spacing
- Create overly complex designs

---

*All assets are text-based ASCII art for terminal display*
