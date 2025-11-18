"""
AIComponent - Defines enemy behavior patterns

This component controls how enemies behave during their turns: wandering,
chasing the player, fleeing, standing still, etc.

Educational Notes:
------------------
AI in roguelikes is typically simple but effective. Common patterns include:
- **Wander:** Random movement, low threat
- **Chase:** Pursue player when in range
- **Guard:** Stay in place until provoked
- **Flee:** Run away when low on health
- **Ranged:** Keep distance and attack from afar

By storing AI behavior in a component, we can:
- Mix and match behaviors easily
- Change AI at runtime (e.g., peaceful enemy becomes aggressive)
- Save/load AI state
- Test AI independently of game logic
"""

from src.components.base import Component
from typing import Dict, Any, Optional
from enum import Enum, auto


class AIBehavior(Enum):
    """
    Enumeration of AI behavior types.

    Educational Note:
        Using an Enum instead of strings prevents typos and makes
        the code more maintainable. The IDE can autocomplete these
        and catch errors at design time.
    """
    WANDER = auto()      # Random movement
    CHASE = auto()       # Pursue player
    GUARD = auto()       # Stay in place
    FLEE = auto()        # Run away
    PATROL = auto()      # Follow a path


class AIComponent(Component):
    """
    Component defining entity AI behavior.

    Attributes:
        behavior: Current AI behavior mode
        aggro_range: Distance at which enemy notices player
        chase_range: Maximum distance to chase player
        intelligence: AI intelligence level ("low", "medium", "high")
        target_entity_id: ID of entity being targeted (usually player)
        state_data: Additional state for complex behaviors

    Educational Note:
        AI components store configuration, not logic. The AI system
        reads these values and makes decisions based on them.

        This separation allows:
        - Data-driven AI (configure in JSON)
        - Reusable AI logic (one system, many entities)
        - Easy testing (mock components, test system)

    Example:
        >>> # Create a wandering enemy that aggros at 4 tiles
        >>> ai = AIComponent(
        ...     behavior="wander",
        ...     aggro_range=4,
        ...     chase_range=8
        ... )
        >>>
        >>> # Create a guard that doesn't move
        >>> guard_ai = AIComponent(
        ...     behavior="guard",
        ...     aggro_range=3,
        ...     chase_range=5
        ... )
    """

    def __init__(
        self,
        behavior: str = "wander",
        aggro_range: int = 4,
        chase_range: int = 8,
        intelligence: str = "low",
        target_entity_id: Optional[int] = None
    ):
        """
        Initialize AI component.

        Args:
            behavior: Behavior type (wander, chase, guard, flee, patrol)
            aggro_range: Tiles away player must be to notice them
            chase_range: Maximum distance to pursue player
            intelligence: AI intelligence ("low", "medium", "high")
            target_entity_id: ID of target entity (None = no target)

        Educational Note:
            We accept string for behavior to make JSON configuration easier.
            Could also use AIBehavior enum and convert in from_dict.
        """
        super().__init__()

        # Core behavior settings
        self.behavior = behavior
        self.aggro_range = aggro_range
        self.chase_range = chase_range
        self.intelligence = intelligence

        # Current AI state
        self.target_entity_id = target_entity_id
        self.state_data: Dict[str, Any] = {}

        # Patrol route (for patrol behavior)
        self.patrol_points: list = []
        self.patrol_index: int = 0

    def set_target(self, entity_id: Optional[int]) -> None:
        """
        Set the target entity for this AI.

        Args:
            entity_id: Target entity ID, or None to clear target

        Educational Note:
            Targeting is crucial for AI:
            - Chase behavior needs a target
            - Flee behavior needs to know what to flee from
            - Combat needs to know who to attack

        Example:
            >>> ai.set_target(player.entity_id)
            >>> # AI will now pursue/attack player
        """
        self.target_entity_id = entity_id

    def clear_target(self) -> None:
        """
        Clear the current target.

        Educational Note:
            Clearing target happens when:
            - Target dies
            - Target escapes (beyond chase_range)
            - Enemy forgets player (stealth mechanic)
        """
        self.target_entity_id = None

    def has_target(self) -> bool:
        """
        Check if AI has a target.

        Returns:
            True if target is set, False otherwise
        """
        return self.target_entity_id is not None

    def set_behavior(self, behavior: str) -> None:
        """
        Change AI behavior at runtime.

        Args:
            behavior: New behavior type

        Educational Note:
            Dynamic behavior changes enable interesting gameplay:
            - Peaceful NPC becomes hostile when attacked
            - Low-health enemy flees
            - Alerted enemy switches from wander to chase

        Example:
            >>> # Enemy takes damage and flees
            >>> if enemy_health.get_hp_percentage() < 0.3:
            ...     ai.set_behavior("flee")
        """
        self.behavior = behavior

    def set_patrol_route(self, patrol_points: list) -> None:
        """
        Set patrol route for patrol behavior.

        Args:
            patrol_points: List of (x, y) coordinates to patrol

        Educational Note:
            Patrol routes create predictable but dynamic enemies.
            Players can learn patterns and time their movements.

        Example:
            >>> route = [(10, 5), (20, 5), (20, 15), (10, 15)]
            >>> ai.set_patrol_route(route)
            >>> # Enemy will patrol in a square pattern
        """
        self.patrol_points = patrol_points
        self.patrol_index = 0

    def get_next_patrol_point(self) -> Optional[tuple]:
        """
        Get next patrol point and advance patrol index.

        Returns:
            Next (x, y) patrol point, or None if no route set

        Educational Note:
            Patrol system cycles through points:
            - Move to point 0
            - Move to point 1
            - ...
            - Move to last point
            - Loop back to point 0
        """
        if not self.patrol_points:
            return None

        point = self.patrol_points[self.patrol_index]
        self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)
        return point

    def to_dict(self) -> Dict[str, Any]:
        """Serialize AI component to dictionary."""
        return {
            'component_type': self.component_type,
            'behavior': self.behavior,
            'aggro_range': self.aggro_range,
            'chase_range': self.chase_range,
            'intelligence': self.intelligence,
            'target_entity_id': self.target_entity_id,
            'state_data': self.state_data,
            'patrol_points': self.patrol_points,
            'patrol_index': self.patrol_index
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIComponent':
        """
        Deserialize AI component from dictionary.

        Args:
            data: Dictionary containing AI data

        Returns:
            New AIComponent instance
        """
        ai = cls(
            behavior=data.get('behavior', 'wander'),
            aggro_range=data.get('aggro_range', 4),
            chase_range=data.get('chase_range', 8),
            intelligence=data.get('intelligence', 'low'),
            target_entity_id=data.get('target_entity_id')
        )

        # Restore patrol data
        ai.patrol_points = data.get('patrol_points', [])
        ai.patrol_index = data.get('patrol_index', 0)
        ai.state_data = data.get('state_data', {})

        return ai
