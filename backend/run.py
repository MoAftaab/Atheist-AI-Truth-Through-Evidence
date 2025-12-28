"""
Development server runner.
Run this from the backend directory with venv activated.

Usage:
    # Activate venv first
    # .\\venv\\Scripts\\activate  # Windows
    # or
    # source venv/bin/activate  # Linux/Mac
    
    # Then run
    # python run.py
"""

import uvicorn
import sys
import os

def check_venv():
    """Check if running in virtual environment."""
    in_venv = (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if not in_venv:
        print("⚠ WARNING: Not running in virtual environment!")
        print("   It's recommended to use venv for backend.")
        print("   Create venv: python -m venv venv")
        print("   Activate: .\\venv\\Scripts\\activate")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("✓ Running in virtual environment")

if __name__ == "__main__":
    check_venv()
    print("\n🚀 Starting backend server...")
    print("   Backend: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

