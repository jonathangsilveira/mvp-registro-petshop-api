from pydantic import BaseModel, RootModel, validator
from typing import List
from datetime import datetime

class NovoAgendamentoServicoSchema(BaseModel):
    """
    Define o contrato de inserção de um novo agendamento do serviço.
    """
    data_agendamento: str = '2024-04-08 20:00:00'
    nome_cliente: str = 'Vitória Tenorio'
    nome_pet: str = 'Cacau'
    valor_servico: float = 50.0
    servico_id: int = 1
    cancelado: bool = False

    @validator('data_agendamento')
    def data_agendamento_deve_ser_valido(cls, value):
        # Valida se a data_agendamento está em um formato válido.
        try:
            _ = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return value
        except Exception as e:
            # se deu erro a tentativa de conversão
            raise ValueError('Formato de data e hora inválido')
        
    @validator('nome_cliente')
    def nome_cliente_deve_ser_informado(cls, value):
        # Valida se a data_agendamento está em um formato válido.
        if len(value) < 1:
            raise ValueError('Nome do cliente deve ser informado!')
        return value
        
    @validator('nome_pet')
    def nome_pet_deve_ser_informado(cls, value):
        # Valida se o nome_pet foi informado.
        if len(value) < 1:
            raise ValueError('Nome do pet deve ser informado!')
        return value
        
    @validator('valor_servico')
    def valor_servico_deve_ser_maior_zero(cls, value: float):
        # Valida se valor do serviço é válido.
        if value < 0.0:
            raise ValueError('Valor do serviço não pode ser zero!')
        return value
            

class AlterarAgendamentoServicoSchema(BaseModel):
    """
    Define o contrato de alteração de um agendamento de serviço.
    """
    id: int
    data_agendamento: str = '2024-04-08 20:34:00'
    nome_cliente: str = 'Vitória Tenorio'
    nome_pet: str = 'Cacau'
    valor_servico: float = 50.0
    servico_id: int = 1
    cancelado: bool = False

class AgendamentoServicoSchema(BaseModel):
    """
    Define o contrato de apresentação de um agendamento do serviço.
    """
    id: int
    data_agendamento: str
    nome_cliente: str
    nome_pet: str
    valor_servico: float
    servico_id: int
    servico_titulo: str
    cancelado: bool
    data_inclusao: str

class AgendamentoServicoPorIdSchema(BaseModel):
    """
    Define contrato para exclusão do agendamento de serviço.
    """
    id: int

class BuscaAgendaPorDataSchema(BaseModel):
    """
    Define contrato para busca de agenda por data.
    """
    data_inicio: str = '2024-04-22'
    data_fim: str = '2024-04-26'

class AgendaSchema(RootModel):
    """
    Define o contrato de exibição da busca de agendamentos por data (BuscaAgendaPorDataSchema).
    """
    root: List[AgendamentoServicoSchema] = []

def apresenta_agendamento(schema: AgendamentoServicoSchema) -> dict[str, any]:
    """
    Converte schema de agendamento de serviço para dict.
    """
    return {
        "id": schema.id,
        "data_agendamento": schema.data_agendamento,
        "nome_cliente": schema.nome_cliente,
        "nome_pet": schema.nome_pet,
        "valor_servico": schema.valor_servico,
        "servico_id": schema.servico_id,
        "servico_titulo": schema.servico_titulo,
        "cancelado": schema.cancelado,
        "data_inclusao": schema.data_inclusao,
    }