"""
Logging System for Game Events

This module provides a centralized logging system for tracking game events,
debugging issues, and monitoring game state.

Educational Notes:
------------------
Logging is critical for debugging and monitoring applications. It provides:
1. Event tracking (what happened when)
2. Error diagnostics (why did it crash)
3. Performance monitoring (how long did it take)
4. Audit trails (who did what)

Python's logging module provides multiple log levels:
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages for unexpected situations
- ERROR: Error messages for serious problems
- CRITICAL: Critical errors that may cause shutdown
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class GameLogger:
    """
    Centralized logging system for the game.

    Provides structured logging with different levels and output destinations.

    Educational Note:
        Using a centralized logger ensures consistent formatting and makes it
        easy to change logging behavior across the entire application.

    Example:
        >>> game_logger = GameLogger("OBDIIGame")
        >>> game_logger.info("Game started")
        >>> game_logger.debug(f"Player position: ({x}, {y})")
        >>> game_logger.error("Failed to load save file")
    """

    def __init__(
        self,
        name: str = "OBDIIGame",
        log_level: int = logging.INFO,
        log_to_file: bool = True,
        log_file_path: Optional[str] = None
    ):
        """
        Initialize the game logger.

        Args:
            name: Logger name (typically application name)
            log_level: Minimum level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Whether to write logs to file
            log_file_path: Path to log file (defaults to logs/game.log)

        Educational Note:
            Log levels filter messages:
            - If log_level is INFO, DEBUG messages are suppressed
            - If log_level is WARNING, INFO and DEBUG are suppressed
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Clear any existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Create formatter for consistent log format
        # Format: [TIMESTAMP] [LEVEL] [MODULE] Message
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler (outputs to terminal)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler (outputs to log file)
        if log_to_file:
            if log_file_path is None:
                # Default to logs/game.log
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)
                log_file_path = log_dir / "game.log"
            else:
                # Create parent directories if they don't exist
                log_file = Path(log_file_path)
                log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self.info(f"GameLogger initialized (level: {logging.getLevelName(log_level)})")

    def debug(self, message: str) -> None:
        """
        Log debug message.

        Args:
            message: Debug message to log

        Educational Note:
            Use DEBUG for detailed diagnostic information useful during
            development but too verbose for production.

        Example:
            >>> logger.debug(f"Pathfinding: checking tile ({x}, {y})")
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """
        Log informational message.

        Args:
            message: Info message to log

        Educational Note:
            Use INFO for general events that are normal but worth recording:
            - Game started/stopped
            - Level loaded
            - Player reached checkpoint

        Example:
            >>> logger.info("Floor 1 loaded successfully")
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """
        Log warning message.

        Args:
            message: Warning message to log

        Educational Note:
            Use WARNING for unexpected situations that aren't errors:
            - Missing optional configuration
            - Deprecated feature usage
            - Resource constraints

        Example:
            >>> logger.warning("Floor ID mismatch in config file")
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """
        Log error message.

        Args:
            message: Error message to log

        Educational Note:
            Use ERROR for serious problems that prevent some functionality:
            - File not found
            - Parse errors
            - Component failures

        Example:
            >>> logger.error("Failed to load save file: corrupted data")
        """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """
        Log critical message.

        Args:
            message: Critical message to log

        Educational Note:
            Use CRITICAL for severe errors that may cause shutdown:
            - Unrecoverable errors
            - System failures
            - Fatal exceptions

        Example:
            >>> logger.critical("Game initialization failed - shutting down")
        """
        self.logger.critical(message)

    def log_event(self, event_type: str, details: str = "") -> None:
        """
        Log a game event with structured format.

        Args:
            event_type: Type of event (e.g., "PLAYER_DEATH", "LEVEL_COMPLETE")
            details: Additional event details

        Educational Note:
            Structured event logging makes it easier to:
            - Parse logs programmatically
            - Generate statistics
            - Debug specific event types

        Example:
            >>> logger.log_event("COMBAT", "Player attacked Enemy (damage: 10)")
            >>> logger.log_event("ITEM_PICKUP", "Player picked up Health Potion")
        """
        message = f"[EVENT:{event_type}] {details}" if details else f"[EVENT:{event_type}]"
        self.logger.info(message)

    def log_performance(self, operation: str, duration_ms: float) -> None:
        """
        Log performance metrics.

        Args:
            operation: Name of the operation
            duration_ms: Duration in milliseconds

        Educational Note:
            Performance logging helps identify bottlenecks:
            - Slow dungeon generation
            - Expensive pathfinding
            - Laggy rendering

        Example:
            >>> import time
            >>> start = time.time()
            >>> # ... do expensive operation ...
            >>> duration = (time.time() - start) * 1000
            >>> logger.log_performance("Dungeon Generation", duration)
        """
        self.logger.info(f"[PERFORMANCE] {operation}: {duration_ms:.2f}ms")

    def set_level(self, level: int) -> None:
        """
        Change logging level at runtime.

        Args:
            level: New log level (use logging.DEBUG, logging.INFO, etc.)

        Educational Note:
            Dynamically changing log levels is useful for:
            - Enabling verbose logging when debugging
            - Reducing log spam in production
            - Temporary diagnostic mode

        Example:
            >>> logger.set_level(logging.DEBUG)  # Enable verbose logging
            >>> # ... debug issue ...
            >>> logger.set_level(logging.INFO)   # Back to normal
        """
        self.logger.setLevel(level)
        self.info(f"Log level changed to {logging.getLevelName(level)}")


# Global logger instance for convenient access
# Educational Note: Using a global logger simplifies logging across modules
_global_logger: Optional[GameLogger] = None


def get_game_logger() -> GameLogger:
    """
    Get the global game logger instance.

    Returns:
        Global GameLogger instance

    Educational Note:
        Singleton pattern ensures all modules use the same logger,
        making it easy to configure logging in one place.

    Example:
        >>> from src.systems.logging_system import get_game_logger
        >>> logger = get_game_logger()
        >>> logger.info("Using global logger")
    """
    global _global_logger

    if _global_logger is None:
        _global_logger = GameLogger()

    return _global_logger


def init_game_logger(
    log_level: int = logging.INFO,
    log_to_file: bool = True,
    log_file_path: Optional[str] = None
) -> GameLogger:
    """
    Initialize the global game logger with custom settings.

    Args:
        log_level: Minimum level to log
        log_to_file: Whether to write logs to file
        log_file_path: Path to log file

    Returns:
        Initialized GameLogger instance

    Educational Note:
        Call this at application startup to configure logging.
        If not called, get_game_logger() creates a default logger.

    Example:
        >>> # At application startup
        >>> logger = init_game_logger(
        ...     log_level=logging.DEBUG,
        ...     log_to_file=True,
        ...     log_file_path="logs/debug.log"
        ... )
    """
    global _global_logger

    _global_logger = GameLogger(
        log_level=log_level,
        log_to_file=log_to_file,
        log_file_path=log_file_path
    )

    return _global_logger


# Convenience module-level functions
# Educational Note: These make logging even simpler for quick usage

def debug(message: str) -> None:
    """Log debug message using global logger."""
    get_game_logger().debug(message)


def info(message: str) -> None:
    """Log info message using global logger."""
    get_game_logger().info(message)


def warning(message: str) -> None:
    """Log warning message using global logger."""
    get_game_logger().warning(message)


def error(message: str) -> None:
    """Log error message using global logger."""
    get_game_logger().error(message)


def critical(message: str) -> None:
    """Log critical message using global logger."""
    get_game_logger().critical(message)


def log_event(event_type: str, details: str = "") -> None:
    """Log game event using global logger."""
    get_game_logger().log_event(event_type, details)


def log_performance(operation: str, duration_ms: float) -> None:
    """Log performance metric using global logger."""
    get_game_logger().log_performance(operation, duration_ms)
