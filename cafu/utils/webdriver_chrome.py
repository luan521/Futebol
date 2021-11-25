from selenium import webdriver

class WebdriverChrome():
    """
    Inicializa a sessão do chromedriver e entra em alguns links úteis
    
    Args:
        path_driver: (str) caminho para o chromedriver 
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
                          Ex <id_jogador>='199017/everton-ribeiro'
    """
    
    def __init__(self, path_driver):
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
        
    def get_odds_dafabet(self, campeonato):
        """
        Entra no link para a busca das odds no site Dafabet

        Args:
            campeonato: (str) completa o link https://www.dafabet.com/pt/dfgoal/sports/240-football/<id_campeonato>. 
                              Ex <campeontato>='brasil-a -> '<id_campeonato>=''22977-brazil/22980-brasileiro-serie-a''
        """
       
        dict_id_campeonato = {
                              'brasil-a': '22977-brazil/22980-brasileiro-serie-a',
                              'brasil-b': '22977-brazil/24267-brasileiro-serie-b',
                              'franca': '23168-france/23169-ligue-1'
                             }
       
        self.web.get(f'https://www.dafabet.com/pt/dfgoal/sports/240-football/{dict_id_campeonato[campeonato]}')