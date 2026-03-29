from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Enterprise(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    work_code = Column(String(50), nullable=True)
    spe_name = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    # Parâmetros financeiros do empreendimento vindos do Excel
    vpl_rate_annual = Column(Float, nullable=False, default=0.0)
    discount_percent = Column(Float, nullable=False, default=0.0)
    delivery_month = Column(String(20), nullable=True)
    launch_date = Column(String(20), nullable=True)
    stage = Column(String(100), nullable=True)

    # Relationships
    units = relationship("Unit", back_populates="enterprise")
    standard_flows = relationship("UnitStandardFlow", back_populates="enterprise")

