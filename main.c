#include <stdio.h>
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

    if (world_size < 3) {
        fprintf(stderr, "World size tem que ser pelo menos 3 para %s\n", argv[0]);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    MPI_Finalize();
}