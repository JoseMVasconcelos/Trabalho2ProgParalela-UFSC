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

- **Réplicas (n)**: Para as `réplicas`, são atribuido os `ranks 2-n`, dependendo da quantidade de processos escolhino na execução. As réplicas esperam uma solicitação, e para cada palavra chave recebida, pesquisa nos arquivos `.txt` da pasta `texts`. Após esgotarem todas as linhas e todas as palavras chaves, retornam o número de ocorrências em cada arquivo, para o mesmo endereço do solicitante. Elas rodam em paralelo uma com a outra, e não tem ordem para responder ao solicitante. O `nó raiz` pode solicitar na ordem `1, 3, 2` e receber na ordem `3, 2, 1`.

- **TIMESTAMPS**: A cada envio/recebimento do `cliente` e `nó raiz`, é printado uma mensagem na tela, junto a um TIMESTAMP: 
  
    `CLIENTE enviando pesquisa para nó raiz: blockchain criptomoedas bitcoin. TIMESTAMP: 2024-06-20 17:24:16.480956`.
    
     Essa foi uma decisão tomada para burlar o sistema de print desordenado do python. O python coloca todas as mensagens a serem printadas em um buffer, e elas podem sair na ordem errada, o timestamp server para entender a orderm correta das mensagens.

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

### Casos de Teste e Resultados Esperados
Número de réplicas = 2

`CLIENTE enviando pesquisa para nó raiz: saúde mental psicologia terapia.`

`NÓ RAIZ envia palavra chaves ['mental', 'terapia'] para réplica 1.`

`NÓ RAIZ envia palavra chaves ['saúde', 'psicologia'] para réplica 0.`

`CLIENTE recebeu o resultado do nó raiz!: {'A Evolução e o Impacto dos Video Games na Sociedade Moderna.txt': 2, 'Desafios Ecológicos A Crise Ambiental do Século XXI.txt': 1}`

Observando os textos:
#### A Evolução e o Impacto dos Video Games na Sociedade Moderna:
Os video games, desde sua criação nas décadas de 1970 e 1980, evoluíram de simples jogos de arcade para complexas obras interativas que abrangem diversos gêneros e plataformas. Inicialmente, jogos como Pong e Space Invaders cativaram jogadores com suas mecânicas simples e gráficos rudimentares. No entanto, o avanço da tecnologia permitiu que os video games se tornassem cada vez mais sofisticados, oferecendo experiências imersivas com gráficos em alta definição, narrativa envolvente e jogabilidade inovadora. Hoje, os jogos são jogados em consoles, computadores e dispositivos móveis, alcançando uma audiência global diversificada.

A indústria de video games é uma das mais lucrativas do entretenimento, superando até mesmo a indústria cinematográfica em termos de receita. Este crescimento impressionante é impulsionado não apenas pela venda de jogos, mas também por modelos de negócios inovadores como jogos gratuitos com compras dentro do aplicativo, assinaturas de serviços de jogos e esportes eletrônicos (eSports). Os eSports, em particular, se tornaram um fenômeno cultural, com competições internacionais atraindo milhões de espectadores e oferecendo prêmios substanciais. Plataformas de streaming como Twitch e YouTube Gaming permitiram que jogadores transmitissem suas partidas ao vivo, criando novas oportunidades de carreira e fomentando uma comunidade global de gamers.

Além do entretenimento, os video games têm mostrado um impacto significativo em várias áreas da sociedade. Na educação, jogos são utilizados como ferramentas de aprendizado, promovendo habilidades cognitivas, resolução de problemas e colaboração. Na saúde, a gamificação está sendo usada para reabilitação física e `mental`, oferecendo terapias interativas para pacientes. No entanto, os video games também enfrentam críticas e desafios, como a preocupação com a dependência, o impacto na saúde `mental` e a representação de violência. A pesquisa e o debate contínuos sobre os efeitos dos video games são essenciais para maximizar seus benefícios e mitigar seus riscos, garantindo que continuem a ser uma força positiva na sociedade moderna.

### Conclusão

Os resultados dos testes demonstraram que a implementação do sistema de acionamento automático em carros autônomos, utilizando programação multithread em C, é capaz de lidar eficientemente com diferentes configurações e cenários, mantendo a integridade das operações mesmo em condições de alta carga e probabilidade de falha. A utilização de múltiplas threads, semáforos e mutexes proporcionou uma execução concorrente e segura do sistema, garantindo tempos de resposta rápidos e uma distribuição eficiente das tarefas entre os componentes do sistema. Esses resultados validam a abordagem adotada e destacam a viabilidade do uso de técnicas de programação paralela na construção de sistemas complexos e robustos.
