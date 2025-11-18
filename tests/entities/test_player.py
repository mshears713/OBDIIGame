"""
Tests for Player Entity Factory

Educational Note:
    These tests verify the player entity is created correctly with all
    necessary components and helper functions work as expected.
"""

import pytest
from src.entities.player import (
    create_player,
    get_player_position,
    set_player_position,
    is_player,
    get_player_health,
    is_player_alive
)
from src.entities.entity import Entity
from src.components import (
    PositionComponent,
    RenderComponent,
    HealthComponent,
    NameComponent,
    InputComponent
)


class TestCreatePlayer:
    """Test player creation factory."""

    def test_create_player_default(self):
        """Test creating player with default parameters."""
        player = create_player()

        assert isinstance(player, Entity)
        assert player.has_tag("player")

    def test_create_player_with_position(self):
        """Test creating player at specific position."""
        player = create_player(x=10, y=15)

        pos = player.get_component(PositionComponent)
        assert pos is not None
        assert pos.x == 10
        assert pos.y == 15

    def test_create_player_with_name(self):
        """Test creating player with custom name."""
        player = create_player(name="Hero")

        name = player.get_component(NameComponent)
        assert name is not None
        assert name.name == "Hero"

    def test_player_has_required_components(self):
        """Test player has all necessary components."""
        player = create_player()

        # Should have all core components
        assert player.has_component(PositionComponent)
        assert player.has_component(RenderComponent)
        assert player.has_component(HealthComponent)
        assert player.has_component(NameComponent)
        assert player.has_component(InputComponent)

    def test_player_render_component(self):
        """Test player has correct render configuration."""
        player = create_player()

        render = player.get_component(RenderComponent)
        assert render is not None
        assert render.char == '@'
        assert render.color == 'white'
        assert render.render_order == 3

    def test_player_health_component(self):
        """Test player starts with correct HP."""
        player = create_player()

        health = player.get_component(HealthComponent)
        assert health is not None
        assert health.current_hp == 100
        assert health.max_hp == 100
        assert health.is_alive()

    def test_player_input_component(self):
        """Test player has input component enabled."""
        player = create_player()

        input_comp = player.get_component(InputComponent)
        assert input_comp is not None
        assert input_comp.accepts_input is True


class TestPlayerHelperFunctions:
    """Test player helper functions."""

    def test_get_player_position(self):
        """Test getting player position."""
        player = create_player(x=20, y=25)

        x, y = get_player_position(player)
        assert x == 20
        assert y == 25

    def test_set_player_position(self):
        """Test setting player position."""
        player = create_player(x=10, y=10)

        set_player_position(player, 30, 35)

        x, y = get_player_position(player)
        assert x == 30
        assert y == 35

    def test_is_player_true(self):
        """Test is_player identifies player entity."""
        player = create_player()
        assert is_player(player) is True

    def test_is_player_false(self):
        """Test is_player rejects non-player entities."""
        entity = Entity()
        assert is_player(entity) is False

    def test_get_player_health(self):
        """Test getting player health."""
        player = create_player()

        current, maximum = get_player_health(player)
        assert current == 100
        assert maximum == 100

    def test_get_player_health_after_damage(self):
        """Test getting player health after taking damage."""
        player = create_player()

        health = player.get_component(HealthComponent)
        health.take_damage(30)

        current, maximum = get_player_health(player)
        assert current == 70
        assert maximum == 100

    def test_is_player_alive_true(self):
        """Test is_player_alive for living player."""
        player = create_player()
        assert is_player_alive(player) is True

    def test_is_player_alive_false(self):
        """Test is_player_alive for dead player."""
        player = create_player()

        health = player.get_component(HealthComponent)
        health.take_damage(200)  # Fatal damage

        assert is_player_alive(player) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
