from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base

class GlobalParameter(Base):
    """
    Tabela para armazenar configurações globais do sistema.
    Ex: vpl_rate_annual, default_commission, etc.
    """
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
