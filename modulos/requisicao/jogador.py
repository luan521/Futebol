class UltimosCincoJogos():
    
    def __init__(self, web):
        self.web = web

    def x_path(self, pos_h, pos_v):
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/div/div/div/div[2]/table/tbody/tr[{pos_v}]/td[{pos_h}]'
    
    def date(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(2,jogo)).text
    
    def adversario(self, jogo):
        return self.web.find_element_by_xpath(self.x_path(3,jogo)).text
    
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