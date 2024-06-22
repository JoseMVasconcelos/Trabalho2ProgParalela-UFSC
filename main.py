import os
import fnmatch
import datetime
import time
import re
import random
from mpi4py import MPI

#mpirun -n 4 python3 main.py
#Feito por José Vasconcelos (22100906) e Marcos Roberto (22100915)

if not MPI.Is_initialized():
    MPI.Init()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def client():
    queries = [
  "inteligência artificial aprendizado de máquina redes neurais",
  "mudança climática aquecimento global energia renovável",
  "blockchain criptomoedas bitcoin",
  "saúde mental psicologia terapia",
  "educação online e-learning cursos virtuais",
  "biotecnologia engenharia genética clonagem",
  "carros elétricos veículos autônomos mobilidade sustentável",
  "realidade virtual realidade aumentada VR",
  "empreendedorismo startups inovação",
  "big data análise de dados ciência de dados",
  "computação quântica algoritmos quânticos q-bits",
  "robótica automação inteligência artificial",
  "energia solar painéis solares sustentabilidade",
  "economia compartilhada Uber Airbnb",
  "alimentação saudável dieta balanceada nutrição",
  "literatura clássica romances históricos autores famosos",
  "fotografia digital câmeras DSLR edição de fotos",
  "jogos de vídeo eSports indústria de games",
  "moda sustentável slow fashion upcycling",
  "desenvolvimento pessoal autoajuda produtividade",
  "viagens destinos turísticos guia de viagens",
  "meditação mindfulness bem-estar",
  "economia circular reciclagem gestão de resíduos",
  "inteligência emocional habilidades sociais empatia",
  "fintech bancos digitais pagamentos móveis",
  "cidades inteligentes urbanismo tecnologia urbana",
  "impressão 3D fabricação aditiva prototipagem rápida",
  "cinema filmes clássicos diretores famosos",
  "música compositores clássicos bandas de rock",
  "história eventos históricos figuras históricas",
  "política governança políticas públicas",
  "esportes futebol olimpíadas",
  "arte pintura museus",
  "tecnologia da informação TI infraestrutura de rede",
  "cibersegurança hacking proteção de dados",
  "direito legislação jurisprudência",
  "marketing digital SEO redes sociais",
  "gestão de projetos metodologias ágeis scrum",
  "negócios internacionais comércio exterior globalização",
  "meio ambiente preservação ambiental biodiversidade",
  "física quântica teoria das cordas mecânica quântica",
  "engenharia civil construção infraestrutura",
  "engenharia elétrica circuitos eletrônica",
  "engenharia de software desenvolvimento de sistemas programação",
  "engenharia mecânica mecatrônica projetos mecânicos",
  "agricultura sustentável agroecologia permacultura",
  "energia eólica turbinas eólicas energia limpa",
  "microbiologia bactérias vírus doenças infecciosas",
  "neurociência cérebro neuroplasticidade",
  "psiquiatria transtornos mentais psicofarmacologia",
  "literatura contemporânea romances best-sellers",
  "história da arte movimentos artísticos renascimento",
  "gastronomia culinária receitas pratos típicos",
  "vinhos enologia degustação de vinhos",
  "cervejas artesanais microcervejarias tipos de cerveja",
  "economia macroeconomia microeconomia teoria econômica",
  "administração gestão empresarial liderança",
  "recursos humanos recrutamento treinamento desenvolvimento",
  "finanças investimentos mercado de ações bolsa de valores",
  "imóveis mercado imobiliário compra e venda de imóveis",
  "arquitetura design de interiores projetos arquitetônicos",
  "turismo ecológico viagens sustentáveis natureza",
  "fotografia de paisagem técnicas fotográficas edição de imagens",
  "design gráfico branding identidade visual",
  "publicidade propaganda campanhas publicitárias",
  "mídias sociais influenciadores marketing de conteúdo",
  "e-commerce lojas virtuais comércio eletrônico",
  "logística cadeia de suprimentos transporte",
  "transportes mobilidade urbana infraestrutura viária",
  "educação infantil pedagogia desenvolvimento infantil",
  "ensino superior universidades cursos acadêmicos",
  "pesquisa científica metodologia científica publicações",
  "biologia evolução genética ecossistemas",
  "química orgânica reações químicas compostos químicos",
  "física teórica relatividade teoria quântica",
  "matemática álgebra geometria cálculo",
  "estatística probabilidade análise estatística",
  "medicina diagnóstico tratamentos doenças",
  "enfermagem cuidados de saúde assistência médica",
  "odontologia saúde bucal tratamentos dentários",
  "fisioterapia reabilitação terapias físicas",
  "nutrição esportiva dietas suplementação",
  "gerontologia envelhecimento qualidade de vida",
  "economia doméstica finanças pessoais orçamento familiar",
  "psicopedagogia dificuldades de aprendizagem métodos educativos",
  "direitos humanos justiça social igualdade",
  "sociologia comportamento social interações humanas",
  "antropologia culturas tradições rituais",
  "linguística aquisição de linguagem gramática",
  "filosofia ética metafísica epistemologia",
  "teologia estudos religiosos espiritualidade",
  "astrologia signos horóscopo mapa astral",
  "astronomia planetas estrelas galáxias",
  "geologia formação de rochas tectônica de placas",
  "geografia física geografia humana cartografia",
  "ecologia conservação ambiental sustentabilidade"
]
    query_position = 0
    root_rank = 1

    while query_position < len(queries):
        print(f"CLIENTE enviando pesquisa para nó raiz: {queries[query_position]}. TIMESTAMP: " + str(datetime.datetime.now()))
        comm.send(queries[query_position], dest=root_rank, tag=0)
        print(f"CLIENTE recebeu o resultado do nó raiz!: {comm.recv(source=root_rank)}. TIMESTAMP: " + str(datetime.datetime.now()))
        query_position += 1
        print('------------------------------------------------------------------------------------')
        time.sleep(random.randint(1, 2))
    comm.Abort()
    

def root(num_replicas):
    #Endereço do cliente e das réplicas
    client_rank = 0
    replicas_ranks = []
    for i in range(num_replicas):
        replicas_ranks.append(i+2)

    while True:
        query_response = dict()
        #Recebe a query do cliente e separa em palavras 
        client_query = comm.recv(source=client_rank)
        print("NÓ RAIZ recebeu pesquisa do cliente. TIMESTAMP: " + str(datetime.datetime.now()))
        keywords = client_query.split(" ")
        keywordArray = []
        
        #Envia as palavras para as réplicas
        replicas_index = 0
        for word in keywords:
            if len(keywordArray) < num_replicas:
                keywordArray.append([word])
            else:
                keywordArray[replicas_index].append(word)
            replicas_index = (replicas_index + 1) % num_replicas

        for i in range(len(keywordArray)):
            print(f"NÓ RAIZ envia palavra chaves {keywordArray[i]} para réplica {replicas_ranks[i]-2}. TIMESTAMP: " + str(datetime.datetime.now()))
            comm.send(keywordArray[i], dest=replicas_ranks[i], tag=0)

        for i in range(len(keywordArray)):
            status = MPI.Status()
            results = comm.recv(source=MPI.ANY_SOURCE, status = status)
            print(f"NÓ RAIZ recebeu resultados da réplica {status.Get_source()-2}. TIMESTAMP: " + str(datetime.datetime.now()))
            for result in results:
                if result[0] in query_response.keys():
                    query_response[result[0]] = query_response.get(result[0]) + result[1]
                else:
                    query_response.update({result[0]: result[1]})

        if query_response:
            comm.send(query_response, dest=client_rank, tag=0)
        else:
            comm.send("Sem ocorrências!", dest=client_rank, tag=0)

    
def replica():
    status = MPI.Status()
    
    while True:
        results = []
        resultsDebug = []
        keywords = comm.recv(source=MPI.ANY_SOURCE, status = status)
        for root, dirnames, filenames in os.walk("./texts"):
            for filename in fnmatch.filter(filenames, "*.txt"):
                occurrences = 0
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    for unfilteredLine in file:
                        separatedLine = re.sub(r'[^\w\s]|\n', ' ', unfilteredLine).lower()
                        separatedLine = separatedLine .split(" ")
                        for word in separatedLine:
                            for keyword in keywords:
                                if keyword == word:
                                    occurrences += 1
                if occurrences >= 1:
                    results.append((filename, occurrences))
        
        comm.send(results, dest=status.Get_source(), tag=0)

class main():

    num_replicas = size - 2

    if (size < 3):
        print("Pelo menos 3 processos!")
        exit(1)

    if (rank == 0):
        client()

    if (rank == 1):
        root(num_replicas)

    if (rank > 1):
        replica()

main()