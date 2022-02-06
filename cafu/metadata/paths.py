paths = {
         'initial_path': '/home/luan/futebol/Futebol',
         'credentials': '/home/luan/futebol/credentials',
         'logs_cafu': '/home/luan/futebol/logs_cafu'
        }

def path(key):
    """
    Args:
        key: (str) chave do dicionário paths
    Returns:
        str: caminho 
    """
    
    return paths[key]