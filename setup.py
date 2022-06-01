import os
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Get install requires
requirements = f'{os.path.dirname(os.path.realpath(__file__))}/requirements.txt'

if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires = f.read().splitlines()

#  avoid typing large names for conda activate and for project imports
setup(
    name='modules',
    version='0.0.0',
    description='Aposta automática Dafabet',
    author='Luan Henrique',
    author_email='oracle.cafu@example.com',
    url='',
    packages=find_packages(exclude=('docs', 'testes_py')),
    entry_points={
    'console_scripts': [
        'initialize_datalake = cafu.utils.etl.datalake:initialize_datalake', 
        'validate_datalake = cafu.utils.etl.validate:validate_datalake',
        'invalidate_datalake = cafu.utils.etl.validate:invalidate_datalake',
        'first_validation_execution = cafu.utils.etl.validate:first_validation_execution',
        'campeonatos_espn = cafu.metadata.campeonatos_espn:campeonato_espn',
        'proximas_partidas = cafu.utils.etl.datalake:proximas_partidas'
    ],
},
    install_requires=install_requires,
)