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
    
    # Adicionada nova var criada que crashou o uvicorn
    DATABASE_URL: Optional[str] = None

    # Domain defaults used by the application runtime.
    # The workbook remains a reverse-engineering/parity artifact, not an operational dependency.
    DEFAULT_MODIFICATION_KIND: str = "Não"
    DEFAULT_DECORATED_VALUE_PER_M2: float = 0.0
    DEFAULT_FACILITY_VALUE_PER_M2: float = 0.0
    DEFAULT_PRIZE_ENABLED: bool = True
    DEFAULT_FULLY_INVOICED: bool = False
    DEFAULT_HAS_PERMUTA: bool = False
    DEFAULT_PRIMARY_COMMISSION_LABEL: str = "Intermediada"
    DEFAULT_PRIMARY_COMMISSION_PERCENT: float = 0.05
    DEFAULT_PRIZE_COMMISSION_LABEL: str = "Prêmio"
    DEFAULT_PRIZE_COMMISSION_PERCENT: float = 0.005

    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Constructing the connection string for pyodbc + sqlalchemy
        # mssql+pyodbc://user:pass@server/db?driver=...
        creds = f"{self.DB_USER}:{self.DB_PASSWORD}@" if self.DB_PASSWORD else f"{self.DB_USER}@"
        return f"mssql+pyodbc://{creds}{self.DB_SERVER}/{self.DB_NAME}?driver={self.DB_DRIVER}"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
