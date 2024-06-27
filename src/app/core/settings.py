import os


class Settings:
    # General settings
    PROJECT_NAME: str = "Clover Kingdom"
    PROJECT_DESCRIPTION: str = "API to handle new Studets requests and Grimoires"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_HOSTNAME: str = os.getenv("DB_HOSTNAME", "postgres")
    DB_PORT: str = os.getenv("DB_PORT", 5432)
    DB_DATABASE: str = os.getenv("DB_DATABASE", "postgres")

    SQLALCHEMY_DATABASE_URL: str = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"
    )


settings = Settings()
