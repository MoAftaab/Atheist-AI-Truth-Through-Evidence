"""
Quick script to verify database URL format.
"""

from app.config import settings
import urllib.parse

print("=" * 60)
print("Database URL Check")
print("=" * 60)

db_url = settings.DATABASE_URL
print(f"Raw DATABASE_URL: {db_url}")
print()

# Parse the URL
try:
    parsed = urllib.parse.urlparse(db_url)
    print(f"Scheme: {parsed.scheme}")
    print(f"Username: {parsed.username}")
    print(f"Password: {'*' * len(parsed.password) if parsed.password else 'None'}")
    print(f"Host: {parsed.hostname}")
    print(f"Port: {parsed.port}")
    print(f"Database: {parsed.path.lstrip('/')}")
    print()
    
    # Check password encoding
    if "%40" in db_url:
        print("✓ Password contains %40 (URL-encoded @)")
        decoded_password = urllib.parse.unquote(parsed.password or "")
        if "@" in decoded_password:
            print(f"  Decoded password contains @: {decoded_password[:10]}...")
    elif "@" in parsed.password or (parsed.password and "@" in parsed.password):
        print("⚠ WARNING: Password may contain unencoded @")
        print("  Make sure @ is encoded as %40 in the URL")
    
    print()
    print("Expected format:")
    print("postgresql://username:password%40786@host:port/database")
    print("                    ^^^^")
    print("                    %40 = @")
    
except Exception as e:
    print(f"Error parsing URL: {e}")



