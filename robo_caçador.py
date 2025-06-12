# Este é o nosso robô autônomo. Ele é o coração da "inteligência" do sistema.
# Seu trabalho é:
# 1. Olhar nosso banco de dados para ver os projetos que já temos.
# 2. Visitar o site de freelancers e ver os projetos listados lá.
# 3. Comparar e, se encontrar um projeto que não temos, salvá-lo através da nossa própria API.
# 4. Ao salvar, ele avisa nosso notificador para nos mandar a novidade no Telegram.

import requests
from bs4 import BeautifulSoup
import time
from notifier import send_telegram_message

# A URL da nossa própria API, que o robô usará para se comunicar com o banco de dados.
API_URL = "http://127.0.0.1:8000"

def buscar_e_salvar_projetos():
    """Função principal do robô, chamada pelo agendador."""
    print(f"[{time.ctime()}] --- Robô Caçador em ação! Buscando novos projetos... ---")
    
    # 1. Pega os links de todos os projetos que já existem no nosso banco
    try:
        response = requests.get(f"{API_URL}/projetos/?limit=2000")
        response.raise_for_status()
        projetos_existentes = response.json()
        links_existentes = {projeto['link'] for projeto in projetos_existentes}
        print(f"INFO: Encontrados {len(links_existentes)} links de projetos já salvos no banco.")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Não foi possível conectar à API para buscar projetos existentes. Erro: {e}")
        return

    # 2. Busca os projetos na página do 99Freelas
    url_99freelas = 'https://www.99freelas.com.br/projects'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    try:
        response = requests.get(url_99freelas, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        projetos_encontrados = soup.find_all('li', class_='result-item')
        
        novos_projetos_count = 0
        for projeto in reversed(projetos_encontrados): # Usamos 'reversed' para buscar dos mais antigos para os mais novos
            link_element = projeto.find('h1', class_='title').find('a')
            if not link_element:
                continue

            link = "https://www.99freelas.com.br" + link_element['href']

            # 3. Se o link já está no nosso banco, pulamos para o próximo
            if link in links_existentes:
                continue

            # 4. Se for um projeto novo, extrai os dados e salva via API
            titulo = link_element.get_text(strip=True)
            descricao_element = projeto.find('div', class_='item-text description formatted-text')
            descricao = descricao_element.get_text(separator='\n', strip=True) if descricao_element else "Descrição não encontrada."
            
            novo_projeto_data = {
                "titulo": titulo,
                "descricao": descricao,
                "link": link
            }
            
            print(f"NOVO PROJETO ENCONTRADO: '{titulo}'. Tentando salvar via API...")
            try:
                post_response = requests.post(f"{API_URL}/projetos/", json=novo_projeto_data)
                
                # CORREÇÃO DA LÓGICA: Notificar apenas no sucesso (status 200)
                if post_response.status_code == 200:
                    novos_projetos_count += 1
                    # Se o projeto foi salvo com sucesso, envia a notificação!
                    mensagem = f"🎉 *Novo Projeto Encontrado!*\n\n*Título:* {titulo}\n\n[Ver Projeto]({link})"
                    send_telegram_message(mensagem)
                else:
                    print(f"AVISO: API retornou erro ao salvar projeto. Status: {post_response.status_code} - Resposta: {post_response.text}")
            
            except requests.exceptions.RequestException as e:
                print(f"ERRO de conexão ao salvar projeto via API: {e}")
        
        if novos_projetos_count == 0:
            print("INFO: Nenhum projeto novo encontrado nesta busca.")
        else:
            print(f"SUCESSO: Busca finalizada. {novos_projetos_count} novos projetos foram encontrados e notificados.")

    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao acessar a página do 99Freelas: {e}")

# Bloco que permite executar este arquivo diretamente para um teste manual
if __name__ == "__main__":
    buscar_e_salvar_projetos()