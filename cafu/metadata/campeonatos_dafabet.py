dict_id_campeonato = {
                      'brasil-a': '22977-brazil/22980-brasileiro-serie-a',
                      'brasil-b': '22977-brazil/24267-brasileiro-serie-b',
                      'franca': '23168-france/23169-ligue-1'
                     }

def campeonato_dafabet(campeonato=None):
    """
    Args:
        campeonato: (str) chave do dicionário dict_id_campeonato
    Returns:
        str or dict: completa o link https://www.dafabet.com/pt/dfgoal/sports/240-football/<id_campeonato>. 
        Ex <campeontato>='brasil-a -> '<id_campeonato>=''22977-brazil/22980-brasileiro-serie-a''.
        Se <campeonato>=None, retorna <dict_id_campeonato>
    """
    
    if campeonato is None:
        return dict_id_campeonato
    else:
        return dict_id_campeonato[campeonato]