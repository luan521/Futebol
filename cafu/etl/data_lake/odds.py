from datetime import datetime, date, timedelta
from unidecode import unidecode
from tqdm import tqdm
from cafu.utils.etl.datalake import proximas_partidas
from cafu.metadata.campeonatos_dafabet import campeonato_dafabet
from cafu.queries.odds import GetOdds
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def update_odds(spark):
    """
    Atualiza datalake.odds
    
    Args:
        spark: (spark session) 
    """
    
    # campeonatos que terão jogos, hoje ou amanhã
    pr_part = proximas_partidas()
    dafabet = campeonato_dafabet()
    after_tomorrow = date.today()+timedelta(days=2)
    campeonatos = []
    for c in pr_part:
        for t in pr_part[c]:
            try:
                prox_jogo = datetime.strptime(pr_part[c][t], '%Y-%m-%d').date()
                if (prox_jogo<=after_tomorrow) and (c in dafabet):
                    campeonatos.append([c,t])
            except:
                pass
            
    if len(campeonatos)==0:
        logging.info("INFO etl.data_lake.odds.update_odds: "
                     "No match today or tomorrow.")
        return
    
    # atualizando
    query = GetOdds()
    for c in campeonatos:
        stop = False
        index = 0
        while not stop:
            query.get_campeonato_dafabet(c[0])
            descricao_partida = query.join_link_odds_partida(index)
            if descricao_partida is not None:
                if (
                    ('Hoje' in descricao_partida['horario']) or
                    ('Amanhã' in descricao_partida['horario'])
                   ):
                    query.open_odds()
                    odds = query.get_odds()
                    if len(odds)==2: # garantido que a coleta foi bem sucedida
                        return
                    for k1 in odds:
                        for k2 in odds[k1]:
                            odds[k1][k2] = float(odds[k1][k2])
                    for k1 in tqdm(odds):
                        try:
                            df = spark.createDataFrame([odds[k1]])
                            df = (
                                     df
                                     .withColumn('time_casa', F.lit(descricao_partida['time_casa']))
                                     .withColumn('time_visitante', F.lit(descricao_partida['time_visitante']))
                                     .withColumn('horario', F.lit(descricao_partida['horario']))
                                     .withColumn('campeonato_metadata', F.lit(c))
                                     .withColumn('temporada_metadata', F.lit(t))
                                     .withColumn('date_update', F.lit(datetime.now()))
                                 )
                            for c in df.columns:
                                df = df.withColumnRenamed(c, (c.replace(' ','_')
                                                               .replace(',','_'))
                                                         )
                            dir_ = k1.replace('/','-')
                            dir_ = unidecode(dir_.lower())
                            df.write.parquet(f'teste/{dir_}', mode='append')
                            logging.info(f"INFO etl.data_lake.odds.update_odds: "
                                         f"Updated {c}.{descricao_partida['time_casa']} vs "
                                         f"{descricao_partida['time_visitante']}.{k1}")
                        except Exception as err:
                            logging.error(f"ERROR etl.data_lake.odds.update_odds: "
                                          f"Could not update {c}.{descricao_partida['time_casa']} vs "
                                          f"{descricao_partida['time_visitante']}.{k1}")
                            logging.error(err)
                else:
                    stop = True
            else:
                stop = True
            index+=1
    query.web.close() # encerra a sessão