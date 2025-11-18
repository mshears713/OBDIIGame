# Save Games Directory

This directory is used to store your game save files.

## Docker Usage

When running the game with Docker, this directory is automatically mounted as a volume, ensuring your save games persist between container runs.

## Save File Format

Save files are stored in JSON format and typically named `savegame.json`.

## Backup Your Saves

It's recommended to periodically backup your save files to prevent data loss.

```bash
# Example backup command
cp savegame.json savegame.backup.json
```

## Note

This directory is excluded from version control (listed in `.gitignore`) to prevent accidentally committing your personal save files.
