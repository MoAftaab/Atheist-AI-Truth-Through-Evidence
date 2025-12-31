"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from app.config import settings
from app.routers import auth, queries, health
from app.database import engine, Base

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Quran-centric, citation-locked Question Answering system"
)

# Startup event for DB
@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database connected and tables created")
    except OperationalError as e:
        print(f"⚠️ Database connection error: {e}")
        print("⚠️ Database not available. Some features may not work.")
    except Exception as e:
        print(f"⚠️ Database setup error: {e}")
        import traceback
        traceback.print_exc()

# Configure CORS - MUST be added before routers
# Get origins from settings (parsed from CORS_ORIGINS env variable)
cors_origins = settings.cors_origins_list

print(f"🔧 CORS Origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Explicit list of allowed origins (production-safe)
    allow_credentials=True,  # Required for cookies/auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Includes OPTIONS for preflight
    allow_headers=["Content-Type", "Authorization", "Accept"],  # Explicit headers (production-safe)
    expose_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["authentication"])
app.include_router(queries.router, prefix=f"{settings.API_V1_PREFIX}/queries", tags=["queries"])

@app.get("/")
async def root():
    return {
        "message": "Atheist AI API",
        "version": settings.VERSION,
        "docs": "/docs"
    }
