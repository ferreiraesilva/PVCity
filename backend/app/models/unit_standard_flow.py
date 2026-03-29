from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UnitStandardFlow(Base):
    """
    Define a estrutura de pagamento padrão (tabela) de um empreendimento.
    Equivale à aba 'Tabela Venda - Parcela' do Excel.
    """
    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(Integer, ForeignKey("enterprise.id"), nullable=False, index=True)
    
    periodicity = Column(String(50), nullable=False) # Sinal, Mensais, etc.
    installment_count = Column(Integer, nullable=False, default=1)
    start_month = Column(Integer, nullable=True) # Mês de início (offset)
    installment_value = Column(Float, nullable=False, default=0.0)
    percent = Column(Float, nullable=False, default=0.0)
    row_slot = Column(Integer, nullable=False) # Ordem visual na analise

    enterprise = relationship("Enterprise", back_populates="standard_flows")
