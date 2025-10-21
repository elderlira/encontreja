import uuid
from sqlalchemy import Column, String, Integer, SmallInteger, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid = True), primary_key = True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    rua = Column(String)
    numero = Column(String(20))
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(20), nullable=False)
    email = Column(String, unique=True, nullable=True)
    telefone = Column(String(20), nullable=False)
    tipo_usuario = Column(SmallInteger, nullable=False)
    criando_em = Column(TIMESTAMP, server_default=func.now())
    nivel_acesso =  Column(SmallInteger, default=0)

    pessoa_fisica = relationship("PessoaFisica", back_populates="usuario", uselist=False)
    pessoa_juridica = relationship("PessoaJuridica", back_populates="usuario", uselist=False)
    dados_bancarios = relationship("DadosBancarios", back_populates="usuarios", uselist=False)


class PessoaFisica(Base):
    __tablename__ = "pessoa_fisica"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf = Column(String(14), unique=True, nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    usuario = relationship("Usuario", back_populates="pessoa_fisica")

class PessoaJuridica(Base):
    __tablename__ = "pessoa_juridica"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnpj = Column(String(18), unique=True, nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    usuario = relationship("Usuario", back_populates="pessoa_juridica")

class DadosBancarios(Base):
    __tablename__ = "dados_bancarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    agencia = Column(String(20), nullable=False)
    conta = Column(String(20), nullable=False)
    tipo_conta = Column(SmallInteger, nullable=False)
    chave_pix = Column(String(255), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)

    usuario = relationship("Usuario", back_populates="dados_bancarios")
