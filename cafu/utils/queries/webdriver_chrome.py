from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from cafu.metadata.campeonatos_dafabet import campeonato_dafabet
from cafu.metadata.paths import path
path_driver = path('initial_path')+'/chromedriver'

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

class WebdriverChrome():
    """
    Inicializa a sessão do chromedriver e entra em alguns links úteis. 
    Método self.web.close() fecha a sessão do Chrome driver
    
    Args:
        start_webdriver: (bool) se o Chrome driver deve ser iniciado
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, start_webdriver=True, headless=True):
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            if start_webdriver:
                self.web = webdriver.Chrome(path_driver, options=chrome_options)
                
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome: "
                         f"Chromedriver started successfully. <start_webdriver>={start_webdriver}, "
                         f"<headless>={headless}")
        except Exception as err:
            logging.error("ERROR utils.queries.webdriver_chrome.WebdriverChrome: Unexpected error: "
                          f"Could started Chromedriver. <start_webdriver>={start_webdriver}, "
                          f"<headless>={headless}")
            logging.error(err)
        
    def get_ult_cinco_jogos_jogador(self, id_jogador):
        """
        Entra no link para a busca das informações dos últimos cinco jogos do jogador

        Args:
            id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
                              Ex <id_jogador>='199017/everton-ribeiro'
        """
        
        try:
            self.web.get(f'https://www.espn.com.br/futebol/jogador/_/id/{id_jogador}')
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome.get_ult_cinco_jogos_jogador: "
                         f"Function executed successfully. <id_jogador>={id_jogador}")
        except Exception as err:
            logging.error(f"ERROR utils.queries.webdriver_chrome.WebdriverChrome.get_ult_cinco_jogos_jogador: "
                          f"Unexpected error: Could not execute function. <id_jogador>={id_jogador}")
            logging.error(err)
        
    def get_estatisticas_jogador(self, id_jogador):
        """
        Entra no link para a busca das estatísticas do jogador

        Args:
            id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/estatisticas/_/id/<id_jogador>. 
                              Ex <id_jogador>='199017/everton-ribeiro'
        """
        
        try:
            self.web.get(f'https://www.espn.com.br/futebol/jogador/estatisticas/_/id/{id_jogador}')
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome.get_estatisticas_jogador: "
                         f"Function executed successfully. <id_jogador>={id_jogador}")
        except Exception as err:
            logging.error(f"ERROR utils.queries.webdriver_chrome.WebdriverChrome.get_estatisticas_jogador: "
                          f"Unexpected error: Could not execute function. <id_jogador>={id_jogador}")
            logging.error(err)
        
    def get_bio_jogador(self, id_jogador):
        """
        Entra no link para a busca da biografia do jogador

        Args:
            id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/bio/_/id/<id_jogador>. 
                              Ex <id_jogador>='199017/everton-ribeiro'
        """
        
        try:
            self.web.get(f'https://www.espn.com.br/futebol/jogador/bio/_/id/{id_jogador}')
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome.get_bio_jogador: "
                         f"Function executed successfully. <id_jogador>={id_jogador}")
        except Exception as err:
            logging.error(f"ERROR utils.queries.webdriver_chrome.WebdriverChrome.get_bio_jogador: "
                          f"Unexpected error: Could not execute function. <id_jogador>={id_jogador}")
            logging.error(err)
        
    def get_campeonato_dafabet(self, chave_campeonato):
        """
        Entra no link para a busca das odds no site Dafabet

        Args:
            chave_campeonato: (str) chave do dicionário dict_id_campeonato, caminho metadata/campeonatos_dafabet
        """
        
        try:
            id_campeonato = campeonato_dafabet(chave_campeonato)
            self.web.get(f'https://www.dafabet.com/pt/dfgoal/sports/240-football/{id_campeonato}')
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome.get_campeonato_dafabet: "
                         f"Function executed successfully. <chave_campeonato>={chave_campeonato}")
        except Exception as err:
            logging.error(f"ERROR utils.queries.webdriver_chrome.WebdriverChrome.get_campeonato_dafabet: "
                          f"Unexpected error: Could not execute function. <chave_campeonato>={chave_campeonato}")
            logging.error(err)