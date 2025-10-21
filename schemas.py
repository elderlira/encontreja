from pydantic import BaseModel, Field
from typing import Optional

class DadosBancariosSchema(BaseModel):
    agencia: str
    conta:str
    tipo_conta: int
    chave_pix: str

class UsuarioCreateSchema(BaseModel):
    nome: str
    rua: Optional[str] = None
    numero: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    cep: str
    email: str
    telefone: str
    tipo_usuario: int = Field(..., description="0 = pessoa física, 1 = pessoa jurídica")
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    dados_bancarios: DadosBancariosSchema

