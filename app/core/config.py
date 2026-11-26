from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Genomic Variant Analysis Platform"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: SecretStr = SecretStr(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/variants_db"
    )
    AWS_REGION: str = "eu-north-1"
    S3_BUCKET_NAME: str = "genomic-variants-bucket-dev"
