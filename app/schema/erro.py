from typing import Optional
from pydantic import BaseModel

class ErroSchema(BaseModel):
    """
    Define contrato para exibição de erros da API.
    """
    mensagem: str = "Erro ao adicionar novo serviço!"
    
def apresentar_erro(schema: ErroSchema) -> dict[str, Optional[any]]:
    return {"mensagem": schema.mensagem}