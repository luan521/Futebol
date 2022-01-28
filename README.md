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
├───cafu
│   ├───etl
│   ├───metadata
│   ├───queries
│   ├───utils
│   │   ├───etl
│   │   ├───queries
├───imagens_doc
└───notebooks
    ├───etl
    │   ├───prod
    │   └───sketch
    └───requisicao
        ├───prod
        └───sketch
```