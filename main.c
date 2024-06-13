#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <dirent.h>
#include <sys/stat.h>
#include <mpi.h>

//Feito por José Vasconcelos (22100906) e Marcos Roberto (22100915)
//Para compilar: mpicc main.c -o main

// bool hasSearchWord(char *fileContect, char *searchWord) {
//     return strstr(fileContect, searchWord) != NULL;
// }

#define STRING_SIZE 100
#define TRUE 1
#define FALSE 0


char str[STRING_SIZE];

int clientNode() {
    char clientRequisitions[3][STRING_SIZE] = {"Lorem Ipsum Dolo", "Teste 2", "Brabo se funcionar"};
    int clientReqPosition = 0;
    int root_rank = 1;

    strcpy(str, clientRequisitions[clientReqPosition]);
    MPI_Send(str, strlen(str)+1, MPI_CHAR, root_rank, 0, MPI_COMM_WORLD);

    return 0;
}

int rootNode(int numReplicas) {
    int client_rank = 0;
    int replicas_rank[numReplicas];
    int replicaQueue = 0;

    for (int i = 0; i < numReplicas; i++) {
        replicas_rank[i] = i+2;
    }

    MPI_Recv(&str, STRING_SIZE, MPI_CHAR, client_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    
    char *token = strtok(str, " ");
    while (token != NULL) {
        MPI_Send(token, strlen(token)+1, MPI_CHAR, replicas_rank[replicaQueue], 0, MPI_COMM_WORLD);
        replicaQueue = (replicaQueue + 1) % (numReplicas);
        token = strtok(NULL, " ");
    }
    return 0;
}

int findKeywordOccurenccess(char *folderPath, char *fileName, char *keyWord) {
    char filePath[256];
    sprintf(filePath, "%s/%s", folderPath, fileName);

    printf("%s\n", filePath);
    FILE *file = fopen(filePath, "r");
    char line[256];
    int lineCount = 0;
    int occurenceCount = 0;

    if (file == NULL) {
        perror("fopen");
        return 0;
    }

    while (fgets(line, sizeof(line), file)) {
        lineCount++;
        if (strstr(line, keyWord) != NULL) {
            occurenceCount++;
        }
    }

    //printf("Ocorrências da palavra chave '%s' no arquivo '%s': %d\n", keyWord, fileName, occurenceCount);
    fclose(file);
    return occurenceCount;
}

void findTxtFiles(char *keyWord) {
    char folderPath[7] = "./texts";
    struct dirent *entry;
    DIR *dp = opendir(folderPath);

    if (dp == NULL) {
        perror("opendir");
        return;
    }

    while ((entry = readdir(dp))) {
        if (entry->d_type == DT_REG) {
            const char *dot = strrchr(entry->d_name, '.');
            if (dot && strcmp(dot, ".txt") == 0) {
                char *fileName = entry->d_name;
                int occurence = findKeywordOccurenccess(folderPath, fileName, keyWord);
            }
        }
    }

    closedir(dp);
}

void replicaNode(int world_rank) {
    int root_rank = 1;
    int occurenceCount = 0;
    char token[STRING_SIZE];

    while (TRUE) {
        MPI_Recv(&token, STRING_SIZE, MPI_CHAR, root_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Réplica %d recebeu: %s\n", world_rank, token);
        findTxtFiles(token);
    }
}

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    int numReplicas = world_size - 2;

    if (world_size < 3) {
        fprintf(stderr, "World size tem que ser pelo menos 3 para %s\n", argv[0]);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    //Processo Cliente
    if (world_rank == 0) {
        clientNode();
    }

    //Processo Raiz
    if (world_rank == 1) {
        rootNode(numReplicas);
    }

    // Processos Réplicas
    if (world_rank > 1) {
        replicaNode(world_rank);
    }

    MPI_Finalize();
}