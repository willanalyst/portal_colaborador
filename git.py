import requests
import base64
import os

# Configurações
token = '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'
username = 'willanalyst'
repositorio = 'portal_colaborador'
caminho_pasta = 'C:/Users/watai/OneDrive/Documents/Projetos Web/Portal do Colaborador'

# Cabeçalho para autenticação
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
}

def upload_arquivo(nome_arquivo, conteudo):
    url = f'https://api.github.com/repos/{username}/{repositorio}/contents/{nome_arquivo}'
    data = {
        'message': f'Adicionando {nome_arquivo}',
        'content': base64.b64encode(conteudo).decode()
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f'Arquivo {nome_arquivo} adicionado com sucesso.')
    else:
        print(f'Falha ao adicionar {nome_arquivo}: {response.content}')

# Percorrer os arquivos na pasta e fazer o upload
for arquivo in os.listdir(caminho_pasta):
    caminho_completo = os.path.join(caminho_pasta, arquivo)
    if os.path.isfile(caminho_completo):
        with open(caminho_completo, 'rb') as file:
            upload_arquivo(arquivo, file.read())
