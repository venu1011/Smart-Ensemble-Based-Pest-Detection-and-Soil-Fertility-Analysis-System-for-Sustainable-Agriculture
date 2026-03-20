"""
Helper utility functions
"""

import os
import pickle
import logging
from pathlib import Path
from typing import Tuple, Optional, List
from werkzeug.utils import secure_filename

from config.settings import Config

logger = logging.getLogger(__name__)


def allowed_file(filename: str, allowed_extensions: set = None) -> bool:
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file to check
        allowed_extensions: Set of allowed extensions (defaults to Config.ALLOWED_EXTENSIONS)
        
    Returns:
        True if file extension is allowed, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = Config.ALLOWED_EXTENSIONS
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def ensure_directory(directory: Path) -> None:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Path to directory
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        raise


def load_class_names(file_path: Path, default: List[str] = None) -> List[str]:
    """
    Load class names from pickle file
    
    Args:
        file_path: Path to class names pickle file
        default: Default class names if file doesn't exist
        
    Returns:
        List of class names
    """
    if default is None:
        default = Config.DEFAULT_CLASS_NAMES
    
    if not file_path.exists():
        logger.warning(f"Class names file not found at {file_path}, using defaults")
        return default
    
    try:
        with open(file_path, 'rb') as f:
            class_names = pickle.load(f)
            logger.info(f"Loaded class names: {class_names}")
            return class_names
    except Exception as e:
        logger.error(f"Error loading class names from {file_path}: {e}")
        return default


def validate_npk_values(nitrogen: str, phosphorus: str, potassium: str) -> Tuple[float, float, float]:
    """
    Validate and convert NPK values to float
    
    Args:
        nitrogen: Nitrogen value as string
        phosphorus: Phosphorus value as string
        potassium: Potassium value as string
        
    Returns:
        Tuple of (nitrogen, phosphorus, potassium) as floats
        
    Raises:
        ValueError: If values cannot be converted to float or are negative
    """
    try:
        n = float(nitrogen) if nitrogen else 0.0
        p = float(phosphorus) if phosphorus else 0.0
        k = float(potassium) if potassium else 0.0
        
        # Validate non-negative
        if n < 0 or p < 0 or k < 0:
            raise ValueError("NPK values cannot be negative")
        
        return n, p, k
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid NPK values: {e}")


def secure_file_path(filename: str, upload_folder: Path) -> Path:
    """
    Get secure file path for upload
    
    Args:
        filename: Original filename
        upload_folder: Upload folder path
        
    Returns:
        Secure file path
    """
    secure_name = secure_filename(filename)
    return upload_folder / secure_name

