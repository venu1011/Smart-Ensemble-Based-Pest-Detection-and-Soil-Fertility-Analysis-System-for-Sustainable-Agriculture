"""
Ensemble Model
Combines CNN and classical ML models using weighted voting
"""

import numpy as np


class EnsemblePredictor:
    """Ensemble predictor combining CNN and ML models"""
    
    def __init__(self, cnn_predictor, ml_predictor, num_classes=4):
        """
        Initialize ensemble predictor
        
        Args:
            cnn_predictor: CNN predictor instance
            ml_predictor: ML predictor instance
            num_classes: Number of pest classes
        """
        self.cnn_predictor = cnn_predictor
        self.ml_predictor = ml_predictor
        self.num_classes = num_classes
        
        # Weights for ensemble (CNN gets higher weight as it's more powerful)
        self.cnn_weight = 0.5
        self.ml_weight = 0.5
        self.ml_model_weights = {
            'rf': 0.4,   # Random Forest gets highest weight among ML models
            'svm': 0.35,
            'knn': 0.25
        }
    
    def predict(self, image, features):
        """
        Ensemble prediction combining CNN and ML models
        
        Args:
            image: Preprocessed image for CNN
            features: Extracted features for ML models
            
        Returns:
            Dictionary containing:
                - class: Predicted class index
                - confidence: Confidence score (0-100)
                - probabilities: Probability distribution over classes
                - cnn_prediction: CNN prediction details
                - ml_prediction: ML prediction details
        """
        # CNN prediction
        cnn_class, cnn_confidence, cnn_probs = self.cnn_predictor.predict(image)
        
        # Handle CNN output shape mismatch (CNN may have been trained with more classes)
        # If CNN was trained with 5 classes including 'archive' at index 1, we need to skip it
        if len(cnn_probs) > self.num_classes:
            # CNN has more classes - this likely means it was trained with 'archive' included
            # Expected CNN class order: [Aphids(0), archive(1), Beetles(2), Caterpillars(3), Locusts(4)]
            # Desired order: [Aphids, Beetles, Caterpillars, Locusts] = indices [0, 2, 3, 4]
            if len(cnn_probs) == 5:
                # Skip index 1 (archive) and take indices [0, 2, 3, 4]
                cnn_probs = np.array([cnn_probs[0], cnn_probs[2], cnn_probs[3], cnn_probs[4]])
                # Map CNN class index: if cnn_class is 1 (archive), find next best; otherwise map correctly
                if cnn_class == 1:  # archive class
                    # Find the next best class (excluding archive)
                    cnn_class = np.argmax([cnn_probs[0], cnn_probs[1], cnn_probs[2], cnn_probs[3]])
                    cnn_confidence = float(cnn_probs[cnn_class]) * 100
                elif cnn_class > 1:  # Beetles, Caterpillars, or Locusts (indices 2,3,4 -> 1,2,3)
                    cnn_class = cnn_class - 1
                    cnn_confidence = float(cnn_probs[cnn_class]) * 100
                # If cnn_class is 0 (Aphids), it stays 0, no change needed
            else:
                # Fallback: just take first num_classes
                cnn_probs = cnn_probs[:self.num_classes]
                cnn_probs = cnn_probs / np.sum(cnn_probs)  # Renormalize
                if cnn_class >= self.num_classes:
                    cnn_class = np.argmax(cnn_probs)
                    cnn_confidence = float(cnn_probs[cnn_class]) * 100
        elif len(cnn_probs) < self.num_classes:
            # CNN has fewer classes - pad with zeros (shouldn't happen, but handle it)
            padding = np.zeros(self.num_classes - len(cnn_probs))
            cnn_probs = np.concatenate([cnn_probs, padding])
            cnn_probs = cnn_probs / np.sum(cnn_probs)  # Renormalize
        
        # ML prediction
        ml_predictions = self.ml_predictor.predict(features)
        
        # Combine ML model probabilities using weighted average
        ml_combined_probs = np.zeros(self.num_classes)
        for model_name, pred in ml_predictions.items():
            weight = self.ml_model_weights[model_name]
            ml_combined_probs += weight * pred['probabilities']
        
        # Normalize ML probabilities
        ml_combined_probs = ml_combined_probs / np.sum(ml_combined_probs)
        ml_class = np.argmax(ml_combined_probs)
        ml_confidence = float(ml_combined_probs[ml_class]) * 100
        
        # Ensemble: weighted average of CNN and ML probabilities
        ensemble_probs = (
            self.cnn_weight * cnn_probs + 
            self.ml_weight * ml_combined_probs
        )
        ensemble_probs = ensemble_probs / np.sum(ensemble_probs)  # Normalize
        
        # Final prediction
        ensemble_class = np.argmax(ensemble_probs)
        ensemble_confidence = float(ensemble_probs[ensemble_class]) * 100
        
        return {
            'class': int(ensemble_class),
            'confidence': round(ensemble_confidence, 2),
            'probabilities': ensemble_probs.tolist(),
            'cnn_prediction': {
                'class': int(cnn_class),
                'confidence': round(cnn_confidence, 2)
            },
            'ml_prediction': {
                'class': int(ml_class),
                'confidence': round(ml_confidence, 2),
                'individual_predictions': {
                    name: {
                        'class': int(pred['class']),
                        'confidence': round(float(pred['probabilities'][pred['class']]) * 100, 2)
                    }
                    for name, pred in ml_predictions.items()
                }
            }
        }

