"""
Training Script for Pest Detection Models
Trains CNN and ML models on pest image dataset
"""

import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras

from preprocessing.image_preprocessing import ImagePreprocessor
from feature_extraction.feature_extractor import FeatureExtractor
from models.cnn_model import create_lightweight_cnn
from models.ml_models import MLModelTrainer


def load_dataset(dataset_path, image_size=(224, 224)):
    """
    Load dataset from folder structure
    
    Expected structure:
    dataset/
        Aphids/
            img1.jpg
            img2.jpg
            ...
        Locusts/
            img1.jpg
            ...
        ...
    
    Args:
        dataset_path: Path to dataset directory
        image_size: Target image size
        
    Returns:
        Tuple (images, labels, class_names)
    """
    images = []
    labels = []
    class_names = []
    
    # Get class folders (exclude 'archive' and other non-class folders)
    exclude_folders = {'archive', '__pycache__', '.git'}
    class_folders = [f for f in os.listdir(dataset_path) 
                     if os.path.isdir(os.path.join(dataset_path, f)) 
                     and f not in exclude_folders]
    class_folders.sort()  # Ensure consistent ordering
    
    print(f"Found classes: {class_folders}")
    
    for class_idx, class_name in enumerate(class_folders):
        class_path = os.path.join(dataset_path, class_name)
        class_names.append(class_name)
        
        # Get all images in class folder
        image_files = [f for f in os.listdir(class_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        
        print(f"Loading {len(image_files)} images from {class_name}...")
        
        for img_file in image_files:
            img_path = os.path.join(class_path, img_file)
            try:
                # Load and resize image
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, image_size)
                    images.append(img)
                    labels.append(class_idx)
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
                continue
    
    return np.array(images), np.array(labels), class_names


def train_cnn(X_train, y_train, X_val, y_val, num_classes, model_save_path='models/cnn_model.h5'):
    """
    Train CNN model
    
    Args:
        X_train: Training images
        y_train: Training labels
        X_val: Validation images
        y_val: Validation labels
        num_classes: Number of classes
        model_save_path: Path to save trained model
    """
    print("\n" + "="*50)
    print("Training CNN Model")
    print("="*50)
    
    # Normalize images
    X_train_norm = X_train.astype(np.float32) / 255.0
    X_val_norm = X_val.astype(np.float32) / 255.0
    
    # Create model
    model = create_lightweight_cnn(input_shape=(224, 224, 3), num_classes=num_classes)
    
    # Print model summary
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(model_save_path, save_best_only=True, monitor='val_loss'),
        keras.callbacks.ReduceLROnPlateau(patience=5, factor=0.5, min_lr=1e-7)
    ]
    
    # Train model
    history = model.fit(
        X_train_norm, y_train,
        batch_size=32,
        epochs=50,
        validation_data=(X_val_norm, y_val),
        callbacks=callbacks,
        verbose=1
    )
    
    print(f"\nCNN model saved to {model_save_path}")
    return model, history


def train_ml_models(X_train, y_train, model_save_path='models'):
    """
    Train ML models (RF, SVM, KNN)
    
    Args:
        X_train: Training features
        y_train: Training labels
        model_save_path: Path to save models
    """
    print("\n" + "="*50)
    print("Training ML Models")
    print("="*50)
    
    # Extract features for ML models
    print("Extracting features...")
    preprocessor = ImagePreprocessor()
    feature_extractor = FeatureExtractor()
    
    X_features = []
    for img in X_train:
        # Preprocess image
        preprocessed = preprocessor.preprocess_array(img)
        # Extract features
        features = feature_extractor.extract_features(preprocessed)
        X_features.append(features)
    
    X_features = np.array(X_features)
    print(f"Extracted {X_features.shape[1]} features from {X_features.shape[0]} images")
    
    # Train ML models
    trainer = MLModelTrainer()
    trainer.train(X_features, y_train)
    
    # Save models
    os.makedirs(model_save_path, exist_ok=True)
    trainer.save_models(model_save_path)
    
    print(f"\nML models saved to {model_save_path}/")
    return X_features


def main():
    """Main training function"""
    # Configuration
    DATASET_PATH = 'dataset'
    CNN_MODEL_PATH = 'models/cnn_model.h5'
    ML_MODEL_PATH = 'models'
    
    # Check if dataset exists
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset path '{DATASET_PATH}' not found!")
        print("Please create a dataset folder with the following structure:")
        print("dataset/")
        print("  Aphids/")
        print("    img1.jpg")
        print("    ...")
        print("  Locusts/")
        print("    ...")
        print("  Beetles/")
        print("    ...")
        print("  Caterpillars/")
        print("    ...")
        return
    
    # Load dataset
    print("Loading dataset...")
    images, labels, class_names = load_dataset(DATASET_PATH)
    
    if len(images) == 0:
        print("No images found in dataset!")
        return
    
    print(f"\nTotal images: {len(images)}")
    print(f"Classes: {class_names}")
    print(f"Class distribution: {np.bincount(labels)}")
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    print(f"\nTrain set: {len(X_train)}")
    print(f"Validation set: {len(X_val)}")
    print(f"Test set: {len(X_test)}")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Train CNN
    num_classes = len(class_names)
    cnn_model, cnn_history = train_cnn(
        X_train, y_train, X_val, y_val, 
        num_classes, CNN_MODEL_PATH
    )
    
    # Train ML models
    train_ml_models(X_train, y_train, ML_MODEL_PATH)
    
    # Save class names
    import pickle
    with open('models/class_names.pkl', 'wb') as f:
        pickle.dump(class_names, f)
    
    print("\n" + "="*50)
    print("Training Complete!")
    print("="*50)
    print(f"CNN model: {CNN_MODEL_PATH}")
    print(f"ML models: {ML_MODEL_PATH}/")
    print(f"Class names: models/class_names.pkl")


if __name__ == '__main__':
    main()

