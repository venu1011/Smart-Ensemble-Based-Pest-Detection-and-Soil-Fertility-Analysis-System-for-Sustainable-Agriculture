#!/usr/bin/env python
"""
Production-ready application launcher
"""

import os
from app import app, config, logger

if __name__ == '__main__':
    # Use environment variable for port or default to 5000
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    app.run(
        host=host,
        port=port,
        debug=config.DEBUG
    )

