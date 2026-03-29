from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class RealEstateAgency(Base):
    """
    Lista de imobiliárias parceiras disponíveis no sistema.
    Equivale à aba 'Imobs' do Excel.
    """
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
