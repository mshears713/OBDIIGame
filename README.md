# Modular Python Roguelike: Exploring Automotive ECU Systems

[![Tests](https://img.shields.io/badge/tests-559%20passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> An educational roguelike game for learning Python game development, procedural generation, and Entity-Component-System (ECS) architecture through the lens of automotive ECU systems.

**Project Status:** ✅ **Stable Release v1.0** - Fully playable with comprehensive documentation

---

## Quick Start

### CLI Version (Original)

```bash
# Clone the repository
git clone <repository-url>
cd OBDIIGame

# Install dependencies
pip install -r requirements.txt

# Run the game (CLI/ASCII version)
python main.py
```

### Pygame GUI Version (New!)

```bash
# Install Pygame (in addition to other dependencies)
pip install pygame

# Run the game with graphical interface
python run_pygame.py

# Run with custom options
python run_pygame.py --width 1920 --height 1080 --tile-size 24

# Run with effects disabled for better performance
python run_pygame.py --no-animations --no-particles
```

The Pygame version includes:
- **Graphical tile-based rendering** with fallback colored sprites
- **Animated tiles** for CAN pathways, sparks, and voltage traps
- **HUD panel** displaying HP, stats, and message log
- **Floating combat text** showing damage numbers
- **Particle effects** for attacks and traps
- **Minimap overlay** showing explored areas
- **Sound effects and ambient audio** (placeholder support)
- **Smooth camera** following the player

See [QUICKSTART.md](QUICKSTART.md) for detailed getting started guide.

---

## Overview

This project is a modular, multi-file Python roguelike game that invites players to explore a fictionalized, dungeon-like representation of a vehicle’s onboard computer system—known as the Engine Control Unit (ECU). Each dungeon floor symbolizes a different automotive subsystem such as the CAN Bus, Fuel Injection, or O2 Sensing, layered with unique hazards, enemies, items, and gameplay mechanics inspired by automotive diagnostic principles. The game employs procedural generation for unpredictable dungeon layouts, turn-based movement, ASCII or lightweight graphical tile rendering, and a component-based architecture designed for future extensibility.

Beyond creating an engaging game, this project is an educational journey aimed at intermediate Python developers eager to enhance their skills in procedural generation algorithms, entity-component design patterns, data-driven content management, and state persistence through file I/O. Over 2-3 weeks, learners will build a solid foundation in game programming fundamentals within a clear, modular codebase, backed by rich inline documentation and interactive teaching aids embedded throughout the development process.

The scope deliberately balances complexity: it includes essential roguelike features like dungeon generation, combat, inventory, and crafting while excluding advanced AI, multiplayer functionalities, or polished graphical interfaces. This approach ensures achievable milestones while providing an in-depth exposure to software architecture and game mechanics relevant to real-world applications.

---

## Teaching Goals

### Learning Goals

- **Implement procedural generation algorithms for tile-based dungeon map creation:** Learn how to algorithmically generate rooms and corridors to create varied dungeons dynamically.
- **Apply component-based entity system design for modular and extensible game architecture:** Understand decoupling game logic into reusable components for ease of maintenance and extension.
- **Develop data-driven content management using JSON or YAML:** Separate game data from code to facilitate dynamic content updates and modding.
- **Practice turn-based game loop programming with user input handling and state updates:** Gain mastery in managing discrete game cycles reacting to player actions.
- **Design file I/O operations for save/load functionality:** Implement persistence to let players save progress and restore game states reliably.

### Technical Goals

- **Create a modular Python codebase structured in multiple files/modules:** Organize code for clarity and scalability.
- **Implement procedural dungeon generation producing tile-based ASCII or lightweight graphical maps:** Build visual dungeon layouts using simple rendering techniques.
- **Develop core turn-based movement, combat mechanics, and inventory management:** Deliver fundamental gameplay loops with interacting systems.
- **Build a save/load system enabling game state persistence and restoration:** Incorporate file serialization and deserialization for game continuity.

### Priority Notes

- Timeframe: 2–3 weeks
- Complexity: Medium, suitable for intermediate Python developers
- Scope: Core roguelike mechanics, procedural generation, turn-based gameplay, basic crafting systems
- Technical focus on modularity, data-driven design, and extensibility
- Avoidance of advanced AI or heavy graphical requirements

---

## Technology Stack

- **Frontend:** CLI + Pygame GUI (Optional)
  - *CLI Version:* Terminal-based ASCII rendering focusing on core mechanics and simplicity
  - *Pygame Version:* Graphical tile-based rendering with animations, particles, and effects
  - *Rationale:* Dual interface allows learning both terminal-based and graphical game development
  - *Alternatives:* Could use `curses` for enhanced CLI or other GUI libraries (e.g., pyglet, arcade)
  - *Learning:* Master both terminal UI and event-driven graphical interfaces

- **Backend:** Python
  - *Rationale:* Python offers clear syntax, strong community support, and wide range of libraries fitting project needs.
  - *Alternatives:* Could use other languages (e.g., JavaScript or C++), but Python strikes optimal balance of accessibility and power.
  - *Learning:* Builds proficiency in Python modular design, file I/O, and game architecture.

- **Storage:** JSON files
  - *Rationale:* JSON is human-readable, easy to parse, and widely supported for data-driven content.
  - *Alternatives:* YAML is also possible, but JSON chosen for simplicity and broad ecosystem.
  - *Learning:* Teaches schema design and configuration management.

- **Special Libraries:** `pytest` for testing
  - *Rationale:* Enables robust automated tests for game components ensuring correctness.
  - *Learning:* Encourages test-driven development practices.

**Framework Rationale:**

This stack was chosen to optimize learning for intermediate developers by focusing on fundamental programming concepts without burdens of complex graphics or networking. Python's modular capabilities and JSON integration provide a clear path to building extensible, maintainable game systems. CLI-driven interaction encourages deep understanding of game loops and state management, while embedded teaching elements support hands-on education.

---

## Architecture Overview

The application follows a modular, component-based entity system (ECS) architecture, separating data from behavior to maximize flexibility and reusability.

- **Entities:** Game objects (player, enemies, items) composed of multiple modular components.
- **Components:** Define discrete behaviors or data, e.g., PositionComponent, RenderComponent, SignalComponent.
- **Systems:** Manage core functionality like rendering, movement, combat, and procedural generation, operating on entities via their components.
- **Data Loader:** JSON-based content loader imports dungeon floor layouts, enemies, items, and crafting recipes into the system.
- **Game Loop:** Turn-based loop cycles through player input, state updates, AI stubs, and rendering.
- **Save/Load:** Serializes current state to disk and restores on load.

### Data Flow

1. **Content Loading:** JSON files parsed -> data models (Floors, Entities, Items)
2. **Entity Creation:** Entities instantiated with relevant components per floor config
3. **Game Play:** Player commands processed -> update entity states
4. **Rendering:** ASCII map and entities drawn on terminal
5. **Save/Load:** Game state serialized/deserialized from JSON or similar formats

```text
+----------------+       +-----------------+       +------------------+
|  JSON Content  |  ---> | Data Models /   |  ---> | Entity & Component|
|  Definitions   |       | Configurations  |       |   Instantiation  |
+----------------+       +-----------------+       +------------------+
                                                             |
                                                             v
+----------------+       +-----------------+       +------------------+
| Input Handling |  <--> | Game Loop &     |  ---> | Rendering System  |
| (Player Cmds)  |       | Core Mechanics  |       | (ASCII Graphics) |
+----------------+       +-----------------+       +------------------+
                                                             |
                                                             v
                                                  +------------------+
                                                  | Save/Load System |
                                                  +------------------+
```

*Key Patterns:*  
- **Entity-Component-System (ECS):** Modular, flexible design over traditional inheritance  
- **Data-Driven Development:** Using JSON for easy modification and extension  
- **Procedural Generation:** Algorithms producing varied content dynamically

---

## Implementation Plan

### Phase 1: Foundations & Setup

**Overview:**  
Establish the foundational project infrastructure, including repository setup, core Python modules, and basic data models essential for later development.

**Steps:**

#### Step 1: Initialize project repository and folder structure

**Description:**  
Create version control repository (e.g., Git) and define folder hierarchy organizing source code, assets, configs, tests, and docs.

**Educational Features to Include:**  
- Inline project structure diagrams  
- Hover tooltips explaining purpose of each folder  
- Example visualizations of repo layout in UI

**Dependencies:** None

**Implementation Notes:**  
Emphasize modularity and clear separation of concerns for future scalability.

---

#### Step 2: Set up basic Python module structure and main entry point

**Description:**  
Establish Python package/modules with an executable main script orchestrating initialization and game start.

**Educational Features to Include:**  
- Inline code comments describing module import patterns  
- Tooltips in IDE preview highlighting main flow  
- Example sequence diagrams for module interaction

**Dependencies:** Step 1

**Implementation Notes:**  
Encourage using `if __name__ == "__main__":` for script entry.

---

#### Step 3: Define Tile and Map data models as Python dataclasses

**Description:**  
Design immutable data models for dungeon Tiles and Map using Python `dataclasses` to reduce boilerplate.

**Educational Features to Include:**  
- Comments explaining benefits of `dataclasses` (auto-generated methods, readability)  
- Tooltip comparison demo: traditional class vs dataclass syntax  
- Interactive examples showing usage

**Dependencies:** Step 2

**Implementation Notes:**  
Highlight immutability and type annotations.

---

#### Step 4: Design Component base class and Entity system framework

**Description:**  
Implement abstract Component base class and Entity management infrastructure laying groundwork for ECS.

**Educational Features to Include:**  
- Inline help section illustrating component-based design pattern  
- Examples of component reuse and modularity  
- Tooltips explaining key design decisions

**Dependencies:** Step 3

**Implementation Notes:**  
Plan for adding/removing components dynamically.

---

#### Step 5: Create basic PositionComponent and RenderComponent

**Description:**  
Develop fundamental components managing spatial location and rendering character representation.

**Educational Features to Include:**  
- Inline comments describing properties and behaviors  
- Visual UI examples showing entity placement and rendering  
- Tooltips explaining coordinates and ASCII chars

**Dependencies:** Step 4

**Implementation Notes:**  
Test rendering accuracy early.

---

#### Step 6: Implement simple ASCII Map Renderer

**Description:**  
Build a renderer that systematically displays map tiles and entities as ASCII characters in terminal.

**Educational Features to Include:**  
- Interactive demo toggling rendering styles  
- Tooltips explaining ASCII mapping choices  
- Inline comments clarifying render loops

**Dependencies:** Steps 3, 5

**Implementation Notes:**  
Consider performance and clarity.

---

#### Step 7: Establish JSON data structure for dungeon floor definitions

**Description:**  
Design JSON schema detailing floor layouts, tile types, parameters, and metadata.

**Educational Features to Include:**  
- Example JSON snippets with annotated keys  
- Tooltip explanations for each field and data type  
- Inline JSON comments illustrating schema

**Dependencies:** Steps 1, 3

**Implementation Notes:**  
Enforce schema consistency for validation.

---

#### Step 8: Implement JSON loader utility functions

**Description:**  
Create utilities to load and parse JSON configurations safely with error handling.

**Educational Features to Include:**  
- Code comments explaining JSON parsing patterns  
- Tooltip walkthrough linking JSON fields to internal data models

**Dependencies:** Step 7

**Implementation Notes:**  
Plan for extensibility to additional JSON content types.

---

#### Step 9: Integrate JSON data loader for floor configuration

**Description:**  
Connect loader utilities with Map model to instantiate dungeon floors dynamically.

**Educational Features to Include:**  
- Inline integration examples with data flow tooltips  
- Mini UI showing loaded JSON preview

**Dependencies:** Steps 6, 8

**Implementation Notes:**  
Test mapping accuracy meticulously.

---

#### Step 10: Document core architecture basics in developer docs

**Description:**  
Produce foundational documentation describing major systems and design rationale.

**Educational Features to Include:**  
- Structured docs with diagrams and expandable sections  
- Inline code samples illustrating relationships  
- Contextual tooltips clarifying terminology

**Dependencies:** All previous steps

**Implementation Notes:**  
Encourage internal documentation best practices.

---

### Phase 2: Core Game Systems Implementation

**Overview:**  
Develop the main game mechanics — dungeon generation, gameplay entities, input handling, combat, and inventory management — along with the central turn-based game loop.

**Steps:**

#### Step 11: Implement procedural dungeon generation - room and corridor layout

**Description:**  
Build algorithms to generate randomized rooms and corridors forming dungeon floors.

**Educational Features to Include:**  
- Detailed commenting on algorithm flow  
- Interactive visualization demo with step toggles  
- Tooltips explaining parameters (room size, corridor length)

**Dependencies:** Step 9

**Implementation Notes:**  
Focus on balanced procedural outputs for gameplay.

---

#### Step 12: Enhance Map class to support procedural dungeon layout

**Description:**  
Extend Map model to represent dynamically generated dungeon structures.

**Educational Features to Include:**  
- Comparison examples: static vs procedural maps  
- Tooltips clarifying new Map methods/properties

**Dependencies:** Step 11

**Implementation Notes:**  
Optimize data representations for performance.

---

#### Step 13: Create Player entity with base components

**Description:**  
Assemble player Entity combining Position, Render, Inventory, and control components.

**Educational Features to Include:**  
- Component responsibility tooltips  
- Code snippets showing entity construction

**Dependencies:** Steps 5, 9

**Implementation Notes:**  
Design flexible player entity for future feature expansions.

---

#### Step 14: Implement turn-based game loop skeleton

**Description:**  
Establish the primary loop controlling game turn progression, input processing, and game state updates.

**Educational Features to Include:**  
- Interactive demos tracking loop phases  
- Tooltips explaining timing and state transition  
- Inline comments illustrating integration with other systems

**Dependencies:** Steps 13, 15

**Implementation Notes:**  
Allow easy insertion of additional game phases later.

---

#### Step 15: Add input handling for movement commands

**Description:**  
Implement command parser recognizing player inputs and translating to movement.

**Educational Features to Include:**  
- UI tooltips describing allowable keys  
- Inline comments on parsing and validation logic  
- Small input testing interface

**Dependencies:** Step 14

**Implementation Notes:**  
Validate input robustness and error feedback.

---

#### Step 16: Implement basic Enemy entity with AI component stub

**Description:**  
Create Enemy entities structured similarly to player with placeholder AI components.

**Educational Features to Include:**  
- Documentation of enemy component design  
- Tooltips clarifying AI stub purposes and extension points

**Dependencies:** Steps 5, 9

**Implementation Notes:**  
Prepare for later AI feature rollout.

---

#### Step 17: Populate dungeon floor with enemies and items from configuration

**Description:**  
Add mechanisms to spawn enemies and items based on JSON floor data.

**Educational Features to Include:**  
- Interactive demos showing data-driven spawning  
- Inline comments exposing spawn logic and JSON mapping

**Dependencies:** Steps 9, 16

**Implementation Notes:**  
Check consistency between JSON definitions and game entities.

---

#### Step 18: Implement simple melee combat system

**Description:**  
Develop fundamental mechanics for turn-based combat between player and enemies.

**Educational Features to Include:**  
- Walkthroughs simulating combat scenarios  
- Tooltips explaining damage calculation, turn resolution

**Dependencies:** Steps 16, 17

**Implementation Notes:**  
Ensure clear feedback for player actions.

---

#### Step 19: Create InventoryComponent and basic item pickup mechanism

**Description:**  
Design inventory system attached to entities and logic for item pickup interacting with inventory.

**Educational Features to Include:**  
- Tooltips for inventory capacity and item types  
- Code comments showing component design  
- Demo showcasing item pickup and inventory state update

**Dependencies:** Step 17

**Implementation Notes:**  
Focus on extendability for diverse item interactions.

---

#### Step 20: Add simple user feedback messages

**Description:**  
Implement a messaging system to provide timely feedback on player actions and events.

**Educational Features to Include:**  
- Tooltip explanations for message types and triggers  
- Log window UI with annotated example messages

**Dependencies:** Steps 14, 18

**Implementation Notes:**  
Ensure messages improve player situational awareness.

---

### Phase 3: Additional Features & Refinements

**Overview:**  
Expand core mechanics with signal-crafting, tile effects, status conditions, and integrate robust save/load functionality.

**Steps:**

#### Step 21: Design data schema for signal-crafting recipes in JSON

**Description:**  
Define JSON structure to represent crafting recipes for signals enabling new gameplay mechanics.

**Educational Features to Include:**  
- Documented JSON schema with tooltips  
- Interactive examples of varied recipes

**Dependencies:** Step 7

**Implementation Notes:**  
Prepare flexible recipe formulation.

---

#### Step 22: Implement SignalComponent for entities

**Description:**  
Build component enabling entities to emit, combine, or process signals as per recipes.

**Educational Features to Include:**  
- Inline comments describing properties and behaviors  
- UI tooltips illustrating component states

**Dependencies:** Step 4

**Implementation Notes:**  
Make component modular for varied usage.

---

#### Step 23: Develop signal-crafting system applying recipes

**Description:**  
Implement logic combining signals to produce new effects in-game.

**Educational Features to Include:**  
- Interactive crafting demos with user experimentation  
- Tooltip explanations of recipe application mechanics

**Dependencies:** Steps 21, 22

**Implementation Notes:**  
Test crafting outcomes for balance.

---

#### Step 24: Extend JSON loader to support modular enemy/item definitions

**Description:**  
Enhance JSON parsing utilities to dynamically load modular enemy and item configurations.

**Educational Features to Include:**  
- Help section showing modular JSON design patterns  
- Inline comments on extensibility points

**Dependencies:** Step 8

**Implementation Notes:**  
Promote content scalability.

---

#### Step 25: Implement tile effects and hazard mechanics

**Description:**  
Create tile types causing various effects or hazards affecting entity health or status.

**Educational Features to Include:**  
- UI tooltips for tile effects  
- Code explanations of effect triggers and responses  
- Visual demos of tile impact

**Dependencies:** Steps 6, 17

**Implementation Notes:**  
Balance gameplay challenge.

---

#### Step 26: Add status effect component for entities

**Description:**  
Design component managing temporary status effects influencing entity capabilities.

**Educational Features to Include:**  
- Inline comments describing lifecycle of effects  
- UI hints showing active effects with descriptions

**Dependencies:** Step 4

**Implementation Notes:**  
Enable stackable or timed effects.

---

#### Step 27: Integrate status effects with combat and movement restrictions

**Description:**  
Modify combat and movement mechanics to account for status effects restrictions and enhancements.

**Educational Features to Include:**  
- Detailed documentation of integration points  
- Interactive scenarios demonstrating effect consequences

**Dependencies:** Steps 18, 26

**Implementation Notes:**  
Ensure seamless user experience.

---

#### Step 28: Implement save/load system for game state persistence

**Description:**  
Implement serialization and deserialization of entire game state, enabling save and restore.

**Educational Features to Include:**  
- Inline comments on serialization design  
- Help section with example save files and tooltips  
- Interactive save/load demo UI

**Dependencies:** Steps 9, 14

**Implementation Notes:**  
Test edge cases rigorously.

---

#### Step 29: Add save/load commands to the game loop

**Description:**  
Integrate save and load commands into input handling and main loop operations.

**Educational Features to Include:**  
- Tooltips explaining commands' usage and limitations  
- Inline code annotations on command parsing and error handling

**Dependencies:** Steps 15, 28

**Implementation Notes:**  
Design for user-friendliness and robustness.

---

#### Step 30: Handle edge cases such as invalid moves, empty inventory, and no signal recipes

**Description:**  
Implement comprehensive input validation, graceful failure handling, and user feedback on common errors and edge cases.

**Educational Features to Include:**  
- Help panel with error examples and explanations  
- UI tooltips clarifying error causes and resolutions  
- Document inline checks in codebase

**Dependencies:** Steps 15, 19, 23

**Implementation Notes:**  
Improve game stability and polish UX.

---

### Phase 4: Polish, Testing & Robustness

**Overview:**  
Enhance reliability by implementing extensive unit tests, input validation, error handling, performance optimization, logging, and code refactoring.

**Steps:**

#### Step 31: Write pytest unit tests for component classes

**Description:**  
Create unit tests verifying functionality and correctness of individual components.

**Educational Features to Include:**  
- Inline comments in tests explaining coverage  
- Documentation of test strategies and example assertions

**Dependencies:** Components implemented in Phase 1-3

**Implementation Notes:**  
Foster test-driven development.

---

#### Step 32: Add tests for procedural dungeon generation outputs

**Description:**  
Test dungeon generation for correctness, completeness, and variety.

**Educational Features to Include:**  
- Comments on expected generation features  
- Example test outputs with explanatory tooltips

**Dependencies:** Step 11

**Implementation Notes:**  
Prevent regressions in procedural code.

---

#### Step 33: Create tests for JSON loading and data validation

**Description:**  
Verify JSON content parsing, schema adherence, and error reporting.

**Educational Features to Include:**  
- Explanations of validation scenarios in tests  
- Interactive schema validation examples

**Dependencies:** Step 8

**Implementation Notes:**  
Maintain content integrity.

---

#### Step 34: Add input sanitization and validation in command parser

**Description:**  
Improve robustness of user input by sanitizing and validating commands.

**Educational Features to Include:**  
- Tooltips explaining validation rules  
- Inline comments showing sanitization steps

**Dependencies:** Step 15

**Implementation Notes:**  
Reduce input errors and crashes.

---

#### Step 35: Enhance error handling for file I/O operations

**Description:**  
Implement comprehensive error management and user feedback for file reading/writing.

**Educational Features to Include:**  
- Error message guides with tooltips  
- Inline code annotations on exception handling

**Dependencies:** Step 28

**Implementation Notes:**  
Improve user experience and reliability.

---

#### Step 36: Optimize map rendering to minimize redundant redraws

**Description:**  
Enhance rendering efficiency by limiting unnecessary redraw operations.

**Educational Features to Include:**  
- Profiling annotations in code  
- Performance demos illustrating gains

**Dependencies:** Step 6

**Implementation Notes:**  
Enhance responsiveness.

---

#### Step 37: Implement basic logging for debugging game events

**Description:**  
Add logging infrastructure to record significant game events for debugging.

**Educational Features to Include:**  
- Help section explaining log usage  
- Annotated example log entries

**Dependencies:** Core game loop operational

**Implementation Notes:**  
Aid in bug diagnostics.

---

#### Step 38: Add boundary and invalid state checks in entity system

**Description:**  
Guard against invalid entity states and out-of-bound positions.

**Educational Features to Include:**  
- Inline comments documenting checks  
- UI tooltips appearing on invalid state detection

**Dependencies:** Steps 4, 5

**Implementation Notes:**  
Prevent runtime errors.

---

#### Step 39: Test save/load with various game states and fix serialization bugs

**Description:**  
Thorough testing of persistence mechanism and correction of serialization issues.

**Educational Features to Include:**  
- Debugging notes in test code  
- Walkthroughs of common bugs  
- Save/load UI status tooltips

**Dependencies:** Step 28

**Implementation Notes:**  
Ensure consistent state restoration.

---

#### Step 40: Refactor code for clarity and modularity based on test feedback

**Description:**  
Improve overall code quality guided by testing results and developer experience.

**Educational Features to Include:**  
- Inline refactoring rationale  
- Before/after code comparisons with tooltips

**Dependencies:** All prior code

**Implementation Notes:**  
Maintain clean, maintainable codebase.

---

### Phase 5: Documentation, Examples & Finalization

**Overview:**  
Complete detailed developer documentation, prepare examples and assets, finalize packaging, and release the project.

**Steps:**

#### Step 41: Write detailed developer guide for entity-component system

**Description:**  
Compose multi-section documentation explaining ECS architecture, design patterns, and usage best practices.

**Educational Features to Include:**  
- Diagrams, code snippets, tooltips reinforcing concepts

**Dependencies:** Step 4

**Implementation Notes:**  
Serve as cornerstone for future extensions.

---

#### Step 42: Document data-driven floor and content design

**Description:**  
Produce comprehensive explanation of JSON-driven content configuration and schemas.

**Educational Features to Include:**  
- Annotated JSON examples with expandable sections  
- Interactive schema explorer

**Dependencies:** Step 7

**Implementation Notes:**  
Facilitate content community contributions.

---

#### Step 43: Add gameplay tutorial example in a sample floor JSON

**Description:**  
Create an embedded tutorial floor guiding players through basic mechanics.

**Educational Features to Include:**  
- Contextual in-app hints and tooltips linked to tutorial

**Dependencies:** Step 9

**Implementation Notes:**  
Enhance new user onboarding.

---

#### Step 44: Prepare placeholder ASCII asset sets and add to assets folder

**Description:**  
Develop simple ASCII art assets for visual consistency and user engagement.

**Educational Features to Include:**  
- Tooltips describing asset usage  
- Interactive ASCII art viewer

**Dependencies:** Step 6

**Implementation Notes:**  
Encourage art experimentation.

---

#### Step 45: Create a quickstart guide for running the game

**Description:**  
Write concise instructions for installing dependencies and launching gameplay.

**Educational Features to Include:**  
- Step-by-step walkthroughs with screenshots  
- Tooltips addressing common setup issues

**Dependencies:** Step 1

**Implementation Notes:**  
Reduce setup friction.

---

#### Step 46: Package requirements and setup files for easy installation

**Description:**  
Prepare `setup.py` or equivalent and dependencies files.

**Educational Features to Include:**  
- Comments explaining setup scripts  
- Help section with installation troubleshooting tips

**Dependencies:** Step 45

**Implementation Notes:**  
Aim for seamless installation experience.

---

#### Step 47: Add developer notes on extending core systems

**Description:**  
Provide guidance and best practices for adding subsystems, entities, or mechanics.

**Educational Features to Include:**  
- Expandable notes with examples and tooltips

**Dependencies:** Step 41

**Implementation Notes:**  
Lower barrier for future contributions.

---

#### Step 48: Perform final manual playtest and fix minor bugs

**Description:**  
Conduct thorough gameplay testing to identify and resolve residual issues.

**Educational Features to Include:**  
- Bug-reporting UI with guidance tooltips  
- Developer notes summarizing fixes applied

**Dependencies:** All phases

**Implementation Notes:**  
Ensure polished final product.

---

#### Step 49: Finalize README with project overview and contribution guidelines

**Description:**  
Complete the main README file with comprehensive descriptions and how to contribute.

**Educational Features to Include:**  
- Anchors and tooltips for navigation  
- Sample contribution workflows

**Dependencies:** Step 1, Step 41

**Implementation Notes:**  
Support community adoption.

---

#### Step 50: Tag final version and prepare repository for handoff

**Description:**  
Create release tags, clean up repository, and prepare for transfer or open-source sharing.

**Educational Features to Include:**  
- Documentation on semantic versioning  
- Tooltips explaining repository hygiene

**Dependencies:** Final release readiness

**Implementation Notes:**  
Facilitate smooth transitions.

---

## Global Teaching Notes

Embed the program itself as a hands-on educational tool by incorporating:

- **Contextual tooltips:** Reveal concepts progressively as users navigate features.
- **Interactive demos:** Visualize algorithms (e.g., dungeon generation), component interactions, and signal crafting.
- **Inline documentation:** Blend teaching commentary with code samples and UI cues.
- **Guided tutorials:** Stepwise walkthroughs connecting JSON data, entity behavior, and gameplay mechanics.
- **Discoverable help and feedback:** Empower users to learn by exploring, supported by rich UI hints.
- **Linking data, code, and runtime:** Visually and interactively demonstrate mapping from configuration to game state.

This approach fosters active learning targeting intermediate programmers eager to deepen mastery in game architecture and procedural systems.

---

## Setup Instructions

1. **Python Version:** Ensure Python 3.8 or higher installed.
2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Currently includes `pytest` only)*
4. **Project Structure Overview:**
   ```
   /project-root
     /src                # Source Python modules
     /assets             # ASCII assets
     /config             # JSON configuration files
     /tests              # Unit tests
     main.py             # Main entry script
     requirements.txt    # Dependency list
     README.md           # Project documentation
   ```
5. **Environment Variables:** None required for initial setup.
6. **Run Game:**
   ```bash
   python main.py
   ```

---

## Development Workflow

- **Phase-by-Phase Approach:**  
  Progress sequentially through phases, mastering foundations before expanding features.
- **Testing Strategy:**  
  Implement unit tests as components develop, focusing on core functionality first, then edge cases.
- **Debugging Tips:**  
  Use logging and error messages embedded in UI; leverage `pytest` for systematic verification.
- **Iteration:**  
  Refactor regularly based on test feedback and gameplay insights; modular design supports parallel development of features.
- **Embedded Learning:**  
  Encourage reading inline documentation and interacting with demos/tooltips for deeper understanding.

---

## Success Metrics

- **Functional Requirements Met:**  
  Procedural dungeon generation, turn-based gameplay, combat, inventory, signal crafting, save/load, modular architecture fully implemented.
- **Learning Objectives Achieved:**  
  Evidence of understanding through documented designs, code modularity, JSON data separation, and test coverage.
- **Quality Criteria:**  
  Stable gameplay with robust input validation, error handling, clear user feedback, and efficient rendering.
- **Testing Completeness:**  
  Comprehensive `pytest` test suite covering critical components, generation, serialization, and input systems.

---

## Next Steps After Completion

- **Extensions or Enhancements:**  
  Add advanced AI behaviors, richer graphical rendering, multiplayer features, or polish GUI using `curses` or other libraries.
- **Related Projects to Try:**  
  Build other roguelike or simulation games focusing on different domains or mechanics.
- **Skills to Practice Next:**  
  Explore network programming, database integration, or UI frameworks to broaden software development expertise.
- **Portfolio Presentation Tips:**  
  Highlight modular architecture and educational approach; include walkthroughs of procedural generation and component system design in demos or write-ups.

---

## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or creating new content, your help is appreciated.

### How to Contribute

1. **Fork the Repository**
   ```bash
   git fork <repository-url>
   git clone <your-fork-url>
   cd OBDIIGame
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make Your Changes**
   - Follow the existing code style (PEP 8)
   - Add tests for new features
   - Update documentation as needed
   - Ensure all tests pass: `pytest tests/`

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

   Use clear, descriptive commit messages:
   - `Add feature: signal decay system`
   - `Fix bug: negative damage calculation`
   - `Update docs: ECS component guide`
   - `Refactor: simplify combat calculation`

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR on GitHub with:
   - Clear description of changes
   - Link to related issues
   - Screenshots/examples if applicable

### Contribution Guidelines

#### Code Standards
- **Python Version:** 3.8+
- **Style:** Follow PEP 8, use type hints
- **Testing:** Write tests for new features (pytest)
- **Documentation:** Add docstrings and inline comments
- **Modularity:** Keep components focused and reusable

#### What to Contribute

**Bug Fixes**
- Check existing issues first
- Include test case reproducing the bug
- Explain the fix in PR description

**New Features**
- Discuss major features in an issue first
- Follow ECS architecture patterns
- Add comprehensive tests
- Update relevant documentation

**Content Creation**
- New floors (JSON in `config/floors/`)
- New enemies (JSON in `config/enemies/`)
- New items (JSON in `config/items/`)
- New crafting recipes (JSON in `config/recipes/`)
- ASCII art assets (TXT in `assets/`)

See [docs/DATA_DRIVEN_DESIGN.md](docs/DATA_DRIVEN_DESIGN.md) for content creation guide.

**Documentation**
- Fix typos and clarify explanations
- Add examples and tutorials
- Improve API documentation
- Translate to other languages

**Testing**
- Add test coverage for untested code
- Create integration tests
- Add edge case tests

#### Development Setup

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run type checking (optional)
mypy src/

# Format code (optional)
black src/ tests/
```

### Community Guidelines

- **Be Respectful:** Treat all contributors with respect
- **Be Constructive:** Provide helpful feedback
- **Be Patient:** Remember everyone is learning
- **Ask Questions:** No question is too small
- **Help Others:** Share your knowledge

### Getting Help

- **Documentation:** Check [docs/](docs/) folder
- **Issues:** Search existing issues or create new one
- **Discussions:** Start a discussion for questions
- **Examples:** See `demo_phase*.py` for code examples

### Content Contribution Examples

**Creating a New Enemy:**
```json
{
  "enemy_id": "memory_leak",
  "name": "Memory Leak",
  "description": "A corrupted process consuming resources",
  "components": {
    "health": {"max_hp": 15, "current_hp": 15},
    "combat": {"damage": 3, "defense": 1},
    "render": {"char": "M", "color": "red"}
  }
}
```

**Creating a New Floor:**
- See [config/floors/floor_0.json](config/floors/floor_0.json) for tutorial example
- See [docs/DATA_DRIVEN_DESIGN.md](docs/DATA_DRIVEN_DESIGN.md) for complete schema

### Recognition

Contributors will be acknowledged in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- Release notes
- Project documentation

---

## Documentation

### For Players
- **[QUICKSTART.md](QUICKSTART.md)** - Get started playing
- **[INSTALL.md](INSTALL.md)** - Detailed installation guide

### For Developers
- **[docs/ECS_DEVELOPER_GUIDE.md](docs/ECS_DEVELOPER_GUIDE.md)** - Entity-Component-System guide
- **[docs/DATA_DRIVEN_DESIGN.md](docs/DATA_DRIVEN_DESIGN.md)** - Content creation guide
- **[docs/EXTENDING_SYSTEMS.md](docs/EXTENDING_SYSTEMS.md)** - System extension guide
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Architecture overview

### Additional Resources
- **Phase Progress Reports:** See `PHASE*_PROGRESS.md` files
- **Test Examples:** See `tests/` directory
- **Demo Scripts:** See `demo_phase*.py` files

---

## Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/components/test_combat.py

# Run with coverage report
pytest tests/ --cov=src --cov-report=term-missing
```

**Test Statistics:**
- 559 passing tests
- Components: 100% covered
- Systems: 100% covered
- Data loaders: 100% covered

---

## Project Structure

```
/OBDIIGame
├── src/                    # Source code
│   ├── components/         # ECS components
│   ├── systems/            # Game systems
│   ├── entities/           # Entity definitions
│   ├── data_loader/        # JSON loaders
│   ├── procedural/         # Dungeon generation
│   ├── models.py           # Core data models
│   └── game_loop.py        # Main game loop
├── config/                 # Game content (JSON)
│   ├── floors/             # Floor definitions
│   ├── enemies/            # Enemy definitions
│   ├── items/              # Item definitions
│   └── recipes/            # Crafting recipes
├── assets/                 # ASCII art assets
│   ├── ui/                 # UI screens
│   ├── characters/         # Character art
│   ├── enemies/            # Enemy art
│   ├── items/              # Item art
│   └── tiles/              # Tile art
├── tests/                  # Test suite
│   ├── components/         # Component tests
│   ├── systems/            # System tests
│   └── data_loader/        # Loader tests
├── docs/                   # Documentation
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── setup.py                # Package configuration
├── pyproject.toml          # Build configuration
└── README.md               # This file
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- **pytest:** MIT License
- **mypy:** MIT License (optional dev dependency)

---

## Acknowledgments

### Educational Inspiration
This project was designed as a comprehensive educational tool for teaching:
- Python software architecture
- Game development fundamentals
- Procedural generation algorithms
- Entity-Component-System patterns
- Data-driven design principles

### Technology Credits
- **Python Community** - For excellent documentation and libraries
- **pytest Team** - For the robust testing framework
- **Roguelike Development Community** - For inspiration and design patterns

### Special Thanks
- All contributors who have helped improve this project
- The open-source community for sharing knowledge and tools
- Educators and students using this project for learning

---

## Changelog

### v1.0.0 (2025-11-18)
- ✅ Complete Entity-Component-System implementation
- ✅ Procedural dungeon generation
- ✅ Turn-based combat system
- ✅ Inventory and crafting systems
- ✅ Save/load functionality
- ✅ Tutorial floor (Floor 0)
- ✅ Comprehensive documentation (325+ pages)
- ✅ 559 passing tests
- ✅ 17 ASCII art assets
- 🐛 Fixed: Tutorial floor naming convention
- 🐛 Fixed: Negative damage calculation bug

See [PHASE5_PROGRESS.md](PHASE5_PROGRESS.md) for detailed development history.

---

## FAQ

**Q: What Python version do I need?**
A: Python 3.8 or higher.

**Q: Can I use this for learning?**
A: Absolutely! This project was specifically designed as an educational tool.

**Q: How do I add new content?**
A: See [docs/DATA_DRIVEN_DESIGN.md](docs/DATA_DRIVEN_DESIGN.md) for detailed guides on creating floors, enemies, items, and recipes.

**Q: Can I use this code in my own project?**
A: Yes! This project is MIT licensed. See [LICENSE](LICENSE) for details.

**Q: How do I report bugs?**
A: Create an issue on GitHub with a clear description and steps to reproduce.

**Q: Can I contribute?**
A: Yes! See the [Contributing](#contributing) section above.

**Q: Where can I find more examples?**
A: Check the `demo_phase*.py` files and the `tests/` directory.

---

## Support

- **Issues:** Report bugs or request features via GitHub Issues
- **Discussions:** Ask questions in GitHub Discussions
- **Documentation:** Comprehensive guides in `docs/` folder
- **Examples:** Working examples in `demo_*.py` and `tests/`

---

## Roadmap

### Future Enhancements (Post v1.0)
- [ ] Advanced AI behaviors and enemy patterns
- [ ] More floor themes and environments
- [ ] Enhanced crafting system with more recipes
- [ ] Status effect system expansion
- [ ] Quest and objective system
- [ ] Achievement system
- [ ] Multiple difficulty modes
- [ ] Enhanced ASCII graphics with colors
- [ ] Sound effects (terminal bell)
- [ ] Mod support and plugin system

### Community Requests
Have an idea? Create an issue with the "enhancement" label!

---

# Thank you for exploring the Modular Python Roguelike project!
Embark on this development journey to sharpen your Python skills and gain a lasting foundation in game system architecture and procedural design. Happy coding!

**Star ⭐ this repository if you find it helpful!**
