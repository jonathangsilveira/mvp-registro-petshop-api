from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime
from typing import Union

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

class AgendamentoServicoEntity(BaseEntity):
    __tablename__ = 'agendamento_servico'

    id = Column('pk_agendamento_servico', Integer, 
                primary_key=True, autoincrement=True)
    data_inclusao = Column('data_inclusao', DateTime, 
                           default=datetime.now())
    data_agendamento = Column('data_agendamento', DateTime, 
                              unique=True, nullable=False)
    eh_cancelado = Column('cancelado', Boolean, 
                          default=False)
    nome_cliente = Column('nome_cliente', String(140), 
                          nullable=False)
    nome_pet = Column('nome_pet', String(100), 
                      nullable=False)
    valor_servico = Column('valor_servico', Float, 
                           nullable=False)
    servico_id = Column(Integer, ForeignKey('servico.pk_servico'), 
                        nullable=False)
    
    def __init__(self, data_agendamento: datetime, nome_cliente: str, 
                 nome_pet: str, valor_servico: float, 
                 servico_id: int, eh_cancelado: bool = False, 
                 data_inclusao: Union[datetime, None] = None) -> None:
        """
        Cria um registro de agendamento de serviço para o cliente.

        Arguments:
            data_agendamento: Data de agendamento do serviço.
            nome_cliente: Nome do cliente que será prestado o serviço.
            nome_pet: Nome do pet que será aplicado o serviço.
            valor_servico: Valor cobrado pelo serviço prestado.
            servico_id: Código do serviço prestado.
            eh_cancelado: Se o agendamento foi cancelado. Default: False.
            data_inclusao: Data de inclusão do agendamento do serviço.
        """
        self.data_agendamento = data_agendamento
        self.nome_cliente = nome_cliente
        self.nome_pet = nome_pet
        self.valor_servico = valor_servico
        self.servico_id = servico_id
        self.eh_cancelado = eh_cancelado
        
        if data_inclusao:
            self.data_inclusao = data_inclusao