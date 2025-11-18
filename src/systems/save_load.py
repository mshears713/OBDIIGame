"""
Save/Load System - Game state persistence

This module handles saving and loading game state to/from disk,
enabling players to save progress and resume later.

Educational Note:
    Save/load systems must serialize the entire game state (entities,
    components, maps, player progress) to a format that can be stored
    and restored. We use JSON for human-readability and debugging.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.entities.entity import Entity
from src.components import *
from src.models import Map, Tile


class SaveLoadSystem:
    """
    System managing game state persistence.

    Educational Note:
        Save files contain:
        - Player entity and all components
        - All entities on current floor
        - Map state
        - Game metadata (floor, turn count, etc.)

    Example:
        >>> save_system = SaveLoadSystem()
        >>> save_system.save_game(game_state, "slot1")
        >>> loaded_state = save_system.load_game("slot1")
    """

    def __init__(self, save_dir: str = "saves"):
        """
        Initialize save/load system.

        Args:
            save_dir: Directory for save files
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

    def save_game(
        self,
        game_state: Dict[str, Any],
        slot_name: str = "quicksave"
    ) -> bool:
        """
        Save game state to a file.

        Args:
            game_state: Game state dictionary
            slot_name: Save slot name

        Returns:
            True if save succeeded

        Educational Note:
            Game state should include:
            - player: Player entity
            - entities: List of all entities
            - current_map: Map object
            - floor: Current floor number
            - turn: Current turn count
        """
        try:
            save_data = {
                'version': '1.0',
                'timestamp': datetime.now().isoformat(),
                'slot_name': slot_name,
                'game_state': self._serialize_game_state(game_state)
            }

            save_path = self.save_dir / f"{slot_name}.json"

            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Save failed: {e}")
            return False

    def load_game(self, slot_name: str = "quicksave") -> Optional[Dict[str, Any]]:
        """
        Load game state from a file.

        Args:
            slot_name: Save slot name

        Returns:
            Game state dictionary or None if load failed
        """
        try:
            save_path = self.save_dir / f"{slot_name}.json"

            if not save_path.exists():
                print(f"Save file not found: {save_path}")
                return None

            with open(save_path, 'r') as f:
                save_data = json.load(f)

            game_state = self._deserialize_game_state(save_data['game_state'])

            return game_state

        except Exception as e:
            print(f"Load failed: {e}")
            return None

    def list_saves(self) -> List[Dict[str, Any]]:
        """
        List all available save files.

        Returns:
            List of save file info dictionaries
        """
        saves = []

        for save_path in self.save_dir.glob("*.json"):
            try:
                with open(save_path, 'r') as f:
                    save_data = json.load(f)

                saves.append({
                    'slot_name': save_data.get('slot_name'),
                    'timestamp': save_data.get('timestamp'),
                    'file_path': str(save_path)
                })
            except:
                pass

        return sorted(saves, key=lambda x: x['timestamp'], reverse=True)

    def delete_save(self, slot_name: str) -> bool:
        """Delete a save file."""
        save_path = self.save_dir / f"{slot_name}.json"

        if save_path.exists():
            save_path.unlink()
            return True

        return False

    def _serialize_game_state(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize game state to JSON-compatible format."""
        serialized = {}

        # Serialize player
        if 'player' in game_state:
            serialized['player'] = game_state['player'].to_dict()

        # Serialize entities
        if 'entities' in game_state:
            serialized['entities'] = [e.to_dict() for e in game_state['entities']]

        # Serialize map (if present)
        if 'current_map' in game_state:
            game_map = game_state['current_map']
            serialized['current_map'] = {
                'width': game_map.width,
                'height': game_map.height,
                'tiles': [[tile.tile_type for tile in row] for row in game_map.tiles]
            }

        # Copy simple values
        for key in ['floor', 'turn', 'messages']:
            if key in game_state:
                serialized[key] = game_state[key]

        return serialized

    def _deserialize_game_state(self, serialized: Dict[str, Any]) -> Dict[str, Any]:
        """Deserialize game state from JSON format."""
        from src.components import (
            Component,
            PositionComponent,
            RenderComponent,
            HealthComponent,
            NameComponent,
            InputComponent,
            SignalComponent
        )
        from src.components.status_effect import StatusEffectComponent
        from src.components.tile_effect import TileEffectComponent

        # Component registry for deserialization
        component_registry = {
            'PositionComponent': PositionComponent,
            'RenderComponent': RenderComponent,
            'HealthComponent': HealthComponent,
            'NameComponent': NameComponent,
            'InputComponent': InputComponent,
            'SignalComponent': SignalComponent,
            'StatusEffectComponent': StatusEffectComponent,
            'TileEffectComponent': TileEffectComponent,
        }

        game_state = {}

        # Deserialize player
        if 'player' in serialized:
            game_state['player'] = Entity.from_dict(
                serialized['player'],
                component_registry
            )

        # Deserialize entities
        if 'entities' in serialized:
            game_state['entities'] = [
                Entity.from_dict(e_data, component_registry)
                for e_data in serialized['entities']
            ]

        # Deserialize map (if present)
        if 'current_map' in serialized:
            map_data = serialized['current_map']
            game_map = Map(map_data['width'], map_data['height'])
            game_map.initialize_empty()

            for y in range(map_data['height']):
                for x in range(map_data['width']):
                    tile_type = map_data['tiles'][y][x]
                    game_map.tiles[y][x] = Tile(tile_type)

            game_state['current_map'] = game_map

        # Copy simple values
        for key in ['floor', 'turn', 'messages']:
            if key in serialized:
                game_state[key] = serialized[key]

        return game_state


# Global save/load system instance
_save_load_system: Optional[SaveLoadSystem] = None


def get_save_load_system() -> SaveLoadSystem:
    """Get global save/load system instance."""
    global _save_load_system
    if _save_load_system is None:
        _save_load_system = SaveLoadSystem()
    return _save_load_system
