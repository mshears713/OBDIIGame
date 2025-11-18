"""
Unit Tests for ASCII Renderer System

Tests map and entity rendering to ASCII output.
"""

import pytest
from src.models import Map, Tile, TileType
from src.entities.entity import Entity
from src.components import PositionComponent, RenderComponent, create_player_render
from src.systems.renderer import ASCIIRenderer, render_simple_map


class TestASCIIRenderer:
    """Test suite for ASCIIRenderer."""

    def test_initialization_default(self):
        """Test creating renderer with default size."""
        renderer = ASCIIRenderer()
        assert renderer.width == 80
        assert renderer.height == 24

    def test_initialization_custom_size(self):
        """Test creating renderer with custom size."""
        renderer = ASCIIRenderer(width=40, height=20)
        assert renderer.width == 40
        assert renderer.height == 20

    def test_render_empty_map(self):
        """Test rendering an empty map with walls."""
        renderer = ASCIIRenderer(width=10, height=5)
        dungeon_map = Map(width=10, height=5)
        dungeon_map.initialize_empty(Tile.create_wall())

        output = renderer.render(dungeon_map)

        lines = output.split('\n')
        assert len(lines) == 5
        assert all(len(line) == 10 for line in lines)
        # All characters should be walls
        assert all(char == '#' for line in lines for char in line)

    def test_render_floor_map(self):
        """Test rendering a map filled with floor tiles."""
        renderer = ASCIIRenderer(width=5, height=3)
        dungeon_map = Map(width=5, height=3)
        dungeon_map.initialize_empty(Tile.create_floor())

        output = renderer.render(dungeon_map)

        lines = output.split('\n')
        assert len(lines) == 3
        # All characters should be floors
        assert all(char == '.' for line in lines for char in line)

    def test_render_map_with_mixed_tiles(self):
        """Test rendering a map with different tile types."""
        renderer = ASCIIRenderer(width=5, height=3)
        dungeon_map = Map(width=5, height=3)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Add some walls
        dungeon_map.set_tile(0, 0, Tile.create_wall())
        dungeon_map.set_tile(4, 0, Tile.create_wall())
        dungeon_map.set_tile(0, 2, Tile.create_wall())
        dungeon_map.set_tile(4, 2, Tile.create_wall())

        output = renderer.render(dungeon_map)

        lines = output.split('\n')
        # Check corners are walls
        assert lines[0][0] == '#'  # Top-left
        assert lines[0][4] == '#'  # Top-right
        assert lines[2][0] == '#'  # Bottom-left
        assert lines[2][4] == '#'  # Bottom-right

        # Check center is floor
        assert lines[1][2] == '.'

    def test_render_single_entity(self):
        """Test rendering a map with a single entity."""
        renderer = ASCIIRenderer(width=5, height=5)
        dungeon_map = Map(width=5, height=5)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Create entity at center
        entity = Entity(tags=['player'])
        entity.add_component(PositionComponent(x=2, y=2))
        entity.add_component(RenderComponent(char='@', color='white', render_order=1))

        output = renderer.render(dungeon_map, [entity])

        lines = output.split('\n')
        # Entity should be at center (row 2, column 2)
        assert lines[2][2] == '@'
        # Other positions should be floors
        assert lines[0][0] == '.'
        assert lines[4][4] == '.'

    def test_render_multiple_entities(self):
        """Test rendering multiple entities at different positions."""
        renderer = ASCIIRenderer(width=7, height=5)
        dungeon_map = Map(width=7, height=5)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Create player
        player = Entity(tags=['player'])
        player.add_component(PositionComponent(x=3, y=2))
        player.add_component(create_player_render())

        # Create enemies
        enemy1 = Entity(tags=['enemy'])
        enemy1.add_component(PositionComponent(x=1, y=1))
        enemy1.add_component(RenderComponent(char='E', color='red', render_order=1))

        enemy2 = Entity(tags=['enemy'])
        enemy2.add_component(PositionComponent(x=5, y=3))
        enemy2.add_component(RenderComponent(char='G', color='green', render_order=1))

        output = renderer.render(dungeon_map, [player, enemy1, enemy2])

        lines = output.split('\n')
        # Check entity positions
        assert lines[2][3] == '@'  # Player
        assert lines[1][1] == 'E'  # Enemy1
        assert lines[3][5] == 'G'  # Enemy2

    def test_render_entity_render_order(self):
        """Test that entities with higher render_order appear on top."""
        renderer = ASCIIRenderer(width=5, height=5)
        dungeon_map = Map(width=5, height=5)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Create two entities at same position with different render orders
        lower_entity = Entity()
        lower_entity.add_component(PositionComponent(x=2, y=2))
        lower_entity.add_component(RenderComponent(char='L', render_order=1))

        higher_entity = Entity()
        higher_entity.add_component(PositionComponent(x=2, y=2))
        higher_entity.add_component(RenderComponent(char='H', render_order=2))

        output = renderer.render(dungeon_map, [lower_entity, higher_entity])

        lines = output.split('\n')
        # Higher render_order should be on top
        assert lines[2][2] == 'H'

    def test_render_invisible_entity_not_shown(self):
        """Test that invisible entities are not rendered."""
        renderer = ASCIIRenderer(width=5, height=5)
        dungeon_map = Map(width=5, height=5)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Create invisible entity
        entity = Entity()
        entity.add_component(PositionComponent(x=2, y=2))
        entity.add_component(RenderComponent(char='X', visible=False))

        output = renderer.render(dungeon_map, [entity])

        lines = output.split('\n')
        # Entity should not appear (floor should be visible)
        assert lines[2][2] == '.'

    def test_render_entity_without_required_components(self):
        """Test that entities without Position or Render components are skipped."""
        renderer = ASCIIRenderer(width=5, height=5)
        dungeon_map = Map(width=5, height=5)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Entity with only position (no render)
        entity1 = Entity()
        entity1.add_component(PositionComponent(x=1, y=1))

        # Entity with only render (no position)
        entity2 = Entity()
        entity2.add_component(RenderComponent(char='X'))

        # Should not crash, entities just won't appear
        output = renderer.render(dungeon_map, [entity1, entity2])

        lines = output.split('\n')
        # Both positions should show floor
        assert lines[1][1] == '.'

    def test_render_with_camera_offset(self):
        """Test rendering with camera offset to show different map area."""
        renderer = ASCIIRenderer(width=5, height=5)
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Place a marker at (7, 7)
        dungeon_map.set_tile(7, 7, Tile.create_stairs_down())

        # Render with camera at (5, 5) - should show coordinates 5-9, 5-9
        output = renderer.render(dungeon_map, camera_x=5, camera_y=5)

        lines = output.split('\n')
        # Stairs at (7,7) should appear at screen position (2,2)
        assert lines[2][2] == '>'

    def test_display_to_string(self):
        """Test conversion of 2D display array to string."""
        renderer = ASCIIRenderer()

        display = [
            ['#', '#', '#'],
            ['.', '@', '.'],
            ['#', '#', '#']
        ]

        result = renderer._display_to_string(display)

        expected = "###\n.@.\n###"
        assert result == expected

    def test_get_render_order_with_component(self):
        """Test getting render order from entity with RenderComponent."""
        renderer = ASCIIRenderer()

        entity = Entity()
        entity.add_component(RenderComponent(render_order=5))

        order = renderer._get_render_order(entity)
        assert order == 5

    def test_get_render_order_without_component(self):
        """Test getting render order from entity without RenderComponent."""
        renderer = ASCIIRenderer()

        entity = Entity()

        order = renderer._get_render_order(entity)
        assert order == -1

    def test_render_with_border(self):
        """Test rendering with decorative border."""
        renderer = ASCIIRenderer(width=5, height=3)
        dungeon_map = Map(width=5, height=3)
        dungeon_map.initialize_empty(Tile.create_floor())

        output = renderer.render_with_border(dungeon_map, title="Test Floor")

        lines = output.split('\n')

        # Should have border rows (top + 3 content + bottom = 5 lines)
        assert len(lines) == 5

        # Check border characters
        assert lines[0].startswith('╔')
        assert lines[0].endswith('╗')
        assert lines[-1].startswith('╚')
        assert lines[-1].endswith('╝')

        # Check title appears in top border
        assert "Test Floor" in lines[0]

        # Content lines should have side borders
        assert all(line.startswith('║') for line in lines[1:-1])
        assert all(line.endswith('║') for line in lines[1:-1])

    def test_render_map_larger_than_view(self):
        """Test rendering when map is larger than renderer viewport."""
        renderer = ASCIIRenderer(width=5, height=5)
        dungeon_map = Map(width=20, height=20)
        dungeon_map.initialize_empty(Tile.create_wall())

        # Render without camera offset - should show first 5x5
        output = renderer.render(dungeon_map)

        lines = output.split('\n')
        assert len(lines) == 5
        assert all(len(line) == 5 for line in lines)

    def test_render_empty_entity_list(self):
        """Test rendering with empty entity list."""
        renderer = ASCIIRenderer(width=5, height=5)
        dungeon_map = Map(width=5, height=5)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Render with empty list
        output = renderer.render(dungeon_map, [])

        lines = output.split('\n')
        # Should just show the map, no entities
        assert all(char == '.' for line in lines for char in line)

    def test_render_with_none_entities(self):
        """Test rendering with None entity list (default parameter)."""
        renderer = ASCIIRenderer(width=5, height=5)
        dungeon_map = Map(width=5, height=5)
        dungeon_map.initialize_empty(Tile.create_floor())

        # Render with default None entities
        output = renderer.render(dungeon_map)

        lines = output.split('\n')
        # Should just show the map, no entities
        assert all(char == '.' for line in lines for char in line)


def test_render_simple_map_function():
    """Test the convenience render_simple_map function doesn't crash."""
    dungeon_map = Map(width=5, height=5)
    dungeon_map.initialize_empty(Tile.create_floor())

    # Should not crash
    # Note: Can't easily test console output, but at least verify it runs
    try:
        render_simple_map(dungeon_map)
    except Exception as e:
        pytest.fail(f"render_simple_map raised exception: {e}")
