"""
AgriAI Platform - Application Settings & Configuration Module
Loads configuration from environment variables or .env file with robust fallbacks.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Core Application Settings
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "agriai_development_secret_key_123456789"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AgriAI - Smart Agriculture Intelligence Platform"
    VERSION: str = "1.0.0"

    # Server Configuration
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_PORT: int = 8501

    # Regional Defaults (Andhra Pradesh focus, extensible to other states)
    DEFAULT_STATE: str = "Andhra Pradesh"
    DEFAULT_DISTRICT: str = "Guntur"
    TARGET_DISTRICTS: str = (
        "Guntur,Krishna,Kurnool,Anantapur,East Godavari,Chittoor,Prakasam,"
        "West Godavari,Visakhapatnam,Nellore,YSR Kadapa,Srikakulam,Vizianagaram"
    )

    # Local Storage Directories
    DATA_DIR: str = "./data"
    RAW_DATA_DIR: str = "./data/raw"
    PROCESSED_DATA_DIR: str = "./data/processed"
    SAMPLE_DATA_DIR: str = "./data/sample"
    UPLOAD_DIR: str = "./data/uploads"
    MODEL_REGISTRY_DIR: str = "./disease_detection/saved_models"
    ML_MODEL_DIR: str = "./ml/saved_models"

    # PostgreSQL Database
    POSTGRES_USER: str = "agriai_admin"
    POSTGRES_PASSWORD: str = "agriai_local_pass"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "agriai_db"
    DATABASE_URL: str = "postgresql://agriai_admin:agriai_local_pass@localhost:5432/agriai_db"

    # Snowflake Cloud Warehouse (Optional)
    SNOWFLAKE_ACCOUNT: str = ""
    SNOWFLAKE_USER: str = ""
    SNOWFLAKE_PASSWORD: str = ""
    SNOWFLAKE_DATABASE: str = "AGRIAI_DW"
    SNOWFLAKE_WAREHOUSE: str = "COMPUTE_WH"
    SNOWFLAKE_SCHEMA: str = "GOLD_MARTS"
    SNOWFLAKE_ROLE: str = "ACCOUNTADMIN"

    # AWS S3 Cloud Storage (Optional)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "ap-south-1"
    S3_BUCKET_NAME: str = "agriai-data-lake-ap"

    # Generative AI & LLM Settings
    LLM_PROVIDER: str = "mock"  # "mock", "gemini", "openai", "groq"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_DB_TYPE: str = "faiss"
    CHROMA_PERSIST_DIR: str = "./data/vector_store"

    # Weather Service
    WEATHER_PROVIDER: str = "open-meteo"
    OPENWEATHERMAP_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def district_list(self) -> List[str]:
        return [d.strip() for d in self.TARGET_DISTRICTS.split(",") if d.strip()]


# Global settings singleton
settings = Settings()
