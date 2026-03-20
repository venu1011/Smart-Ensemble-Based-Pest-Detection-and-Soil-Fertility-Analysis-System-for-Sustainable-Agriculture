# Smart Pest & Soil Fertility Analysis System

A production-grade intelligent system for pest detection and soil fertility analysis using Machine Learning and Deep Learning ensemble methods, optimized for rural, low-resource agricultural environments.

## 🎯 System Overview

This system combines:
- **Computer Vision**: Deep Learning CNN for pest image classification
- **Machine Learning**: Ensemble of Random Forest, SVM, and KNN models
- **Image Processing**: Advanced feature extraction (57 features)
- **Soil Analysis**: NPK-based fertility assessment
- **Recommendation Engine**: Intelligent pest control and fertilizer recommendations

## 📋 Features

- **Pest Detection**: Identifies 4 common pests (Aphids, Locusts, Beetles, Caterpillars)
- **Soil Fertility Analysis**: Analyzes NPK (Nitrogen, Phosphorus, Potassium) levels
- **Ensemble Prediction**: Combines CNN and ML models for improved accuracy
- **Feature Extraction**: Extracts exactly 57 features (color, texture, shape, edge)
- **Real-time Analysis**: Fast inference optimized for CPU-only environments
- **Modern UI**: Beautiful Bootstrap 5 interface with responsive design
- **Production Ready**: Logging, error handling, configuration management

## 🏗️ System Architecture

```
Smart Pest & Soil Analysis System
├── Configuration Management (config/)
├── Image Preprocessing (preprocessing/)
├── Feature Extraction (feature_extraction/) - 57 features
├── Deep Learning Model (models/cnn_model.py)
├── Classical ML Models (models/ml_models.py)
│   ├── Random Forest
│   ├── Support Vector Machine (SVM)
│   └── K-Nearest Neighbors (KNN)
├── Ensemble Predictor (ensemble/)
├── Soil Analyzer (soil_analysis/)
└── Recommendation Engine (recommendations/)
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd soil_prediction
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: TensorFlow installation may take some time. The system is designed to work with CPU-only TensorFlow.

### Step 3: Configure Environment (Optional)

Copy `.env.example` to `.env` and modify if needed:

```bash
cp .env.example .env
```

### Step 4: Prepare Dataset (Optional for Training)

Create a dataset folder with the following structure:

```
dataset/
├── Aphids/
│   ├── image1.jpg
│   └── ...
├── Locusts/
│   ├── image1.jpg
│   └── ...
├── Beetles/
│   └── ...
└── Caterpillars/
    └── ...
```

### Step 5: Train Models (Optional)

If you have a dataset, train the models:

```bash
python train_models.py
```

This will:
- Load images from the `dataset/` folder
- Preprocess and extract features
- Train CNN model
- Train ML models (RF, SVM, KNN)
- Save models to `models/` directory

**Note**: If models are not available, the system will run in demo mode with dummy predictions.

## 🚀 Running the Application

### Development Mode

```bash
python app.py
```

Or using the launcher:

```bash
python run.py
```

### Production Mode

Set environment variable:

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
python run.py
```

Or use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

The application will start on `http://localhost:5000`

## 📱 Usage Guide

### 1. Upload Pest Image

- Click "Choose File" to select a pest image
- Supported formats: PNG, JPG, JPEG, GIF, BMP
- Maximum file size: 16MB

### 2. Enter Soil NPK Values

- **Nitrogen (N)**: Enter nitrogen value (e.g., 25)
- **Phosphorus (P)**: Enter phosphorus value (e.g., 15)
- **Potassium (K)**: Enter potassium value (e.g., 120)

### 3. Analyze

- Click the "Analyze" button
- System will:
  - Preprocess the image
  - Extract 57 features
  - Run ensemble prediction
  - Analyze soil fertility
  - Generate recommendations

### 4. View Results

Results are displayed in multiple sections:

- **Feature Extraction**: Shows preprocessing and feature extraction progress
- **Prediction Result**: Displays detected pest and confidence score
- **Soil Fertility Analysis**: Shows NPK status and overall fertility
- **Recommendations**: Provides pest control and fertilizer suggestions
- **Summary**: Combined results and recommendations

## 🔧 Project Structure

```
soil_prediction/
├── app.py                      # Main Flask application
├── run.py                      # Application launcher
├── train_models.py            # Model training script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                   # This file
│
├── config/                     # Configuration management
│   ├── __init__.py
│   └── settings.py            # Configuration settings
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── helpers.py             # Helper functions
│   └── logger.py              # Logging configuration
│
├── preprocessing/              # Image preprocessing
│   ├── __init__.py
│   └── image_preprocessing.py
│
├── feature_extraction/         # Feature extraction
│   ├── __init__.py
│   └── feature_extractor.py   # Extracts 57 features
│
├── models/                     # Model definitions
│   ├── __init__.py
│   ├── cnn_model.py           # CNN model architecture
│   └── ml_models.py           # ML models (RF, SVM, KNN)
│
├── ensemble/                   # Ensemble predictor
│   ├── __init__.py
│   └── ensemble_predictor.py  # Combines CNN + ML predictions
│
├── soil_analysis/              # Soil fertility analysis
│   ├── __init__.py
│   └── soil_analyzer.py       # NPK analysis logic
│
├── recommendations/            # Recommendation engine
│   ├── __init__.py
│   └── recommendation_engine.py
│
├── templates/                  # HTML templates
│   └── index.html             # Main UI page
│
├── static/                     # Static files
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   ├── images/                # Images
│   └── uploads/               # Uploaded pest images
│
├── logs/                       # Application logs
│   └── app.log                # Log file
│
└── dataset/                    # Training dataset (create this)
    ├── Aphids/
    ├── Locusts/
    ├── Beetles/
    └── Caterpillars/
```

## 🔬 Technical Details

### Feature Extraction (57 Features)

1. **Color Features (24)**
   - RGB statistics: mean, std, min, max (12 features)
   - HSV statistics: mean, std, min, max (12 features)

2. **Texture Features (16)**
   - GLCM (Gray-Level Co-occurrence Matrix): contrast, correlation, energy, homogeneity
   - Computed at 4 angles (0°, 45°, 90°, 135°)

3. **Shape Features (8)**
   - Contour area, perimeter
   - Aspect ratio, extent
   - Circularity, solidity
   - Bounding box width, height

4. **Edge Features (9)**
   - Canny edge: pixel count, density, mean (3 features)
   - Sobel edge: mean, std, max, min, sum (5 features)

### Model Architecture

**CNN Model:**
- 4 Convolutional blocks with Batch Normalization
- MaxPooling and Dropout for regularization
- Fully connected layers
- Softmax output for 4 classes

**Ensemble Method:**
- CNN weight: 50%
- ML models weight: 50%
  - Random Forest: 40%
  - SVM: 35%
  - KNN: 25%
- Weighted voting for final prediction

### Soil Analysis Thresholds

| Nutrient | Low | Medium | High |
|----------|-----|--------|------|
| Nitrogen (N) | < 20 | 20-40 | > 40 |
| Phosphorus (P) | < 10 | 10-20 | > 20 |
| Potassium (K) | < 100 | 100-200 | > 200 |

## ⚙️ Configuration

The application uses a configuration system that supports different environments:

- **Development**: Debug mode enabled, detailed logging
- **Production**: Debug disabled, minimal logging, requires SECRET_KEY

Configuration can be set via:
- Environment variables (recommended for production)
- `.env` file (for local development)
- Default values in `config/settings.py`

## 📝 Logging

The application includes comprehensive logging:

- Console output for development
- File logging (rotating, max 10MB, 5 backups)
- Configurable log levels
- Logs stored in `logs/` directory

## 🛠️ Development

### Code Structure

- **Modular Design**: Each component is in a separate module
- **Type Hints**: Added for better code clarity
- **Error Handling**: Comprehensive exception handling
- **Logging**: Detailed logging throughout
- **Configuration**: Centralized configuration management

### Testing

Test the system with sample images:
1. Use clear, well-lit pest images
2. Ensure proper NPK value ranges
3. Check logs for any errors

## 🎓 Academic Use

This project is suitable for:
- Final-year engineering projects
- Academic research
- Learning ML/DL ensemble methods
- Computer vision applications
- Agricultural technology research

## 🔮 Future Enhancements

- Real-time camera integration
- Mobile app version
- Cloud-based model serving
- Multi-language support
- Integration with IoT sensors
- Database for historical analysis
- API endpoints for external integration

## 📝 License

This project is provided as-is for educational and research purposes.

## 👨‍💻 Development

### Running in Development

```bash
export FLASK_ENV=development
python app.py
```

### Running in Production

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
python run.py
```

Or with Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - app:app
```

## 🙏 Acknowledgments

Built with:
- TensorFlow/Keras for deep learning
- Scikit-learn for machine learning
- OpenCV for image processing
- Flask for web framework
- Bootstrap 5 for UI

---

**Note**: This system is designed for educational and research purposes. For production use, ensure proper model training with a comprehensive dataset and validation.
