# Oracle cafu
Serviço para aposta automática em partidas de futebol, no site [Dafabet](https://www.dafabet.com/pt/dfgoal/sports/240-football)

1. Coleta de dados
2. ETL (Data Lake e banco de dados)
3. Cluster Analysis
4. Streaming / Dashboard
5. Modelagem
6. Aposta automática

## Folder structure
```
├── cafu -> biblioteca
│   ├── etl
│   │   ├── __init__.py
│   │   └── partidas_campeonato.py
│   ├── __init__.py
│   ├── metadata
│   │   ├── campeonatos_dafabet.py
│   │   ├── campeonatos_espn.py
│   │   ├── __init__.py
│   │   └── paths.py
│   ├── queries
│   │   ├── __init__.py
│   │   ├── jogador.py
│   │   ├── odds.py
│   │   └── partida.py
│   └── utils
│       ├── etl
│       │   ├── __init__.py
│       │   └── partidas_campeonato.py
│       ├── __init__.py
│       ├── loop_try.py
│       └── queries
│           ├── dafabet.py
│           ├── __init__.py
│           ├── temp.py
│           └── webdriver_chrome.py
├── chromedriver -> ChromeDriver 91.0.4472.101. chromedriver_linux64. Supports Chrome version 91 
├── docs -> documentação da biblioteca
├── imagens_doc -> imagens para a documentação da biblioteca
│   ├── biografia.png
│   ├── estatisticas.png
│   └── ult_5_jogos.png
├── notebooks -> notebools de exemplo
│   ├── etl
│   │   ├── prod
│   │   │   └── busca_automatica_campeonato.ipynb
│   │   └── sketch
│   │       └── busca_automatica_campeonato.ipynb
│   ├── requisicao
│   │   ├── prod
│   │   │   ├── jogador.ipynb
│   │   │   ├── partida.ipynb
│   │   │   └── site_aposta.ipynb
│   │   └── sketch
│   │       ├── no_show_webdriver.ipynb
│   │       ├── site_aposta-Copy1.ipynb
│   │       └── site_aposta.ipynb
│   └── sketch
│       ├── example.txt
│       └── Untitled.ipynb
├── README.md
├── requirements.txt 
├── run_doc.sh -> gerar documentação automática da biblioteca em docs.build.html.module
└── setup.py
```

## Prerequisites
1. Criar arquivo 'dafabet.json':
    - 'user': usuário no site dafabet
    - 'password': senha no site dafabet
2. Atualizar caminhos locais em cafu/metadata/paths.py
3. Verificar se o chromedriver possui a versão compatível com o Google Chrome
4. Criar ambiente virtual:
```
>> conda create -n futebol python=3.8 
>> conda activate futebol 
>> pip install --user ipykernel 
>> python -m ipykernel install --user --name=futebol 
```
5. Instalar o projeto junto com os requirements:
```
>> pip install .
```
**Acesse docs.build.html.module e notebooks para aprender as funcionalidades do projeto**

## Contents
Links e conteúdos relevantes para o projeto
- [ambiente virtual](https://ichi.pro/pt/criando-um-ambiente-virtual-para-jupyter-notebook-com-pip-e-conda-guia-muito-simples-103212890404103)
- [SSD + HD: Como salvar arquivos automaticamente no HD?](https://www.youtube.com/watch?v=BKxCnUlK6c0)
- [COMO DIRECIONAR ARQUIVOS DO SSD PARA O HD](https://www.youtube.com/watch?v=5IanANDJxE8)
- [python logging](https://docs.python.org/3/howto/logging.html)
- [Saindo do Zero com a Biblioteca OS no Python](https://www.youtube.com/watch?v=ROCyIPA1wWA) pode ser útil na montagem do data lake
- [Como Criar Barra de Progresso no Python para os seus Códigos](https://www.youtube.com/watch?v=qRFPGuBc-KE)
- [Docker em 22 minutos - teoria e prática (Rápido!)](https://www.youtube.com/watch?v=Kzcz-EVKBEQ)
- [Step-by-Step Python and Postgres Tutorial with psycopg2](https://www.youtube.com/watch?v=2PDkXviEMD0)
- [Como iniciar um projeto Django com PostgreSQL e Docker - Dicas de Python](https://www.youtube.com/watch?v=xxjzwdtWozI)
- [Data Science - PostgreSQL Database using Python Programming](https://www.youtube.com/watch?v=d1atQKLFHgY)

## Next steps
- Verificar, informações aparentemente excluídas do site ESPN:
    - [cafu.queries.jogador.UltimosCincoJogos](https://www.espn.com.br/futebol/jogador/_/id/252107/vinicius-junior) 
    - [cafu.queries.jogador.Estatisticas](https://www.espn.com.br/futebol/jogador/estatisticas/_/id/252107/vinicius-junior)
- etl para a construção do data lake, utilizar o airflow
