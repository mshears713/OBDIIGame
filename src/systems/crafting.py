"""
Signal Crafting System - Combines signals to create powerful effects

This system manages the signal-crafting mechanic where players combine diagnostic
signals according to recipes to produce effects, tools, and abilities.

Educational Notes on Crafting Systems:
--------------------------------------
Crafting systems add strategic depth to games by:
1. Creating resource management decisions (what to craft vs save)
2. Encouraging exploration (finding new recipes)
3. Rewarding experimentation (discovering combinations)
4. Providing player agency (choose your own solutions)

In the context of this automotive ECU roguelike:
- Signals are the raw materials (sensor data, codes, packets)
- Recipes are the procedures (diagnostic algorithms, exploits)
- Crafting is the analysis/manipulation of ECU communication

Design Philosophy:
    The crafting system is data-driven - all recipes are defined in JSON
    files, allowing easy modification and extension without code changes.

    The system validates requirements before crafting to prevent:
    - Partial signal consumption
    - Failed crafting attempts
    - Lost resources

    Effects are applied through a flexible effect system that can:
    - Heal entities
    - Deal damage
    - Apply status effects
    - Reveal information
    - Spawn items
    - Display messages
"""

import json
import os
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

from src.components.signal import SignalComponent
from src.components.health import HealthComponent


class Recipe:
    """
    Represents a single signal-crafting recipe.

    Educational Note:
        This is a data class holding recipe information. We could use
        @dataclass, but implementing it as a regular class provides more
        control over validation and educational annotations.

    Attributes:
        recipe_id: Unique identifier
        name: Display name
        description: What this recipe does
        category: Recipe category (diagnostic, offensive, defensive, utility)
        inputs: List of required signal inputs
        outputs: List of produced signal outputs
        requirements: Prerequisites (floor level, items, skill checks)
        effects: Effects applied when crafted
        metadata: Discovery hints, difficulty, tags
    """

    def __init__(self, recipe_data: Dict[str, Any]):
        """
        Initialize recipe from JSON data.

        Args:
            recipe_data: Dictionary loaded from recipe JSON file

        Educational Note:
            We store the entire recipe data dict and provide properties
            to access fields. This makes the Recipe object a thin wrapper
            around JSON data, keeping it simple and maintainable.
        """
        self.data = recipe_data
        self.recipe_id: str = recipe_data.get("recipe_id", "unknown")
        self.name: str = recipe_data.get("name", "Unknown Recipe")
        self.description: str = recipe_data.get("description", "")
        self.category: str = recipe_data.get("category", "utility")

        self.inputs: List[Dict[str, Any]] = recipe_data.get("inputs", [])
        self.outputs: List[Dict[str, Any]] = recipe_data.get("outputs", [])
        self.requirements: Dict[str, Any] = recipe_data.get("requirements", {})
        self.effects: Dict[str, Any] = recipe_data.get("effects", {})
        self.metadata: Dict[str, Any] = recipe_data.get("metadata", {})

    def get_difficulty(self) -> str:
        """Get recipe difficulty level."""
        return self.metadata.get("difficulty", "unknown")

    def is_discoverable(self) -> bool:
        """Check if recipe can be discovered in-game."""
        return self.metadata.get("discoverable", True)

    def get_hint(self) -> str:
        """Get discovery hint for this recipe."""
        return self.metadata.get("hint", "")

    def get_tags(self) -> List[str]:
        """Get recipe tags for categorization."""
        return self.metadata.get("tags", [])

    def __repr__(self) -> str:
        return f"Recipe(id={self.recipe_id}, name={self.name}, category={self.category})"


class CraftingSystem:
    """
    System managing signal-crafting recipes and execution.

    Educational Note:
        This is a singleton-style system that loads all recipes once and
        provides methods to query and execute them. In a larger game, you
        might use dependency injection or a service locator pattern.

        For this educational project, we keep it simple: one global
        crafting system managing all recipes.

    Responsibilities:
        - Load recipes from JSON files
        - Validate crafting requirements
        - Execute crafting (consume inputs, produce outputs, apply effects)
        - Provide recipe discovery/filtering
    """

    def __init__(self, recipes_dir: str = "config/recipes"):
        """
        Initialize crafting system and load all recipes.

        Args:
            recipes_dir: Directory containing recipe JSON files

        Educational Note:
            We load all recipes at initialization rather than lazy-loading
            because:
            1. Small number of recipes (performance not a concern)
            2. Fail-fast if recipe files are malformed
            3. Simpler code - no lazy loading complexity
            4. Recipes available immediately for queries
        """
        self.recipes_dir = Path(recipes_dir)
        self.recipes: Dict[str, Recipe] = {}
        self.load_all_recipes()

    def load_all_recipes(self) -> None:
        """
        Load all recipe JSON files from the recipes directory.

        Educational Note:
            This method:
            1. Scans the recipes directory for .json files
            2. Loads each file and parses JSON
            3. Creates Recipe objects
            4. Stores them in the recipes dictionary

            Error handling:
            - Skips files that can't be parsed (with warning)
            - Skips SCHEMA.md and other non-recipe files
            - Continues loading even if some recipes fail
        """
        if not self.recipes_dir.exists():
            print(f"Warning: Recipes directory not found: {self.recipes_dir}")
            return

        # Find all JSON files in recipes directory
        recipe_files = list(self.recipes_dir.glob("*.json"))

        for recipe_file in recipe_files:
            try:
                with open(recipe_file, 'r') as f:
                    recipe_data = json.load(f)

                recipe = Recipe(recipe_data)
                self.recipes[recipe.recipe_id] = recipe

            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse recipe file {recipe_file}: {e}")
            except Exception as e:
                print(f"Warning: Failed to load recipe {recipe_file}: {e}")

        print(f"Loaded {len(self.recipes)} crafting recipes")

    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        """
        Get a recipe by ID.

        Args:
            recipe_id: Recipe identifier

        Returns:
            Recipe object if found, None otherwise
        """
        return self.recipes.get(recipe_id)

    def get_all_recipes(self) -> List[Recipe]:
        """
        Get all loaded recipes.

        Returns:
            List of all Recipe objects
        """
        return list(self.recipes.values())

    def get_recipes_by_category(self, category: str) -> List[Recipe]:
        """
        Get all recipes in a specific category.

        Args:
            category: Category to filter by (diagnostic, offensive, defensive, utility)

        Returns:
            List of recipes in the category

        Example:
            >>> crafting = CraftingSystem()
            >>> healing_recipes = crafting.get_recipes_by_category("defensive")
        """
        return [r for r in self.recipes.values() if r.category == category]

    def get_craftable_recipes(
        self,
        signal_component: SignalComponent,
        current_floor: int = 1,
        special_items: Optional[List[str]] = None
    ) -> List[Recipe]:
        """
        Get all recipes that can be crafted with current resources.

        Args:
            signal_component: Entity's signal component
            current_floor: Current dungeon floor level
            special_items: List of special item IDs the entity has

        Returns:
            List of craftable recipes

        Educational Note:
            "Craftable" means:
            1. Entity has all required input signals
            2. Meets floor level requirement
            3. Has special item if required
            4. (Skill check is probabilistic, so we include it)

            This method is used to highlight craftable recipes in UI.
        """
        if special_items is None:
            special_items = []

        craftable = []

        for recipe in self.recipes.values():
            if self.can_craft(recipe, signal_component, current_floor, special_items):
                craftable.append(recipe)

        return craftable

    def can_craft(
        self,
        recipe: Recipe,
        signal_component: SignalComponent,
        current_floor: int = 1,
        special_items: Optional[List[str]] = None
    ) -> bool:
        """
        Check if a recipe can be crafted.

        Args:
            recipe: Recipe to check
            signal_component: Entity's signal component
            current_floor: Current dungeon floor level
            special_items: List of special item IDs the entity has

        Returns:
            True if recipe can be crafted

        Educational Note:
            This is the main validation method called before attempting
            to craft. It checks:
            1. Floor level requirement
            2. Special item requirement
            3. Signal availability

            Note: Skill checks are probabilistic and checked during craft(),
            not here. This allows showing "difficult" recipes as craftable
            even though they might fail.
        """
        if special_items is None:
            special_items = []

        # Check floor requirement
        min_floor = recipe.requirements.get("min_floor", 1)
        if current_floor < min_floor:
            return False

        # Check special item requirement
        required_item = recipe.requirements.get("special_item")
        if required_item and required_item not in special_items:
            return False

        # Check signal requirements
        if not signal_component.can_afford_recipe(recipe.inputs):
            return False

        return True

    def craft(
        self,
        recipe: Recipe,
        signal_component: SignalComponent,
        entity: Any,
        game_state: Optional[Any] = None
    ) -> Tuple[bool, str]:
        """
        Execute a crafting recipe.

        Args:
            recipe: Recipe to craft
            signal_component: Entity's signal component (for consuming/adding signals)
            entity: The entity crafting (for applying effects)
            game_state: Optional game state for advanced effects

        Returns:
            Tuple of (success: bool, message: str)

        Educational Note:
            Crafting process:
            1. Validate requirements (one last time)
            2. Perform skill check if required
            3. Consume input signals (only consumed ones)
            4. Produce output signals
            5. Apply effects (damage, healing, status, etc.)
            6. Return success status and message

            This method is transactional: if skill check fails, no signals
            are consumed. This prevents frustrating partial failures.
        """
        # Final validation
        if not signal_component.can_afford_recipe(recipe.inputs):
            return False, f"Insufficient signals to craft {recipe.name}"

        # Perform skill check if required
        skill_check = recipe.requirements.get("skill_check")
        if skill_check is not None:
            import random
            roll = random.randint(1, 100)
            if roll > skill_check:
                return False, f"Crafting {recipe.name} failed! (Required {skill_check}, rolled {roll})"

        # Consume input signals
        for input_signal in recipe.inputs:
            signal_type = input_signal.get("signal_type")
            quantity = input_signal.get("quantity", 1)
            consumed = input_signal.get("consumed", True)

            if consumed:
                signal_component.remove_signal(signal_type, quantity)

        # Produce output signals
        for output_signal in recipe.outputs:
            signal_type = output_signal.get("signal_type")
            quantity = output_signal.get("quantity", 1)
            signal_component.add_signal(signal_type, quantity)

        # Apply effects
        messages = []
        for effect in recipe.effects.get("on_craft", []):
            effect_msg = self._apply_effect(effect, entity, signal_component, game_state)
            if effect_msg:
                messages.append(effect_msg)

        # Success message
        success_msg = f"Successfully crafted {recipe.name}!"
        if messages:
            success_msg += " " + " ".join(messages)

        return True, success_msg

    def _apply_effect(
        self,
        effect: Dict[str, Any],
        entity: Any,
        signal_component: SignalComponent,
        game_state: Optional[Any] = None
    ) -> str:
        """
        Apply a single effect from a recipe.

        Args:
            effect: Effect dictionary from recipe
            entity: Target entity
            signal_component: Entity's signal component
            game_state: Optional game state

        Returns:
            Message describing effect result

        Educational Note:
            This is an extensible effect system. Each effect type has
            specific logic. Common effect types:

            - heal: Restore HP
            - damage: Deal damage (requires target selection in UI)
            - apply_status: Add status effect (Phase 3 feature)
            - message: Display text to player
            - reveal_enemies: Show enemy info (requires game_state)
            - spawn: Create items/entities (requires game_state)

            For Phase 3, we implement basic effects (heal, message).
            More complex effects will be added later.
        """
        effect_type = effect.get("effect_type")

        # Heal effect
        if effect_type == "heal":
            health = entity.get_component(HealthComponent)
            if health:
                amount = effect.get("value", 0)
                actual = health.heal(amount)
                return f"Healed {actual} HP."

        # Message effect
        elif effect_type == "message":
            text = effect.get("text", "")
            # In a full implementation, this would display in game UI
            # For now, we just return it
            return text

        # Damage effect (requires target - handled by UI)
        elif effect_type == "damage":
            # This effect requires a target entity selected in UI
            # Return instruction for now
            return "Damage effect ready (select target)."

        # Apply status effect (Phase 3 Step 26-27)
        elif effect_type == "apply_status":
            # Status system not yet implemented
            return "Status effect applied (placeholder)."

        # Reveal enemies (requires game state)
        elif effect_type == "reveal_enemies":
            # Requires access to game state and enemy entities
            return "Enemy scan activated (placeholder)."

        # Clear status (utility effect)
        elif effect_type == "clear_status":
            return "Status effects cleared (placeholder)."

        return ""

    def discover_recipe(self, recipe_id: str) -> bool:
        """
        Mark a recipe as discovered (for discoverable recipes).

        Args:
            recipe_id: Recipe to discover

        Returns:
            True if recipe exists and is discoverable

        Educational Note:
            In a full implementation, this would track which recipes
            the player has discovered in their save file. For now, it's
            a placeholder for future save/load integration.

            Recipe discovery could happen through:
            - Finding recipe scrolls/data chips
            - Analyzing enemy signals
            - Experimentation (trying combinations)
            - Quest rewards
        """
        recipe = self.get_recipe(recipe_id)
        if recipe and recipe.is_discoverable():
            # TODO: Track discovered recipes in player save data
            return True
        return False

    def search_recipes(self, query: str) -> List[Recipe]:
        """
        Search recipes by name, description, or tags.

        Args:
            query: Search string

        Returns:
            List of matching recipes

        Educational Note:
            Simple text search for recipe discovery. A more advanced
            implementation might use:
            - Fuzzy matching
            - Tag-based filtering
            - Category filtering
            - Difficulty filtering
        """
        query_lower = query.lower()
        results = []

        for recipe in self.recipes.values():
            # Search in name
            if query_lower in recipe.name.lower():
                results.append(recipe)
                continue

            # Search in description
            if query_lower in recipe.description.lower():
                results.append(recipe)
                continue

            # Search in tags
            if any(query_lower in tag.lower() for tag in recipe.get_tags()):
                results.append(recipe)
                continue

        return results


# Global crafting system instance
# Educational Note:
#     In a real game engine, you'd use dependency injection or a service
#     locator pattern. For this educational project, a global instance
#     is simpler and sufficient.
_crafting_system: Optional[CraftingSystem] = None


def get_crafting_system() -> CraftingSystem:
    """
    Get the global crafting system instance.

    Returns:
        CraftingSystem singleton

    Educational Note:
        Lazy singleton pattern - creates instance on first access.
        This ensures recipes are only loaded once, when needed.
    """
    global _crafting_system
    if _crafting_system is None:
        _crafting_system = CraftingSystem()
    return _crafting_system


def reset_crafting_system() -> None:
    """
    Reset the global crafting system (for testing).

    Educational Note:
        Useful for unit tests to ensure clean state between tests.
    """
    global _crafting_system
    _crafting_system = None
