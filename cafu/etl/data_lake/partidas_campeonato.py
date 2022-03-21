import pandas as pd
import pyspark.sql.functions as F
import json
from tqdm import tqdm
import time
from datetime import datetime
from cafu.utils.etl.datalake import partidas_desatualizadas
from cafu.utils.etl.partidas_campeonato import id_left_right
from cafu.utils.string import convert_str_var_time
from cafu.metadata.campeonatos_espn import campeonato_espn
from cafu.metadata import get_schema
from cafu.queries.partida import Partida
from cafu.metadata.paths import path
path_datalake = path('datalake')

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def _teste_partidas_campeonato(df, qt_jogos_rodada, qt_partidas_campeonato, 
                               ids, excedentes, campeonato, temporada, runtime_str):
    """
    Método interno da biblioteca cafu.
    Testa as condições de sucesso da função partidas_campeonato
    """
    
    times = list(df['time_casa'].append(df['time_visitante']).drop_duplicates().sort_values())
    jogos_faltantes = {}
    for i, t in enumerate(times):
        index_filter = df['time_casa']==t
        times_enfrentados = list(df[index_filter]['time_visitante'].drop_duplicates().sort_values())
        times_copy = times[:i]+times[(i+1):]
        f = list(set(times_copy).difference(times_enfrentados))
        if len(f) > 0:
            jogos_faltantes[t] = f
    
    success = True
    if df.shape[0] != qt_partidas_campeonato:
        success = False
        logging.error(f"ERROR etl.data_lake.partidas_campeonato.partidas_campeonato: "
                      f"Unexpected number of lines in returned dataframe (expected amount of league matches): "
                      f"<returned>={df.shape[0]}, <expected>={qt_partidas_campeonato}. "
                      f"Return <min_id_campeonato>={min(ids)}, <max_id_campeonato>={max(ids)}, <excedentes>={excedentes}. "
                      f"<campeonato>={campeonato}, <temporada>={temporada}, <qt_jogos_rodada>={qt_jogos_rodada}. "
                      f"runtime = {runtime_str}")
    if len(times)!=2*qt_jogos_rodada:
        success = False
        logging.error(f"ERROR etl.data_lake.partidas_campeonato.partidas_campeonato: "
                      f"Unexpected number of teams: "
                      f"<returned>={len(times)} <expected>={2*qt_jogos_rodada}. "
                      f"Return <min_id_campeonato>={min(ids)}, <max_id_campeonato>={max(ids)}, <excedentes>={excedentes}. "
                      f"<campeonato>={campeonato}, <temporada>={temporada}, <qt_jogos_rodada>={qt_jogos_rodada}. "
                      f"runtime = {runtime_str}")
    if len(jogos_faltantes)>0:
        success = False
        logging.error(f"ERROR etl.data_lake.partidas_campeonato.partidas_campeonato: "
                      f"Not all returned teams faced each other: "
                      f"<jogos_faltantes>={jogos_faltantes}. "
                      f"Return <min_id_campeonato>={min(ids)}, <max_id_campeonato>={max(ids)}, <excedentes>={excedentes}. "
                      f"<campeonato>={campeonato}, <temporada>={temporada}, <qt_jogos_rodada>={qt_jogos_rodada}. "
                      f"runtime = {runtime_str}")
    if success:
        logging.info(f"SUCCESS etl.data_lake.partidas_campeonato.partidas_campeonato: Function executed successfully. "
                 f"Return <min_id_campeonato>={min(ids)}, <max_id_campeonato>={max(ids)}. "
                 f"<campeonato>={campeonato}, <temporada>={temporada}, <qt_jogos_rodada>={qt_jogos_rodada}. "
                 f"runtime = {runtime_str}")

def partidas_campeonato(campeonato, temporada):
    """
    Busca as partidas do campeonato, no site da ESPN
        
    Args:
        campeonato: (str) chave primária do dicionário campeonatos, caminho metadata/campeonatos_espn
        temporada: (str) chave secundária do dicionário campeonatos, caminho metadata/campeonatos_espn
    Returns:
         pandas dataframe: jogo_id, dates, rodada, time_casa, time_visitante
    """
    
    logging.info(f"INFO etl.data_lake.partidas_campeonato.partidas_campeonato: "
                 f"Function started. <campeonato>={campeonato}, <temporada>={temporada}")

    init = time.time()
    
    dados_campeonato = campeonato_espn(campeonato, temporada)
    campeonato = dados_campeonato['nome']
    id_inicial =dados_campeonato['id']
    qt_jogos_rodada = dados_campeonato['qt_jogos_rodada']
    qt_partidas_campeonato = 2*qt_jogos_rodada*(2*qt_jogos_rodada-1)
    ids, partidas, dates = id_left_right(id_inicial, campeonato, qt_partidas_campeonato)
    ids, partidas, dates = id_left_right(id_inicial+1, campeonato, qt_partidas_campeonato,
                                         left=False, partidas=partidas, dates=dates, ids=ids)
    
    try:
        data = []
        excedentes = len(partidas)%qt_jogos_rodada
        for i in range(len(partidas)-excedentes):
            data.append([ids[i], dates[i], partidas[i]])
        df = pd.DataFrame(data, columns=['jogo_id', 'dates', 'partida']).sort_values('jogo_id')
        df.index = range(df.shape[0])

        # criando coluna "rodada"
        dates = []
        for i in range(0,df.shape[0], qt_jogos_rodada):
            median_date = df.iloc[i:i+qt_jogos_rodada]['dates'].median()
            dates_0 = [median_date for i in range(qt_jogos_rodada)]
            dates = dates+dates_0
        df['median_dates'] = dates[:df.shape[0]]
        df = df.sort_values(['median_dates'])
        rodadas = [i for i in range(1,(qt_jogos_rodada*2-1)*2+1) for j in range(qt_jogos_rodada)]
        df['rodada'] = rodadas[:df.shape[0]]
        df = df.drop('median_dates',axis=1)
        df = df.sort_values(['jogo_id'])

        df[['time_casa','time_visitante']] = pd.DataFrame(df['partida'].values.tolist(), index= df.index)
        df = df.drop('partida', axis=1)
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        _teste_partidas_campeonato(df, qt_jogos_rodada, qt_partidas_campeonato, 
                                   ids, excedentes, campeonato, temporada, runtime_str)
        
        return df
    except Exception as err:
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.error(f"ERROR etl.data_lake.partidas_campeonato.partidas_campeonato: Unexpected error: "
                      f"Could not execute function. Return <min_id_campeonato>={min(ids)}, "
                      f"<max_id_campeonato>={max(ids)}. <campeonato>={campeonato}, <temporada>={temporada}, "
                      f"<qt_jogos_rodada>={qt_jogos_rodada}. runtime = {runtime_str}")
        logging.error(err)
        return
    
def update_jogos_ids():
    """
    Atualiza datalake.jogos_ids
    """
    
    logging.info("INFO etl.data_lake.partidas_campeonato.update_jogos_ids: "
                 "Function started")
    
    # buscando campeonatos definidos no projeto
    campeonatos0 = campeonato_espn()
    campeonatos = [
                   [k1, k2] for k1 in list(campeonatos0.keys()) 
                            for k2 in list(campeonatos0[k1].keys())
                  ]
    
    # buscando campeonatos já atualizados
    r = open(path('datalake')+'/metadata.json')
    metadata = json.load(r)
    campeonatos_atualizados = [
                           [k1, k2] for k1 in list(metadata['jogos_ids'].keys()) 
                                    for k2 in list(metadata['jogos_ids'][k1].keys())
                                    if metadata['jogos_ids'][k1][k2] != 'failed'
                          ]
    
    # removendo campeonatos já atualizados
    for c in campeonatos_atualizados: campeonatos.remove(c)
    
    # atualizando campeonatos
    for c in campeonatos:
        camp, temporada = c[0], c[1]
        try:
            df = partidas_campeonato(camp, temporada)           
            path_save = path('datalake')+f'/jogos_ids/{camp}/{temporada}.csv'
            df.to_csv(path_save, index=False)
            metadata['jogos_ids'][camp][temporada] = 'evaluation'
            with open(path('datalake')+'/metadata.json', 'w') as fp:
                json.dump(metadata, fp)
            logging.info(f"INFO etl.data_lake.partidas_campeonato.update_partidas_campeonato: "
                         f"Update league {camp} | {temporada}.")
        except Exception as err:
            logging.error("ERROR etl.data_lake.partidas_campeonato.update_partidas_campeonato: "
                          f"Could not update league {camp} | {temporada}")
            logging.error(err)
            return
        
    if len(campeonatos)==0:    
        logging.info("INFO etl.data_lake.partidas_campeonato.update_partidas_campeonato: "
                     "All leagues already up to date")
        
def update_partidas(spark):
    """
    Atualiza datalake.partidas
    
    Args:
        spark: (spark session) 
    """
    
    logging.info("INFO etl.data_lake.partidas_campeonato.update_partidas: "
                 "Function started")
    
    partidas = partidas_desatualizadas()
    if len(partidas)==0:
        logging.info("INFO etl.data_lake.partidas_campeonato.update_partidas: "
                     "Already up to date")
    for c in partidas:
        for t in partidas[c]:
            init = time.time()
            for jogo_id in tqdm(partidas[c][t]):
                req = Partida(jogo_id, check_status = False)
                failed = []
                try:
                    # dataframe df_resumo
                    campeonato = req.campeonato()
                    date = req.day()
                    time_casa, time_visitante = req.nomes_times()
                    formacao_time_casa, formacao_time_visitante = req.formacao()
                    time_casa_gols_feitos, time_visitante_gols_feitos = req.placar()
                    time_casa_posse, time_visitante_posse = req.posse()
                    chutes_fora_nogol = req.chutes_fora_nogol()
                    time_casa_faltas_cometidas, time_visitante_faltas_cometidas = req.faltas()
                    time_casa_cartoes_amarelos, time_visitante_cartoes_amarelos = req.cartoes_amarelos()
                    time_casa_cartoes_vermelhos, time_visitante_cartoes_vermelhos = req.cartoes_vermelhos()
                    time_casa_impedimentos, time_visitante_impedimentos = req.impedimentos()
                    time_casa_escanteios, time_visitante_escanteios = req.escanteios()
                    time_casa_defesas, time_visitante_defesas = req.defesas()

                    data = [
                            {
                             'jogo_id': jogo_id,   
                             'campeonato': campeonato,
                             'campeonato_metadata': c,
                             'temporada_metadata': t, 
                             'date': date,
                             'time_casa': time_casa,
                             'time_visitante': time_visitante,
                             'formacao_time_casa': formacao_time_casa,
                             'formacao_time_visitante': formacao_time_visitante,
                             'time_casa_gols_feitos': time_casa_gols_feitos,
                             'time_visitante_gols_feitos': time_visitante_gols_feitos,
                             'time_casa_posse': time_casa_posse,
                             'time_visitante_posse': time_visitante_posse,
                             'time_casa_chutes_fora': chutes_fora_nogol[0][0],
                             'time_casa_chutes_nogol': chutes_fora_nogol[0][1],
                             'time_visitante_chutes_fora': chutes_fora_nogol[1][0],
                             'time_visitante_chutes_nogol': chutes_fora_nogol[1][1],
                             'time_casa_faltas_cometidas': time_casa_faltas_cometidas,
                             'time_visitante_faltas_cometidas': time_visitante_faltas_cometidas,
                             'time_casa_cartoes_amarelos': time_casa_cartoes_amarelos,
                             'time_visitante_cartoes_amarelos': time_visitante_cartoes_amarelos,
                             'time_casa_cartoes_vermelhos': time_casa_cartoes_vermelhos,
                             'time_visitante_cartoes_vermelhos': time_visitante_cartoes_vermelhos,
                             'time_casa_impedimentos': time_casa_impedimentos,
                             'time_visitante_impedimentos': time_visitante_impedimentos,   
                             'time_casa_escanteios': time_casa_escanteios,   
                             'time_visitante_escanteios': time_visitante_escanteios,   
                             'time_casa_defesas': time_casa_defesas,   
                             'time_visitante_defesas': time_visitante_defesas,   
                             'date_update':  datetime.now()
                            }
                           ]

                    schema = get_schema('partidas_resumo')
                    df_resumo = spark.createDataFrame(data, schema=schema)
                except Exception as err:
                    logging.error(f"ERROR etl.data_lake.partidas_campeonato.update_partidas: "
                                  f"Could not create dataframe df_resumo. "
                                  f"<campeonato>={c}, <temporada>={t}, <jogo_id>={jogo_id}")
                    logging.error(err)
                    failed.append('df_resumo')
                try:
                    # dataframe df_jogadores
                    jogadores = req.jogadores()
                    jogadores_casa = (
                                         spark.createDataFrame(jogadores[0])
                                         .withColumn('casa_visitante', F.lit('casa'))
                                         .withColumn('jogo_id', F.lit(jogo_id))
                                     )
                    jogadores_visitante = (
                                              spark.createDataFrame(jogadores[1])
                                              .withColumn('casa_visitante', F.lit('visitante'))
                                              .withColumn('jogo_id', F.lit(jogo_id))
                                          )
                    df_jogadores = (
                                       jogadores_casa
                                       .unionByName(jogadores_visitante)
                                       .withColumn('date_update', F.lit(datetime.now()))
                                   )

                    schema = get_schema('partidas_jogadores_minutagens')
                    df_jogadores = spark.createDataFrame(df_jogadores.collect(), schema=schema)
                except Exception as err:
                    logging.error(f"ERROR etl.data_lake.partidas_campeonato.update_partidas: "
                                  f"Could not create dataframe df_jogadores. "
                                  f"<campeonato>={c}, <temporada>={t}, <jogo_id>={jogo_id}")
                    logging.error(err)
                    failed.append('df_jogadores')
                try:
                    # dataframe df_gols
                    gols = req.gols()
                    if gols[0] is not None:
                        gols_casa = (
                                         spark.createDataFrame(gols[0])
                                         .withColumn('casa_visitante', F.lit('casa'))
                                         .withColumn('jogo_id', F.lit(jogo_id))
                                    )
                    if gols[1] is not None:
                        gols_visitante = (
                                              spark.createDataFrame(gols[1])
                                              .withColumn('casa_visitante', F.lit('visitante'))
                                              .withColumn('jogo_id', F.lit(jogo_id))
                                         )
                    if (gols[0] is not None) and (gols[1] is not None):
                        df_gols = (
                                      gols_casa
                                      .unionByName(gols_visitante)
                                      .withColumn('minuto_gol', F.explode('minutos_gols'))
                                      .drop('minutos_gols')
                                      .withColumn('date_update', F.lit(datetime.now()))
                                  )
                    elif gols[0] is not None:
                        df_gols = (
                                      gols_casa
                                      .withColumn('minuto_gol', F.explode('minutos_gols'))
                                      .drop('minutos_gols')
                                      .withColumn('date_update', F.lit(datetime.now()))
                                  )
                    elif gols[1] is not None:
                        df_gols = (
                                      gols_visitante
                                      .withColumn('minuto_gol', F.explode('minutos_gols'))
                                      .drop('minutos_gols')
                                      .withColumn('date_update', F.lit(datetime.now()))
                                  )

                    if (gols[0] is not None) or (gols[1] is not None):
                        schema = get_schema('partidas_gols')
                        df_gols = spark.createDataFrame(df_gols.collect(), schema=schema)
                    else:
                        df_gols = None
                except Exception as err:
                    logging.error(f"ERROR etl.data_lake.partidas_campeonato.update_partidas: "
                                  f"Could not create dataframe df_gols. "
                                  f"<campeonato>={c}, <temporada>={t}, <jogo_id>={jogo_id}")
                    logging.error(err)
                    failed.append('df_gols')
                try:
                    # dataframe df_minuto_a_minuto
                    minuto_a_minuto = req.minuto_a_minuto()
                    df_minuto_a_minuto = (
                                             spark.createDataFrame(minuto_a_minuto)
                                             .withColumnRenamed('descrição', 'descricao')
                                             .withColumn('jogo_id', F.lit(jogo_id))
                                             .withColumn('date_update', F.lit(datetime.now()))
                                         )

                    schema = get_schema('partidas_descricoes')
                    df_minuto_a_minuto = spark.createDataFrame(df_minuto_a_minuto.collect(), schema=schema)
                except Exception as err:
                    logging.error(f"ERROR etl.data_lake.partidas_campeonato.update_partidas: "
                                  f"Could not create dataframe df_minuto_a_minuto. "
                                  f"<campeonato>={c}, <temporada>={t}, <jogo_id>={jogo_id}")
                    logging.error(err)
                    failed.append('df_minuto_a_minuto')
                status = 'Finalizado'
                if len(failed)>0:
                    # checkando se o erro foi ocasionando 
                    # por conta do cancelamento da partida
                    req = Partida(jogo_id)
                    status = req.status
                    if status=='Cancelado':
                        data = [{
                                 'jogo_id': jogo_id,   
                                 'campeonato': campeonato,
                                 'campeonato_metadata': c,
                                 'temporada_metadata': t,
                                 'date_update': datetime.now()
                               }]
                        schema = get_schema('partidas_canceladas')
                        df_cancelada = spark.createDataFrame(data, schema = schema)
                        df_cancelada.write.parquet(path_datalake+'/partidas/partidas_canceladas/df_canceladas',
                                                   mode='append')
                        logging.info(f"INFO etl.data_lake.partidas_campeonato.update_partidas: "
                                      f"Canceled match, info updated in "
                                      f"{path_datalake}/partidas/partidas_canceladas/df_canceladas. "
                                      f"<campeonato>={c}, <temporada>={t}, <jogo_id>={jogo_id}")
                try:
                    if 'df_resumo' not in failed:
                        df_resumo.write.parquet(path_datalake+
                                                f'/partidas/resumo/{c}/df_resumo', 
                                                mode='append')
                    if 'df_jogadores' not in failed:
                        df_jogadores.write.parquet(path_datalake+
                                                   f'/partidas/jogadores_minutagens/{c}/df_jogadores',
                                                   mode='append')
                    if ('df_gols' not in failed) and (df_gols is not None):
                        df_gols.write.parquet(path_datalake+
                                              f'/partidas/gols/{c}/df_gols', 
                                              mode='append')
                    if 'df_minuto_a_minuto' not in failed:
                        df_minuto_a_minuto.write.parquet(path_datalake+
                                                         f'/partidas/descricoes/{c}/df_minuto_a_minuto', 
                                                         mode='append')
                except Exception as err:
                    logging.error(f"ERROR etl.data_lake.partidas_campeonato.update_partidas: "
                                  f"Unexpected error: Could not execute append data. "
                                  f"<campeonato>={c}, <temporada>={t}, <jogo_id>={jogo_id}")
                    logging.error(err)
                    return
                # atualizando datalake/metadata.json
                r = open(path_datalake+'/metadata.json')
                metadata = json.load(r) 
                try:
                    metadata['partidas'][c][t][jogo_id] = {
                                                           'status': 'evaluation', 
                                                           'status_partida': status,
                                                           'failed': failed
                                                          }
                except:
                    metadata['partidas'][c][t] = {}
                    metadata['partidas'][c][t][jogo_id] = {
                                                           'status': 'evaluation', 
                                                           'status_partida': status,
                                                           'failed': failed
                                                          }
                with open(path_datalake+'/metadata.json', 'w') as fp:
                    json.dump(metadata, fp)
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"INFO etl.data_lake.partidas_campeonato.update_partidas: "
                         f"Update league {c} | {t}. runtime = {runtime_str}")