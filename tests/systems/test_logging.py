"""
Unit tests for Logging System

Tests cover:
- Logger initialization
- Different log levels
- File and console output
- Event logging
- Performance logging
- Log level changes
"""

import pytest
import logging
import tempfile
from pathlib import Path
from src.systems.logging_system import (
    GameLogger,
    get_game_logger,
    init_game_logger,
    debug, info, warning, error, critical,
    log_event, log_performance
)


class TestGameLogger:
    """Test suite for GameLogger class."""

    def test_logger_initialization(self):
        """Test basic logger initialization."""
        logger = GameLogger(name="TestLogger")

        assert logger.logger is not None
        assert logger.logger.name == "TestLogger"

    def test_logger_with_custom_level(self):
        """Test initialization with custom log level."""
        logger = GameLogger(log_level=logging.DEBUG)

        assert logger.logger.level == logging.DEBUG

    def test_debug_logging(self):
        """Test debug level logging."""
        logger = GameLogger(log_level=logging.DEBUG, log_to_file=False)

        # Should not raise exception
        logger.debug("This is a debug message")

    def test_info_logging(self):
        """Test info level logging."""
        logger = GameLogger(log_to_file=False)

        logger.info("This is an info message")

    def test_warning_logging(self):
        """Test warning level logging."""
        logger = GameLogger(log_to_file=False)

        logger.warning("This is a warning message")

    def test_error_logging(self):
        """Test error level logging."""
        logger = GameLogger(log_to_file=False)

        logger.error("This is an error message")

    def test_critical_logging(self):
        """Test critical level logging."""
        logger = GameLogger(log_to_file=False)

        logger.critical("This is a critical message")

    def test_log_event(self):
        """Test structured event logging."""
        logger = GameLogger(log_to_file=False)

        logger.log_event("PLAYER_DEATH", "Player killed by enemy")
        logger.log_event("LEVEL_COMPLETE")

    def test_log_performance(self):
        """Test performance logging."""
        logger = GameLogger(log_to_file=False)

        logger.log_performance("Dungeon Generation", 123.45)

    def test_set_log_level(self):
        """Test changing log level at runtime."""
        logger = GameLogger(log_level=logging.INFO, log_to_file=False)

        # Initially INFO level
        assert logger.logger.level == logging.INFO

        # Change to DEBUG
        logger.set_level(logging.DEBUG)
        assert logger.logger.level == logging.DEBUG

        # Change to WARNING
        logger.set_level(logging.WARNING)
        assert logger.logger.level == logging.WARNING

    def test_file_logging(self):
        """Test logging to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"

            logger = GameLogger(
                log_to_file=True,
                log_file_path=str(log_file)
            )

            logger.info("Test message")

            # Verify file was created and contains message
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test message" in content
            assert "[INFO]" in content

    def test_log_file_creates_directory(self):
        """Test that log directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "subdir" / "logs" / "test.log"

            # Directory doesn't exist yet
            assert not log_file.parent.exists()

            # Create logger (should create directory)
            logger = GameLogger(
                log_to_file=True,
                log_file_path=str(log_file)
            )

            # Verify directory was created
            assert log_file.parent.exists()

    def test_multiple_log_messages(self):
        """Test logging multiple messages."""
        logger = GameLogger(log_to_file=False)

        for i in range(10):
            logger.info(f"Message {i}")

    def test_log_formatting(self):
        """Test log message format."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"

            logger = GameLogger(
                log_to_file=True,
                log_file_path=str(log_file)
            )

            logger.info("Test message")

            content = log_file.read_text()

            # Should contain timestamp
            assert "[" in content and "]" in content

            # Should contain level
            assert "[INFO]" in content

            # Should contain message
            assert "Test message" in content


class TestGlobalLogger:
    """Test global logger functions."""

    def setup_method(self):
        """Reset global logger before each test."""
        # Import the module to access global variable
        import src.systems.logging_system as log_sys
        log_sys._global_logger = None

    def test_get_game_logger(self):
        """Test getting global logger instance."""
        logger1 = get_game_logger()
        logger2 = get_game_logger()

        # Should return same instance
        assert logger1 is logger2

    def test_init_game_logger(self):
        """Test initializing global logger with custom settings."""
        logger = init_game_logger(
            log_level=logging.DEBUG,
            log_to_file=False
        )

        assert logger is not None
        assert logger.logger.level == logging.DEBUG

    def test_module_level_debug(self):
        """Test module-level debug function."""
        # Should not raise exception
        debug("Debug message")

    def test_module_level_info(self):
        """Test module-level info function."""
        info("Info message")

    def test_module_level_warning(self):
        """Test module-level warning function."""
        warning("Warning message")

    def test_module_level_error(self):
        """Test module-level error function."""
        error("Error message")

    def test_module_level_critical(self):
        """Test module-level critical function."""
        critical("Critical message")

    def test_module_level_log_event(self):
        """Test module-level log_event function."""
        log_event("TEST_EVENT", "Test details")

    def test_module_level_log_performance(self):
        """Test module-level log_performance function."""
        log_performance("Test Operation", 100.5)


class TestLoggingLevels:
    """Test logging level filtering."""

    def test_debug_level_shows_all(self):
        """Test that DEBUG level shows all messages."""
        logger = GameLogger(log_level=logging.DEBUG, log_to_file=False)

        # All these should work without error
        logger.debug("Debug")
        logger.info("Info")
        logger.warning("Warning")
        logger.error("Error")
        logger.critical("Critical")

    def test_info_level_filters_debug(self):
        """Test that INFO level filters DEBUG messages."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"

            logger = GameLogger(
                log_level=logging.INFO,
                log_to_file=True,
                log_file_path=str(log_file)
            )

            logger.debug("Debug message")
            logger.info("Info message")

            content = log_file.read_text()

            # DEBUG should be filtered out
            assert "Debug message" not in content

            # INFO should be present
            assert "Info message" in content

    def test_warning_level_filters_info_and_debug(self):
        """Test that WARNING level filters INFO and DEBUG."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"

            logger = GameLogger(
                log_level=logging.WARNING,
                log_to_file=True,
                log_file_path=str(log_file)
            )

            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")

            content = log_file.read_text()

            assert "Debug message" not in content
            assert "Info message" not in content
            assert "Warning message" in content


class TestLoggingUseCases:
    """Test realistic logging use cases."""

    def test_game_startup_logging(self):
        """Test logging during game startup."""
        logger = GameLogger(log_to_file=False)

        logger.info("Game starting...")
        logger.info("Loading configuration...")
        logger.info("Initializing systems...")
        logger.info("Game ready!")

    def test_combat_event_logging(self):
        """Test logging combat events."""
        logger = GameLogger(log_to_file=False)

        logger.log_event("COMBAT_START", "Player vs Enemy")
        logger.log_event("ATTACK", "Player deals 10 damage")
        logger.log_event("ATTACK", "Enemy deals 5 damage")
        logger.log_event("COMBAT_END", "Player victory")

    def test_error_recovery_logging(self):
        """Test logging errors and recovery."""
        logger = GameLogger(log_to_file=False)

        logger.error("Failed to load save file")
        logger.info("Starting new game instead")

    def test_performance_monitoring(self):
        """Test performance logging."""
        logger = GameLogger(log_to_file=False)

        logger.log_performance("Dungeon Generation", 125.3)
        logger.log_performance("Pathfinding", 5.2)
        logger.log_performance("Rendering", 16.7)

    def test_debug_session(self):
        """Test typical debug session workflow."""
        logger = GameLogger(log_level=logging.DEBUG, log_to_file=False)

        logger.debug("Entering function: calculate_damage()")
        logger.debug(f"Parameters: attacker=Player, target=Enemy")
        logger.debug(f"Base damage: 10")
        logger.debug(f"Damage modifiers: +5")
        logger.debug(f"Final damage: 15")
        logger.info("Damage calculation complete")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
