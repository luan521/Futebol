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
├───cafu -> biblioteca
│   ├───etl
│   ├───metadata
│   ├───queries
│   ├───utils
│   │   ├───etl
│   │   ├───queries
├───docs -> documentação da biblioteca
│   ├───build
│   │   ├───doctrees
│   │   │   └───module
│   │   └───html
│   │       ├───module
│   │       ├───_images
│   │       ├───_modules
│   │       │   ├───cafu
│   │       │   │   ├───etl
│   │       │   │   ├───metadata
│   │       │   │   └───queries
│   │       │   └───modulos
│   │       │       ├───fluxos
│   │       │       ├───process
│   │       │       ├───queries
│   │       │       └───utils
│   │       ├───_sources
│   │       │   └───module
│   │       └───_static
│   │           ├───css
│   │           │   └───fonts
│   │           └───js
│   └───source
│       └───module
├───imagens_doc -> imagens para a documentação da biblioteca
└───notebooks -> notebools de exemplo
    ├───etl
    │   ├───prod
    │   └───sketch
    ├───requisicao
    │   ├───prod
    │   └───sketch
    └───sketch
```

## Contents
Links e conteúdos relevantes para o projeto
- [ambiente virtual](https://ichi.pro/pt/criando-um-ambiente-virtual-para-jupyter-notebook-com-pip-e-conda-guia-muito-simples-103212890404103)
- [SSD + HD: Como salvar arquivos automaticamente no HD?](https://www.youtube.com/watch?v=BKxCnUlK6c0)
- [COMO DIRECIONAR ARQUIVOS DO SSD PARA O HD](https://www.youtube.com/watch?v=5IanANDJxE8)
- [python logging](https://docs.python.org/3/howto/logging.html)
- [Saindo do Zero com a Biblioteca OS no Python](https://www.youtube.com/watch?v=ROCyIPA1wWA) pode ser útil na montagem do data lake
- [Como Criar Barra de Progresso no Python para os seus Códigos](https://www.youtube.com/watch?v=qRFPGuBc-KE)

## Next steps
- notebooks prod devem estar sempre funcionando &#9745;
- incluir logs no código
    - método nacionalidade da classe cafu.queries.Bio, nem todos jogadores possuem esse parâmetro definido, ex id_jogador = '252107/vinicius-junior'
- chromedriver não mostrar o navegador -> opção default &#9745;
- otimizar o espaço do PC: SSD e HD
- migrar projeto para o linux
- finalizar o código que constrói o data lake e construir o airflow
