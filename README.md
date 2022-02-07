# Oracle cafu
- Coleta de dados
- ETL
- Cluster Analysis
- Streaming / Dashboard
- Modelagem
- Aposta automática

O objetivo é criar diversos modelos que consigam fazer previsões em uma partida de futebol. Por exemplo: Em uma partida entre Liverpool e Manchester City pela Premier League, dado informações dos dois times nas últimas partidas do campeonato, qual a probabilidade do Liverpool marcar o primeiro gol da partida? Ou então, qual a probabilidade de ocorrer mais de três gols na partida? Criaremos um banco de dados, e depois modelos de Machine Learning, que buscam responder perguntas como estas.

Com as probabilidades computadas, e possuindo odds de sites de apostas, podemos otimizar nossas apostas.

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
├── create_virtual_env.sh -> criar mambiente virtual
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

## Contents
Links e conteúdos relevantes para o projeto
- [ambiente virtual](https://ichi.pro/pt/criando-um-ambiente-virtual-para-jupyter-notebook-com-pip-e-conda-guia-muito-simples-103212890404103)
- [SSD + HD: Como salvar arquivos automaticamente no HD?](https://www.youtube.com/watch?v=BKxCnUlK6c0)
- [COMO DIRECIONAR ARQUIVOS DO SSD PARA O HD](https://www.youtube.com/watch?v=5IanANDJxE8)
- [python logging](https://docs.python.org/3/howto/logging.html)
- [Saindo do Zero com a Biblioteca OS no Python](https://www.youtube.com/watch?v=ROCyIPA1wWA) pode ser útil na montagem do data lake
- [Como Criar Barra de Progresso no Python para os seus Códigos](https://www.youtube.com/watch?v=qRFPGuBc-KE)
- [Docker em 22 minutos - teoria e prática (Rápido!)](https://www.youtube.com/watch?v=Kzcz-EVKBEQ)

## Next steps
- notebooks prod devem estar sempre funcionando &#9745;
- incluir logs no código &#9745;
- chromedriver não mostrar o navegador -> opção default &#9745;
- otimizar o espaço do PC: SSD e HD &#9745;
- migrar projeto para o linux
    - duas branchs development devem existir (development-linux e development-windows). As duas devem se encontrar no mesmo nível, prontas para a construção do etl, que será feito no ambiente linux (branch derivada da development-linux)
- etl para a construção do data lake, utilizar o airflow