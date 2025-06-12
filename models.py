# Este arquivo define a "forma" (o schema) das nossas tabelas no banco de dados.
# Cada classe aqui representa uma tabela.

from sqlalchemy import Column, Integer, String
from database import Base

# --- Modelo da Tabela de Projetos ---
class Projeto(Base):
    # O nome da tabela que será criada no banco de dados.
    __tablename__ = "projetos"

    # Definição das colunas da tabela:
    id = Column(Integer, primary_key=True, index=True) # ID numérico, chave primária e indexado para buscas rápidas.
    titulo = Column(String, index=True) # Título do projeto, também indexado.
    descricao = Column(String) # Descrição do projeto.
    link = Column(String, unique=True) # Link para o projeto original. `unique=True` garante que não salvaremos o mesmo projeto duas vezes.


# --- Modelo da Tabela de Usuários ---
class Usuario(Base):
    # O nome da tabela no banco.
    __tablename__ = "usuarios"

    # Definição das colunas:
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) # E-mail é único (não pode haver dois usuários com o mesmo e-mail) e indexado.
    hashed_password = Column(String) # Coluna para armazenar a senha já criptografada.