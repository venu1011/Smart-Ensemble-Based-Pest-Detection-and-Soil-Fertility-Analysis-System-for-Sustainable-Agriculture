"""
Application Configuration Settings
"""

import os
from pathlib import Path
from typing import List, Set


class Config:
    """Base configuration class"""
    
    # Application
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = False
    TESTING: bool = False
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    MODEL_DIR: Path = BASE_DIR / 'models'
    DATASET_DIR: Path = BASE_DIR / 'dataset'
    UPLOAD_FOLDER: Path = BASE_DIR / 'static' / 'uploads'
    LOG_DIR: Path = BASE_DIR / 'logs'
    
    # File upload
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: Set[str] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # Model files
    CNN_MODEL_FILE: str = 'cnn_model.h5'
    RF_MODEL_FILE: str = 'rf_model.pkl'
    SVM_MODEL_FILE: str = 'svm_model.pkl'
    KNN_MODEL_FILE: str = 'knn_model.pkl'
    SCALER_FILE: str = 'scaler.pkl'
    CLASS_NAMES_FILE: str = 'class_names.pkl'
    
    # Default class names
    DEFAULT_CLASS_NAMES: List[str] = ['Aphids', 'Beetles', 'Caterpillars', 'Locusts']
    
    # Feature extraction
    NUM_FEATURES: int = 57
    IMAGE_SIZE: tuple = (224, 224)
    
    # Ensemble weights
    CNN_WEIGHT: float = 0.5
    ML_WEIGHT: float = 0.5
    RF_WEIGHT: float = 0.4
    SVM_WEIGHT: float = 0.35
    KNN_WEIGHT: float = 0.25
    
    # Logging
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE: str = 'app.log'
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'
    
    @classmethod
    def get_cnn_model_path(cls) -> Path:
        """Get path to CNN model file"""
        return cls.MODEL_DIR / cls.CNN_MODEL_FILE
    
    @classmethod
    def get_class_names_path(cls) -> Path:
        """Get path to class names file"""
        return cls.MODEL_DIR / cls.CLASS_NAMES_FILE
    
    @classmethod
    def get_ml_model_files(cls) -> List[str]:
        """Get list of ML model file names"""
        return [
            cls.RF_MODEL_FILE,
            cls.SVM_MODEL_FILE,
            cls.KNN_MODEL_FILE,
            cls.SCALER_FILE
        ]
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist"""
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.MODEL_DIR.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG: bool = True
    LOG_LEVEL: str = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG: bool = False
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    LOG_LEVEL: str = 'WARNING'
    
    @classmethod
    def validate(cls) -> None:
        """Validate production configuration"""
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set in production environment")


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:
    """
    Get configuration class based on environment
    
    Args:
        config_name: Configuration name ('development', 'production', etc.)
        
    Returns:
        Configuration class instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])

