from time import sleep
from cafu.utils.queries.dafabet import TrafficOddsPartida

class GetOdds(TrafficOddsPartida):
    """
    Busca as odds da partida
    
    Args:
        path_driver: (str) caminho para o chromedriver, optional
    """
    
    def __init__(self, path_driver=None):
        super().__init__(path_driver)
        
    def open_odds(self, max_iterate=30):
        """
        Entra no link "Todos os mercados" e abre todas as odds
        
        Args:
            max_iterate: número máximo de tentativas
        Returns:
            bool: se a execução foi bem sucedida
        """
        
        market_group_all_selector = self.web.find_element_by_xpath('//*[@id="market_group_all"]')
        market_group_all_selector.click()
        
        i = 1
        success = False 
        while (i<=max_iterate) and not success:
            try:
                eventos = self.web.find_elements_by_class_name('event_path-title.ellipsis.rollup-title.x.collapsed')
                for e in eventos:
                    try:
                        e.click()
                    except:
                        pass
                if len(eventos) == 0:
                    success = True
            except:
                pass
            i+=1

        return success
    
    def _close_open_bets(self):
        """
        Método interno da classe.
        Fecha as apostas abertas, para prosseguir com a coleta das odds
        """
        
        stop = False
        while not stop:
            try:
                class_button_exit = 'remove.icon-remove.icons-remove'
                button_exit = self.web.find_elements_by_class_name(class_button_exit)[0]
                button_exit.click()
            except:
                stop = True
        
    def get_odds(self):
        """
        Busca todas as odds da partida
        """
        
        class_name_all_odds = 'formatted_price.price'
        elements_all_odds = self.web.find_elements_by_class_name(class_name_all_odds)

        response = {}
        for e in elements_all_odds:
            odds = e.text
            if odds != '':
                e.click()
                class_evento = 'market-description.bg-info.text-md.text-light.p5.m0.pl10'
                class_tipo_aposta = 'selection-market-period-description'
                evento = self.web.find_elements_by_class_name(class_evento)[0].text
                sleep(2)
                tipo_aposta = self.web.find_elements_by_class_name(class_tipo_aposta)[0].text
                sleep(2)
                try:
                    response[tipo_aposta][evento] = odds
                except:
                    response[tipo_aposta] = {evento: odds} 
            self._close_open_bets()
        return response