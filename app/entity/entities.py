from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

BaseEntity = declarative_base()

class ServicoEntity(BaseEntity):
    __tablename__ = 'servico'

    id = Column('pk_servico', Integer, 
                primary_key=True, autoincrement=True)
    titulo = Column('titulo', String(100), 
                    unique=True, nullable=False)
    preco_unitario = Column('preco_unit', Float, 
                            nullable=False)
    eh_ativo = Column('ativo', Boolean, default=False)
    
    def __init__(self, titulo: str, preco_unitario: float, 
                 eh_ativo: bool = True) -> None:
        """
        Cria um serviço.

        Arguments:
            titulo: Título do serviço.
            preco_unitario: Preço unitário do serviço.
        """
        self.titulo = titulo
        self.preco_unitario = preco_unitario
        self.eh_ativo = eh_ativo