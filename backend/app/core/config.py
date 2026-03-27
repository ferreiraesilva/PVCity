from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "PVCity Backend"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DB_SERVER: str = "localhost"
    DB_NAME: str = "city"
    DB_USER: str = "city_apping"
    DB_PASSWORD: Optional[str] = None
    DB_DRIVER: str = "{ODBC Driver 18 for SQL Server}"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Constructing the connection string for pyodbc + sqlalchemy
        # mssql+pyodbc://user:pass@server/db?driver=...
        creds = f"{self.DB_USER}:{self.DB_PASSWORD}@" if self.DB_PASSWORD else f"{self.DB_USER}@"
        return f"mssql+pyodbc://{creds}{self.DB_SERVER}/{self.DB_NAME}?driver={self.DB_DRIVER}"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
