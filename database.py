# Este arquivo é responsável por configurar a conexão com o banco de dados.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base # Import modernizado

# --- Configuração do Banco de Dados ---

# 1. Define a URL do banco. Para SQLite, é o caminho do arquivo.
DATABASE_URL = "sqlite:///./freelancer_panel.db"

# 2. Cria o "motor" (engine) do SQLAlchemy, que gerencia a conexão.
# O argumento connect_args é específico para o SQLite e permite que a API o acesse de forma segura.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Cria uma fábrica de "sessões" (SessionLocal). Cada sessão é uma conversa individual com o banco.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Cria uma classe Base. Todos os nossos modelos de tabela (ex: Projeto, Usuario) herdarão dela.
Base = declarative_base()