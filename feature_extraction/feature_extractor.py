"""
Feature Extraction Module
Extracts exactly 57 features from pest images:
- Color features (RGB, HSV statistics)
- Texture features (GLCM)
- Shape features (contour area, perimeter)
- Edge features (Canny, Sobel statistics)
"""

import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops


class FeatureExtractor:
    """Extracts 57 features from pest images"""
    
    def __init__(self):
        """Initialize feature extractor"""
        self.num_features = 57
    
    def extract_features(self, image):
        """
        Extract 57 features from preprocessed image
        
        Args:
            image: Preprocessed image (RGB, normalized [0,1])
            
        Returns:
            numpy array of 57 features
        """
        # Convert to uint8 for OpenCV operations
        img_uint8 = (image * 255).astype(np.uint8)
        
        features = []
        
        # ========== COLOR FEATURES (24 features) ==========
        # RGB statistics (12 features: mean, std for each channel)
        r, g, b = cv2.split(img_uint8)
        features.extend([
            np.mean(r), np.std(r),
            np.mean(g), np.std(g),
            np.mean(b), np.std(b)
        ])
        
        # RGB min/max (6 features)
        features.extend([
            np.min(r), np.max(r),
            np.min(g), np.max(g),
            np.min(b), np.max(b)
        ])
        
        # HSV statistics (12 features: mean, std for each channel)
        hsv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        features.extend([
            np.mean(h), np.std(h),
            np.mean(s), np.std(s),
            np.mean(v), np.std(v)
        ])
        
        # HSV min/max (6 features)
        features.extend([
            np.min(h), np.max(h),
            np.min(s), np.max(s),
            np.min(v), np.max(v)
        ])
        
        # ========== TEXTURE FEATURES (16 features) ==========
        # Convert to grayscale for GLCM
        gray = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2GRAY)
        
        # GLCM features (4 properties x 4 angles = 16 features)
        # Using distances [1] and angles [0, 45, 90, 135]
        glcm = graycomatrix(gray, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], 
                           levels=256, symmetric=True, normed=True)
        
        # Extract GLCM properties
        contrast = graycoprops(glcm, 'contrast')[0]
        correlation = graycoprops(glcm, 'correlation')[0]
        energy = graycoprops(glcm, 'energy')[0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0]
        
        features.extend(contrast)  # 4 features
        features.extend(correlation)  # 4 features
        features.extend(energy)  # 4 features
        features.extend(homogeneity)  # 4 features
        
        # ========== SHAPE FEATURES (8 features) ==========
        # Convert to binary for contour detection
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # Get largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            # Additional shape features
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = float(w) / h if h > 0 else 0
            extent = float(area) / (w * h) if (w * h) > 0 else 0
            
            # Circularity
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            # Solidity
            hull = cv2.convexHull(largest_contour)
            hull_area = cv2.contourArea(hull)
            solidity = float(area) / hull_area if hull_area > 0 else 0
            
            features.extend([area, perimeter, aspect_ratio, extent, circularity, solidity, w, h])
        else:
            # Default values if no contours found
            features.extend([0, 0, 0, 0, 0, 0, 0, 0])
        
        # ========== EDGE FEATURES (9 features) ==========
        # Canny edge detection
        canny = cv2.Canny(gray, 50, 150)
        canny_pixels = np.sum(canny > 0)
        canny_density = canny_pixels / (gray.shape[0] * gray.shape[1])
        canny_mean = np.mean(canny)
        features.extend([canny_pixels, canny_density, canny_mean])
        
        # Sobel edge detection
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        sobel_mean = np.mean(sobel_magnitude)
        sobel_std = np.std(sobel_magnitude)
        sobel_max = np.max(sobel_magnitude)
        sobel_min = np.min(sobel_magnitude)
        sobel_sum = np.sum(sobel_magnitude)
        
        features.extend([sobel_mean, sobel_std, sobel_max, sobel_min, sobel_sum])
        
        # Convert to numpy array and ensure exactly 57 features
        features = np.array(features, dtype=np.float32)
        
        # Pad or truncate to exactly 57 features
        if len(features) < 57:
            # Pad with zeros if needed
            features = np.pad(features, (0, 57 - len(features)), 'constant')
        elif len(features) > 57:
            # Truncate if needed
            features = features[:57]
        
        return features

