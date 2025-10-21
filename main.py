from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Usuario, PessoaFisica, PessoaJuridica, DadosBancarios
from schemas import UsuarioCreateSchema

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Encontreja")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cadastro_usuario")
def cadastro_usuario(usuario: UsuarioCreateSchema, db: Session = Depends(get_db)):

    if usuario.tipo_usuario not in (0, 1):
        raise HTTPException(status_code=400, detail="tipo_usuario deve ser 0 (física) ou 1 (jurídica)")

    novo_usuario = Usuario(
        nome=usuario.nome,
        rua=usuario.rua,
        numero=usuario.numero,
        bairro=usuario.bairro,
        cidade=usuario.cidade,
        estado=usuario.estado,
        cep=usuario.cep,
        email=usuario.email,
        telefone=usuario.telefone,
        tipo_usuario=usuario.tipo_usuario
    )
    db.add(novo_usuario)
    db.flush()

    if usuario.tipo_usuario == 0:
        if not usuario.cpf:
            raise HTTPException(status_code=400, detail="CPF é obrigatório para pessoa física")
        pessoa_fisica = PessoaFisica(cpf=usuario.cpf, usuario_id=novo_usuario.id)
        db.add(pessoa_fisica)

    if usuario.tipo_usuario == 1:
        if not usuario.cnpj:
            raise HTTPException(status_code=400, detail="CNPJ é obrigatório para pessoa jurídica")
        pessoa_juridica = PessoaJuridica(cnpj=usuario.cnpj, usuario_id=novo_usuario.id)
        db.add(pessoa_juridica)

    db.add(DadosBancarios(
        agencia=usuario.dados_bancarios.agencia,
        conta=usuario.dados_bancarios.conta,
        tipo_conta=usuario.dados_bancarios.tipo_conta,
        chave_pix=usuario.dados_bancarios.chave_pix,
        usuario_id=novo_usuario.id
    ))

    db.commit()
    db.refresh(novo_usuario)
    return {"mensagem": "Usuário cadastrado com sucesso!", "id": str(novo_usuario.id)}
