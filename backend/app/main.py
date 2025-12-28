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

# Configure CORS
# For development, allow all origins. For production, use specific origins from .env
cors_origins = settings.cors_origins_list
# Add common development origins if not already present
if "http://localhost:3000" not in cors_origins:
    cors_origins.append("http://localhost:3000")
if "http://127.0.0.1:3000" not in cors_origins:
    cors_origins.append("http://127.0.0.1:3000")

print(f"🔧 CORS Origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
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
