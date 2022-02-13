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
├── chromedriver.exe -> ChromeDriver 98.0.4758.80. chromedriver_win32. Supports Chrome version 98
├── ChromeSetup.exe -> Instalador Google Chrome version 98.0.4758.82
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
3. Instalar o Google chrome version 98, utilize o insalador ChromeSetup.exe, siga o [tutorial](https://www.youtube.com/watch?v=9pQP99uquYs&t=148s)
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
