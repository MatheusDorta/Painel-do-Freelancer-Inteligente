# Este arquivo define os "schemas" Pydantic.
# Pense neles como os "formulários" ou "passaportes" da nossa API.
# Eles garantem que os dados que entram e saem da API tenham a forma correta.

from pydantic import BaseModel

# --- Schemas de Projeto ---

# O schema Base contém os campos comuns, compartilhados entre criação e leitura.
class ProjetoBase(BaseModel):
    titulo: str
    descricao: str | None = None # O campo é opcional.
    link: str
    
# O schema de Criação herda do Base. Usado para receber dados para criar um novo projeto.
class ProjetoCreate(ProjetoBase):
    pass # Não adiciona novos campos, então 'pass' é suficiente.

# O schema principal (de leitura) é usado para retornar dados da API.
class Projeto(ProjetoBase):
    id: int # Ao ler do banco, o projeto já terá um ID.
    
    # A classe Config com from_attributes = True (antigo orm_mode)
    # permite que o Pydantic leia os dados de um objeto SQLAlchemy.
    class Config:
        from_attributes = True

# --- Schemas de Usuário ---

# O schema Base com os dados essenciais do usuário.
class UsuarioBase(BaseModel):
    email: str
    
# O schema para criar um usuário. Note que ele pede a senha.
class UsuarioCreate(UsuarioBase):
    password: str
    
# O schema para retornar um usuário da API.
# Note que ele NÃO inclui a senha, por segurança!
class Usuario(UsuarioBase):
    id: int
    
    class Config:
        from_attributes = True