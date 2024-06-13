#include <stdio.h>
#include <string.h>
#include <mpi.h>

//Feito por José Vasconcelos (22100906) e Marcos Roberto (22100915)
//Para compilar: mpicc main.c -o main

//CLIENT RANK SHOULD AWAYS BE 0!
//ROOT NODE RANK SHOULD AWAYS BE 1!
//REPLICAS RANKS SHOULD BE FROM 2->N!
//SO IF I START WITH 8 PROCESSES, REPLICAS RANKS SHOULD BE 2->7!
int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    //POPULAR COM MAIS TEXTO
    char clientRequisitions[100][100] = {"Lorem Ipsum Dolo", "Teste 2", "Brabo se funcionar"};
    int clientReqPosition = 0;


    if (world_size < 3) {
        fprintf(stderr, "World size tem que ser pelo menos 3 para %s\n", argv[0]);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    //Processo Cliente
    if (world_rank == 0) {
        int root_rank = 1;
        char str[] = clientRequisitions[clientReqPosition];  
        int stringSize = strlen(str);
        MPI_Send(&str, stringSize, MPI_BYTE, root_rank, 0, MPI_COMM_WORLD);

    }

    //Processo Raiz
    if (world_rank == 1) {
        MPI_Status = status;
        int client_rank = 0;
        MPI_Rev(&stringSize, 100, MPI_BYTE, client_rank, 0, MPI_COMM_WORLD, &status);
        MPI_Get_count(&status, MPI_BYTE, &stringSize);
        char *token = strtok(clientRequisitions[clientReqPosition], " ");
        while (token != NULL) {
            printf("%s\n", token);
            token = strtok(NULL, " ");
        }
    }

    //Processos Réplicas
    if (world_rank > 1) {
        printf("%s\n", clientRequisitions[clientReqPosition+2]);
    }

    MPI_Finalize();
}