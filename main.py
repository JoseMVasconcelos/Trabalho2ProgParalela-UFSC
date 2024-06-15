import os
import fnmatch
from mpi4py import MPI
#mpirun -n 4 python3 main.py

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def client():
    queries = ["Lorem Ipsum Dolo", "Teste2", "Brabo se funcionar"]
    query_position = 0
    root_rank = 1

    while query_position < len(queries):
        print(f"CLIENTE enviando pesquisa para nó raiz: {queries[query_position]}")
        comm.send(queries[query_position], dest=root_rank)
        print(f"CLIENTE recebeu o resultado do nó raiz!: {comm.recv(source=root_rank)}")
        query_position += 1
    

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
        print("NÓ RAIZ recebeu pesquisa do cliente")
        keywords = client_query.split(" ")
        
        #Envia as palavras para as réplicas
        replicas_index = 0
        for word in keywords:
            print(f"NÓ RAIZ envia palavra chave {word} para réplica {replicas_index}")
            comm.send(word, dest=replicas_ranks[replicas_index])
            results = comm.recv(source=replicas_ranks[replicas_index])
            print(f"NÓ RAIZ recebeu resultados da réplica {replicas_index}")
            for result in results:
                if result[0] in query_response.keys():
                    query_response[result[0]] = query_response.get(result[0]) + result[1]
                else:
                    query_response.update({result[0]: result[1]})
            replicas_index = (replicas_index + 1) % num_replicas
        print("NÓ RAIZ enviando resposta para o cliente")
        if query_response:
            comm.send(query_response, dest=client_rank)
        else:
            comm.send("Sem ocorrências!", dest=client_rank)

    
def replica():
    status = MPI.Status()

    while True:
        results = []

        keyword = comm.recv(source=MPI.ANY_SOURCE, status = status)
        for root, dirnames, filenames in os.walk("./texts"):
            for filename in fnmatch.filter(filenames, "*.txt"):
                occurrences = 0
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        if keyword in line:
                            occurrences += 1
                if occurrences >= 1:
                    results.append((filename, occurrences))
        comm.send(results, dest=status.Get_source())

class main():

    num_replicas = size - 2

    if (size < 3):
        print("Need at least 3 processes")
        exit(1)

    if (rank == 0):
        client()

    if (rank == 1):
        root(num_replicas)

    if (rank > 1):
        replica()

main()