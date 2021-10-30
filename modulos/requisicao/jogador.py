from modulos.process.webdriver_chrome import WebdriverChrome

class UltimosCincoJogos(WebdriverChrome):
    """
    Extrai informações das cinco últimas partidas do jogador
    
    Args:
        path_driver: (str) caminho para o chromedriver 
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
                          Ex <id_jogador>='199017/everton-ribeiro'
    """
    
    def __init__(self, path_driver, id_jogador):
        super().__init__(path_driver)
        self.get_ult_cinco_jogos_jogador(id_jogador)

    def _x_path(self, pos_h, pos_v):
        """
        Método interno da classe.
        Define o xpath do método find_element_by_xpath da biblioteca selenium, para a busca de uma informação em um jogo
        
        .. figure:: ../../../imagens_doc/ult_5_jogos.png
        
        Args:
            pos_h: (int) posição horizontal da informação na tabela, referente a coluna (1-time, 2-data, ....)
            pos_v: (int) posição vertical da informação na tabela, referente ao jogo (1-último, 2-penultimo, ...)
        Returns:
            str: xpath 
        """
        
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/div/div/div/div[2]/table/tbody/tr[{pos_v}]/td[{pos_h}]'
    
    def time(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: time do jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(1,jogo)).text
    
    def date(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: data da partida 
        """
        
        return self.web.find_element_by_xpath(self._x_path(2,jogo)).text
    
    def casa_fora(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: se o jogo foi em casa ou fora
        """
        
        identificador = self.web.find_element_by_xpath(self._x_path(3,jogo)).text.split('\n')[0]
        if identificador == 'x':
            return 'casa'
        elif identificador == 'em':
            return 'fora'
    
    def adversario(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: time adversário
        """
        
        return self.web.find_element_by_xpath(self._x_path(3,jogo)).text.split('\n')[1]
    
    def campeonato(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: campeonato
        """
        
        return self.web.find_element_by_xpath(self._x_path(4,jogo)).text
    
    def resultado(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            dict: resultado-(V, E, D), placar
        """
        
        info = self.web.find_element_by_xpath(self._x_path(5,jogo)).text.split('\n')
        response = {'resultado': info[0], 'placar':info[1]}
        return response
    
    def titular_reserva(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: se o jogador foi titular ou reserva
        """
        
        return self.web.find_element_by_xpath(self._x_path(6,jogo)).text
    
    def gols(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de gols marcados pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(7,jogo)).text)
        return response
    
    def assistencias(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de assistências feitas pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(8,jogo)).text)
        return response
    
    def finalizacoes(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de finalizações feitas pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(9,jogo)).text)
        return response
    
    def finalizacoes_no_gol(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de finalizações no gol, feitas pelo jogador
        """
        
        reponse = int(self.web.find_element_by_xpath(self._x_path(10,jogo)).text)
        return response
    
    def faltas_cometidas(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de faltas cometidas pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(11,jogo)).text)
        return response
    
    def faltas_sofridas(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de faltas sofridas pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(12,jogo)).text)
        return response
    
    def impedimentos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de impedimentos do jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(13,jogo)).text)
        return response
    
    def cartoes_amarelos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de cartões amarelos levador pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(14,jogo)).text)
        return response
    
    def cartoes_vermelhos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de cartões vermelhos levador pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(15,jogo)).text)
        return response
    
class Estatisticas():
    
    def __init__(self, path_driver, id_jogador):
        super().__init__(path_driver)
        self.get_estatisticas_jogador(id_jogador)

    def _x_path(self, pos_h, pos_v):
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{pos_v}]/td[{pos_h}]'
    
    def campeonato(self, temporada):
        x_path = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/table/tbody/tr[{temporada}]/td[1]'
        return self.web.find_element_by_xpath(x_path).text
    
    def time(self, temporada):
        x_path = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/table/tbody/tr[{temporada}]/td[2]/div/a'
        return self.web.find_element_by_xpath(x_path).text
    
    def titular(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(1,temporada)).text
    
    def reserva(self, temporada):
        if temporada == 1:
            x_path = '//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[1]/div/div[2]'
            response = self.web.find_element_by_xpath(x_path).text.split(' ')[1]
            response = response.replace('(','').replace(')','')
            return response
        else:
            return None
        
    def faltas_cometidas(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(2,temporada)).text
    
    def faltas_sofridas(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(3,temporada)).text
    
    def cartoes_amarelos(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(4,temporada)).text
    
    def cartoes_vermelhos(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(5,temporada)).text
    
    def gols(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(6,temporada)).text
    
    def assistencias(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(7,temporada)).text
    
    def finalizacoes(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(8,temporada)).text
    
    def finalizacoes_no_gol(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(9,temporada)).text
    
    def impedimentos(self, temporada):
        return self.web.find_element_by_xpath(self._x_path(10,temporada)).text
    
class Bio():
    
    def __init__(self, path_driver, id_jogador):
        super().__init__(path_driver)
        self.get_bio_jogador(id_jogador)

    def x_path(self, pos):
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[1]/div/div[{pos}]/div/span[2]'
    
    def time(self, ordem):
        x_path_time = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/a[{ordem}]/div/span[1]'
        x_path_temps = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/a[{ordem}]/div/span[2]'
        return self.web.find_element_by_xpath(x_path_time).text, self.web.find_element_by_xpath(x_path_temps).text
    
    def posicao(self):
        return self.web.find_element_by_xpath(self.x_path(2)).text
    
    def altura(self):
        return web.find_element_by_xpath(self.x_path(3)).text.split(', ')[0]
    
    def massa(self):
        return web.find_element_by_xpath(self.x_path(3)).text.split(', ')[1]
    
    def data_nascimento(self):
        return web.find_element_by_xpath(self.x_path(4)).text.split(' (')[0]
    
    def nacionalidade(self):
        return web.find_element_by_xpath(self.x_path(5)).text.split(' (')[0]