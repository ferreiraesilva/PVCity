from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Unit(Base):
    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(Integer, ForeignKey("enterprise.id"), nullable=False, index=True)

    code = Column(String(50), index=True, nullable=False)
    product_unit_key = Column(String(255), index=True, nullable=True)
    unit_type = Column(String(50), nullable=True)
    suites = Column(Integer, nullable=True)
    garage_code = Column(String(50), nullable=True)
    garage_spots = Column(Integer, nullable=True)
    private_area_m2 = Column(Float, nullable=False, default=0.0)
    base_price = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=True)

    # Campos de viabilidade
    ideal_capture_percent = Column(Float, nullable=False, default=1.0)

    # Relationship
    enterprise = relationship("Enterprise", back_populates="units")
    proposals = relationship("Proposal", back_populates="unit")

