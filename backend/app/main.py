"""Main FastAPI application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import get_settings
from app.core.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    init_db()
    yield
    # Shutdown


app = FastAPI(
    title="Leadlet API",
    description="""
    Multi-image leaflet ingestion and structuring platform.

    ## Features

    - **Multi-Image Ingestion**: Upload multiple images as a single document bundle
    - **AI-Powered Extraction**: Uses Claude Vision to extract structured data
    - **Company & Product Cataloguing**: Automatic categorization and taxonomy
    - **CSV Export**: Excel-ready data exports

    ## Endpoints

    - `/api/v1/ingestion` - Upload and process leaflet images
    - `/api/v1/companies` - Company data and overview
    - `/api/v1/products` - Product catalogue
    - `/api/v1/export` - CSV data exports
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Leadlet API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
