#!/usr/bin/env python3
"""
Quick Setup Test Script

Tests if the backend is properly configured and ready to run.
Run this before starting the server to catch common issues early.

Usage:
    python test_setup.py
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported."""
    print("[TEST] Testing imports...")
    try:
        import fastapi
        import librosa
        import numpy as np
        import sqlite3
        print("[OK] All imports successful")
        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def test_model_files():
    """Test if model files exist."""
    print("\n[TEST] Testing model files...")
    base_dir = Path(__file__).parent
    model_path = base_dir / "models" / "emotion_model.h5"
    encoder_path = base_dir / "models" / "label_encoder.pkl"
    
    if not model_path.exists():
        print(f"[ERROR] Model file not found: {model_path}")
        return False
    
    if not encoder_path.exists():
        print(f"[ERROR] Encoder file not found: {encoder_path}")
        return False
    
    print(f"[OK] Model file found: {model_path}")
    print(f"[OK] Encoder file found: {encoder_path}")
    return True

def test_model_loading():
    """Test if model can be loaded."""
    print("\n[TEST] Testing model loading...")
    try:
        from app.core.model_loader import model_loader
        success, error = model_loader.load_model()
        if success:
            print("[OK] Model loaded successfully")
            print(f"   Input shape: {model_loader.model.input_shape}")
            print(f"   Classes: {list(model_loader.encoder.classes_)}")
            return True
        else:
            print(f"[ERROR] Model loading failed: {error}")
            return False
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
        return False

def test_database():
    """Test database setup."""
    print("\n[TEST] Testing database...")
    try:
        from app.services.database import create_table, get_connection
        create_table()
        conn = get_connection()
        conn.close()
        print("[OK] Database setup successful")
        return True
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return False

def test_config():
    """Test configuration."""
    print("\n[TEST] Testing configuration...")
    try:
        from app.core.config import (
            MODEL_PATH, ENCODER_PATH, DB_PATH,
            SAMPLE_RATE, DURATION, N_MFCC
        )
        print("[OK] Configuration loaded")
        print(f"   Sample rate: {SAMPLE_RATE}")
        print(f"   Duration: {DURATION}s")
        print(f"   MFCC coefficients: {N_MFCC}")
        return True
    except Exception as e:
        print(f"[ERROR] Configuration error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("EmoTalk Backend Setup Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Model Files", test_model_files),
        ("Configuration", test_config),
        ("Database", test_database),
        ("Model Loading", test_model_loading),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"[ERROR] {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! Backend is ready to run.")
        print("   Start server with: uvicorn app.main:app --reload")
        return 0
    else:
        print("\n[WARNING] Some tests failed. Please fix issues before running server.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

