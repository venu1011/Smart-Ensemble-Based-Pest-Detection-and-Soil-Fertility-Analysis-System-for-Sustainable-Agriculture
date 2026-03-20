# Project Structure

## Core Application Files

- `app.py` - Main Flask application
- `train_models.py` - Model training script
- `requirements.txt` - Python dependencies

## Documentation

- `README.md` - Complete project documentation
- `QUICKSTART.md` - Quick start guide
- `FINAL_RESULTS.md` - Training results and performance metrics

## Project Modules

- `preprocessing/` - Image preprocessing
- `feature_extraction/` - Feature extraction (57 features)
- `models/` - Model definitions and trained models
- `ensemble/` - Ensemble predictor
- `soil_analysis/` - NPK soil analysis
- `recommendations/` - Recommendation engine

## Web Interface

- `templates/` - HTML templates (Bootstrap 5)
- `static/` - Static files (CSS, JS, uploads)

## Data

- `dataset/` - Training dataset (organized into class folders)
  - `Aphids/` - 499 images
  - `Beetles/` - 416 images
  - `Caterpillars/` - 434 images
  - `Locusts/` - 485 images
  - `archive/` - Original dataset archive (optional, can be removed to save space)

## Trained Models (in `models/` directory)

- `cnn_model.h5` - CNN model (16.4 MB)
- `rf_model.pkl` - Random Forest model (5.3 MB)
- `svm_model.pkl` - SVM model (551 KB)
- `knn_model.pkl` - KNN model (271 KB)
- `scaler.pkl` - Feature scaler
- `class_names.pkl` - Class names mapping

