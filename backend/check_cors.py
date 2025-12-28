"""
Quick script to check CORS configuration.
Run this to verify CORS settings are loaded correctly.
"""

from app.config import settings

print("=" * 60)
print("CORS Configuration Check")
print("=" * 60)
print(f"CORS_ORIGINS env var: {settings.CORS_ORIGINS}")
print(f"Parsed origins list: {settings.cors_origins_list}")
print("=" * 60)


