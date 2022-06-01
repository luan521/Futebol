# Importando as bibliotecas
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
script_home = '~/futebol/Futebol/testes_py/'
# Definindo alguns argumentos básicos
default_args = {
   'owner': 'luan_henrique',
   'email': ['oracle.cafu@gmail.com'],
   'start_date': datetime(2022, 5, 31),
   'retries': 2,
   'retry_delay': timedelta(minutes=2),
   }
# Nomeando a DAG e definindo quando ela vai ser executada
with DAG(
   'update-datalake',
   schedule_interval='@daily',
   catchup=False,
   default_args=default_args
   ) as dag:
    # Definindo as tarefas que a DAG vai executar
    t1 = BashOperator(
       task_id='jogos_ids',
       bash_command=f"""
       cd {script_home}
       python3 update_datalake_jogos_ids.py
       """)
    t2 = BashOperator(
       task_id='partidas',
       bash_command=f"""
       cd {script_home}
       python3 update_datalake_partidas.py
       """)
    t3 = BashOperator(
       task_id='odds',
       bash_command=f"""
       cd {script_home}
       python3 update_datalake_odds.py
       """)
    t4 = BashOperator(
       task_id='null_values_partidas',
       bash_command=f"""
       cd {script_home}
       python3 update_datalake_null_values_partida.py
       """)
    t5 = BashOperator(
       task_id='jogadores',
       bash_command=f"""
       cd {script_home}
       python3 update_datalake_jogadores.py
       """)
    t6 = BashOperator(
       task_id='null_values_jogadores',
       bash_command=f"""
       cd {script_home}
       python3 update_datalake_null_values_jogadores.py
       """)
# Definindo o padrão de execução
t1 >> [t2,t3] >> t5 >> t6
t2 >> t4