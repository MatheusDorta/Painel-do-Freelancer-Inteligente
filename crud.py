# Este arquivo contém todas as funções que interagem diretamente com o banco de dados.
# CRUD é um acrônimo para Create (Criar), Read (Ler), Update (Atualizar), e Delete (Deletar).
# Separar essa lógica mantém nosso código de API (main.py) mais limpo e organizado.

from sqlalchemy.orm import Session

# Nossos módulos locais
import models
import schemas
# Importa o contexto de senha do nosso módulo de segurança, em vez de recriá-lo.
from security import pwd_context


# --- CRUD de Usuário ---

def get_user_by_email(db: Session, email: str):
    """Busca um usuário no banco de dados pelo seu e-mail."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Cria um novo usuário no banco de dados, com a senha já criptografada."""
    # Criptografa a senha recebida do schema antes de salvar
    hashed_password = pwd_context.hash(usuario.password)
    # Cria a instância do modelo do banco de dados
    db_usuario = models.Usuario(email=usuario.email, hashed_password=hashed_password)
    
    # Adiciona, "commita" (salva) e atualiza a instância com os dados do banco (como o ID)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario


# --- CRUD de Projeto ---

def get_projetos(db: Session, skip: int = 0, limit: int = 100):
    """Busca uma lista de projetos no banco, com suporte para paginação."""
    return db.query(models.Projeto).offset(skip).limit(limit).all()


def create_projeto(db: Session, projeto: schemas.ProjetoCreate):
    """Cria um novo projeto no banco de dados."""
    db_projeto = models.Projeto(
        titulo=projeto.titulo,
        descricao=projeto.descricao,
        link=projeto.link
    )
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto