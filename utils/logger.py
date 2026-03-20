"""
Logging configuration
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from config.settings import Config


def setup_logger(
    name: str = 'app',
    log_level: str = None,
    log_file: Optional[str] = None,
    log_dir: Path = None
) -> logging.Logger:
    """
    Setup application logger
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Log file name (optional)
        log_dir: Log directory path
        
    Returns:
        Configured logger instance
    """
    if log_level is None:
        log_level = Config.LOG_LEVEL
    
    if log_dir is None:
        log_dir = Config.LOG_DIR
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    console_format = logging.Formatter(Config.LOG_FORMAT, Config.LOG_DATE_FORMAT)
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / log_file
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(Config.LOG_FORMAT, Config.LOG_DATE_FORMAT)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

