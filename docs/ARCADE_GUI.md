# OBD-II Chronicles - Arcade GUI

## Overview

The Arcade GUI is a modern, sprite-based graphical interface for OBD-II Chronicles that layers a polished visual experience over the existing CLI-based roguelike engine. **All core game logic, mechanics, AI, combat, and systems remain unchanged** - the Arcade GUI simply provides a beautiful way to experience the game.

## Features

### Visual Enhancements
- **Sprite-based rendering** - ASCII tiles converted to colorful sprites
- **Smooth camera system** - Follows player with easing and screen shake effects
- **Particle effects** - Voltage arcs, sparks, glitches, smoke, and fire
- **Animated sprites** - Enemies and hazards pulse and flicker with life
- **Dynamic lighting** - Atmospheric glow, shadows, and fog of war
- **Professional HUD** - Health bars, meters, status indicators, and message log

### Audio
- **Sound effects** - Combat, movement, electrical effects
- **Ambient loops** - Subsystem-specific atmospheric audio
- **Theme music** - Immersive background tracks (when assets available)

### Quality of Life
- **Intuitive controls** - WASD/Arrows for movement, clear keybindings
- **Visual feedback** - Effects respond to game events automatically
- **Subsystem transitions** - Smooth scene changes with flavor text
- **Side-by-side compatibility** - CLI and GUI versions coexist peacefully

## Installation

### Requirements
- Python 3.8 or higher
- Arcade 2.6.17 or higher

### Install Arcade

```bash
# Using pip
pip install arcade

# Or install all dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "import arcade; print(f'Arcade {arcade.VERSION} installed successfully!')"
```

## Running the Game

### Arcade GUI (Recommended)

```bash
python run_arcade.py
```

The game will automatically:
1. Check if Arcade is available
2. Launch the GUI if available
3. Fall back to CLI if Arcade is not installed

### Force CLI Mode

```bash
python run_arcade.py --cli
```

### Traditional CLI

```bash
python main.py
```

## Controls

### Movement
- **WASD** or **Arrow Keys** - Move in 4 directions
- **Numpad (1-9)** - Move in 8 directions (diagonal support)

### Actions
- **Space** or **.** (period) - Wait / Skip turn
- **I** - Open inventory
- **G** - Get / Pick up items
- **E** - Use / Equip item
- **R** - Drop item
- **>** - Descend stairs (go deeper)
- **<** - Ascend stairs (go up)

### System
- **Q** or **ESC** - Quit game
- **H** or **?** - Show help

### Combat
- Walk into an enemy to attack (automatic)
- Health bars show damage dealt

## Architecture

### Directory Structure

```
gui/
└── arcade_view/
    ├── __init__.py          # Package initialization
    ├── window.py            # Main GameWindow class
    ├── renderer.py          # Rendering coordinator
    ├── sprites.py           # Sprite management and factory
    ├── camera.py            # Smooth camera with shake
    ├── hud.py               # HUD and UI elements
    ├── effects.py           # Particle effects system
    ├── lighting.py          # Dynamic lighting
    ├── sound.py             # Audio management
    ├── input.py             # Input translation
    ├── scenes.py            # Scene transitions
    ├── assets.py            # Asset loading and caching
    └── config.py            # Configuration constants
```

### Core Design Principles

1. **Non-invasive Integration**
   - Game engine (`src/`) remains completely unchanged
   - No modifications to core game logic
   - GUI is an optional layer on top

2. **Component-based Architecture**
   - Each system (rendering, input, effects) is independent
   - Easy to extend or modify individual components
   - Clear separation of concerns

3. **Turn-based Compatibility**
   - Real-time rendering with turn-based gameplay
   - Input queuing for smooth interaction
   - Visual updates between turns

## Key Components

### GameWindow (window.py)

The main window class that orchestrates everything:
- Inherits from `arcade.Window`
- Manages the game loop
- Coordinates all subsystems
- Bridges Arcade events to game commands

```python
from gui.arcade_view import GameWindow
import arcade

window = GameWindow()
arcade.run()
```

### Renderer (renderer.py)

Coordinates all rendering operations:
- Manages sprite lists (terrain, items, actors, effects)
- Updates camera position
- Triggers particle effects
- Handles visual feedback

### Camera (camera.py)

Smooth camera system:
- Follows player with configurable easing
- Screen shake for impacts and explosions
- Viewport management
- World-to-screen coordinate conversion

### Effects (effects.py)

Particle effect system:
- **Voltage arcs** - Electric blue particles for voltage spikes
- **Sparks** - Yellow-white discharge effects
- **Glitches** - Multicolor digital corruption
- **Smoke/Fire** - Combustion and damage effects
- **Data decode** - Matrix-style green particles
- **Impacts** - Collision and hit effects

### HUD (hud.py)

Professional heads-up display:
- Health bar with color coding (green → yellow → red)
- Inventory status
- Signal/data collection
- Turn counter
- Enemy count
- Message log (last 5 messages)
- Control reminders

### Lighting (lighting.py)

Dynamic lighting system:
- Player flashlight/glow
- Static light sources
- Pulsing lights (for warning indicators)
- Flickering lights (fire, faulty wiring)
- Temporary lights (explosions, sparks)
- Fog of war atmosphere

### Sound (sound.py)

Audio management:
- Lazy loading of sound files
- Volume control (master, SFX, ambient, music)
- Looping ambient sounds
- One-shot sound effects
- Subsystem-themed audio

### Input (input.py)

Input translation layer:
- Converts Arcade keyboard events to game Commands
- Maintains compatibility with existing input system
- Supports multiple control schemes
- Key remapping ready

## Customization

### Configuration

Edit `gui/arcade_view/config.py` to customize:

```python
# Window size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Visual settings
TILE_WIDTH = 32
TILE_HEIGHT = 32
CAMERA_SPEED = 0.1  # Camera smoothing

# Performance
TARGET_FPS = 60

# Colors
COLOR_PLAYER = (100, 200, 255)  # Cyan
COLOR_ENEMY = (255, 100, 100)   # Red
```

### Adding Custom Sprites

1. Create sprite assets (32x32 PNG files)
2. Place in `assets/sprites/` directory
3. Update `assets.py` to load them:

```python
def get_entity_texture(self, entity_name: str):
    texture_path = self.asset_dir / 'sprites' / f'{entity_name}.png'
    if texture_path.exists():
        return arcade.load_texture(str(texture_path))
    # ... fallback to procedural texture
```

### Adding Custom Sounds

1. Add sound files (WAV or OGG) to `assets/sounds/`
2. Use the sound system:

```python
from gui.arcade_view.sound import get_sound_manager, GameSounds

sound_manager = get_sound_manager()
sound_manager.play_sound(GameSounds.SPARK)
sound_manager.play_ambient('ambient_ecu', loop=True)
```

### Creating New Particle Effects

Extend `ParticleEffectManager` in `effects.py`:

```python
def create_custom_effect(self, x: float, y: float):
    emitter = Emitter(
        center_xy=(x, y),
        emit_controller=EmitterIntervalWithTime(0.01, 0.5),
        particle_factory=lambda emitter: FadeParticle(
            filename_or_texture=arcade.make_soft_circle_texture(10, (255, 0, 255)),
            change_xy=(random.uniform(-50, 50), random.uniform(-50, 50)),
            lifetime=random.uniform(0.3, 0.7),
            scale=random.uniform(0.4, 1.0)
        )
    )
    self.emitters.append(emitter)
```

## Performance Optimization

### Spatial Hashing

Sprite lists use spatial hashing for efficient collision detection:

```python
SPRITE_LISTS_ENABLE_SPATIAL_HASH = True
```

### Draw Call Batching

Sprites are batched by texture for efficient rendering:
- All floor tiles in one batch
- All wall tiles in one batch
- Minimizes GPU state changes

### Camera Culling

Only sprites within the viewport are rendered:
- Camera tracks visible bounds
- Off-screen sprites skipped
- Maintains 60 FPS even with large maps

## Troubleshooting

### "Module 'arcade' not found"

```bash
pip install arcade
```

### Low FPS / Performance Issues

1. Reduce particle count in `config.py`:
```python
PARTICLE_COUNT_MEDIUM = 10  # Down from 15
```

2. Disable lighting effects:
```python
# Comment out lighting in renderer.py
# self.light_layer = LightingSystem()
```

3. Reduce screen resolution:
```python
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
```

### Black screen on startup

Check Python version:
```bash
python --version  # Should be 3.8+
```

Update graphics drivers:
- Arcade requires OpenGL 3.3+
- Update GPU drivers if experiencing issues

### Sound not playing

Sounds are optional. If sound files don't exist:
- Game continues without audio
- No errors thrown
- Check console for "Warning: Could not load sound" messages

## Future Enhancements

### Planned Features
- [ ] Mini-map in HUD corner
- [ ] Inventory screen overlay
- [ ] Mouse support for menus
- [ ] Keybinding configuration UI
- [ ] Save/Load game screens
- [ ] Achievement notifications
- [ ] Boss fight animations
- [ ] Parallax background layers

### Asset Creation
- [ ] Custom sprite sheets for enemies
- [ ] Animated tile sets
- [ ] Sound effect library
- [ ] Background music tracks
- [ ] Subsystem-themed tilesets

### Advanced Features
- [ ] Shader effects (CRT, glitch)
- [ ] Weather effects
- [ ] Procedural sprite generation
- [ ] Replay system with recording
- [ ] Level editor mode

## Development Notes

### Testing the GUI

```bash
# Run with verbose output
python run_arcade.py

# Test specific features
python -m pytest tests/test_arcade_gui.py  # If tests exist
```

### Debugging

Enable debug mode in `config.py`:

```python
DEBUG_MODE = True
SHOW_FPS = True
SHOW_SPRITE_HITBOXES = True
```

### Contributing

When adding features:
1. Keep game engine (`src/`) unchanged
2. Add new GUI components in `gui/arcade_view/`
3. Update this documentation
4. Test both CLI and GUI modes
5. Maintain 60 FPS performance target

## Technical Details

### Coordinate Systems

1. **Grid Coordinates** - Game engine uses tile-based grid (e.g., x=10, y=5)
2. **World Coordinates** - Arcade uses pixels (e.g., x=320, y=160)
3. **Screen Coordinates** - Viewport-relative pixels

Conversion:
```python
world_x = grid_x * TILE_WIDTH + TILE_WIDTH / 2
world_y = grid_y * TILE_HEIGHT + TILE_HEIGHT / 2
```

### Update Loop

```
Arcade (60 FPS) ──> on_update() ──> Process pending command
                         │              │
                         │              └──> Game.process_command()
                         │                       │
                         │                       └──> Turn-based logic
                         │
                         └──> Update renderer/camera/effects
                                   │
                                   └──> Create visual feedback
```

### Event Flow

```
Keyboard ──> on_key_press() ──> InputHandler ──> Command
                                                      │
                                                      └──> Queued
                                                            │
                                                            └──> Next update()
```

## Credits

- **Engine**: Original OBD-II Chronicles game engine
- **GUI Framework**: Python Arcade library
- **Design**: Turn-based roguelike with modern graphics

## License

Same license as OBD-II Chronicles project.

## Support

For issues or questions:
1. Check this documentation
2. Review `config.py` for customization options
3. Test CLI mode (`python main.py`) to isolate GUI issues
4. Check Arcade documentation: https://api.arcade.academy/

---

**Enjoy the visual upgrade! The game engine you know, now with the polish you deserve.**
