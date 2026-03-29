from app.db.base_class import Base

# Alembic iterates through Base.metadata. Import all models here.
from app.models.enterprise import Enterprise
from app.models.unit import Unit
from app.models.proposal import Proposal
from app.models.unit_standard_flow import UnitStandardFlow
from app.models.real_estate_agency import RealEstateAgency
