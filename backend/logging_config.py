"""
Structured Logging Configuration for Math Mentor
Provides consistent logging across all modules.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = "math_mentor",
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up a structured logger with consistent formatting.
    
    Args:
        name: Logger name (usually __name__ of the module)
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        format_string: Custom format string (optional)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format
    if format_string is None:
        format_string = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


# Pre-configured loggers for each module
def get_solver_logger() -> logging.Logger:
    return setup_logger("math_mentor.solver")


def get_executor_logger() -> logging.Logger:
    return setup_logger("math_mentor.executor")


def get_ocr_logger() -> logging.Logger:
    return setup_logger("math_mentor.ocr")


def get_parser_logger() -> logging.Logger:
    return setup_logger("math_mentor.parser")


def get_deck_logger() -> logging.Logger:
    return setup_logger("math_mentor.deck_generator")


# Convenience: get logger for any module
def get_logger(module_name: str) -> logging.Logger:
    return setup_logger(f"math_mentor.{module_name}")
