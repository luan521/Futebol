from selenium import webdriver
from cafu.metadata.campeonatos_dafabet import campeonato_dafabet

class WebdriverChrome():
    """
    Inicializa a sessão do chromedriver e entra em alguns links úteis
    
    Args:
        path_driver: (str) caminho para o chromedriver 
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
                          Ex <id_jogador>='199017/everton-ribeiro'
    """
    
    def __init__(self, path_driver=None):
        if path_driver is not None:
            self.web = webdriver.Chrome(path_driver)
        
    def get_ult_cinco_jogos_jogador(self, id_jogador):
        """
        Entra no link para a busca das informações dos últimos cinco jogos do jogador

        Args:
            id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
                              Ex <id_jogador>='199017/everton-ribeiro'
        """
        
        self.web.get(f'https://www.espn.com.br/futebol/jogador/_/id/{id_jogador}')
        
    def get_estatisticas_jogador(self, id_jogador):
        """
        Entra no link para a busca das estatísticas do jogador

        Args:
            id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/estatisticas/_/id/<id_jogador>. 
                              Ex <id_jogador>='199017/everton-ribeiro'
        """
        
        self.web.get(f'https://www.espn.com.br/futebol/jogador/estatisticas/_/id/{id_jogador}')
        
    def get_bio_jogador(self, id_jogador):
        """
        Entra no link para a busca da biografia do jogador

        Args:
            id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/bio/_/id/<id_jogador>. 
                              Ex <id_jogador>='199017/everton-ribeiro'
        """
        
        self.web.get(f'https://www.espn.com.br/futebol/jogador/bio/_/id/{id_jogador}')
        
    def get_campeonato_dafabet(self, chave_campeonato):
        """
        Entra no link para a busca das odds no site Dafabet

        Args:
            chave_campeonato: (str) chave do dicionário dict_id_campeonato, caminho metadata/campeonatos_dafabet
        """
        
        id_campeonato = campeonato_dafabet(chave_campeonato)
        self.web.get(f'https://www.dafabet.com/pt/dfgoal/sports/240-football/{id_campeonato}')