class UltimosCincoJogos():
    
    def __init__(self, web):
        self.web = web

    def x_path(self, pos_h, pos_v):
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/div/div/div/div[2]/table/tbody/tr[{pos_v}]/td[{pos_h}]'
    
    def date(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(2,jogo)).text
    
    def casa_fora(self, jogo):
        identificador = self.web.find_element_by_xpath(self.x_path(3,jogo)).text.split('\n')[0]
        if identificador == 'x':
            return 'casa'
        elif identificador == 'em':
            return 'fora'
    
    def adversario(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(3,jogo)).text.split('\n')[1]
    
    def campeonato(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(4,jogo)).text
    
    def resultado(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(5,jogo)).text
    
    def titular_reserva(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(6,jogo)).text
    
    def gols(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(7,jogo)).text
    
    def assistencias(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(8,jogo)).text
    
    def finalizacoes(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(9,jogo)).text
    
    def finalizacoes_no_gol(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(10,jogo)).text
    
    def faltas_cometidas(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(11,jogo)).text
    
    def faltas_sofridas(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(12,jogo)).text
    
    def impedimentos(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(13,jogo)).text
    
    def cartoes_amarelos(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(14,jogo)).text
    
    def cartoes_vermelhos(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(15,jogo)).text
    
class Estatisticas():
    
    def __init__(self, web):
        self.web = web

    def x_path(self, pos_h, pos_v):
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{pos_v}]/td[{pos_h}]'
    
    def campeonato(self, temporada):
        x_path = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/table/tbody/tr[{temporada}]/td[1]'
        return self.web.find_element_by_xpath(x_path).text
    
    def time(self, temporada):
        x_path = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div/div[2]/div[2]/table/tbody/tr[{temporada}]/td[2]/div/a'
        return self.web.find_element_by_xpath(x_path).text
    
    def titular(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(1,temporada)).text
    
    def reserva(self, temporada):
        if temporada == 1:
            x_path = '//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[1]/div/div[2]'
            response = self.web.find_element_by_xpath(x_path).text.split(' ')[1]
            response = response.replace('(','').replace(')','')
            return response
        else:
            return None
        
    def faltas_cometidas(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(2,temporada)).text
    
    def faltas_sofridas(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(3,temporada)).text
    
    def cartoes_amarelos(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(4,temporada)).text
    
    def cartoes_vermelhos(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(5,temporada)).text
    
    def gols(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(6,temporada)).text
    
    def assistencias(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(7,temporada)).text
    
    def finalizacoes(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(8,temporada)).text
    
    def finalizacoes_no_gol(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(9,temporada)).text
    
    def impedimentos(self, temporada):
        return self.web.find_element_by_xpath(self.x_path(10,temporada)).text
    
class Bio():
    
    def __init__(self, web):
        self.web = web

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