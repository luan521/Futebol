from cafu.utils.webdriver_chrome import WebdriverChrome

user = 'luan61'
password = 'Lh5970'

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