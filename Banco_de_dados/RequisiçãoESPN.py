from FunçõesRequisiçãoESPN import teste_jogo_finalizado
from FunçõesRequisiçãoESPN import campeonato
from FunçõesRequisiçãoESPN import data
from FunçõesRequisiçãoESPN import formacao
from FunçõesRequisiçãoESPN import nomes_times
from FunçõesRequisiçãoESPN import jogadores
from FunçõesRequisiçãoESPN import gols
from FunçõesRequisiçãoESPN import placar
from FunçõesRequisiçãoESPN import posse
from FunçõesRequisiçãoESPN import chutes_fora_nogol
from FunçõesRequisiçãoESPN import faltas
from FunçõesRequisiçãoESPN import cartoes_amarelos
from FunçõesRequisiçãoESPN import cartoes_vermelhos
from FunçõesRequisiçãoESPN import impedimentos
from FunçõesRequisiçãoESPN import escanteios
from FunçõesRequisiçãoESPN import defesas
from FunçõesRequisiçãoESPN import minuto_a_minuto

class RequisiçãoFutbeol():

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