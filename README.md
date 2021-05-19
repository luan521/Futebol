O projeto se divide em três etapas: 

- Requisição
- Banco de dados
- Modelos.

O objetivo é criar diversos modelos que consigam fazer previsões em uma partida de futebol. Por exemplo: Em uma partida entre Liverpool e Manchester City pela Premier League, dado informações dos dois times nas últimas partidas do campeonato, qual a probabilidade do Liverpool marcar o primeiro gol da partida? Ou então, qual a probabilidade de ocorrer mais de três gols na partida? Criaremos um banco de dados, e depois modelos de Machine Learning, que buscam responder perguntas como estas.

Contudo, antes de tudo precisamos criar uma biblioteca capaz de buscar jogos de futebol passados, de maneira automática.

# Requisição

Retorna as informações, do site ESPN, de um jogo de futebol. Sendo https://www.espn.com.br/futebol/partida?jogoId=569989 o link de um jogo, no site da ESPN, o id <u>569989</u> identifica o jogo de maneira única, chamaremos está variável de jogo_id.

**Bibliotecas necessárias:** FunçõesAuxiliares, FunçõesRequisiçãoESPN, RequisiçãoESPN.

~~~~python
from RequisiçãoESPN import RequisiçãoFutbeol

jogo_id =  # Exemplo: jogo_id ='588117' identifica o jogo Grêmio x Cuiabá, pela Copa do Brasil. 

req = RequisiçãoFutbeol(jogo_id)

req.req_teste_jogo_finalizado() # Retorna se o jogo ja foi finalizado.
req.req_campeonato() # Retorna o campeonato.
req.req_data() # Retorna a data.
req.req_nomes_times() # Retorna o nome dos times.
req.req_formacao() # Retorna as formações dos times.
req.req_jogadores() # Retorna as escalações, e substituições.
req.req_gols() # Retorna os gols que ocorreram, autor do gol e tempo. 
req.req_placar() # Retorna o placar. 
req.req_posse() # Retorna a posse de bola.
req.req_chutes_fora_nogol() # Retorna a quantidade de chutes, no gol e fora do gol.
req.req_faltas() # Retorna a quantidade de faltas cometidas.
req.req_cartoes_amarelos() # Retorna a quantidade de cartões amarelos.
req.req_cartoes_vermelhos() # Retorna a quantidade de cartões vermelhos.
req.req_impedimentos() # Retorna a quantidade de impedimentos.
req.req_escanteios() # Retorna a quantidade de escanteios.
req.req_defesas() 
req.req_minuto_a_minuto() # Retorna a descrição do jogo, minuto a minuto.
~~~~

Executando o código acima, as informações do jogo estarão contidas no objeto req. Para visualizar as respectivas informações, execute:

~~~~python
req.jogo_finalizado
req.campeonato
req.data
req.nomes_times
req.formacao
req.jogadores
req.gols
req.placar
req.posse
req.chutes_fora_nogol
req.faltas
req.cartoes_amarelos
req.cartoes_vermelhos
req.impedimentos
req.escanteios
req.defesas
req.minuto_a_minuto
~~~~

# Banco de dados

Utilizando a biblioteca de requisição, que nos retorna as informações de um jogo, um banco de dados pode ser criado utilizando estas informações. Para isto, nos beneficiamos do método de organização dos campeonatos no site ESPN, isto é, os jogos_id dos jogos de cada campeonato, são ordenados pelas rodadas. Por exemplo: Os jogos_ids entre '569989' e '569980' se referem a primeira rodada do campeonato brasileiro de 2020, enquanto que os jogos_ids entre '569979' e '569970' se referem a segunda rodada, e assim por diante. No entanto, para cada campeonato, os jogos_ids podem ser organizados de forma crescente ou decrescente (aumentando a rodada), sendo assim,  esta característica deve ser introduzida na função que inicializa o banco de dados de um campeonato qualquer.

As funcionalidades desta etapa são divididas nas seguintes funções:

- **inicializar_campeonato:** Inicia o banco de dados de um campeonato, e salva as informações em uma pasta introduzida na entrada da função.
-  **atualizar_campeonato:** Atualiza as informações do campeonato, no banco de dados. 
- **decodificar_campeonato:** Busca o banco de dados (do campeonato) em sua pasta, e retorna as partidas decodificadas, pois o campeonato encontra-se codificado no banco de dados, com o uso da biblioteca <u>pickle</u>.
- **times_rodadas:** Retorna os jogos de cada time, ordenados pelas rodadas, separados por dentro e fora de casa.
- **times_datas:** Retorna os jogos de cada time, ordenados pela data, separados por dentro e fora de casa.

**Bibliotecas necessárias:** FunçõesAuxiliares, FunçõesRequisiçãoESPN, RequisiçãoESPN, FunçõesAuxiliaresBanco, BandoDeDados.

- **inicializar_campeonato**

~~~~python
from BancoDeDados import inicializar_campeonato

caminho =  # Exemplo: caminho =  'OneDrive/Documentos/programas/ProjetoAposta/bancodedados/campeonatos/'.Identifica em qual pasta o banco será salvo. 
nome_campeonato = # Identifica o nome do banco, que será salvo.
jogo_id_inicial = # Identifica o primeiro jogo que será salvo, de acordo com a introdução da etapa Banco de dados.
rodada_inicial = # Exemplo: rodada_inicial = 1. Neste exemplo, inicializamos o campeonato na primeira rodada. 
quantidade_jogos_rodada = # Exemplo: quantidade_jogos_rodada = 10.Identifica quantos jogos ocorrem em uma rodada.

inicializar_campeonato(caminho, nome_campeonato, jogo_id_inicial, rodada_inicial, quantidade_jogos_rodada) # Executando esta função, o banco do campeonato será inicializado, e salvo na pasta fornecida pela variável caminho.
~~~~

Ao executar a função <u>inicializar_campeonato</u>, o programa irá realizar a seguinte pergunta: <u>Os jogos_ids do campeonato, são crescentes ou decrescentes?</u> De acordo com o que foi dito na introdução da etapa <u>Banco de dados</u>.

- **atualizar_campeonato**

~~~~python
from BancoDeDados import atualizar_campeonato

caminho =  # Exemplo: caminho =  OneDrive/Documentos/programas/ProjetoAposta/bancodedados/campeonatos/'.Identifica em qual pasta o banco, que será atualizado, esta salvo.
nome_campeonato = # Identifica o nome do banco, que será atualizado.

atualizar_campeonato(caminho, nome_campeonato) # Executando esta função, o campeonato será atualizado.
~~~~

Ao executar a função <u>atualizar_campeonato</u>, o programa irá realizar o seguinte requerimento: <u>Digite a quantidade de rodadas que deseja lançar.</u>

- **decodificar_campeonato / times_rodadas / times_datas**

~~~~python
from BancoDeDados import decodificar_campeonato
from BancoDeDados import times_rodadas
from BancoDeDados import times_datas

caminho =  # Exemplo: caminho =  'OneDrive/Documentos/programas/ProjetoAposta/bancodedados/campeonatos/'.Identifica em qual pasta o banco, que será buscado, esta salvo.
nome_campeonato = # Identifica o nome do banco, que será buscado.

e1 = decodificar_campeonato(nome_campeonato, caminho) # e1[0]: Armazena todas as rodadas do campeonato, lançados no banco de dados. e1[1]: Armazena informações do campeonato.
e2 = times_rodadas(e1[0]) # e2 armazena os jogos de cada time, ordenados pelas rodadas, separados por dentro e fora de casa.
e3 = times_datas(e2) # e3 armazena os jogos de cada time, ordenados pela data, separados por dentro e fora de casa.
~~~~

# Próximos passos

Reinicialização do projeto. Serão feitas melhorias nas etapas de requisição e banco de dados, para prosseguirmos para a modelagem.

- Requisição e Banco de dados
  - Melhorias no código de requerimento
  - Tratamento do objeto req.minuto_a_minuto, transformar em várias tabelas de forma a obter dados estruturados
  - requerimento nas páginas dos jogadores
- Banco de dados
  - Verificar uma possibilidade: Ao inserir um novo campeonato, passamos apenas seu nome (identificado no site ESPN) e uma função busca um jogo_id de uma partida do campeonato, contudo a função buscará todos os jogo_id do campeonato em torno do jogo_id de partida
  - No banco de dados, teremos várias tabelas de falta, finalização, gols, times, jogadoes,... Contudo, todos os campeonatos serão salvos nas mesmas tabelas, e poderão ser filtrados por um código pré-determinado
  - Com as funções de requisição prontas, construir a pipeline que gera o banco de dados. Pesquisar uma ferramenta para disparar a execução da pipeline, e acompanhar sua execução, da melhor forma possível.
- Melhorar versionamento do projeto
  - utilizar melhor o git
  - Criar um kernel para o projeto, para mantermos sempre um arquivo de requirements atualizado