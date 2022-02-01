from time import sleep
from tqdm import tqdm
from cafu.utils.queries.dafabet import TrafficOddsPartida
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'\\logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

class GetOdds(TrafficOddsPartida):
    """
    Busca as odds da partida
    
    Args:
        start_webdriver: (bool) se o Chrome driver deve ser iniciado
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, start_webdriver=True, headless=True):
        super().__init__(start_webdriver, headless)
        
        self.qt_mercados = None
        
    def open_odds(self, max_iterate=30):
        """
        Entra no link "Todos os mercados" e abre todas as odds
        
        Args:
            max_iterate: número máximo de tentativas
        Returns:
            int: quantidade de mercados na partida
        """
        
        try:
            market_group_all_selector = self.web.find_element_by_xpath('//*[@id="market_group_all"]')
            qt_mercados = market_group_all_selector.text.split('(')[1][:-1]
            market_group_all_selector.click()
            
            logging.info("P-1 SUCCESS queries.odds.GetOdds.open_odds: Open link Todos os mercados")
        except Exception as err:
            logging.error("ERROR queries.odds.GetOdds.open_odds: Unexpected error: Could not open link Todos os mercados")
            logging.error(err)
            
            return
        
        i = 1
        success = False 
        while (i<=max_iterate) and not success:
            try:
                eventos = self.web.find_elements_by_class_name('event_path-title.ellipsis.rollup-title.x.collapsed')
                for e in tqdm(eventos):
                    try:
                        e.click()
                    except:
                        pass
                if len(eventos) == 0:
                    success = True
            except:
                pass
            i+=1

        if success:
            logging.info("SUCCESS queries.odds.GetOdds.open_odds: Function executed successfully")
            
            return qt_mercados
        else:
            logging.error(f"ERROR queries.odds.GetOdds.open_odds: Unexpected error: Could not execute function with default max_iterate. <max_iterate>={max_iterate}")
            
            return
    
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

        try:
            response = {}
            for e in tqdm(elements_all_odds):
                odds = e.text
                if odds != '':
                    e.click()
                    class_evento = 'market-description.bg-info.text-md.text-light.p5.m0.pl10'
                    class_tipo_aposta = 'selection-market-period-description'
                    evento = self.web.find_elements_by_class_name(class_evento)[0].text
                    sleep(1)
                    tipo_aposta = self.web.find_elements_by_class_name(class_tipo_aposta)[0].text
                    sleep(1)
                    try:
                        response[tipo_aposta][evento] = odds
                    except:
                        response[tipo_aposta] = {evento: odds} 
                self._close_open_bets()
                sleep(1)
                
            logging.info("SUCCESS queries.odds.GetOdds.get_odds: Function executed successfully")
            
            return response
        except Exception as err:
            logging.error("ERROR queries.odds.GetOdds.get_odds: Unexpected error: Could not execute function")
            logging.error(err)