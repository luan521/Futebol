import requests as r
from html2json import collect
import json
from bs4 import BeautifulSoup

from modulos.process.utils import sem_espaco, padrao, padrao_inicio_fim, mes
from modulos.process.process_info_espn import jogadores_inscritos, teste_gols, gols_casa_visitante

# ----------------------------------------------------------------------------------------------------------

def teste_jogo_finalizado(jogo_id):
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    ind_jogo_finalizado=padrao_inicio_fim(['class="game-time">\n'],['</span>\n'],abt)
    if len(ind_jogo_finalizado)>0:
        teste_jogo_finalizado = 'True'
    else:
        teste_jogo_finalizado = 'False'
    
    return teste_jogo_finalizado

# ----------------------------------------------------------------------------------------------------------

def campeonato(jogo_id):
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    ind=padrao_inicio_fim(['class="game-details','header">\n'],['</div>\n'],abt)
    abt1=abt[ind[0][0]:ind[0][1]][2:-1]
    
    campeonato=''
    for x in abt1:
        campeonato=campeonato + ' ' + x
    campeonato=campeonato[1:-1]
    
    return campeonato

# ----------------------------------------------------------------------------------------------------------

def data(jogo_id):
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    ind=padrao_inicio_fim(['<title>\n'],['</title>\n'],abt)
    
    abt1=abt[ind[0][0]:ind[0][1]]
    ind_date=padrao_inicio_fim(['partida'],['ESPN\n'],abt1)[0][0]+2
    
    date=abt1[ind_date:ind_date+3]
    date[1]=date[1][:-1]
    
    date[0] = int(date[0])
    date[1] = mes(date[1])
    date[2] = int(date[2])
    
    return date

# ----------------------------------------------------------------------------------------------------------

def formacao(jogo_id):
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    formacao_casa = None
    formacao_visitante = None
    
    teste = teste_jogo_finalizado(jogo_id)
    if teste == 'True':
        ind_formacao_casa=padrao_inicio_fim(['class="formations__text">\n'],['</div>\n'],abt)[0][0]+1
        ind_formacao_visitante=padrao_inicio_fim(['class="formations__text">\n'],['</div>\n'],abt)[1][0]+1
        formacao_casa = abt[ind_formacao_casa][:-1] 
        formacao_visitante = abt[ind_formacao_visitante][:-1]
    
    return formacao_casa, formacao_visitante
    
# ----------------------------------------------------------------------------------------------------------    

def nomes_times(jogo_id):
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
        
    ind=padrao_inicio_fim(['<title>\n'],['</title>\n'],abt)
    abt1=abt[ind[0][0]:ind[0][1]]
    ind_time_casa=padrao_inicio_fim(['<title>\n'],['X'],abt1)
    ind_time_visitante=padrao_inicio_fim(['X'],['-'],abt1)
    
    time_0=abt1[ind_time_casa[0][0]+1:ind_time_casa[0][1]-1]
    time_casa=''
    for x in time_0:
        time_casa = time_casa + ' ' + x
    time_casa=time_casa[1:]
    
    time_0=abt1[ind_time_visitante[0][0]+1:ind_time_visitante[0][1]-1]
    time_visitante=''
    for x in time_0:
        time_visitante = time_visitante + ' ' + x
    time_visitante=time_visitante[1:]
    
    return time_casa, time_visitante

# ----------------------------------------------------------------------------------------------------------

def jogadores(jogo_id):
    
    jogadores_casa_0, jogadores_visitante_0 = jogadores_inscritos(jogo_id)

    jogadores_casa_1=[]
    jogadores_visitante_1=[]
    s=1
    i=0
    while s<=12:
        if s<12 or jogadores_casa_0[i][2]!=0:
            jogadores_casa_1.append(jogadores_casa_0[i])
        i+=1
        if jogadores_casa_0[i][2]==0:
            s+=1
        
    s=1
    i=0
    while s<=12:
        if s<12 or jogadores_visitante_0[i][2]!=0:
            jogadores_visitante_1.append(jogadores_visitante_0[i])
        i+=1
        if jogadores_visitante_0[i][2]==0:
            s+=1
            
    jogadores_casa=[]
    jogadores_visitante=[]
    for i in range(len(jogadores_casa_1)):
        jogadores_casa.append({'nome': jogadores_casa_1[i][0], 'camisa': jogadores_casa_1[i][1], 'inicio_jogando': jogadores_casa_1[i][2], 'final_jogando': 90})
        if i<len(jogadores_casa_1)-1 and jogadores_casa_1[i+1][2]!=0:
            jogadores_casa[i]['final_jogando']=jogadores_casa_1[i+1][2]
        
    for i in range(len(jogadores_visitante_1)):
        jogadores_visitante.append({'nome': jogadores_visitante_1[i][0], 'camisa': jogadores_visitante_1[i][1], 'inicio_jogando': jogadores_visitante_1[i][2], 'final_jogando': 90})
        if i<len(jogadores_visitante_1)-1 and jogadores_visitante_1[i+1][2]!=0:
            jogadores_visitante[i]['final_jogando']=jogadores_visitante_1[i+1][2]
            
    return jogadores_casa, jogadores_visitante
    
# ----------------------------------------------------------------------------------------------------------    
    
def gols(jogo_id):

    teste_casa, teste_visitante = teste_gols(jogo_id)
    
    gols_casa = None
    if teste_casa:
        gols_casa = gols_casa_visitante(0,jogo_id)
    
    gols_visitante = None
    if teste_visitante:
        if teste_casa:
            gols_visitante = gols_casa_visitante(1,jogo_id)
        else:
            gols_visitante = gols_casa_visitante(0,jogo_id)
            
    return gols_casa, gols_visitante

# ---------------------------------------------------------------------------------------------------------- 

def placar(jogo_id):
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    ind_casa=padrao_inicio_fim(['<span', 'class="score', 'icon-font-after"', 'data-home-away="home"', 'data-stat="score">\n'],['</span>\n'],abt)
    gols_casa=abt[ind_casa[0][0]:ind_casa[0][1]][5][:-1]
    gols_casa=int(gols_casa)
    
    ind_visitante=padrao_inicio_fim(['<span', 'class="score', 'icon-font-before"', 'data-home-away="away"', 'data-stat="score">\n'],['</span>\n'],abt)
    gols_visitante=abt[ind_visitante[0][0]:ind_visitante[0][1]][5][:-1]
    gols_visitante=int(gols_visitante)
    
    return gols_casa, gols_visitante

# ---------------------------------------------------------------------------------------------------------- 

def posse(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    ind = padrao_inicio_fim(['Posse\n'],['</div>\n'],abt)
    abt1 = abt[ind[0][0]:ind[0][1]]
    ind = padrao(['data-stat="possessionPct">\n'],abt1)
    
    resultado_casa = float(abt1[ind[0][1]][:-2])/100
    resultado_visitante = float(abt1[ind[1][1]][:-2])/100
    
    return resultado_casa, resultado_visitante
    
# ---------------------------------------------------------------------------------------------------------- 

def chutes_fora_nogol(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    ind=padrao_inicio_fim(['chutes', '(no', 'gol)\n'],['data-home-away="away"'],abt)
    abt1=abt[ind[0][0]:ind[0][1]+10]
    
    ind=padrao(['data-stat="shotsSummary">\n'],abt1)
    resultado_casa = abt1[ind[0][1]:ind[0][1]+2]
    resultado_visitante =abt1[ind[1][1]:ind[1][1]+2]
    
    resultado_casa[1] = int(resultado_casa[1][1:-2])
    resultado_visitante[1] = int(resultado_visitante[1][1:-2])
    resultado_casa[0] = int(resultado_casa[0]) - resultado_casa[1]
    resultado_visitante[0] = int(resultado_visitante[0]) - resultado_visitante[1]
    
    return resultado_casa, resultado_visitante

# ---------------------------------------------------------------------------------------------------------- 

def faltas(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    imp=padrao(['faltas\n'],abt)
    
    resultado_casa = int(abt[imp[0][0]-3][:-1])
    resultado_visitante = int(abt[imp[0][0]+5][:-1])
    
    return resultado_casa, resultado_visitante

# ---------------------------------------------------------------------------------------------------------- 

def cartoes_amarelos(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    imp=padrao(['Cartões','amarelos\n'],abt)
    
    resultado_casa = int(abt[imp[0][0]-3][:-1])
    resultado_visitante = int(abt[imp[0][0]+6][:-1])
    
    return resultado_casa, resultado_visitante

# ---------------------------------------------------------------------------------------------------------- 

def cartoes_vermelhos(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    imp=padrao(['Cartões','Vermelhos\n'],abt)
    
    resultado_casa = int(abt[imp[0][0]-3][:-1])
    resultado_visitante = int(abt[imp[0][0]+6][:-1])
    
    return resultado_casa, resultado_visitante

# ---------------------------------------------------------------------------------------------------------- 

def impedimentos(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    imp=padrao(['Impedimentos\n'],abt)
    
    resultado_casa = int(abt[imp[0][0]-3][:-1])
    resultado_visitante = int(abt[imp[0][0]+5][:-1])
    
    return resultado_casa, resultado_visitante

# ---------------------------------------------------------------------------------------------------------- 

def escanteios(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    imp=padrao(['Escanteios\n'],abt)
    
    resultado_casa = int(abt[imp[0][0]-3][:-1])
    resultado_visitante = int(abt[imp[0][0]+5][:-1])
    
    return resultado_casa, resultado_visitante

# ---------------------------------------------------------------------------------------------------------- 

def defesas(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    imp=padrao(['defesas\n'],abt)
    
    resultado_casa = int(abt[imp[0][0]-3][:-1])
    resultado_visitante = int(abt[imp[0][0]+5][:-1])
    
    return resultado_casa, resultado_visitante

# ---------------------------------------------------------------------------------------------------------- 

def minuto_a_minuto(jogo_id):
    req = r.get("https://www.espn.com.br/futebol/comentario?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    ind = padrao_inicio_fim(['Principais\n'],['data-behavior="soccer_commentary_key_events"'],abt)
    abt1 = abt[ind[0][0]:ind[0][1]]
    
    ind = padrao_inicio_fim(['class="time-stamp">\n'],['</tr>\n'],abt1)
    
    minuto_a_minuto = []
    for x in ind:
        acontecimento = abt1[x[0]:x[1]]
    
        ind1 = padrao(['class="time-stamp">\n'],acontecimento)
        try:
            tempo = int(acontecimento[ind1[0][1]][:-2])
        except:
            final_do_jogo = True
            for x in minuto_a_minuto:
                if x['tempo'] < 90:
                    final_do_jogo = False
            if final_do_jogo:
                tempo = 90
            else:
                tempo = 0
    
        ind2=padrao_inicio_fim(['class="game-details">\n'],['</td>\n'],acontecimento)
        descricao = ''
        for palavra in acontecimento[ind2[0][0]+1:ind2[0][1]-1]:
            descricao = descricao + ' ' + palavra
        descricao = descricao[1:-1]
    
        minuto_a_minuto.append({'tempo': tempo, 'descrição' : descricao})
        
    return minuto_a_minuto

# ---------------------------------------------------------------------------------------------------------- 

class RequisicaoPartida():

    def __init__(self, jogo_id):
        
        self.jogo_id = jogo_id
        self.erros = []
        
        self.jogo_finalizado = None
        self.campeonato = None
        self.data = None
        self.nomes_times = None
        self.formacao = None
        self.jogadores = None
        self.gols = None
        self.placar = None
        self.posse = None
        self.chutes_fora_nogol = None
        self.faltas = None
        self.cartoes_amarelos = None
        self.cartoes_vermelhos = None
        self.impedimentos = None
        self.escanteios = None
        self.defesas = None
        self.minuto_a_minuto = None
    
    def req_teste_jogo_finalizado(self):
        try:
            self.jogo_finalizado = teste_jogo_finalizado(self.jogo_id)
        except:
            self.erros.append('jogo_finalizado')
            
    def req_campeonato(self):
        try:
            self.campeonato = campeonato(self.jogo_id)
        except:
            self.erros.append('campeonato')
            
    def req_data(self):
        try:
            self.data = data(self.jogo_id)
        except:
            self.erros.append('data')
            
    def req_nomes_times(self):
        try:
            self.nomes_times = nomes_times(self.jogo_id)
        except:
            self.erros.append('nomes_times')
            
    def req_formacao(self):
        try:
            self.formacao = formacao(self.jogo_id)
        except:
            self.erros.append('formacao')
            
    def req_jogadores(self):
        try:
            self.jogadores = jogadores(self.jogo_id)
        except:
            self.erros.append('jogadores')
            
    def req_gols(self):
        try:
            self.gols = gols(self.jogo_id)
        except:
            self.erros.append('gols')
            
    def req_placar(self):
        try:
            self.placar = placar(self.jogo_id)
        except:
            self.erros.append('placar')
            
    def req_posse(self):
        try:
            self.posse = posse(self.jogo_id)
        except:
            self.erros.append('posse')
            
    def req_chutes_fora_nogol(self):
        try:
            self.chutes_fora_nogol = chutes_fora_nogol(self.jogo_id)
        except:
            self.erros.append('chutes_fora_nogol')
            
    def req_faltas(self):
        try:
            self.faltas = faltas(self.jogo_id)
        except:
            self.erros.append('faltas')
            
    def req_cartoes_amarelos(self):
        try:
            self.cartoes_amarelos = cartoes_amarelos(self.jogo_id)
        except:
            self.erros.append('cartoes_amarelos')
            
    def req_cartoes_vermelhos(self):
        try:
            self.cartoes_vermelhos = cartoes_vermelhos(self.jogo_id)
        except:
            self.erros.append('cartoes_vermelhos')
            
    def req_impedimentos(self):
        try:
            self.impedimentos = impedimentos(self.jogo_id)
        except:
            self.erros.append('impedimentos')
            
    def req_escanteios(self):
        try:
            self.escanteios = escanteios(self.jogo_id)
        except:
            self.erros.append('escanteios')
            
    def req_defesas(self):
        try:
            self.defesas = defesas(self.jogo_id)
        except:
            self.erros.append('defesas')
            
    def req_minuto_a_minuto(self):
        try:
            self.minuto_a_minuto = minuto_a_minuto(self.jogo_id)
        except:
            self.erros.append('minuto_a_minuto')