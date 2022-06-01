import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

from cafu.etl import update_jogos_ids

def f():
    update_jogos_ids()

if __name__=='__main__':
    f()