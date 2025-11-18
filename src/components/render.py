"""
RenderComponent - Visual representation component for entities

This component defines how an entity appears when rendered in the game.

Educational Notes:
------------------
The RenderComponent separates visual representation from game logic.
An entity's appearance is just data - the RenderSystem handles actual drawing.

This separation allows:
- Changing visuals without touching game logic
- Multiple rendering backends (ASCII, graphical, etc.)
- Easy visual effects (color changes, animations)
- Consistent rendering across the game
"""

from src.components.base import Component
from typing import Dict, Any, Optional


class RenderComponent(Component):
    """
    Component defining visual representation of an entity.

    Attributes:
        char: ASCII character used to display this entity (e.g., '@' for player)
        color: Color name for the character (e.g., 'white', 'red')
        bg_color: Background color (optional, defaults to None/transparent)
        render_order: Z-order for rendering (higher = drawn on top)
        visible: Whether this entity should be rendered

    Educational Note:
        In ASCII/terminal games, each entity is represented by a single character.
        Common conventions:
            @ = Player
            # = Wall
            . = Floor
            ! = Potion
            % = Food
            $ = Gold/treasure
            > = Stairs down
            < = Stairs up

        The render_order determines layering when multiple entities occupy
        the same tile. For example:
            render_order=0: Tiles/floor
            render_order=1: Items
            render_order=2: Corpses
            render_order=3: Living creatures
            render_order=4: Special effects

    Example:
        >>> # Create a player render component
        >>> player_render = RenderComponent(
        ...     char='@',
        ...     color='white',
        ...     render_order=3
        ... )
        >>>
        >>> # Create an enemy render component
        >>> enemy_render = RenderComponent(
        ...     char='E',
        ...     color='red',
        ...     render_order=3
        ... )
    """

    def __init__(
        self,
        char: str = '?',
        color: str = 'white',
        bg_color: Optional[str] = None,
        render_order: int = 0,
        visible: bool = True
    ):
        """
        Initialize render component.

        Args:
            char: ASCII character to display (default '?')
            color: Foreground color name (default 'white')
            bg_color: Background color name (default None)
            render_order: Rendering layer/priority (default 0)
            visible: Whether entity should be rendered (default True)

        Educational Note:
            Default char of '?' helps identify entities that haven't been
            properly configured - they'll show up as question marks in-game.
        """
        super().__init__()
        self.char = char
        self.color = color
        self.bg_color = bg_color
        self.render_order = render_order
        self.visible = visible

    def get_display_char(self) -> str:
        """
        Get the character to display.

        Returns:
            The ASCII character for this entity

        Educational Note:
            This method provides a future extension point. For example, we
            could add animation by cycling through multiple characters, or
            change appearance based on entity state.

        Example:
            >>> render = RenderComponent(char='@', color='white')
            >>> print(render.get_display_char())
            @
        """
        return self.char

    def set_char(self, char: str) -> None:
        """
        Change the display character.

        Args:
            char: New character to display

        Educational Note:
            Useful for visual effects or state changes:
            - Door opening: '+' -> '/'
            - Damaged enemy: 'E' -> 'e'
            - Powered-up player: '@' -> '★'

        Example:
            >>> door = RenderComponent(char='+', color='brown')
            >>> # When door opens:
            >>> door.set_char('/')
        """
        self.char = char

    def get_color(self) -> str:
        """
        Get the foreground color.

        Returns:
            Color name string

        Example:
            >>> render = RenderComponent(char='E', color='red')
            >>> assert render.get_color() == 'red'
        """
        return self.color

    def set_color(self, color: str) -> None:
        """
        Change the foreground color.

        Args:
            color: New color name

        Educational Note:
            Color changes can indicate status effects:
            - Poisoned: normal_color -> 'green'
            - Frozen: normal_color -> 'cyan'
            - Burning: normal_color -> 'orange'

        Example:
            >>> enemy = RenderComponent(char='E', color='red')
            >>> # When frozen:
            >>> enemy.set_color('cyan')
        """
        self.color = color

    def show(self) -> None:
        """
        Make this entity visible.

        Educational Note:
            Visibility control is useful for:
            - Fog of war (hide unexplored areas)
            - Stealth mechanics (invisible enemies)
            - Spawning effects (fade in)

        Example:
            >>> render = RenderComponent(visible=False)
            >>> # When player explores area:
            >>> render.show()
            >>> assert render.visible is True
        """
        self.visible = True

    def hide(self) -> None:
        """
        Make this entity invisible.

        Example:
            >>> render = RenderComponent()
            >>> render.hide()
            >>> assert render.visible is False
        """
        self.visible = False

    def is_visible(self) -> bool:
        """
        Check if entity is currently visible.

        Returns:
            True if visible, False if hidden

        Educational Note:
            The RenderSystem should check this before drawing entities.
            This allows efficient culling of off-screen or hidden entities.

        Example:
            >>> render = RenderComponent()
            >>> if render.is_visible():
            >>>     draw_entity(render)
        """
        return self.visible

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize render component to dictionary.

        Returns:
            Dictionary representation of render data

        Educational Note:
            Explicit serialization gives us control over what gets saved.
            For example, we might not save temporary visual effects.
        """
        return {
            'component_type': self.component_type,
            'char': self.char,
            'color': self.color,
            'bg_color': self.bg_color,
            'render_order': self.render_order,
            'visible': self.visible
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RenderComponent':
        """
        Deserialize render component from dictionary.

        Args:
            data: Dictionary containing render data

        Returns:
            New RenderComponent instance

        Example:
            >>> data = {
            ...     'char': '@',
            ...     'color': 'yellow',
            ...     'render_order': 3
            ... }
            >>> render = RenderComponent.from_dict(data)
            >>> assert render.char == '@'
        """
        return cls(
            char=data.get('char', '?'),
            color=data.get('color', 'white'),
            bg_color=data.get('bg_color'),
            render_order=data.get('render_order', 0),
            visible=data.get('visible', True)
        )


# Common render component factory functions
# Educational Note: Factory functions provide convenient, self-documenting
# ways to create common entity visual configurations

def create_player_render() -> RenderComponent:
    """
    Create standard player render component.

    Returns:
        RenderComponent configured for player character

    Example:
        >>> player_render = create_player_render()
        >>> assert player_render.char == '@'
    """
    return RenderComponent(
        char='@',
        color='white',
        render_order=3
    )


def create_enemy_render(char: str = 'E', color: str = 'red') -> RenderComponent:
    """
    Create standard enemy render component.

    Args:
        char: Character to use for enemy (default 'E')
        color: Color for enemy (default 'red')

    Returns:
        RenderComponent configured for enemy

    Educational Note:
        Different enemy types can use different characters:
        - 'g' for goblins
        - 'D' for dragons
        - 'z' for zombies
        Uppercase often indicates stronger/boss versions.

    Example:
        >>> goblin = create_enemy_render(char='g', color='green')
        >>> dragon = create_enemy_render(char='D', color='red')
    """
    return RenderComponent(
        char=char,
        color=color,
        render_order=3
    )


def create_item_render(char: str = '!', color: str = 'cyan') -> RenderComponent:
    """
    Create standard item render component.

    Args:
        char: Character to use for item (default '!')
        color: Color for item (default 'cyan')

    Returns:
        RenderComponent configured for item

    Educational Note:
        Common item symbols:
        - '!' for potions
        - '%' for food
        - '$' for gold/currency
        - '?' for unidentified items
        - '/' for weapons
        - '[' for armor

    Example:
        >>> potion = create_item_render(char='!', color='magenta')
        >>> gold = create_item_render(char='$', color='yellow')
    """
    return RenderComponent(
        char=char,
        color=color,
        render_order=1  # Items render below creatures
    )
