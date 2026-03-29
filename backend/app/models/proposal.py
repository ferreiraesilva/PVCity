from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
import datetime
from app.db.base_class import Base

class Proposal(Base):
    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("unit.id"), nullable=False, index=True)
    
    # Meta
    broker_name = Column(String(255), nullable=True)
    scenario_mode = Column(String(50), default="NORMAL") # NORMAL ou PERMUTA
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # JSON columns are broadly supported (in Postgres natively, in MSSQL as nvachar + json ops if using recent ODBC, OR SQLAlchemy gracefully serializes dicts if we use generic dialects).
    # This stores the whole snapshot of the "Simulador" payload.
    payload_snapshot = Column(JSON, nullable=False)
    
    # Summary of result
    pv_status = Column(String(50))
    capture_percent = Column(Float)
    
    # Relationship
    unit = relationship("Unit", back_populates="proposals")
