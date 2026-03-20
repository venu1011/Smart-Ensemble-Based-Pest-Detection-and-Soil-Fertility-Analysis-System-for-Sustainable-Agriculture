# Quick Start Guide

## Installation (5 minutes)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python verify_setup.py
   ```

3. **Create dataset structure (optional, for training):**
   ```bash
   python create_dummy_dataset.py
   ```

## Running the Application

### Option 1: Run without trained models (Demo Mode)

The system will work with dummy predictions:

```bash
python app.py
```

Then open: `http://localhost:5000`

### Option 2: Train models first (Recommended)

1. **Prepare dataset:**
   - Add pest images to `dataset/Aphids/`, `dataset/Locusts/`, etc.
   - At least 50-100 images per class recommended

2. **Train models:**
   ```bash
   python train_models.py
   ```

3. **Run application:**
   ```bash
   python app.py
   ```

## Using the System

1. **Upload Image:** Select a pest image (PNG, JPG, JPEG, GIF, BMP)
2. **Enter NPK Values:**
   - Nitrogen (N): e.g., 25
   - Phosphorus (P): e.g., 15
   - Potassium (K): e.g., 120
3. **Click Analyze:** Wait for processing
4. **View Results:**
   - Pest detection result
   - Soil fertility analysis
   - Recommendations

## Troubleshooting

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify installation: `python verify_setup.py`

### Model Not Found
- System runs in demo mode without models
- Train models: `python train_models.py`
- Ensure `models/` directory exists

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`

## Next Steps

- Add your pest images to train custom models
- Adjust NPK thresholds in `soil_analysis/soil_analyzer.py`
- Customize recommendations in `recommendations/recommendation_engine.py`

