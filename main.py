# Este é o arquivo principal da nossa API.
# Ele é responsável por criar a aplicação FastAPI, configurar os endpoints (as "URLs"),
# e iniciar o agendador de tarefas em segundo plano.

# --- Imports de Bibliotecas ---
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# --- Imports dos Nossos Módulos ---
import models, schemas, crud, security
from database import engine, SessionLocal
from robo_caçador import buscar_e_salvar_projetos

# --- Configuração Inicial ---

# Esta linha diz ao SQLAlchemy para criar todas as tabelas no banco de dados
# (definidas em models.py) assim que a aplicação iniciar.
models.Base.metadata.create_all(bind=engine)

# Cria a instância principal da aplicação FastAPI.
app = FastAPI(title="Painel do Freelancer Inteligente")

# --- Lógica do Agendador (Scheduler) ---

# Cria um agendador que roda em segundo plano.
scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")
# Adiciona a tarefa (job) para executar nossa função do robô a cada 5 minutos.
scheduler.add_job(buscar_e_salvar_projetos, 'interval', minutes=5, id="job_buscar_projetos")

# Evento que é disparado QUANDO a API inicia.
@app.on_event("startup")
def startup_event():
    scheduler.start()
    print("Agendador iniciado. O robô buscará projetos a cada 5 minutos.")
    
# Evento que é disparado QUANDO a API é encerrada.
@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    print("Agendador parado.")

# --- Dependência do Banco de Dados ---

# Cria uma "dependência" que gerencia a sessão com o banco para cada requisição.
# Isso garante que a sessão seja aberta no início e sempre fechada no final.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints da Aplicação (as "URLs") ---

@app.post("/token", summary="Gera um token de acesso para login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password.value):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", response_class=HTMLResponse, summary="Serve a página de login")
def ler_pagina_login():
    with open("frontend/login.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/dashboard.html", response_class=HTMLResponse, summary="Serve a página do dashboard")
def ler_pagina_dashboard():
    with open("frontend/dashboard.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/projetos/", response_model=schemas.Projeto, summary="Cria um novo projeto")
def criar_projeto(projeto: schemas.ProjetoCreate, db: Session = Depends(get_db)):
    return crud.create_projeto(db=db, projeto=projeto)

@app.get("/projetos/", response_model=List[schemas.Projeto], summary="Lista todos os projetos")
def ler_projetos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projetos = crud.get_projetos(db, skip=skip, limit=limit)
    return projetos

@app.post("/usuarios/", response_model=schemas.Usuario, summary="Cria um novo usuário")
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    return crud.create_usuario(db=db, usuario=usuario)