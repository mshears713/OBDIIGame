# Pygame GUI Documentation

This document describes the Pygame-based graphical user interface for OBD-II Chronicles.

## Overview

The Pygame GUI is a complete graphical interface built on top of the existing game engine. It preserves all game logic, mechanics, and systems while replacing the ASCII terminal renderer with a modern tile-based graphical display.

**Key Design Principle:** The GUI is a pure presentation layer. All game logic remains in the core engine, ensuring the CLI and GUI versions play identically.

---

## Installation

### Requirements

- Python 3.8 or higher
- Pygame 2.0 or higher

### Installation Steps

```bash
# Install Pygame
pip install pygame

# Or install all requirements including Pygame
pip install -r requirements.txt pygame
```

---

## Running the Game

### Basic Usage

```bash
# Run with default settings
python run_pygame.py
```

### Command-Line Options

```bash
# Display settings
python run_pygame.py --width 1920 --height 1080  # Custom window size
python run_pygame.py --tile-size 24              # Larger tiles
python run_pygame.py --fps 30                    # Lower framerate
python run_pygame.py --fullscreen                # Fullscreen mode

# Feature toggles (improve performance)
python run_pygame.py --no-animations    # Disable tile animations
python run_pygame.py --no-particles     # Disable particle effects
python run_pygame.py --no-sound         # Disable audio
python run_pygame.py --no-minimap       # Disable minimap
python run_pygame.py --no-float-text    # Disable floating text

# Audio settings
python run_pygame.py --music-volume 0.5  # Adjust music volume
python run_pygame.py --sfx-volume 0.7    # Adjust sound effects volume
```

### Full Options List

```
usage: run_pygame.py [options]

Options:
  --width WIDTH         Window width in pixels (default: 1280)
  --height HEIGHT       Window height in pixels (default: 720)
  --tile-size SIZE      Tile size in pixels (default: 16)
  --fps FPS             Target frames per second (default: 60)
  --fullscreen          Run in fullscreen mode
  --no-animations       Disable tile animations
  --no-particles        Disable particle effects
  --no-sound            Disable sound and music
  --no-minimap          Disable minimap overlay
  --no-float-text       Disable floating combat text
  --music-volume VOL    Music volume 0.0-1.0 (default: 0.3)
  --sfx-volume VOL      SFX volume 0.0-1.0 (default: 0.5)
```

---

## Features

### 1. Tile-Based Rendering

The game world is rendered using tiles instead of ASCII characters:

- **Fallback Rendering:** When sprite images aren't available, colored rectangles with ASCII characters are rendered
- **Sprite Support:** The system can load `.png` sprite images from `assets/sprites/`
- **Color Mapping:** Each tile type has a default color (walls, floors, doors, etc.)

**Sprite Naming Convention:**
```
assets/sprites/[char]_[color].png

Examples:
  #_gray.png      - Wall sprite
  ._dark_gray.png - Floor sprite
  @_white.png     - Player sprite
```

### 2. Animated Tiles

Special tiles have animated effects:

| Tile | Character | Animation |
|------|-----------|-----------|
| CAN Pathway | `~` | Pulsing blue glow |
| Spark/Trap | `*` | Flickering yellow/orange |
| Voltage Trap | `^` | Electric arc effect |
| Water/Coolant | `≈` | Flowing wave pattern |
| Power Source | `☼` | Glowing pulse |

**Animation Frame Rate:** 0.3 seconds per frame (configurable in `config.py`)

### 3. HUD Panel

A side panel displays:

- **Player Name:** Character name
- **HP Bar:** Health with warning blink at 30%
- **Message Log:** Last 10 game messages with text wrapping
- **Stats:** (Extensible - fuel, voltage, signals can be added)

**HUD Layout:**
```
┌─────────────────────────┐
│ Player Name             │
│                         │
│ HP: 50/100             │
│ ████████░░░░░░░░        │
│                         │
│ Messages:               │
│ - You attack the enemy  │
│ - Enemy takes 10 damage │
│ - Enemy attacks you     │
│ ...                     │
└─────────────────────────┘
```

### 4. Floating Combat Text

When damage occurs:

- Numbers float upward from the target
- Fade out over 0.8 seconds
- Red color for damage dealt
- Automatically spawned on successful attacks

**Example:**
```
     -15
    -10  ← Fading text
   -5    ← Rising animation
  Enemy
```

### 5. Particle System

Visual effects for:

- **Hit Effects:** Red/orange/yellow particles on successful attacks
- **Trap Activation:** Sparks when voltage traps trigger
- **Custom Effects:** Extensible system for any particle type

**Particle Properties:**
- Random velocity vectors
- Alpha fade over lifetime
- Configurable size and color
- Physics-based movement

### 6. Minimap

A small overview map in the bottom-left corner:

- **Explored Tiles:** Shows areas you've discovered
- **Player Marker:** White square showing your position
- **Tile Colors:**
  - Gray: Walls
  - Dark Gray: Floors
  - White: Player
- **Transparency:** 180/255 alpha for non-intrusive display

**Size:** 4 pixels per map tile (configurable)

### 7. Sound System

Audio support includes:

- **Background Music:** Ambient loops (`.ogg`, `.mp3`, `.wav`)
- **Sound Effects:**
  - `attack.ogg` - Combat sounds
  - `step.ogg` - Movement sounds
  - `blocked.ogg` - Blocked movement
- **Volume Control:** Separate music and SFX volumes

**Asset Locations:**
```
assets/
  music/
    ambient.ogg
  sounds/
    attack.ogg
    step.ogg
    blocked.ogg
```

**Note:** Sound files are optional. The game runs without them.

### 8. Camera System

The viewport follows the player:

- **Centered View:** Player stays in the center of the screen
- **Boundary Clamping:** Camera doesn't scroll past map edges
- **Smooth Tracking:** Updates every frame

### 9. Input Handling

Multiple control schemes supported:

| Action | Keys |
|--------|------|
| Move Up | `W`, `↑`, `K`, `Numpad 8` |
| Move Down | `S`, `↓`, `J`, `Numpad 2` |
| Move Left | `A`, `←`, `H`, `Numpad 4` |
| Move Right | `D`, `→`, `L`, `Numpad 6` |
| Move Up-Left | `Q`, `Y`, `Numpad 7` |
| Move Up-Right | `E`, `U`, `Numpad 9` |
| Move Down-Left | `Z`, `B`, `Numpad 1` |
| Move Down-Right | `C`, `N`, `Numpad 3` |
| Wait/Rest | `Space`, `.`, `Numpad 5` |
| Quit | `ESC`, `Ctrl+Q` |

---

## Architecture

### Directory Structure

```
gui/
  pygame_view/
    __init__.py         - Package exports
    config.py           - Configuration constants
    assets.py           - Asset loading and management
    input.py            - Pygame input handling
    renderer.py         - Main rendering system
    window.py           - Game window and main loop
    animations.py       - Tile animation system
```

### Core Components

#### 1. `config.py` - Configuration

Contains all constants:
- Display settings (tile size, window dimensions)
- Color palette
- Animation timings
- HUD layout
- Audio volumes

#### 2. `assets.py` - Asset Manager

Handles loading and caching:
- Sprites (images)
- Sounds (audio files)
- Fonts (text rendering)
- Animations (sprite sequences)

**Key Methods:**
```python
get_tile_sprite(char, color)  # Load or create tile sprite
load_sound(name)              # Load sound effect
create_text_surface(text)     # Render text
```

#### 3. `input.py` - Input Handler

Converts Pygame events to game commands:
- Maps keyboard events to `Action` enum
- Supports multiple key layouts (WASD, Vi, arrows)
- Future-proof for mouse input

#### 4. `renderer.py` - Main Renderer

Renders all visual elements:
- Map tiles (with animation support)
- Entities (player, enemies, items)
- HUD panel
- Minimap
- Floating text
- Particles

**Rendering Pipeline:**
1. Clear screen
2. Update camera position
3. Render map tiles
4. Render entities (sorted by render order)
5. Render particles
6. Render floating text
7. Render HUD
8. Render minimap
9. Update display

#### 5. `window.py` - Game Window

Main game loop integration:
- Initializes Pygame
- Creates game engine instance
- Runs event loop
- Processes commands
- Updates renderer
- Manages FPS

**Game Loop:**
```python
while running:
    # Handle input events
    for event in pygame.event.get():
        command = input_handler.handle_event(event)
        if command:
            process_command(command)

    # Render frame
    renderer.render(map, entities, player, messages, dt)

    # Update display
    pygame.display.flip()

    # Control framerate
    dt = clock.tick(fps) / 1000.0
```

#### 6. `animations.py` - Animation Manager

Manages animated tiles:
- Generates animation frames
- Tracks current frame indices
- Provides frame lookup by character

**Animation Types:**
- Pulse (glowing effect)
- Flicker (random intensity)
- Electric (lightning bolts)
- Flow (wave patterns)
- Glow (radial fade)

---

## Extending the GUI

### Adding New Sprites

1. Create PNG image (16x16 pixels recommended)
2. Save to `assets/sprites/[char]_[color].png`
3. System automatically loads on demand

Example:
```
assets/sprites/@_white.png  # Player sprite
assets/sprites/E_red.png    # Enemy sprite
```

### Adding New Animations

Edit `gui/pygame_view/animations.py`:

```python
# Add character to ANIMATED_TILES
ANIMATED_TILES = {
    '~': 'can_pathway',
    '*': 'spark',
    '&': 'my_new_animation',  # Add this
}

# Create animation in _generate_animations()
self.animation_frames['my_new_animation'] = self._create_pulse_animation(
    base_char='&',
    colors=[(255, 0, 0), (200, 0, 0)],
    frame_count=2
)
```

### Adding New Sound Effects

1. Add sound file to `assets/sounds/`
2. Play in `window.py`:

```python
if self.config.enable_sound:
    self.asset_manager.play_sound("my_sound", self.config.sfx_volume)
```

### Adding New HUD Elements

Edit `_render_hud()` in `gui/pygame_view/renderer.py`:

```python
# Add after existing stats
y_offset = self._draw_stat_bar(
    hud_x + 20, y_offset, width,
    "Fuel", current_fuel, max_fuel,
    FUEL_BAR_COLOR, FUEL_BAR_BG_COLOR
)
```

### Adding New Particle Effects

Call `renderer.add_particle()`:

```python
renderer.add_particle(
    x=tile_x,
    y=tile_y,
    vx=velocity_x,
    vy=velocity_y,
    color=(255, 100, 0),
    size=5,
    lifetime=1.0
)
```

---

## Performance Optimization

### Low-End Systems

```bash
# Minimal settings for best performance
python run_pygame.py \
  --tile-size 16 \
  --fps 30 \
  --no-animations \
  --no-particles \
  --no-sound
```

### High-End Systems

```bash
# Maximum quality settings
python run_pygame.py \
  --width 1920 \
  --height 1080 \
  --tile-size 24 \
  --fps 60
```

### Profiling

To identify performance bottlenecks:

```python
# Add to window.py
import cProfile
cProfile.run('window.run_loop()', 'pygame_profile.stats')
```

---

## Troubleshooting

### Issue: Window doesn't open

**Solution:** Check Pygame installation:
```bash
python -c "import pygame; print(pygame.ver)"
```

### Issue: No sound

**Possible causes:**
1. Sound files missing in `assets/sounds/`
2. Pygame mixer not initialized
3. `--no-sound` flag enabled

**Solution:**
- Ensure sound files exist
- Check Pygame mixer: `pygame.mixer.get_init()`

### Issue: Poor performance

**Solutions:**
1. Reduce window size: `--width 800 --height 600`
2. Disable effects: `--no-animations --no-particles`
3. Lower FPS: `--fps 30`
4. Reduce tile size: `--tile-size 12`

### Issue: Text is too small

**Solution:**
Increase tile size and window size proportionally:
```bash
python run_pygame.py --tile-size 24 --width 1600 --height 900
```

---

## Differences from CLI Version

| Feature | CLI Version | Pygame Version |
|---------|-------------|----------------|
| Rendering | ASCII text | Tiles + sprites |
| Input | Line-based | Event-driven |
| Animation | None | Tile animations |
| Effects | None | Particles, floating text |
| Audio | None | Music + SFX |
| HUD | Inline text | Graphical panel |
| Map View | Fixed size | Scrolling viewport |
| Performance | Instant | 60 FPS target |

**Important:** Game mechanics are identical. The Pygame version is purely a visual upgrade.

---

## Future Enhancements

Potential additions:

- [ ] Mouse support (click to move, click to attack)
- [ ] Sprite sheets for more complex animations
- [ ] Inventory UI panel
- [ ] Character customization screen
- [ ] Tile lighting effects
- [ ] Screen shake on damage
- [ ] Improved particle variety
- [ ] More sound effects
- [ ] UI skins/themes
- [ ] Accessibility options (colorblind modes, high contrast)

---

## License

The Pygame GUI follows the same license as the main project (MIT License).

---

## Credits

- **Game Engine:** OBD-II Chronicles core team
- **Pygame GUI:** Built as a demonstration of modular architecture
- **Pygame Library:** [pygame.org](https://www.pygame.org)

---

## Support

For issues or questions about the Pygame GUI:

1. Check this documentation
2. Review `gui/pygame_view/` source code (heavily commented)
3. File an issue on the project repository

---

**Happy gaming! 🚗💻🎮**
