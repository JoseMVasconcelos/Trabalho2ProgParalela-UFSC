## Relatório do Trabalho de Programação Paralela

Feito por José Vasconcelos (22100906) e Marcos Roberto (22100915)

### Descrição do Problema

O problema abordado neste trabalho consiste na implementação de um sistema de recuperação de texto utilizando o padrão de scatter/gather. O cliente envia uma consulta ao nó raiz do sistema, que divide a string de busca em palavras-chave e distribui partes iguais para várias réplicas, responsáveis por armazenar os arquivos de texto plano. Cada réplica retorna ao nó raiz os arquivos encontrados e o número de ocorrências das palavras-chave. O nó raiz, então, combina essas respostas e fornece ao cliente uma lista de textos relevantes, juntamente com o número de ocorrências de cada palavra-chave.

### Implementação

O trabalho foi inicialmente desenvolvido na linguagem C, utilizando MPI para gerenciamento de processos distribuidos, porém, após horas de frustração com manipulação de arrays e ponteiros, foi escolhido implementar o trabalho final utilizando Python, com a biblioteca MPI respectiva, `MPI4PY`. 

Da biblioteca MPI4Py, foi utilizado apenas os comandos básicos:

- **MPI.Init()**: Foi feito uma validação para ver se o MPI já não foi inicializado posteriormente, em algumas máquinas, o mpi4py já faz esse trabalho
- **MPI.COMM_WORLD**: Constante para pegar o comunicador padrão
- **comm.Get_rank()**: Função básica para pegar o rank do processo, `cliente rank 0`, `processo rank 1` e ` rank 2-n`.
- **comm.Get_size()**: Função básica para pegar o tamanho do mundo, ou seja, número de processos.
- **comm.send(message, destination)**: Função bloqueante para enviar mensagem ao destino.
- **comm.recv(source, status)**: Função bloqueante para escutar a fonte.
- **comm.abort()**: Função que não foi realmente utilizada para a implementação de `scatter/gather`, servindo apenas como uma maneira de finalizar o código após o cliente realizar todas as queries.

Abaixo, as principais características da implementação:

- **Cliente**: Foi implementado um `cliente`, atribuido ao processo de `rank 0`, o cliente possui um array de strings, as palavras chaves, que serão enviadas ao processo de `rank 1`, o `nó raiz`. Após as consultas realizdas, o `nó raiz` retorna ao `cliente` um dicionário, com a seguinte estrutura: `{Nome do arquivo: número de ocorrências}`.

- **Nó Raiz**: O `nó raiz`, de `rank 1`, espera uma solicitação de pesquisa do `cliente`, quando recebe, separa a query, em palavras chaves separadas, utilizando Round Robin para enviar as palavras às `réplicas`. Por exemplo uma query de `"Computação paralela e distribuida"` e com `3 réplicas`, seria separa em um array da seguinte forma: `[["Computação", "distribuida"], ["paralela"], ["e"]]`. Após enviar as palavras às `réplicas`, o `nó raiz` escuta qualquer fonte, e junta as repostas no dicionário descrito anteriormente. 

- **Réplicas (n)**: Para as `réplicas`, são atribuido os `ranks 2-n`, dependendo da quantidade de processos escolhino na execução. As réplicas esperam uma solicitação, e para cada palavra chave recebida, pesquisa nos arquivos `.txt` da pasta `texts`. As `réplicas` também fazem um tratamento nos textos, removendo pontuações e _linebreaks_ que poderiam atrapalhar na pesquisa. Após esgotarem todas as linhas e todas as palavras chaves, retornam o número de ocorrências em cada arquivo, para o mesmo endereço do solicitante. Elas rodam em paralelo uma com a outra, e não tem ordem para responder ao solicitante. O `nó raiz` pode solicitar na ordem `1, 3, 2` e receber na ordem `3, 2, 1`. 

- **TIMESTAMPS**: A cada envio/recebimento do `cliente` e `nó raiz`, é printado uma mensagem na tela, junto a um TIMESTAMP: 
  
    `CLIENTE enviando pesquisa para nó raiz: blockchain criptomoedas bitcoin. TIMESTAMP: 2024-06-20 17:24:16.480956`.
    
     Essa foi uma decisão tomada para burlar o sistema de print desordenado do python. O python coloca todas as mensagens a serem printadas em um buffer, e elas podem sair na ordem errada, o timestamp server para entender a orderm correta das mensagens.

- **Textos e queries**: Os textos e queries utilizados foram feitos por inteligencias artificiais, e o seus conteudos não possuem peso significativo, servindo apenas para mostrar o funcionamento do trabalho implementado.

### Execução

Para executar o código, rode o comando para certificar que o Python3 está instalado:
```sh
$ python3 --version
```

Se não aparecer uma versão, instale a versão mais nova do python.

Verifique também a versão do MPI:
```sh
$ mpiexec --version
``` 
Se não aparecer uma versão, instale com os comandos:
```sh
$ sudo apt-get install openmpi-bin
$ sudo apt-get install openmpi-doc
$ sudo apt-get install libopenmpi-dev
$ sudo apt-get install mpich
$ sudo apt-get install mpich-devel
$ export PATH=/usr/lib64/mpich/bin:$PATH
```
Com python3 e MPi instalado, execute o seguinte código para instalar a biblioteca mpi4py:
```sh
$ pip3 install mpi4py
```
e rode o programa usando o comando:
```sh
$ mpiexec -n 'numero_de_processos' python3 main.py
```

#### TROUBLESHOOTING
É possível que uma instalação do python e do mpi4py acabe corrompendo e apresentando este erro:

```
$ mpirun -n 4 python3 main.py
Traceback (most recent call last):
     File "main.py", line 5, in <module>
     from mpi4py import MPI
ModuleNotFoundError: No module named 'mpi4py'
```

para resolver, crie um `virtual enviroment`, usando o comando:
```sh
$ python3 -m venv .venv
```

e ative-a usando o comando:
### LINUX
```sh
$ source .venv/bin/activate
```

### WINDOWS
```sh
$ source .venv/Scripts/activate.bat
```
Após ativar o `virtual enviroment`, tente reinstalar a biblioteca `mpi4py` e rodar o código.

### Caso de Teste e Resultados Esperados

## CASO 1
Número de réplicas = 2

`CLIENTE enviando pesquisa para nó raiz: saúde mental psicologia terapia.`

`NÓ RAIZ envia palavra chaves ['saúde', 'psicologia'] para réplica 0.`

`NÓ RAIZ envia palavra chaves ['mental', 'terapia'] para réplica 1.`

`CLIENTE recebeu o resultado do nó raiz!: {'A Evolução e o Impacto dos Video Games na Sociedade Moderna.txt': 4, 'Desafios Ecológicos A Crise Ambiental do Século XXI.txt': 1}.`

### Observando os textos desse caso (palavras chaves encontradas em highlight):
#### A Evolução e o Impacto dos Video Games na Sociedade Moderna:
Os video games, desde sua criação nas décadas de 1970 e 1980, evoluíram de simples jogos de arcade para complexas obras interativas que abrangem diversos gêneros e plataformas. Inicialmente, jogos como Pong e Space Invaders cativaram jogadores com suas mecânicas simples e gráficos rudimentares. No entanto, o avanço da tecnologia permitiu que os video games se tornassem cada vez mais sofisticados, oferecendo experiências imersivas com gráficos em alta definição, narrativa envolvente e jogabilidade inovadora. Hoje, os jogos são jogados em consoles, computadores e dispositivos móveis, alcançando uma audiência global diversificada.

A indústria de video games é uma das mais lucrativas do entretenimento, superando até mesmo a indústria cinematográfica em termos de receita. Este crescimento impressionante é impulsionado não apenas pela venda de jogos, mas também por modelos de negócios inovadores como jogos gratuitos com compras dentro do aplicativo, assinaturas de serviços de jogos e esportes eletrônicos (eSports). Os eSports, em particular, se tornaram um fenômeno cultural, com competições internacionais atraindo milhões de espectadores e oferecendo prêmios substanciais. Plataformas de streaming como Twitch e YouTube Gaming permitiram que jogadores transmitissem suas partidas ao vivo, criando novas oportunidades de carreira e fomentando uma comunidade global de gamers.

Além do entretenimento, os video games têm mostrado um impacto significativo em várias áreas da sociedade. Na educação, jogos são utilizados como ferramentas de aprendizado, promovendo habilidades cognitivas, resolução de problemas e colaboração. Na `saúde`, a gamificação está sendo usada para reabilitação física e `mental`, oferecendo terapias interativas para pacientes. No entanto, os video games também enfrentam críticas e desafios, como a preocupação com a dependência, o impacto na `saúde` `mental` e a representação de violência. A pesquisa e o debate contínuos sobre os efeitos dos video games são essenciais para maximizar seus benefícios e mitigar seus riscos, garantindo que continuem a ser uma força positiva na sociedade moderna.

##### Importante observar que a palavra "terapias" não é percebida, isso ocorre pois foi escolhido um método de implementação, que espera a string EXATA. 

#### Desafios Ecológicos A Crise Ambiental do Século XXI:

Os problemas ecológicos representam uma das maiores ameaças à sustentabilidade e à `saúde` do planeta. A degradação ambiental, impulsionada por atividades humanas como desmatamento, urbanização e agricultura intensiva, tem causado a destruição de habitats naturais, levando à perda de biodiversidade. Espécies inteiras estão sendo extintas a uma taxa alarmante, comprometendo ecossistemas complexos e interconectados que são vitais para a estabilidade ambiental e para a provisão de serviços ecossistêmicos essenciais, como a purificação da água, a polinização e o controle de pragas.

A poluição é outro grande problema ecológico, com efeitos devastadores sobre o ar, a água e o solo. Emissões industriais e de veículos contribuem para a poluição do ar, causando problemas respiratórios em seres humanos e animais, além de contribuir para o aquecimento global. A poluição da água, resultante do despejo de resíduos industriais, agrícolas e domésticos, contamina fontes de água potável e prejudica a vida aquática. Além disso, o uso excessivo de pesticidas e fertilizantes químicos na agricultura degrada a qualidade do solo, tornando-o menos fértil e mais propenso à erosão.

As mudanças climáticas, amplamente atribuídas às atividades humanas, exacerbam todos esses problemas. O aumento das temperaturas globais está associado ao derretimento das calotas polares e ao aumento do nível do mar, ameaçando comunidades costeiras e ecossistemas marinhos. Eventos climáticos extremos, como furacões, secas e enchentes, estão se tornando mais frequentes e intensos, causando destruição em larga escala e colocando em risco a segurança alimentar e hídrica. Para mitigar esses problemas ecológicos, é fundamental adotar políticas de conservação, promover a sustentabilidade e investir em tecnologias limpas que reduzam o impacto ambiental.

#### Sem ocorrencias nos outros textos

## CASO 2
Número de réplicas = 3

`CLIENTE enviando pesquisa para nó raiz: agricultura sustentável agroecologia permacultura.`

`NÓ RAIZ envia palavra chaves ['agricultura', 'permacultura'] para réplica 0.`

`NÓ RAIZ envia palavra chaves ['sustentável'] para réplica 1.` 

`NÓ RAIZ envia palavra chaves ['agroecologia'] para réplica 2.`

`CLIENTE recebeu o resultado do nó raiz!: {'A Importância da Geologia para a Compreensão da Terra e seus Recursos.txt': 2, 'Desafios Ecológicos A Crise Ambiental do Século XXI.txt': 2}`

### Observando os textos desse caso (palavras chaves encontradas em highlight):
#### A Importância da Geologia para a Compreensão da Terra e seus Recursos
A geologia, a ciência que estuda a composição, estrutura, processos e história da Terra, desempenha um papel crucial na nossa compreensão do planeta e na exploração de seus recursos naturais. Ao investigar rochas, minerais, fósseis e processos geológicos, os geólogos podem revelar a história da Terra, desde sua formação há cerca de 4,6 bilhões de anos até os eventos mais recentes que moldaram a superfície terrestre. Esse conhecimento é fundamental não apenas para a ciência pura, mas também para aplicações práticas em diversas indústrias, incluindo a mineração, petróleo e gás, construção civil e gestão de riscos naturais.

A exploração de recursos minerais e energéticos é uma das áreas mais importantes da geologia. Minerais metálicos, como ferro, cobre e ouro, e minerais não metálicos, como calcário e fosfato, são essenciais para a economia global e para a produção de bens de consumo. A geologia também é crucial na prospecção e extração de combustíveis fósseis, como petróleo, gás natural e carvão, que continuam a ser fontes primárias de energia. Técnicas avançadas de prospecção geofísica e geoquímica, juntamente com o uso de imagens de satélite e modelagem computacional, permitem aos geólogos localizar e avaliar depósitos de recursos naturais com maior precisão e eficiência, minimizando os impactos ambientais.

Além de sua importância econômica, a geologia é vital para a compreensão e mitigação de riscos naturais, como terremotos, erupções vulcânicas, deslizamentos de terra e tsunamis. O estudo dos processos geológicos e a análise de dados históricos permitem prever a ocorrência desses eventos e desenvolver estratégias de mitigação para proteger vidas humanas e infraestrutura. A geologia ambiental, uma subdisciplina que examina a interação entre processos geológicos e atividades humanas, também desempenha um papel importante na gestão `sustentável` do ambiente. Questões como a contaminação do solo e da água, a gestão de resíduos e a recuperação de áreas degradadas são abordadas por geólogos ambientais, que trabalham para equilibrar a exploração de recursos com a preservação ecológica.

Em suma, a geologia é uma ciência multifacetada que contribui de maneira significativa para o avanço do conhecimento científico e para a resolução de problemas práticos relacionados aos recursos naturais e aos riscos ambientais. O trabalho dos geólogos é essencial para garantir o uso `sustentável` dos recursos da Terra e para proteger nosso planeta e suas populações contra desastres naturais.

#### Desafios Ecológicos A Crise Ambiental do Século XXI
Os problemas ecológicos representam uma das maiores ameaças à sustentabilidade e à saúde do planeta. A degradação ambiental, impulsionada por atividades humanas como desmatamento, urbanização e `agricultura` intensiva, tem causado a destruição de habitats naturais, levando à perda de biodiversidade. Espécies inteiras estão sendo extintas a uma taxa alarmante, comprometendo ecossistemas complexos e interconectados que são vitais para a estabilidade ambiental e para a provisão de serviços ecossistêmicos essenciais, como a purificação da água, a polinização e o controle de pragas.

A poluição é outro grande problema ecológico, com efeitos devastadores sobre o ar, a água e o solo. Emissões industriais e de veículos contribuem para a poluição do ar, causando problemas respiratórios em seres humanos e animais, além de contribuir para o aquecimento global. A poluição da água, resultante do despejo de resíduos industriais, agrícolas e domésticos, contamina fontes de água potável e prejudica a vida aquática. Além disso, o uso excessivo de pesticidas e fertilizantes químicos na `agricultura` degrada a qualidade do solo, tornando-o menos fértil e mais propenso à erosão.

As mudanças climáticas, amplamente atribuídas às atividades humanas, exacerbam todos esses problemas. O aumento das temperaturas globais está associado ao derretimento das calotas polares e ao aumento do nível do mar, ameaçando comunidades costeiras e ecossistemas marinhos. Eventos climáticos extremos, como furacões, secas e enchentes, estão se tornando mais frequentes e intensos, causando destruição em larga escala e colocando em risco a segurança alimentar e hídrica. Para mitigar esses problemas ecológicos, é fundamental adotar políticas de conservação, promover a sustentabilidade e investir em tecnologias limpas que reduzam o impacto ambiental.

#### Sem ocorrencias nos outros textos

### Conclusão

Com base nos resultados obtidos, podemos concluir que o sistema de busca de palavras-chave desenvolvido demonstrou conseguir identificar e extrair as palavras chaves dos textos fornecidos. A utilização do MPI também facilitou bastante na programação distribuida, que garantiram o paralelismo para um uso mais eficiente das réplicas.
