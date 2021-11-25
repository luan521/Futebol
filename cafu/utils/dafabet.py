from cafu.utils.webdriver_chrome import WebdriverChrome

user = 'luan61'
password = 'Lh5970'

from time import sleep
from cafu.utils.webdriver_chrome import WebdriverChrome

class Login(WebdriverChrome):
    """
    Faz o login no site Dafabet
    
    Args:
        path_driver: (str) caminho para o chromedriver 
        campeonato: (str) completa o link https://www.dafabet.com/pt/dfgoal/sports/240-football/<id_campeonato>. 
                          Ex <campeontato>='brazil -> '<id_campeonato>='22977-brazil'. Optional
    """
    
    def __init__(self, path_driver, campeonato=None):
        super().__init__(path_driver)
        if campeonato is not None:
            self.get_odds_dafabet(campeonato)
        else:
            self.web.get(f'https://www.dafabet.com/pt/dfgoal/sports/240-football')
        
    def login(self):
        """
        Faz o login no site Dafabet
        """
        
        # css selector
        user_path = '#LoginForm_username'
        password_path = '#LoginForm_password'
        enter_button_path = '#LoginForm_submit'

        # get elements
        user_element = self.web.find_element_by_css_selector(user_path)
        password_element = self.web.find_element_by_css_selector(password_path)
        enter_button_element = self.web.find_element_by_css_selector(enter_button_path)
        
        # send values
        user_element.send_keys(user)
        password_element.send_keys(password)
        enter_button_element.click()
        
class TrafficOddsPartida(WebdriverChrome):
    """
    Busca as odds no site Datafabet
    
    Args:
        path_driver: (str) caminho para o chromedriver 
        campeonato: (str) completa o link https://www.dafabet.com/pt/dfgoal/sports/240-football/<id_campeonato>. 
                          Ex <campeontato>='brazil -> '<id_campeonato>='22977-brazil'. Optional
    """
    
    def __init__(self, path_driver, campeonato):
        super().__init__(path_driver)
        self.get_odds_dafabet(campeonato)
        
    def join_link_odds_partida(self, index, max_iterate=5):
        """
        Entra dentro do link de uma partida, no <campeonato>

        Args:
            index: (int) índice da partida do campeonato
            max_iterate: número máximo de tentativas
        Returns:
            str: descrição da partida, quando o método é bem sucedido
        """

        i = 1
        success = False 
        while (i<=max_iterate) and not success:
            try:
                partidas = self.web.find_elements_by_class_name('more_markets')
                qt_odds = partidas[index].text
                if qt_odds == '0':
                    break
                partidas[index].click()
                sleep(2)
                descricao_partida = {}
                try:
                    descricao_partida_texto = self.web.find_elements_by_class_name('event-header-description')[0].text
                    descricao_partida['horario'] = descricao_partida_texto.split('\n')[1][9:]
                    descricao_partida['time_casa'] = descricao_partida_texto.split('\n')[0].split(' vs ')[0]
                    descricao_partida['time_visitante'] = descricao_partida_texto.split('\n')[0].split(' vs ')[1]
                except:
                    descricao_partida_texto = self.web.find_elements_by_class_name('live-event')[0].text
                    descricao_partida['horario'] = 'ao vivo'
                    descricao_partida['time_casa'] = descricao_partida_texto.split(' vs ')[0]
                    descricao_partida['time_visitante'] = descricao_partida_texto.split(' vs ')[1]
                success = True
            except:
                pass
            i+=1

        if success:
            return descricao_partida
        else:
            return 'failure'