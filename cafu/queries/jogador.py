from cafu.utils.webdriver_chrome import WebdriverChrome

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

    def _x_path(self, pos_v, pos_h):
        """
        Método interno da classe.
        Define o xpath do método find_element_by_xpath da biblioteca selenium, para a busca de uma informação em um jogo
        
        .. figure:: ../../../imagens_doc/ult_5_jogos.png
        
        Args:
            pos_v: (int) posição horizontal da informação na tabela, referente a coluna (1-time, 2-data, ....)
            pos_h: (int) posição vertical da informação na tabela, referente ao jogo (1-último, 2-penultimo, ...)
        Returns:
            str: xpath 
        """
        
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/div/div/div/div[2]/table/tbody/tr[{pos_h}]/td[{pos_v}]'
    
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
        
        response = int(self.web.find_element_by_xpath(self._x_path(10,jogo)).text)
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
            int: quantidade de cartões amarelos levados pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(14,jogo)).text)
        return response
    
    def cartoes_vermelhos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de cartões vermelhos levados pelo jogador
        """
        
        response = int(self.web.find_element_by_xpath(self._x_path(15,jogo)).text)
        return response
    
class Estatisticas(WebdriverChrome):
    """
    Extrai informações estatísticas das últimas temporadas do jogador
    
    Args:
        path_driver: (str) caminho para o chromedriver 
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/estatisticas/_/id/<id_jogador>.
                          Ex <id_jogador>='199017/everton-ribeiro'
    """
    
    def __init__(self, path_driver, id_jogador):
        super().__init__(path_driver)
        self.get_estatisticas_jogador(id_jogador)

    def _x_path(self, pos_v, pos_h):
        """
        Método interno da classe.
        Define o xpath do método find_element_by_xpath da biblioteca selenium, para a busca de uma informação em uma temporada
        
        .. figure:: ../../../imagens_doc/estatisticas.png
        
        Args:
            pos_v: (int) posição horizontal da informação na tabela, referente a coluna (1-titular, 2-faltas_cometidas, ....)
            pos_h: (int) posição vertical da informação na tabela, referente a temporada (1-último, 2-penultimo, ...)
        Returns:
            str: xpath 
        """
        
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{pos_h}]/td[{pos_v}]'
    
    def campeonato(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            str: campeonato
        """
        
        x_path = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/table/tbody/tr[{temporada}]/td[1]'
        return self.web.find_element_by_xpath(x_path).text
    
    def time(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            str: time do jogador
        """
        
        x_path = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/table/tbody/tr[{temporada}]/td[2]/div/a'
        return self.web.find_element_by_xpath(x_path).text
    
    def titular(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            str: quantidade de vezes em que o jogador foi titular
        """
        
        return self.web.find_element_by_xpath(self._x_path(1,temporada)).text
    
    def reserva(self, temporada):
        """
        Funciona apenas para a temporada atual
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            str: quantidade de vezes em que o jogador foi reserva
        """
        
        if temporada == 1:
            x_path = '//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[1]/div/div[2]'
            response = self.web.find_element_by_xpath(x_path).text.split(' ')[1]
            response = response.replace('(','').replace(')','')
            return response
        else:
            return None
        
    def faltas_cometidas(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de faltas cometidas pelo jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(2,temporada)).text
    
    def faltas_sofridas(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de faltas sofridas pelo jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(3,temporada)).text
    
    def cartoes_amarelos(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de cartões amarelos levados pelo jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(4,temporada)).text
    
    def cartoes_vermelhos(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de cartões vermelhos levados pelo jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(5,temporada)).text
    
    def gols(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de gols marcados pelo jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(6,temporada)).text
    
    def assistencias(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de assistências feitas pelo jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(7,temporada)).text
    
    def finalizacoes(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de finalizações feitas pelo jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(8,temporada)).text
    
    def finalizacoes_no_gol(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de finalizações no gol, feitas pelo jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(9,temporada)).text
    
    def impedimentos(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de impedimentos do jogador
        """
        
        return self.web.find_element_by_xpath(self._x_path(10,temporada)).text
    
class Bio(WebdriverChrome):
    """
    Extrai informações da biografia do jogador
    
    Args:
        path_driver: (str) caminho para o chromedriver 
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/bio/_/id/<id_jogador>.
                          Ex <id_jogador>='199017/everton-ribeiro'
    """
    
    def __init__(self, path_driver, id_jogador):
        super().__init__(path_driver)
        self.get_bio_jogador(id_jogador)

    def x_path(self, pos):
        """
        Método interno da classe.
        Define o xpath do método find_element_by_xpath da biblioteca selenium, para a busca de uma informação de biografia
        
        .. figure:: ../../../imagens_doc/biografia.png
        
        Args:
            pos: (int) posição na tabela biografia (2-posicao, 3-altura;massa, ...)
        Returns:
            str: xpath 
        """
        
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[1]/div/div[{pos}]/div/span[2]'
    
    def time(self, pos):
        """
        Todos os times do histórico de carreira do jogador
        Args:
            pos: (int) posição na tabela "Histórico da Carreira"
        Returns:
            tuple: time do jogador, quantidade de temporadas
        """
        
        x_path_time = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/a[{pos}]/div/span[1]'
        x_path_temps = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/a[{pos}]/div/span[2]'
        return self.web.find_element_by_xpath(x_path_time).text, self.web.find_element_by_xpath(x_path_temps).text
    
    def posicao(self):
        """
        Returns:
            str: posição do jogador
        """
        
        return self.web.find_element_by_xpath(self.x_path(2)).text
    
    def altura(self):
        """
        Returns:
            str: altura do jogador
        """
        
        return self.web.find_element_by_xpath(self.x_path(3)).text.split(', ')[0]
    
    def massa(self):
        """
        Returns:
            str: massa do jogador
        """
        
        return self.web.find_element_by_xpath(self.x_path(3)).text.split(', ')[1]
    
    def data_nascimento(self):
        """
        Returns:
            str: data de nascimento do jogador
        """
        
        return self.web.find_element_by_xpath(self.x_path(4)).text.split(' (')[0]
    
    def nacionalidade(self):
        """
        Returns:
            str: nacionalidade do jogador
        """
        
        return self.web.find_element_by_xpath(self.x_path(5)).text.split(' (')[0]