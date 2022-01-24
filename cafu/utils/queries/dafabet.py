user = 'luan61'
password = 'Lh5970'

from time import sleep
from cafu.utils.queries.webdriver_chrome import WebdriverChrome

class Login(WebdriverChrome):
    """
    Faz o login no site Dafabet
    
    Args:
        path_driver: (str) caminho para o chromedriver, optional
    """
    
    def __init__(self, path_driver=None):
        super().__init__(path_driver)
        
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
        
class TrafficOddsPartida(Login):
    """
    Tráfego entre as partidas de um campeonato
    
    Args:
        path_driver: (str) caminho para o chromedriver, optional
    """
    
    def __init__(self, path_driver=None):
        super().__init__(path_driver)
        
    def get_quantidade_partidas(self):
        """
        Returns:
            int: Quantidade de partidas no campeonato
        """
        
        partidas = self.web.find_elements_by_class_name('more_markets')
        return len(partidas)
        
    def join_link_odds_partida(self, index, max_iterate=5):
        """
        Entra dentro do link de uma partida, no campeonato

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