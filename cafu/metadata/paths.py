paths = {
         'initial_path': 'C:\\Users\\Luan\\futebol\\Futebol',
         'credentials': 'C:\\Users\\Luan\\futebol\\credentials',
         'logs_cafu': 'C:\\Users\\Luan\\futebol\\logs_cafu'
        }

def path(key):
    """
    Args:
        key: (str) chave do dicionário paths
    Returns:
        str: caminho 
    """
    
    return paths[key]