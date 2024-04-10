from pydantic import BaseModel, RootModel
from typing import List

class NovoAgendamentoServicoSchema(BaseModel):
    """
    Define o contrato de inserção de um novo agendamento do serviço.
    """
    data_agendamento: str = '2024-04-08 20:34:00'
    nome_cliente: str = 'Vitória Tenorio'
    nome_pet: str = 'Cacau'
    valor_servico: float = 50.0
    servico_id: int = 1
    cancelado: bool = False

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