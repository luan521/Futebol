from cafu.utils.queries.webdriver_chrome import WebdriverChrome
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'\\logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

class UltimosCincoJogos(WebdriverChrome):
    """
    Extrai informações das cinco últimas partidas do jogador
    
    Args:
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
                          Ex <id_jogador>='199017/everton-ribeiro'
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, id_jogador, headless=True):
        super().__init__(headless=headless)
        self.get_ult_cinco_jogos_jogador(id_jogador)

    def _x_path(self, pos_v, pos_h, section=2):
        """
        Método interno da classe.
        Define o xpath do método find_element_by_xpath da biblioteca selenium, para a busca de uma informação em um jogo
        
        .. figure:: ../../../imagens_doc/ult_5_jogos.png
        
        Args:
            pos_v: (int) posição horizontal da informação na tabela, referente a coluna (1-time, 2-data, ....)
            pos_h: (int) posição vertical da informação na tabela, referente ao jogo (1-último, 2-penultimo, ...)
            section: (int) parâmetro x_path, default=2, no caso <id_jogador>='199017/everton-ribeiro' <section> foi identificado com valor 1, em 29/01/2022
        Returns:
            str: xpath 
        """
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[{section}]/div/div/div/div/div[2]/table/tbody/tr[{pos_h}]/td[{pos_v}]'
    
    def time(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: time do jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(1,jogo)).text
        except:
            try:
                response = self.web.find_element_by_xpath(self._x_path(1,jogo,section=1)).text
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.time: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.time: Function executed successfully. <jogo>={jogo}")
        
        return response
                
    
    def date(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: data da partida 
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(2,jogo)).text
        except:
            try:
                response = self.web.find_element_by_xpath(self._x_path(2,jogo,section=1)).text
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.date: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.date: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def casa_fora(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: se o jogo foi em casa ou fora
        """
        
        try:
            identificador = self.web.find_element_by_xpath(self._x_path(3,jogo)).text.split('\n')[0]
        except:
            try:
                identificador = self.web.find_element_by_xpath(self._x_path(3,jogo,section=1)).text.split('\n')[0]
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.casa_fora: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
        
        if identificador == 'x':
            response = 'casa'
        elif identificador == 'em':
            response = 'fora'
        else:
            logging.error(f"ERROR queries.jogador.UltimosCincoJogos.casa_fora: Unexpected error: identificador not in (x, em). <jogo>={jogo}")  
            return
        
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.casa_fora: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def adversario(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: time adversário
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(3,jogo)).text.split('\n')[1]
        except:
            try:
                response = self.web.find_element_by_xpath(self._x_path(3,jogo,section=1)).text.split('\n')[1]
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.adversario: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.adversario: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def campeonato(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: campeonato
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(4,jogo)).text
        except:
            try:
                response = self.web.find_element_by_xpath(self._x_path(4,jogo,section=1)).text
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.campeonato: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.campeonato: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def resultado(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            dict: resultado-(V, E, D), placar
        """
        
        try:
            info = self.web.find_element_by_xpath(self._x_path(5,jogo)).text.split('\n')
        except:
            try:
                info = self.web.find_element_by_xpath(self._x_path(5,jogo,section=1)).text.split('\n')
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.resultado: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
        
        try:
            response = {'resultado': info[0], 'placar':info[1]}
            logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.resultado: Function executed successfully. <jogo>={jogo}")
            
            return response
        except:
            logging.error(f"ERROR queries.jogador.UltimosCincoJogos.resultado: Unexpected error: split method. <jogo>={jogo}")
            
            return
    
    def titular_reserva(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: se o jogador foi titular ou reserva
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(6,jogo)).text
        except:
            try:
                response = self.web.find_element_by_xpath(self._x_path(6,jogo,section=1)).text
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.titular_reserva: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.titular_reserva: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def gols(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de gols marcados pelo jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(7,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(7,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.gols: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.gols: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def assistencias(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de assistências feitas pelo jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(8,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(8,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.assistencias: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.assistencias: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def finalizacoes(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de finalizações feitas pelo jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(9,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(9,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.finalizacoes: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.finalizacoes: Function executed successfully. <jogo>={jogo}")
        
        return response
        
    def finalizacoes_no_gol(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de finalizações no gol, feitas pelo jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(10,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(10,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.finalizacoes_no_gol: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.finalizacoes_no_gol: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def faltas_cometidas(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de faltas cometidas pelo jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(11,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(11,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.faltas_cometidas: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.faltas_cometidas: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def faltas_sofridas(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de faltas sofridas pelo jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(12,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(12,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.faltas_sofridas: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.faltas_sofridas: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def impedimentos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de impedimentos do jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(13,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(13,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.impedimentos: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.impedimentos: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def cartoes_amarelos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de cartões amarelos levados pelo jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(14,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(14,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.cartoes_amarelos: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.cartoes_amarelos: Function executed successfully. <jogo>={jogo}")
        
        return response
    
    def cartoes_vermelhos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de cartões vermelhos levados pelo jogador
        """
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(15,jogo)).text)
        except:
            try:
                response = int(self.web.find_element_by_xpath(self._x_path(15,jogo,section=1)).text)
            except Exception as err:
                logging.error(f"ERROR queries.jogador.UltimosCincoJogos.cartoes_vermelhos: Unexpected error: Could not execute function. <jogo>={jogo}")
                logging.error(err)
                
                return
            
        logging.info(f"SUCCESS queries.jogador.UltimosCincoJogos.cartoes_vermelhos: Function executed successfully. <jogo>={jogo}")
        
        return response
    
class Estatisticas(WebdriverChrome):
    """
    Extrai informações estatísticas das últimas temporadas do jogador
    
    Args:
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/estatisticas/_/id/<id_jogador>.
                          Ex <id_jogador>='199017/everton-ribeiro'
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, id_jogador, headless=True):
        super().__init__(headless=headless)
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
        
        try:
            x_path = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/table/tbody/tr[{temporada}]/td[1]'
            response = self.web.find_element_by_xpath(x_path).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.campeonato: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.campeonato: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return
    
    def time(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            str: time do jogador
        """
        
        try:
            x_path = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/table/tbody/tr[{temporada}]/td[2]/div/a'
            response = self.web.find_element_by_xpath(x_path).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.time: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.time: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return
    
    def titular(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            str: quantidade de vezes em que o jogador foi titular
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(1,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.titular: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.titular: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return
            
    def reserva(self, temporada):
        """
        Funciona apenas para a temporada atual
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            str: quantidade de vezes em que o jogador foi reserva
        """
        
        if temporada == 1:
            try:
                x_path = '//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[1]/div/div[2]'
                response = self.web.find_element_by_xpath(x_path).text.split(' ')[1]
                response = response.replace('(','').replace(')','')
                logging.info(f"SUCCESS queries.jogador.Estatisticas.reserva: Function executed successfully. <temporada>={temporada}")
            
                return response
            except Exception as err:
                logging.error(f"ERROR queries.jogador.Estatisticas.reserva: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return
        else:
            logging.warning("WARNING queries.jogador.Estatisticas.reserva: Method works only for current season (<temporada>=1)")
            return
        
    def faltas_cometidas(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de faltas cometidas pelo jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(2,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.faltas_cometidas: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.faltas_cometidas: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
    def faltas_sofridas(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de faltas sofridas pelo jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(3,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.faltas_sofridas: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.faltas_sofridas: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
    def cartoes_amarelos(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de cartões amarelos levados pelo jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(4,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.cartoes_amarelos: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.cartoes_amarelos: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
    def cartoes_vermelhos(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de cartões vermelhos levados pelo jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(5,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.cartoes_vermelhos: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.cartoes_vermelhos: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
    def gols(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de gols marcados pelo jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(6,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.gols: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.gols: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
    def assistencias(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de assistências feitas pelo jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(7,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.assistencias: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.assistencias: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
    def finalizacoes(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de finalizações feitas pelo jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(8,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.finalizacoes: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.finalizacoes: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
    def finalizacoes_no_gol(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de finalizações no gol, feitas pelo jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(9,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.finalizacoes_no_gol: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.finalizacoes_no_gol: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
    def impedimentos(self, temporada):
        """
        Args:
            temporada: (int) (1-atual, 2-passada, ...)
        Returns:
            int: quantidade de impedimentos do jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(10,temporada)).text
            logging.info(f"SUCCESS queries.jogador.Estatisticas.impedimentos: Function executed successfully. <temporada>={temporada}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Estatisticas.impedimentos: Unexpected error: Could not execute function. <temporada>={temporada}")
            logging.error(err)
            
            return 
    
class Bio(WebdriverChrome):
    """
    Extrai informações da biografia do jogador
    
    Args:
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/bio/_/id/<id_jogador>.
                          Ex <id_jogador>='199017/everton-ribeiro'
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, id_jogador, headless=True):
        super().__init__(headless=headless)
        self.get_bio_jogador(id_jogador)

    def _x_path(self, pos):
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
        try:
            response = self.web.find_element_by_xpath(x_path_time).text, self.web.find_element_by_xpath(x_path_temps).text
            logging.info(f"SUCCESS queries.jogador.Bio.time: Function executed successfully. <pos>={pos}")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Bio.time: Unexpected error: Could not execute function. <pos>={pos}")
            logging.error(err)
            
            return 
    
    def posicao(self):
        """
        Returns:
            str: posição do jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(2)).text
            logging.info(f"SUCCESS queries.jogador.Bio.posicao: Function executed successfully")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Bio.posicao: Unexpected error: Could not execute function")
            logging.error(err)
            
            return 
    
    def altura(self):
        """
        Returns:
            str: altura do jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(3)).text.split(', ')[0]
            logging.info(f"SUCCESS queries.jogador.Bio.altura: Function executed successfully")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Bio.altura: Unexpected error: Could not execute function")
            logging.error(err)
            
            return 
    
    def massa(self):
        """
        Returns:
            str: massa do jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(3)).text.split(', ')[1]
            logging.info(f"SUCCESS queries.jogador.Bio.massa: Function executed successfully")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Bio.massa: Unexpected error: Could not execute function")
            logging.error(err)
            
            return 
    
    def data_nascimento(self):
        """
        Returns:
            str: data de nascimento do jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(4)).text.split(' (')[0]
            logging.info(f"SUCCESS queries.jogador.Bio.data_nascimento: Function executed successfully")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Bio.data_nascimento: Unexpected error: Could not execute function")
            logging.error(err)
            
            return
    
    def nacionalidade(self):
        """
        Returns:
            str: nacionalidade do jogador
        """
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(5)).text.split(' (')[0]
            logging.info(f"SUCCESS queries.jogador.Bio.nacionalidade: Function executed successfully")
            
            return response
        except Exception as err:
            logging.error(f"ERROR queries.jogador.Bio.nacionalidade: Unexpected error: Could not execute function")
            logging.error(err)
            
            return