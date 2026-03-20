"""
Image Preprocessing Module
Handles image preprocessing operations using OpenCV
"""

import cv2
import numpy as np


class ImagePreprocessor:
    """Handles image preprocessing operations"""
    
    def __init__(self, target_size=(224, 224)):
        """
        Initialize preprocessor
        
        Args:
            target_size: Target image size (width, height)
        """
        self.target_size = target_size
    
    def preprocess(self, image_path):
        """
        Preprocess image: resize, denoise, enhance contrast, normalize
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image (numpy array)
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image
        image = cv2.resize(image, self.target_size)
        
        # Denoise using bilateral filter (preserves edges)
        image = cv2.bilateralFilter(image, 9, 75, 75)
        
        # Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        image = cv2.merge([l, a, b])
        image = cv2.cvtColor(image, cv2.COLOR_LAB2RGB)
        
        # Normalize to [0, 1]
        image = image.astype(np.float32) / 255.0
        
        return image
    
    def preprocess_array(self, image_array):
        """
        Preprocess image array (already loaded in memory)
        
        Args:
            image_array: Image as numpy array (RGB format)
            
        Returns:
            Preprocessed image (numpy array)
        """
        # Ensure RGB format
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            # Check if BGR (OpenCV default)
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        
        # Resize
        image_array = cv2.resize(image_array, self.target_size)
        
        # Denoise
        image_array = cv2.bilateralFilter(image_array, 9, 75, 75)
        
        # Enhance contrast
        lab = cv2.cvtColor(image_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        image_array = cv2.merge([l, a, b])
        image_array = cv2.cvtColor(image_array, cv2.COLOR_LAB2RGB)
        
        # Normalize
        image_array = image_array.astype(np.float32) / 255.0
        
        return image_array

