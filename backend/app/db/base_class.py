from typing import Any
from sqlalchemy.orm import declarative_base, declared_attr

class CustomBase:
    id: Any
    __name__: str
    
    # Gera o nome da tabela automaticamente baseado no nome da classe
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

Base = declarative_base(cls=CustomBase)
