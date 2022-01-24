dict_id_campeonato = {
                      'brasil-a': '22977-brazil/22980-brasileiro-serie-a',
                      'brasil-b': '22977-brazil/24267-brasileiro-serie-b',
                      'franca': '23168-france/23169-ligue-1'
                     }

def campeonato_dafabet(campeonato):
    """
    Args:
        campeonato: (str) chave do dicionário dict_id_campeonato
    Returns:
        str: completa o link https://www.dafabet.com/pt/dfgoal/sports/240-football/<id_campeonato>. 
             Ex <campeontato>='brasil-a -> '<id_campeonato>=''22977-brazil/22980-brasileiro-serie-a''
    """
    
    return dict_id_campeonato[campeonato]