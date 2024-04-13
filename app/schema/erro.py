from typing import Optional
from pydantic import BaseModel

class ErroSchema(BaseModel):
    """
    Define contrato para exibição de erros da API.
    """
    mensagem: str = "Erro ao adicionar novo serviço!"
    
def apresentar_erro(schema: ErroSchema) -> dict[str, Optional[any]]:
    """
    Converte schema de erro para dict.
    """
    return {"mensagem": schema.mensagem}