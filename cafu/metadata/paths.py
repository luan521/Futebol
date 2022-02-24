paths = {
         'initial_path': '/home/luan/futebol/Futebol',
         'credentials': '/home/luan/futebol/credentials',
         'logs_cafu': '/home/luan/futebol/logs_cafu',
         'dir_teste': '/home/luan/futebol/testes',
         'datalake': '/home/luan/futebol/datalake'
        }

"""
description_paths

- initial_path: caminho local para o projeto 

- credentials: caminho local do arquivo 'dafabet.json', que contém:
         - 'user': usuário no site dafabet
         - 'password': senha no site dafabet

- logs_cafu: caminho local para o diretório onde o arquivo 'logs.txt' será criado, os logs gerados pela execução das funções irão para este arquivo

- dir_teste: caminho local para o diretório de teste, onde resultados dos testes automatizados (testes_py) serão salvos

- datalake: caminho local para o datalake
"""

def path(key):
    """
    Args:
        key: (str) chave do dicionário paths
    Returns:
        str: caminho 
    """
    
    return paths[key]
