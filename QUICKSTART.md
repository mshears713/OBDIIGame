# Quickstart Guide

## Welcome to ECU Rogue!

This guide will get you playing in under 5 minutes.

**Choose your installation method:**
- **🐳 Docker** (Recommended for Windows/WSL) - No Python installation needed!
- **🐍 Native Python** - Direct installation on your system

---

## 🐳 Docker Installation (Windows/WSL/Linux/macOS)

### Prerequisites

- **Docker Desktop** (Windows/macOS) or **Docker Engine** (Linux/WSL)
  - Windows: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
  - WSL2: [Install Docker in WSL](https://docs.docker.com/desktop/wsl/)
  - Linux: `sudo apt-get install docker.io docker-compose` (Ubuntu/Debian)
  - macOS: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)

### Quick Start with Docker

#### Option 1: Using Docker Compose (Easiest)

```bash
# Clone the repository
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

# Build and run the game
docker-compose up --build

# When done playing, press Ctrl+C to stop
```

#### Option 2: Using Docker CLI

```bash
# Clone the repository
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

# Build the Docker image
docker build -t ecu-rogue .

# Run the game
docker run -it --rm -v ${PWD}/saves:/app/saves ecu-rogue

# For Windows PowerShell, use:
docker run -it --rm -v ${PWD}/saves:/app/saves ecu-rogue

# For Windows CMD, use:
docker run -it --rm -v %cd%/saves:/app/saves ecu-rogue
```

### Docker Tips

**Save Games:** Your progress is automatically saved to the `saves/` folder in your project directory.

**Stop the Game:** Press `Ctrl+C` to exit.

**Rebuild after updates:**
```bash
docker-compose build --no-cache
```

**Remove containers:**
```bash
docker-compose down
```

---

## 🐍 Native Python Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)

### Step 1: Clone or Download

```bash
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
```

Or download and extract the ZIP file.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! The game uses minimal dependencies (only `pytest` for development).

### Step 3: Run the Game

```bash
python main.py
```

---

## Platform-Specific Instructions

### Windows 10/11 (Native)

**Using Docker (Recommended):**
1. Install Docker Desktop for Windows
2. Enable WSL2 integration in Docker Desktop settings
3. Follow Docker installation steps above

**Using Python:**
```powershell
# Install Python from Microsoft Store or python.org
# Open PowerShell
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
pip install -r requirements.txt
python main.py
```

### Windows Subsystem for Linux (WSL)

**Using Docker:**
```bash
# Make sure Docker Desktop is running on Windows
# In WSL terminal:
cd ~
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
docker-compose up --build
```

**Using Python:**
```bash
sudo apt update
sudo apt install python3 python3-pip git
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
pip3 install -r requirements.txt
python3 main.py
```

### Linux (Ubuntu/Debian)

```bash
# Install Docker (optional but recommended)
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Or install Python
sudo apt-get install python3 python3-pip

# Clone and run
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

# With Docker:
docker-compose up --build

# Or with Python:
pip3 install -r requirements.txt
python3 main.py
```

### macOS

```bash
# Install Docker Desktop for Mac (recommended)
# Or install Python via Homebrew:
brew install python3

# Clone and run
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

# With Docker:
docker-compose up --build

# Or with Python:
pip3 install -r requirements.txt
python3 main.py
```

---

### First Time Playing?

1. **Start Tutorial** - Press `[T]` from main menu
2. **Learn the basics** - Movement, combat, items, crafting
3. **Complete tutorial** - Earn starter pack
4. **Begin Floor 1** - Start your adventure!

---

## Quick Controls Reference

### Movement
- **Arrow Keys** or **WASD** - Move in 4 directions
- **Numpad 1-9** - Move in 8 directions (diagonal)
- **5** or **.** - Wait/skip turn

### Actions
- **Space/Enter** - Attack enemy / Interact
- **i** - Inventory
- **c** - Crafting
- **g** - Pick up item
- **>** - Stairs down
- **<** - Stairs up

### Game
- **s** - Save game
- **h** or **?** - Help
- **Esc** - Close menus
- **q** - Quit

---

## Your First 5 Minutes

### 1. Start Tutorial (Recommended)
```
Main Menu → [T] Tutorial
```
- Learn movement, combat, items, crafting
- Safe environment with no death penalty
- Earn useful starter items

### 2. Explore the First Room
- Use **WASD** or **Arrow Keys** to move
- Walk around to see the dungeon layout
- Notice the ASCII graphics: walls (#), floor (.), items (!), enemies (letters)

### 3. Pick Up Your First Item
- Walk onto an item (!)
- Press **g** to pick it up
- Press **i** to see your inventory

### 4. Fight Your First Enemy
- Find a **Training Dummy** (d) or **Minor Glitch** (g)
- Walk into it to attack
- Watch your HP in the status bar
- Keep attacking until defeated

### 5. Use an Item
- Press **i** to open inventory
- Select **Signal Boost**
- Press **u** to use it
- Your HP is restored!

### 6. Craft Your First Signal
- Defeat enemies to collect signals
- Press **c** to open crafting menu
- Select **Error Correction Routine**
- Crafting heals you!

---

## Understanding the HUD

```
╔════════════════════════════╗
║      SYSTEM STATUS         ║
╠════════════════════════════╣
║ HP: [████████░░] 80/100    ║  ← Your health
║ Floor: 1                   ║  ← Current dungeon level
║ XP: 15/50                  ║  ← Experience to next level
╠════════════════════════════╣
║ ATK: 10  DEF: 3            ║  ← Your stats
║ Gold: 25g                  ║  ← Currency
╚════════════════════════════╝
```

---

## Common Symbols

| Symbol | Meaning |
|--------|---------|
| `@` | You (the player) |
| `#` | Wall (blocks movement) |
| `.` | Floor (walkable) |
| `+` | Door |
| `>` | Stairs down |
| `<` | Stairs up |
| `!` | Item / Potion |
| `*` | Signal (crafting material) |
| `[` | Equipment |
| `p` | Corrupted Packet (enemy) |
| `g` | Signal Glitch (enemy) |
| `d` | Training Dummy |

---

## Essential Tips for Beginners

### Combat Tips
✅ **Check enemy HP** - Don't fight multiple enemies at once
✅ **Use healing items** - Press `i` then `u` when low on HP
✅ **Retreat when needed** - It's okay to run away
✅ **Learn attack patterns** - Some enemies chase, others wander

### Survival Tips
✅ **Save often** - Press `s` to save your progress
✅ **Explore thoroughly** - Look for items and secrets
✅ **Manage inventory** - Don't carry useless items
✅ **Read descriptions** - Press `i` to inspect items

### Crafting Tips
✅ **Collect all signals** - Defeat enemies for materials
✅ **Experiment** - Try different signal combinations
✅ **Save reusable signals** - Marked with `*` - very valuable!
✅ **Craft before boss** - Use recipes for buffs and healing

---

## Game Progression

### Floor 1: CAN Bus Level
- **Difficulty:** Easy
- **Enemies:** Corrupted Packets, Signal Glitches
- **Goal:** Learn basic mechanics, reach stairs

### Floor 2-5: Intermediate
- **Difficulty:** Medium
- **Enemies:** Stronger variants, new types
- **Goal:** Build power, collect better equipment

### Floor 6-10: Advanced
- **Difficulty:** Hard
- **Enemies:** Elite enemies, mini-bosses
- **Goal:** Prepare for final boss

### Floor 10: Boss Level
- **Difficulty:** Very Hard
- **Boss:** Corrupted Kernel Process
- **Goal:** Defeat boss, complete game!

---

## Frequently Asked Questions

### How do I heal?

1. **Use Items:** Signal Boost restores 20 HP
2. **Craft Healing:** Error Correction Routine heals 15 HP
3. **Wait:** HP regenerates slowly when not in combat

### How do I get stronger?

1. **Level up:** Defeat enemies for XP
2. **Find equipment:** +Defense and +Attack gear
3. **Craft buffs:** Temporary stat boosts
4. **Upgrade stats:** Choose wisely when leveling

### What if I die?

- You can **load your last save** (press `l` from main menu)
- **Tip:** Save before boss fights and after major progress

### How does crafting work?

1. Press **c** to open crafting menu
2. Select a recipe
3. If you have materials, press **Enter** to craft
4. Recipe effect happens immediately
5. Materials are consumed (except reusable ones marked `*`)

### Where do I find signals?

- **Enemy drops:** Most common source
- **Floor items:** Scattered around dungeon
- **Chests:** Open with `e` key
- **Tutorial rewards:** Complete tutorial for free signals

### Can I change difficulty?

- Not directly, but you can:
  - Do **tutorial** for starter items (easier)
  - Skip **tutorial** for hardcore mode (harder)
  - Save/load to retry difficult sections

---

## Troubleshooting

### Game won't start

```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Try running directly
python main.py
```

### Controls not working

- Make sure you're not in a menu
- Press `Esc` to close menus
- Terminal might need focus (click on it)

### Can't see colors

- Your terminal might not support ANSI colors
- Try a different terminal emulator
- Colors are optional - game works without them

### Save file corrupted

- Look in project folder for `savegame.json`
- Make backup copies regularly
- Delete corrupted save to start fresh

---

## Next Steps

### After Completing Tutorial

1. **Start New Game** - Begin Floor 1
2. **Explore thoroughly** - Find all items
3. **Fight carefully** - Don't rush into danger
4. **Save often** - Use `s` key frequently
5. **Experiment with crafting** - Discover recipes

### Advanced Gameplay

Once comfortable with basics:

- **Try different builds** - Focus on attack, defense, or crafting
- **Speedrun** - Complete game as fast as possible
- **Completionist** - Collect all items and signals
- **Challenge runs** - No healing items, no crafting, etc.

### Modding & Content Creation

Want to create your own content?

1. Read `docs/DATA_DRIVEN_DESIGN.md`
2. Create custom floors in `config/floors/`
3. Design new enemies in `config/enemies/`
4. Add items in `config/items/`
5. Create recipes in `config/recipes/`

---

## Additional Resources

### Documentation
- **README.md** - Full project overview
- **docs/ECS_DEVELOPER_GUIDE.md** - Learn the architecture
- **docs/DATA_DRIVEN_DESIGN.md** - Create content
- **docs/ARCHITECTURE.md** - Technical details

### Development
- **tests/** - Run with `pytest`
- **src/** - Source code
- **config/** - JSON content files

### Community
- Report bugs on GitHub Issues
- Share your custom content
- Suggest features and improvements

---

## Quick Reference Card

### Essential Commands
```
MOVEMENT:  WASD / Arrows    INVENTORY:  i
ATTACK:    Move into enemy  CRAFTING:   c
WAIT:      . or 5           HELP:       h or ?
STAIRS:    > (down) < (up)  SAVE:       s
PICK UP:   g                QUIT:       q (with confirm)
```

### Combat Flow
```
1. Approach enemy
2. Move into enemy to attack
3. Repeat until enemy defeated
4. Collect signal drops
5. Heal if needed (i → u)
```

### Crafting Flow
```
1. Collect signals from enemies
2. Press 'c' for crafting menu
3. Select recipe
4. Check if you have materials
5. Press Enter to craft
6. Effect happens immediately
```

---

## Have Fun!

You're now ready to explore the ECU system and defeat corrupted processes!

**Remember:**
- Save often (`s` key)
- Start with tutorial (`T` from main menu)
- Don't be afraid to retreat from fights
- Experiment with crafting
- Read item descriptions

**Good luck, and enjoy the game!** 🎮

---

*For more detailed information, see the full documentation in the `docs/` folder.*
