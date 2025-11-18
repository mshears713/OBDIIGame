"""
ASCII Renderer System

This system handles rendering the dungeon map and entities to the terminal using ASCII characters.

Educational Notes:
------------------
The Renderer is a "system" in the ECS pattern - it processes entities with
specific components (PositionComponent + RenderComponent) and performs an
action (drawing them on screen).

In ECS architecture:
- Components store data (what to draw, where to draw it)
- Systems implement behavior (how to draw it)

This separation allows:
- Swapping rendering backends without changing entities
- Testing game logic without rendering
- Multiple rendering strategies (ASCII, graphical, etc.)
"""

from typing import List, Optional
from src.models import Map, Tile
from src.entities.entity import Entity
from src.components.position import PositionComponent
from src.components.render import RenderComponent


class ASCIIRenderer:
    """
    Renders dungeon maps and entities as ASCII characters in the terminal.

    This renderer operates in two phases:
    1. Render the base map (floors, walls, tiles)
    2. Render entities on top of the map (players, enemies, items)

    Attributes:
        width: Width of the rendering area in characters
        height: Height of the rendering area in characters

    Educational Note:
        ASCII rendering is simple but powerful for roguelikes. It:
        - Runs on any terminal
        - Has minimal dependencies
        - Forces focus on gameplay over graphics
        - Is fast and lightweight

    Example:
        >>> renderer = ASCIIRenderer()
        >>> dungeon_map = Map(width=40, height=20)
        >>> entities = [player, enemy1, enemy2]
        >>> renderer.render(dungeon_map, entities)
        # Displays map and entities in terminal
    """

    def __init__(self, width: int = 80, height: int = 24):
        """
        Initialize the ASCII renderer.

        Args:
            width: Rendering width in characters (default 80)
            height: Rendering height in characters (default 24)

        Educational Note:
            80x24 is a traditional terminal size, dating back to early
            computer terminals. Modern terminals are larger, but these
            dimensions ensure compatibility with minimal displays.
        """
        self.width = width
        self.height = height

    def render(self, dungeon_map: Map, entities: Optional[List[Entity]] = None,
               camera_x: int = 0, camera_y: int = 0) -> str:
        """
        Render the complete game view as a string.

        Args:
            dungeon_map: The Map to render
            entities: List of entities to render on the map
            camera_x: X offset for camera/viewport (for scrolling)
            camera_y: Y offset for camera/viewport (for scrolling)

        Returns:
            Multi-line string representing the rendered scene

        Educational Note:
            This method returns a string rather than printing directly.
            This design allows:
            - Testing the renderer without console output
            - Composing multiple renders
            - Applying post-processing (color codes, etc.)
            - Redirecting output to files or other destinations

        Example:
            >>> output = renderer.render(dungeon_map, entities)
            >>> print(output)  # Display in terminal
            >>> # Or save to file for replay analysis
            >>> with open('game_log.txt', 'a') as f:
            >>>     f.write(output)
        """
        if entities is None:
            entities = []

        # Calculate visible area based on camera position
        view_width = min(self.width, dungeon_map.width - camera_x)
        view_height = min(self.height, dungeon_map.height - camera_y)

        # Create a 2D array to build the rendered output
        # Start with the map tiles
        display = self._render_map(
            dungeon_map, camera_x, camera_y, view_width, view_height
        )

        # Overlay entities on top of the map
        self._render_entities(
            display, entities, camera_x, camera_y, view_width, view_height
        )

        # Convert 2D array to string
        return self._display_to_string(display)

    def _render_map(self, dungeon_map: Map, camera_x: int, camera_y: int,
                    view_width: int, view_height: int) -> List[List[str]]:
        """
        Render the base map tiles to a 2D character array.

        Args:
            dungeon_map: The Map to render
            camera_x: Camera X offset
            camera_y: Camera Y offset
            view_width: Width of visible area
            view_height: Height of visible area

        Returns:
            2D list of characters representing the map

        Educational Note:
            Using a 2D array as intermediate representation allows us to:
            1. Render tiles first
            2. Overlay entities second
            3. Apply effects third (fog of war, lighting)
            This multi-pass approach is common in rendering systems.
        """
        display = []

        for y in range(view_height):
            row = []
            for x in range(view_width):
                # Calculate actual map coordinates
                map_x = camera_x + x
                map_y = camera_y + y

                # Get tile at this position
                tile = dungeon_map.get_tile(map_x, map_y)

                if tile is not None:
                    row.append(tile.ascii_char)
                else:
                    # Out of bounds - show empty space
                    row.append(' ')

            display.append(row)

        return display

    def _render_entities(self, display: List[List[str]], entities: List[Entity],
                        camera_x: int, camera_y: int,
                        view_width: int, view_height: int) -> None:
        """
        Overlay entities onto the display array.

        Args:
            display: 2D character array to modify
            entities: List of entities to render
            camera_x: Camera X offset
            camera_y: Camera Y offset
            view_width: Width of visible area
            view_height: Height of visible area

        Educational Note:
            This method modifies the display array in-place. Entities are
            rendered in order of their render_order (lower values first),
            so higher priority entities appear on top.

            Only entities with both PositionComponent and RenderComponent
            are rendered - this is the ECS pattern in action!
        """
        # Sort entities by render_order so higher values draw on top
        # Educational Note: sorted() creates a new list without modifying original
        sorted_entities = sorted(
            entities,
            key=lambda e: self._get_render_order(e)
        )

        for entity in sorted_entities:
            # Check if entity has required components
            if not entity.has_components(PositionComponent, RenderComponent):
                continue

            position = entity.get_component(PositionComponent)
            render = entity.get_component(RenderComponent)

            # Skip invisible entities
            if not render.is_visible():
                continue

            # Calculate screen position relative to camera
            screen_x = position.x - camera_x
            screen_y = position.y - camera_y

            # Check if entity is within visible area
            if 0 <= screen_x < view_width and 0 <= screen_y < view_height:
                # Place entity character in display
                display[screen_y][screen_x] = render.get_display_char()

    def _get_render_order(self, entity: Entity) -> int:
        """
        Get the render order for an entity.

        Args:
            entity: Entity to check

        Returns:
            Render order value, or -1 if entity has no RenderComponent

        Educational Note:
            Providing a default value (-1) ensures entities without
            RenderComponent sort to the front, though they won't actually
            be rendered since _render_entities checks for the component.
        """
        render = entity.get_component(RenderComponent)
        if render:
            return render.render_order
        return -1

    def _display_to_string(self, display: List[List[str]]) -> str:
        """
        Convert 2D character array to a single string for printing.

        Args:
            display: 2D list of characters

        Returns:
            Multi-line string with each row on a new line

        Educational Note:
            The join() method is an efficient way to build strings in Python.
            Rather than concatenating with +, which creates many intermediate
            strings, join() builds the final string in one operation.

        Example:
            >>> display = [['#', '#', '#'], ['.', '@', '.'], ['#', '#', '#']]
            >>> result = self._display_to_string(display)
            >>> print(result)
            ###
            .@.
            ###
        """
        lines = [''.join(row) for row in display]
        return '\n'.join(lines)

    def render_to_console(self, dungeon_map: Map, entities: Optional[List[Entity]] = None,
                         camera_x: int = 0, camera_y: int = 0,
                         clear_screen: bool = True) -> None:
        """
        Render directly to the console/terminal.

        Args:
            dungeon_map: The Map to render
            entities: List of entities to render
            camera_x: Camera X offset
            camera_y: Camera Y offset
            clear_screen: Whether to clear screen before rendering

        Educational Note:
            This is a convenience method that combines rendering and display.
            During development, you might want clear_screen=False to see
            multiple frames for debugging.

        Example:
            >>> renderer.render_to_console(dungeon_map, entities)
            # Map appears in terminal
        """
        if clear_screen:
            # ANSI escape code to clear screen
            # Educational Note: \033[2J clears screen, \033[H moves cursor to top
            print('\033[2J\033[H', end='')

        output = self.render(dungeon_map, entities, camera_x, camera_y)
        print(output)

    def render_with_border(self, dungeon_map: Map, entities: Optional[List[Entity]] = None,
                          camera_x: int = 0, camera_y: int = 0,
                          title: str = "Dungeon") -> str:
        """
        Render the map with a decorative border and title.

        Args:
            dungeon_map: The Map to render
            entities: List of entities to render
            camera_x: Camera X offset
            camera_y: Camera Y offset
            title: Title to display above the map

        Returns:
            Rendered output with border

        Educational Note:
            Adding UI chrome (borders, titles) makes the game feel more polished.
            This is separate from core rendering to maintain modularity.

        Example:
            >>> output = renderer.render_with_border(map, entities, title="Floor 1: CAN Bus")
            >>> print(output)
            ╔════════════ Floor 1: CAN Bus ════════════╗
            ║ ###########                             ║
            ║ #.........#                             ║
            ║ #....@....#                             ║
            ╚═════════════════════════════════════════╝
        """
        # Render the main content
        content = self.render(dungeon_map, entities, camera_x, camera_y)
        lines = content.split('\n')

        # Calculate border width based on content
        max_width = max(len(line) for line in lines) if lines else 0
        border_width = max_width + 2  # +2 for border characters

        # Create top border with title
        title_display = f" {title} "
        padding = border_width - len(title_display) - 2
        left_pad = padding // 2
        right_pad = padding - left_pad

        top = f"╔{'═' * left_pad}{title_display}{'═' * right_pad}╗"
        bottom = f"╚{'═' * border_width}╝"

        # Add side borders to each line
        bordered_lines = [top]
        for line in lines:
            # Pad line to max width
            padded_line = line.ljust(max_width)
            bordered_lines.append(f"║ {padded_line} ║")
        bordered_lines.append(bottom)

        return '\n'.join(bordered_lines)


# Utility function for quick testing
def render_simple_map(dungeon_map: Map, entities: Optional[List[Entity]] = None) -> None:
    """
    Convenience function to quickly render a map to console.

    Args:
        dungeon_map: The Map to render
        entities: Optional list of entities

    Educational Note:
        This is a quick-and-dirty function for testing and debugging.
        In production code, you'd use the full Renderer class for more control.

    Example:
        >>> from src.systems.renderer import render_simple_map
        >>> render_simple_map(my_map, my_entities)
    """
    renderer = ASCIIRenderer()
    renderer.render_to_console(dungeon_map, entities)
