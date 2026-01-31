# Leadlet

Multi-image leaflet ingestion and structuring platform for extracting, normalizing, and cataloguing company and product information from brochures, leaflets, and product sheets.

## Features

- **Multi-Image Ingestion**: Upload multiple images of company brochures as a single document bundle
- **AI-Powered Extraction**: Uses Claude Vision to extract structured data from images
- **Company Identity Resolution**: Detects company identity even when it appears on only one page
- **Structured Data Output**: Website-ready JSON and Excel-exportable CSV outputs
- **Product Cataloguing**: Automatic categorization and taxonomy generation
- **Search & Retrieval**: Optimized metadata for filtering and comparison

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI**: Anthropic Claude API (Vision + Text)
- **Frontend**: Next.js 14 with React and TypeScript
- **Styling**: Tailwind CSS

## Project Structure

```
leadlet/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Configuration, security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── main.py        # FastAPI application
│   ├── alembic/           # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities
│   └── package.json
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or use SQLite for development)
- Anthropic API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Configure your API keys
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file in the backend directory:

```
DATABASE_URL=postgresql://user:password@localhost/leadlet
ANTHROPIC_API_KEY=your-api-key
SECRET_KEY=your-secret-key
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT
