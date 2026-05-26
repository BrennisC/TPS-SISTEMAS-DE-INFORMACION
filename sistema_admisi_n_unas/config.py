"""Production configuration for Sistema Admisión UNAS."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Application settings
APP_NAME = os.getenv("APP_NAME", "sistema_admisi_n_unas")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/sistema_admisi_n_unas/db_admision.db")

# Redis (optional)
REDIS_URL = os.getenv("REDIS_URL", None)

# CORS
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

# Admin settings
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@unas.edu.pe")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")

# Data directories
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# CSV files path
POSTULANTES_CSV = BASE_DIR / "estudiantes.csv"
RESULTADOS_CSV = BASE_DIR / "sistema_admisi_n_unas" / "resultados_examen.csv"
APELACIONES_CSV = BASE_DIR / "sistema_admisi_n_unas" / "apelaciones.csv"

# Export directories
EXPORT_DIR = DATA_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True, parents=True)

# Report templates
REPORT_DIR = DATA_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True, parents=True)


# Colors for PDF reports
UNAS_BLUE = (0, 51, 102)  # #003366
UNAS_GREEN = (34, 139, 34)  # #228B22