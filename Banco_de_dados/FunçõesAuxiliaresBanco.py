from RequisiçãoESPN import RequisiçãoFutbeol
import pickle as pk
from datetime import date
import pandas as pd
import numpy as np

def comparar_datas(data1, data2):
    
    if data1[2] == data2[2]:
        if data1[1] == data2[1]:
            if data1[0] < data2[0]:
                return data1
            else:
                return data2
        else:
            if data1[1] < data2[1]:
                return data1
            else:
                return data2
    else:
        if data1[2] < data2[2]:
            return data1
        else:
            return data2
        
def indice_nulo(lista):
    
    i = 0
    ind = None
    while ind == None and i < len(lista):
        if lista[i] == 'None':
            ind =i
        i+=1
            
    return ind
        
# Funções auxiliares da função: atualizar_campeonato

def atualizar_rodadas(info, rodadas_inp):
    
    data = date.today()
    data_atual = [data.day, data.month, data.year]
    
    rodadas = rodadas_inp
    
    for x in info:
        if not x['rodada_lançada']:
            if comparar_datas(data_atual, x['data_próximo_jogo']) == x['data_próximo_jogo']:
            
                numero_rodada = x['rodada']
                rodada = rodadas['rodada' + str(numero_rodada)]
                rodada = list(rodada)
                ind = indice_nulo(rodada)
            
                for jogo in x['jogos']:
                
                    jogo_id = jogo['jogo_id']
                
                    req = RequisiçãoFutbeol(jogo_id)
                    req.req_teste_jogo_finalizado()
                    jogo_finalizado = req.jogo_finalizado
                    while jogo_finalizado == None:
                        req = RequisiçãoFutbeol(jogo_id)
                        req.req_teste_jogo_finalizado()
                        jogo_finalizado = req.jogo_finalizado                        
                    
                    if jogo_finalizado == 'True':
                        req.req_campeonato()
                        req.req_data()
                        req.req_nomes_times()
                        req.req_formacao()
                        req.req_jogadores()
                        req.req_gols()
                        req.req_placar()
                        req.req_posse()
                        req.req_chutes_fora_nogol()
                        req.req_faltas()
                        req.req_cartoes_amarelos()
                        req.req_cartoes_vermelhos()
                        req.req_impedimentos()
                        req.req_escanteios()
                        req.req_defesas()
                        req.req_minuto_a_minuto()
                        s = pk.dumps(req)
                    
                        rodada[ind] = s 
                    
                        ind+=1
                    
                rodadas['rodada' + str(numero_rodada)] = rodada
    return rodadas

def atualizar_info(info_inp, rodadas_inp):
    rodadas = rodadas_inp
    info = []
    quantidade_partidas_rodada = info_inp[0]['quantidade_partidas_rodada']
    
    # Retirando os jogos em info, que ja foram lançados no sistema.
    for i in range(len(info_inp)):
        if i ==0:
            info.append({'quantidade_partidas_rodada': info_inp[i]['quantidade_partidas_rodada'], 'jogos_ids_cresc_dec': info_inp[i]['jogos_ids_cresc_dec'],'rodada': info_inp[i]['rodada'], 'rodada_lançada': False,'data_próximo_jogo': info_inp[i]['data_próximo_jogo'], 'jogos': []})
        else:
            info.append({'rodada': info_inp[i]['rodada'], 'rodada_lançada': False,'data_próximo_jogo': info_inp[i]['data_próximo_jogo'], 'jogos': []})
        
        jogos = info_inp[i]['jogos']           
        for m in range(len(jogos)):
            lançar_jogo = True
            for j in rodadas.iloc[:,i]:
                if j != 'None':
                    jogo = pk.loads(j)
                    jogo_id = jogo.jogo_id
                    if jogos[m]['jogo_id'] == jogo_id:
                        lançar_jogo = False
            
            if lançar_jogo:
                info[i]['jogos'].append(jogos[m])
                
        l = len(info[i]['jogos'])
        if l != 0:
            data = info[i]['jogos'][0]['data']
            for k in range(l):
                data = comparar_datas(data, info[i]['jogos'][k]['data'])
            info[i]['data_próximo_jogo'] = data
        else:
            info[i]['data_próximo_jogo'] = None
            info[i]['rodada_lançada'] = True
    
    quantidade_rodadas_campeonato = 4*quantidade_partidas_rodada-2
    # Garantindo que: A última rodada presente em info, que deverá ser atualizada, sempre tenha nenhum jogo lançado até o momento.
    l = len(info[-1]['jogos'])
    if (l != quantidade_partidas_rodada) and (info[-1]['rodada'] < quantidade_rodadas_campeonato): 
  
        numero_rodada = info[-1]['rodada'] + 1
        
        jogos_ids_rodada_passada = [int(info[-1]['jogos'][i]['jogo_id']) for i in range(l)]
        for j in rodadas.iloc[:,-1]:
            if j != 'None':
                jogo = pk.loads(j)
                jogo_id = int(jogo.jogo_id)
                jogos_ids_rodada_passada.append(jogo_id)
        
        if info[0]['jogos_ids_cresc_dec'] == 'decrescente':
            jogo_id_rodada = min(jogos_ids_rodada_passada)-1
        else:
            jogo_id_rodada = max(jogos_ids_rodada_passada)+1
        
        if info[0]['jogos_ids_cresc_dec'] == 'crescente':
            cres = 1
        else:
            cres = -1
        jogos_id = [str(int(jogo_id_rodada) + cres*i) for i in range(quantidade_partidas_rodada)]
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
            data = req.data
        jogos.append({'times':req.nomes_times,'jogo_id': jogo_id, 'data': req.data})
        for i in range(1, quantidade_partidas_rodada):
            jogo_id = jogos_id[i]
            req = RequisiçãoFutbeol(jogo_id)
            req.req_data()
            req.req_nomes_times()
            r_data = req.data
            r_n_times = req.nomes_times
            while r_data == None or r_n_times == None:
                req = RequisiçãoFutbeol(jogo_id)
                req.req_data()
                req.req_nomes_times()
                r_data = req.data
                r_n_times = req.nomes_times
            
            data = comparar_datas(data, req.data)
            jogos.append({'times':req.nomes_times, 'jogo_id': jogo_id, 'data': req.data})
                
        info.append({'rodada': numero_rodada, 'rodada_lançada': False,'data_próximo_jogo': data, 'jogos': jogos})
    
        rodada = ['None' for i in range(quantidade_partidas_rodada)]
        rodadas['rodada' + str(numero_rodada)] = rodada
    
    return info, rodadas

def rodada_lançada(info_atualizado, info):
    rodadas_lançadas = []
    for i in range(len(info)):
        rodadas_lançadas.append({'rodada': info[i]['rodada'], 'jogos': []})
        for j in range(len(info[i]['jogos'])):
            if sum(info[i]['jogos'][j] == np.array(info_atualizado[i]['jogos']))==0:
                rodadas_lançadas[i]['jogos'].append(info[i]['jogos'][j])
                
    rodadas_lançadas = [x for x in rodadas_lançadas if len(x['jogos'])>0]
    
    return rodadas_lançadas
    
        