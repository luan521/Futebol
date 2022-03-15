import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

from cafu.etl import update_partidas
from cafu.utils import get_spark

def f():
    spark = get_spark(1)
    update_partidas(spark)

if __name__=='__main__':
    f()