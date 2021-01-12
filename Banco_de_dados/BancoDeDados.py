from RequisiçãoESPN import RequisiçãoFutbeol
from datetime import date
import pandas as pd
import pickle as pk
import sqlite3 as sql

from FunçõesAuxiliaresBanco import comparar_datas
from FunçõesAuxiliaresBanco import indice_nulo

# ----------------------------------------------------------------------------------------------------------

def inicializar_campeonato(caminho, nome_campeonato, jogo_id_inicial, rodada_inicial, quantidade_partidas_rodada):
    
    jogos_ids_cresc_dec = input('Os jogos_ids do campeonato, são crescentes ou decrescentes? ')
    while jogos_ids_cresc_dec != 'crescente' and jogos_ids_cresc_dec != 'decrescente':
        jogos_ids_cresc_dec = input('Erro! Responda crescente ou decrescente:  ')
        
    if jogos_ids_cresc_dec == 'crescente':
        cres = 1
    else:
        cres = -1
    
    n = quantidade_partidas_rodada
    jogos_id = [str(int(jogo_id_inicial) + cres*i) for i in range(n)]
    jogos = []
    
    jogo_id = jogos_id[0]
    req = RequisiçãoFutbeol(jogo_id)
    req.req_data()
    req.req_nomes_times()
    data = req.data
    while req.nomes_times == None or req.data == None:
        req = RequisiçãoFutbeol(jogo_id)
        req.req_data()
        req.req_nomes_times()
    jogos.append({'times':req.nomes_times,'jogo_id': jogo_id, 'data': req.data})
    for i in range(1,n):
        jogo_id = jogos_id[i]
        req = RequisiçãoFutbeol(jogo_id)
        req.req_data()
        req.req_nomes_times()
        while req.nomes_times == None or req.data == None:
            req = RequisiçãoFutbeol(jogo_id)
            req.req_data()
            req.req_nomes_times()
        data = comparar_datas(data, req.data)
        jogos.append({'times':req.nomes_times, 'jogo_id': jogo_id, 'data': req.data})
    
    estado_campeonato = [{'quantidade_partidas_rodada': n, 'jogos_ids_cresc_dec': jogos_ids_cresc_dec,'rodada': rodada_inicial, 'rodada_lançada': False,'data_próximo_jogo': data, 'jogos': jogos}]
    s = pk.dumps(estado_campeonato)
    info=pd.DataFrame({'info':[s]})
    
    rodadas = pd.DataFrame({'rodada'+str(rodada_inicial): ['None' for i in range(n)]})
    
    try:
        conn = sql.connect(caminho + nome_campeonato + '.db')
        info.to_sql('estado_campeonato', conn, index=False, if_exists='fail')
        rodadas.to_sql('rodadas', conn, index=False, if_exists='fail')
    except:
        return 'Erro: Campeonato ja lançado no banco de dados!'
    
# ----------------------------------------------------------------------------------------------------------

from FunçõesAuxiliaresBanco import atualizar_rodadas
from FunçõesAuxiliaresBanco import atualizar_info
from FunçõesAuxiliaresBanco import rodada_lançada
    
def atualizar_campeonato(caminho, nome_campeonato):
    
    data = date.today()
    data_atual = [data.day, data.month, data.year]
    
    try: 
        arquivo_aberto = open(caminho + nome_campeonato + '.db', 'rb') # Verificando se o campeonato foi inicializado.
        
        conn = sql.connect(caminho + nome_campeonato + '.db')
        df = pd.read_sql('select * from estado_campeonato',conn)
        inf = pk.loads(df['info'][0])
        rodadas = pd.read_sql('select * from rodadas',conn)
    except:
        return 'Campeonato não encontrado.'
    
    qt_rodadas = input('Digite a quantidade de rodadas que deseja lançar: ')
    qt_rodadas = int(qt_rodadas)
    contagem = 1
    rodadas_atualizado = rodadas
    info_atualizado = [x for x in inf]
    stop = False
    while not stop: 
        try:
            rodadas = rodadas_atualizado
            inf = [x for x in info_atualizado]
            rodadas_atualizado = atualizar_rodadas(inf, rodadas) # Atualizando as rodadas do campeonato
        except:
            return 'Erro: Função atualizar_rodadas, Módulo FunçõesAuxiliaresBanco.'
        try:
            info_atualizado, rodadas_atualizado = atualizar_info(inf, rodadas_atualizado) # Atualizando as informações do campeonato
        except:
            info_atualizado, rodadas_atualizado = atualizar_info(inf, rodadas_atualizado)
            #return 'Erro: Função atualizar_info, Módulo FunçõesAuxiliaresBanco.'

        if info_atualizado[0]['data_próximo_jogo'] != None:
            data_próximo_jogo = info_atualizado[0]['data_próximo_jogo']
        else:
            data_próximo_jogo = [1,1,9999]
        for i in range(1,len(info_atualizado)):
            if info_atualizado[i]['data_próximo_jogo'] != None:
                data = info_atualizado[i]['data_próximo_jogo']
            else:
                data = [1,1,9999]
            data_próximo_jogo = comparar_datas(data_próximo_jogo, data)

        print('\nData do próximo jogo, a ser atualizado: ', data_próximo_jogo, '\n\nRODADA LANÇADA\n', rodada_lançada(info_atualizado, inf))
        
        contagem += 1
        if (comparar_datas(data_próximo_jogo, data_atual) != data_próximo_jogo) or (contagem > qt_rodadas):
            stop = True
            
    s = pk.dumps(info_atualizado)
    info_atualizado=pd.DataFrame({'info':[s]})
    conn = sql.connect(caminho + nome_campeonato + '.db')
    info_atualizado.to_sql('estado_campeonato', conn, index=False, if_exists='replace')
    rodadas_atualizado.to_sql('rodadas', conn, index=False, if_exists='replace')
    
# ----------------------------------------------------------------------------------------------------------

def decodificar_campeonato(nome_campeonato, caminho): # Decodifica o campeonato, que foi codificado utilizando a biblioteca pickle.
    
    try: 
        arquivo_aberto = open(caminho + nome_campeonato + '.db', 'rb') # Verificando se o campeonato foi inicializado.
        
        conn = sql.connect(caminho + nome_campeonato + '.db')
        rodadas = pd.read_sql('select * from rodadas',conn)
        info_codigo = pd.read_sql('select * from estado_campeonato',conn)      
    except:
        return ('Campeonato não encontrado.')
    
    info_decodificado = pk.loads(info_codigo['info'][0])
    campeonato_decodificado = rodadas.copy()
    quantidade_rodadas = campeonato_decodificado.shape[1]
    
    for i in range(quantidade_rodadas):
        rodada = []
        for j in range(len(campeonato_decodificado['rodada'+str(i+1)])):
            try:
                rodada.append(pk.loads(campeonato_decodificado['rodada'+str(i+1)][j]))
            except:
                rodada.append(campeonato_decodificado['rodada'+str(i+1)][j])
        campeonato_decodificado['rodada'+str(i+1)] = rodada
        
    return campeonato_decodificado, info_decodificado

# ----------------------------------------------------------------------------------------------------------

def times_rodadas(campeonato): # Retorna todos os jogos executados pelos times, ordenados pelas rodadas. Input: Campeonato decodificado.
    
    times = [] # Todos os times que disputam o campeonato
    
    times_lançados = False
    try:
        for jogo in campeonato['rodada1']:
            times.append(jogo.nomes_times[0])
            times.append(jogo.nomes_times[1])
        times_lançados = True
    except:
        times_lançados = False
    
    rod = 2
    while times_lançados == False and rod < campeonato.shape[1]:
        try:
            for jogo in campeonato['rodada'+str(rod)]:
                times.append(jogo.nomes_times[0])
                times.append(jogo.nomes_times[1])
            times_lançados = True
        except:
            times_lançados = False
        rod += 1
                
    resultado = {time: {'casa': [], 'visitante': []} for time in times}
        
    quantidade_rodadas = campeonato.shape[1]
    
    for i in range(quantidade_rodadas):
        for jogo in campeonato['rodada'+str(i+1)]:
            try:
                resultado[jogo.nomes_times[0]]['casa'].append(jogo)
                resultado[jogo.nomes_times[1]]['visitante'].append(jogo)
            except:
                a = None
    
    return resultado

# ----------------------------------------------------------------------------------------------------------

def times_datas(times_rodadas): # Retorna todos os jogos executados pelos times, ordenados por data. Input: Jogos ordenados pelas rodadas.
    
    resultado = {time: {'casa': [], 'visitante': []} for time in times_rodadas}
    
    for time in times_rodadas:
        
        jogos_restantes = [jogo for jogo in times_rodadas[time]['casa'] if jogo not in resultado[time]['casa']]
        while len(jogos_restantes) > 0: 
            
            lançar_jogo = jogos_restantes[0]
            for jogo in jogos_restantes:
                try:
                    if comparar_datas(lançar_jogo.data, jogo.data) == jogo.data:
                        lançar_jogo = jogo
                except:
                    a = None
            
            resultado[time]['casa'].append(lançar_jogo)
            jogos_restantes = [jogo for jogo in times_rodadas[time]['casa'] if jogo not in resultado[time]['casa']]
            
        jogos_restantes = [jogo for jogo in times_rodadas[time]['visitante'] if jogo not in resultado[time]['visitante']]
        while len(jogos_restantes) > 0: 
            
            lançar_jogo = jogos_restantes[0]
            for jogo in jogos_restantes:
                try:
                    if comparar_datas(lançar_jogo.data, jogo.data) == jogo.data:
                        lançar_jogo = jogo
                except:
                    a = None
            
            resultado[time]['visitante'].append(lançar_jogo)
            jogos_restantes = [jogo for jogo in times_rodadas[time]['visitante'] if jogo not in resultado[time]['visitante']]
            
    return resultado