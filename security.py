# Este arquivo centraliza toda a nossa lógica de segurança:
# - Criptografia e verificação de senhas.
# - Criação de tokens de acesso (JWT).

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

# --- Configuração de Segurança ---

# ATENÇÃO: Esta chave é o segredo para criar e validar os tokens.
# Em um projeto de produção, ela JAMAIS deve estar escrita diretamente no código.
# O ideal é carregá-la de uma variável de ambiente.
SECRET_KEY = "uma-chave-secreta-muito-muito-segura-que-deve-ser-trocada"
ALGORITHM = "HS256" # Algoritmo de assinatura do token.
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Tempo de vida do token de acesso.

# Cria um contexto para o passlib, especificando que o algoritmo padrão para senhas é o bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Funções de Segurança ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara uma senha pura com uma senha já criptografada."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um novo token de acesso (JWT).
    O token contém "claims" (informações), como o 'sub' (subject/assunto, nosso usuário)
    e 'exp' (expiration time/tempo de expiração).
    """
    to_encode = data.copy()
    
    # Calcula o tempo de expiração do token
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Se nenhum tempo for fornecido, usa o padrão definido na constante.
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adiciona o tempo de expiração ao payload do token
    to_encode.update({"exp": expire})
    
    # "Assina" o token com nossa chave secreta e algoritmo.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt