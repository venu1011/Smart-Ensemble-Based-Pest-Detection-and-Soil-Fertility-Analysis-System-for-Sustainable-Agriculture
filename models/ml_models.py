"""
Classical Machine Learning Models
Random Forest, SVM, and KNN for pest classification
"""

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


class MLModelTrainer:
    """Train classical ML models for pest classification"""
    
    def __init__(self):
        """Initialize ML model trainer"""
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
        self.svm_model = SVC(
            kernel='rbf',
            probability=True,
            random_state=42,
            C=1.0,
            gamma='scale'
        )
        self.knn_model = KNeighborsClassifier(
            n_neighbors=5,
            weights='distance',
            n_jobs=-1
        )
        self.scaler = StandardScaler()
    
    def train(self, X_train, y_train):
        """
        Train all ML models
        
        Args:
            X_train: Training features (n_samples, n_features)
            y_train: Training labels (n_samples,)
        """
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train models
        print("Training Random Forest...")
        self.rf_model.fit(X_train_scaled, y_train)
        
        print("Training SVM...")
        self.svm_model.fit(X_train_scaled, y_train)
        
        print("Training KNN...")
        self.knn_model.fit(X_train_scaled, y_train)
    
    def save_models(self, base_path):
        """
        Save all models and scaler
        
        Args:
            base_path: Base path for saving models
        """
        joblib.dump(self.rf_model, f"{base_path}/rf_model.pkl")
        joblib.dump(self.svm_model, f"{base_path}/svm_model.pkl")
        joblib.dump(self.knn_model, f"{base_path}/knn_model.pkl")
        joblib.dump(self.scaler, f"{base_path}/scaler.pkl")
    
    @staticmethod
    def load_models(base_path):
        """
        Load all models and scaler
        
        Args:
            base_path: Base path for loading models
            
        Returns:
            Dictionary containing models and scaler
        """
        return {
            'rf': joblib.load(f"{base_path}/rf_model.pkl"),
            'svm': joblib.load(f"{base_path}/svm_model.pkl"),
            'knn': joblib.load(f"{base_path}/knn_model.pkl"),
            'scaler': joblib.load(f"{base_path}/scaler.pkl")
        }


class MLPredictor:
    """Wrapper class for ML model predictions"""
    
    def __init__(self, models_dict=None, models_path=None):
        """
        Initialize ML predictor
        
        Args:
            models_dict: Dictionary containing models and scaler (optional)
            models_path: Path to saved models directory (optional)
        """
        if models_dict:
            self.models = models_dict
        elif models_path:
            self.models = MLModelTrainer.load_models(models_path)
        else:
            raise ValueError("Either models_dict or models_path must be provided")
    
    def predict(self, features):
        """
        Predict pest class from features
        
        Args:
            features: Feature vector (n_features,) or (1, n_features)
            
        Returns:
            Dictionary with predictions from each model
        """
        # Ensure 2D array
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = self.models['scaler'].transform(features)
        
        # Get predictions from each model
        predictions = {
            'rf': {
                'class': self.models['rf'].predict(features_scaled)[0],
                'probabilities': self.models['rf'].predict_proba(features_scaled)[0]
            },
            'svm': {
                'class': self.models['svm'].predict(features_scaled)[0],
                'probabilities': self.models['svm'].predict_proba(features_scaled)[0]
            },
            'knn': {
                'class': self.models['knn'].predict(features_scaled)[0],
                'probabilities': self.models['knn'].predict_proba(features_scaled)[0]
            }
        }
        
        return predictions

