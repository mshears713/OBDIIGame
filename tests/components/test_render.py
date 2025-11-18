"""
Unit Tests for RenderComponent

Tests visual representation storage and manipulation.
"""

import pytest
from src.components.render import (
    RenderComponent,
    create_player_render,
    create_enemy_render,
    create_item_render
)


class TestRenderComponent:
    """Test suite for RenderComponent."""

    def test_initialization_default(self):
        """Test creating render component with default values."""
        render = RenderComponent()
        assert render.char == '?'
        assert render.color == 'white'
        assert render.bg_color is None
        assert render.render_order == 0
        assert render.visible is True
        assert render.component_type == "RenderComponent"

    def test_initialization_with_parameters(self):
        """Test creating render component with custom values."""
        render = RenderComponent(
            char='@',
            color='yellow',
            bg_color='black',
            render_order=3,
            visible=False
        )
        assert render.char == '@'
        assert render.color == 'yellow'
        assert render.bg_color == 'black'
        assert render.render_order == 3
        assert render.visible is False

    def test_get_display_char(self):
        """Test retrieving display character."""
        render = RenderComponent(char='E')
        assert render.get_display_char() == 'E'

    def test_set_char(self):
        """Test changing display character."""
        render = RenderComponent(char='+')
        render.set_char('/')
        assert render.char == '/'
        assert render.get_display_char() == '/'

    def test_get_color(self):
        """Test retrieving color."""
        render = RenderComponent(color='red')
        assert render.get_color() == 'red'

    def test_set_color(self):
        """Test changing color."""
        render = RenderComponent(color='white')
        render.set_color('green')
        assert render.color == 'green'
        assert render.get_color() == 'green'

    def test_show(self):
        """Test making entity visible."""
        render = RenderComponent(visible=False)
        render.show()
        assert render.visible is True
        assert render.is_visible() is True

    def test_hide(self):
        """Test hiding entity."""
        render = RenderComponent(visible=True)
        render.hide()
        assert render.visible is False
        assert render.is_visible() is False

    def test_is_visible_true(self):
        """Test visibility check returns True when visible."""
        render = RenderComponent(visible=True)
        assert render.is_visible() is True

    def test_is_visible_false(self):
        """Test visibility check returns False when hidden."""
        render = RenderComponent(visible=False)
        assert render.is_visible() is False

    def test_to_dict(self):
        """Test serialization to dictionary."""
        render = RenderComponent(
            char='@',
            color='white',
            bg_color='black',
            render_order=3,
            visible=True
        )
        data = render.to_dict()

        assert data['component_type'] == 'RenderComponent'
        assert data['char'] == '@'
        assert data['color'] == 'white'
        assert data['bg_color'] == 'black'
        assert data['render_order'] == 3
        assert data['visible'] is True

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'char': 'E',
            'color': 'red',
            'bg_color': None,
            'render_order': 2,
            'visible': False
        }
        render = RenderComponent.from_dict(data)

        assert render.char == 'E'
        assert render.color == 'red'
        assert render.bg_color is None
        assert render.render_order == 2
        assert render.visible is False

    def test_from_dict_with_missing_values(self):
        """Test deserialization with missing values uses defaults."""
        data = {}
        render = RenderComponent.from_dict(data)

        assert render.char == '?'
        assert render.color == 'white'
        assert render.bg_color is None
        assert render.render_order == 0
        assert render.visible is True

    def test_serialization_roundtrip(self):
        """Test that serialize -> deserialize preserves data."""
        original = RenderComponent(
            char='D',
            color='purple',
            bg_color='gray',
            render_order=5,
            visible=True
        )

        # Serialize
        data = original.to_dict()

        # Deserialize
        restored = RenderComponent.from_dict(data)

        assert restored.char == original.char
        assert restored.color == original.color
        assert restored.bg_color == original.bg_color
        assert restored.render_order == original.render_order
        assert restored.visible == original.visible


class TestRenderFactories:
    """Test suite for render component factory functions."""

    def test_create_player_render(self):
        """Test player render factory."""
        render = create_player_render()

        assert render.char == '@'
        assert render.color == 'white'
        assert render.render_order == 3
        assert render.visible is True

    def test_create_enemy_render_default(self):
        """Test enemy render factory with defaults."""
        render = create_enemy_render()

        assert render.char == 'E'
        assert render.color == 'red'
        assert render.render_order == 3

    def test_create_enemy_render_custom(self):
        """Test enemy render factory with custom parameters."""
        render = create_enemy_render(char='D', color='purple')

        assert render.char == 'D'
        assert render.color == 'purple'
        assert render.render_order == 3

    def test_create_item_render_default(self):
        """Test item render factory with defaults."""
        render = create_item_render()

        assert render.char == '!'
        assert render.color == 'cyan'
        assert render.render_order == 1  # Items below creatures

    def test_create_item_render_custom(self):
        """Test item render factory with custom parameters."""
        render = create_item_render(char='$', color='yellow')

        assert render.char == '$'
        assert render.color == 'yellow'
        assert render.render_order == 1

    def test_render_order_layering(self):
        """Test that render orders are correct for layering."""
        item = create_item_render()
        player = create_player_render()
        enemy = create_enemy_render()

        # Items (1) should render below creatures (3)
        assert item.render_order < player.render_order
        assert item.render_order < enemy.render_order

        # Player and enemies at same layer (will need position to differentiate)
        assert player.render_order == enemy.render_order
