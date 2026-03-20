"""
CNN Model for Pest Detection
Lightweight CNN using TensorFlow/Keras (CPU-only)
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


def create_lightweight_cnn(input_shape=(224, 224, 3), num_classes=4):
    """
    Create a lightweight CNN model for pest classification
    
    Args:
        input_shape: Input image shape (height, width, channels)
        num_classes: Number of pest classes
        
    Returns:
        Compiled Keras model
    """
    model = keras.Sequential([
        # First Conv Block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second Conv Block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third Conv Block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth Conv Block (lightweight)
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Flatten and Dense layers
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def load_cnn_model(model_path):
    """
    Load a saved CNN model
    
    Args:
        model_path: Path to saved model
        
    Returns:
        Loaded Keras model
    """
    return keras.models.load_model(model_path)


class CNNPredictor:
    """Wrapper class for CNN prediction"""
    
    def __init__(self, model=None, model_path=None):
        """
        Initialize CNN predictor
        
        Args:
            model: Pre-loaded Keras model (optional)
            model_path: Path to saved model (optional)
        """
        if model:
            self.model = model
        elif model_path:
            self.model = load_cnn_model(model_path)
        else:
            raise ValueError("Either model or model_path must be provided")
    
    def predict(self, image):
        """
        Predict pest class from image
        
        Args:
            image: Preprocessed image (numpy array, shape: (H, W, 3))
            
        Returns:
            Tuple (predicted_class_index, confidence_score, all_probabilities)
        """
        # Expand dimensions to add batch dimension
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Predict
        probabilities = self.model.predict(image, verbose=0)[0]
        predicted_class = np.argmax(probabilities)
        confidence = float(probabilities[predicted_class]) * 100
        
        return predicted_class, confidence, probabilities

