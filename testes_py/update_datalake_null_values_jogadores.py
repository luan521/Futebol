import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

from cafu.etl import update_null_values
from cafu.utils import get_spark

def f():
    spark = get_spark(1)
    update_null_values(spark, 'jogadores')

if __name__=='__main__':
    f()