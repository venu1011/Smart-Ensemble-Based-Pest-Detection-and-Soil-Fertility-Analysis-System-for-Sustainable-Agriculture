"""
Smart Pest & Soil Fertility Analysis System
Main Flask Application
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

import numpy as np
from flask import Flask, render_template, request, jsonify

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import get_config, Config
from utils.logger import setup_logger
from utils.helpers import (
    allowed_file,
    ensure_directory,
    load_class_names,
    validate_npk_values,
    secure_file_path
)
from preprocessing.image_preprocessing import ImagePreprocessor
from feature_extraction.feature_extractor import FeatureExtractor
from models.cnn_model import CNNPredictor
from models.ml_models import MLPredictor
from ensemble.ensemble_predictor import EnsemblePredictor
from soil_analysis.soil_analyzer import SoilAnalyzer
from recommendations.recommendation_engine import RecommendationEngine


# Initialize logger
logger = setup_logger('app', log_file='app.log')

# Get configuration
config = get_config(os.environ.get('FLASK_ENV', 'development'))

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Ensure required directories exist
config.ensure_directories()

# Initialize analysis components
preprocessor = ImagePreprocessor()
feature_extractor = FeatureExtractor()
soil_analyzer = SoilAnalyzer()
recommendation_engine = RecommendationEngine()

# Model predictors (will be loaded)
cnn_predictor: Optional[CNNPredictor] = None
ml_predictor: Optional[MLPredictor] = None
ensemble_predictor: Optional[EnsemblePredictor] = None
class_names: list = config.DEFAULT_CLASS_NAMES.copy()


def load_models() -> None:
    """Load trained models"""
    global cnn_predictor, ml_predictor, ensemble_predictor, class_names
    
    try:
        # Check for ML models
        ml_model_files = config.get_ml_model_files()
        ml_models_exist = all(
            (config.MODEL_DIR / f).exists() for f in ml_model_files
        )
        
        if ml_models_exist:
            logger.info(f"Loading ML models from {config.MODEL_DIR}...")
            ml_predictor = MLPredictor(models_path=str(config.MODEL_DIR))
            logger.info("ML models loaded successfully")
        else:
            logger.warning("ML model files not found")
        
        # Check for CNN model
        cnn_model_path = config.get_cnn_model_path()
        if cnn_model_path.exists():
            logger.info(f"Loading CNN model from {cnn_model_path}...")
            cnn_predictor = CNNPredictor(model_path=str(cnn_model_path))
            logger.info("CNN model loaded successfully")
        else:
            logger.warning(f"CNN model not found at {cnn_model_path}")
        
        # Initialize ensemble if both models are available
        if cnn_predictor and ml_predictor:
            ensemble_predictor = EnsemblePredictor(
                cnn_predictor,
                ml_predictor,
                num_classes=len(class_names)
            )
            logger.info("Ensemble predictor initialized")
        else:
            logger.warning("Running in demo mode (some models are missing)")
        
        # Load class names
        class_names = load_class_names(
            config.get_class_names_path(),
            config.DEFAULT_CLASS_NAMES
        )
        
    except Exception as e:
        logger.error(f"Error loading models: {e}", exc_info=True)
        logger.warning("Running in demo mode with dummy predictions")


# Load models at startup
load_models()


@app.route('/')
def index() -> str:
    """Home page route"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file() -> Dict[str, Any]:
    """
    Handle file upload
    
    Returns:
        JSON response with upload status
    """
    try:
        if 'pest_image' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file part in request'
            }), 400
        
        file = request.files['pest_image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': f'Invalid file type. Allowed types: {", ".join(config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Secure filename and save
        file_path = secure_file_path(file.filename, config.UPLOAD_FOLDER)
        file.save(str(file_path))
        
        logger.info(f"File uploaded successfully: {file_path.name}")
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully!',
            'filename': file_path.name,
            'filepath': f'/static/uploads/{file_path.name}'
        })
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Upload error: {str(e)}'
        }), 500


@app.route('/analyze', methods=['POST'])
def analyze() -> Dict[str, Any]:
    """
    Perform pest and soil analysis
    
    Returns:
        JSON response with analysis results
    """
    try:
        # Get uploaded image filename
        filename = request.form.get('image_filename')
        if not filename:
            return jsonify({
                'success': False,
                'message': 'No image provided'
            }), 400
        
        file_path = config.UPLOAD_FOLDER / filename
        if not file_path.exists():
            return jsonify({
                'success': False,
                'message': 'Image file not found'
            }), 404
        
        # Validate and get NPK values
        try:
            nitrogen, phosphorus, potassium = validate_npk_values(
                request.form.get('nitrogen', '0'),
                request.form.get('phosphorus', '0'),
                request.form.get('potassium', '0')
            )
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        
        logger.info(f"Starting analysis for image: {filename}")
        
        # Preprocess image
        preprocessed_image = preprocessor.preprocess(str(file_path))
        
        # Extract features
        features = feature_extractor.extract_features(preprocessed_image)
        logger.debug(f"Extracted {len(features)} features")
        
        # Pest prediction
        if ensemble_predictor:
            pest_prediction = ensemble_predictor.predict(preprocessed_image, features)
            pest_class = pest_prediction['class']
            pest_confidence = pest_prediction['confidence']
            pest_name = class_names[pest_class] if pest_class < len(class_names) else 'Unknown'
            logger.info(f"Pest prediction: {pest_name} (confidence: {pest_confidence}%)")
        else:
            # Demo mode: random prediction
            logger.warning("Using demo mode - generating dummy prediction")
            pest_class = np.random.randint(0, len(class_names))
            pest_name = class_names[pest_class]
            pest_confidence = round(np.random.uniform(70, 95), 2)
            pest_prediction = {
                'class': pest_class,
                'confidence': pest_confidence,
                'cnn_prediction': {'class': pest_class, 'confidence': pest_confidence},
                'ml_prediction': {'class': pest_class, 'confidence': pest_confidence}
            }
        
        # Soil analysis
        soil_analysis = soil_analyzer.analyze(nitrogen, phosphorus, potassium)
        logger.debug(f"Soil analysis: {soil_analysis['overall_status']}")
        
        # Get recommendations
        recommendations = recommendation_engine.get_combined_recommendations(
            pest_class, soil_analysis
        )
        
        # Prepare response (same format as before)
        result = {
            'success': True,
            'pest_prediction': {
                'class': int(pest_class),
                'name': pest_name,
                'confidence': pest_confidence,
                'all_predictions': pest_prediction
            },
            'soil_analysis': soil_analysis,
            'recommendations': recommendations,
            'image_url': f'/static/uploads/{filename}',
            'features_extracted': config.NUM_FEATURES
        }
        
        logger.info("Analysis completed successfully")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in analysis: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Analysis error: {str(e)}'
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error) -> Dict[str, Any]:
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'message': f'File too large. Maximum size: {config.MAX_CONTENT_LENGTH / (1024*1024)}MB'
    }), 413


@app.errorhandler(404)
def not_found(error) -> Dict[str, Any]:
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error) -> Dict[str, Any]:
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    logger.info("="*60)
    logger.info("Smart Pest & Soil Fertility Analysis System")
    logger.info("="*60)
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"Upload folder: {config.UPLOAD_FOLDER}")
    logger.info(f"Models loaded: {ensemble_predictor is not None}")
    logger.info(f"Class names: {class_names}")
    logger.info("="*60)
    
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )
