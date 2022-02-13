paths = {
         'initial_path': 'C:\\Users\\Luan\\futebol\\Futebol',
         'credentials': 'C:\\Users\\Luan\\futebol\\credentials',
         'logs_cafu': 'C:\\Users\\Luan\\futebol\\logs_cafu'
        }

"""
description_paths

- initial_path: caminho local para o projeto 

- credentials: caminho local do arquivo 'dafabet.json', que contém:
         - 'user': usuário no site dafabet
         - 'password': senha no site dafabet

- logs_cafu: caminho local para o diretório onde o arquivo 'logs.txt' será criado, os logs gerados pela execução das funções irão para este arquivo
"""

def path(key):
    """
    Args:
        key: (str) chave do dicionário paths
    Returns:
        str: caminho 
    """
    
    return paths[key]
