from typing import Optional
from pydantic import BaseModel

class ServicoAtivoSchema(BaseModel):
    """
    Define contrato de como deve ser exibido o serviço.
    """
    id: int
    titulo: str
    preco_unitario: float

class ServicosAtivosViewSchema(BaseModel):
    """
    Define contrato de exibição dos resultados dos serviços ativos.
    """
    servicos: list[ServicoAtivoSchema]

def apresentar_servico_ativo(servico_ativo: ServicoAtivoSchema) -> dict[str, any]:
    return {
        "id": servico_ativo.id,
        "titulo": servico_ativo.titulo,
        "preco_unitario": servico_ativo.preco_unitario
    }

def apresentar_servicos_ativos(servicos_ativos: list[ServicoAtivoSchema]) -> list[dict[str, any]]:
    """
    Converte schema de serviços ativos para lista de dict.
    """
    result: list[dict[str, any]] = []
    for servico_ativo in servicos_ativos:
        transformation = apresentar_servico_ativo(servico_ativo)
        result.append(transformation)
    return result