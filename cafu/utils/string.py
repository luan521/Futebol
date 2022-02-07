from Levenshtein import distance
from unidecode import unidecode
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def identify_string_in_list(string, list_strings):
    """
    Args:
        string: (str) 
        list_strings: (list) strings 
    Returns:
        int: index da string mais parecida com <string>, na lista <list_strings>
    """

    # lower: todas as letras minúsculas
    # unidecode: sem acento
    # replace('-',' '): substitui - por espaço
    string = unidecode(string.lower())
    list_strings = [unidecode(s.lower()).replace('-',' ') for s in list_strings] 

    index_string_in_list = 0
    min_dist = distance(string, list_strings[index_string_in_list])
    for i, s in enumerate(list_strings):
        dist = distance(string, list_strings[i])
        if dist < min_dist:
            index_string_in_list = i
            min_dist = dist
    
    if min_dist > 0:
        logging.warning(f"WARNING utils.string.identify_string_in_list: distance(string_input={string}, "
                        f"string_found={list_strings[index_string_in_list]}) = {min_dist}")
    
    return index_string_in_list