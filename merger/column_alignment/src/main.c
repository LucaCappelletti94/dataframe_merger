//
// Created by Luca Cappelletti on 2019-03-09.
//

#include <stdio.h>
#include "main.h"
#include "column_alignment.h"

#define BASIC_ARGS 4

int main(int argc, char **argv){
    if (argc < BASIC_ARGS) {
        printf("Illegal number of basic arguments, expected at least %d, received %d", BASIC_ARGS, argc);
        exit(-1);
    }
    char* path = argv[1];
    char* output = argv[2];
    int datasets_number = (int)strtol(argv[3], NULL, 10);
    int metrics_number = (int)strtol(argv[4], NULL, 10);
    if (argc < BASIC_ARGS + metrics_number*2) {
        printf("Illegal number of arguments, expected %d, received %d", BASIC_ARGS+metrics_number*2, argc);
        exit(-1);
    }
    double *known_negatives_percentages = (double*)malloc(metrics_number* sizeof(double));
    double *weights = (double*)malloc(metrics_number* sizeof(double));

    for(int i=0; i<=metrics_number; i++){
        known_negatives_percentages[i] = strtod(argv[BASIC_ARGS+i+1], NULL);
        weights[i] = strtod(argv[BASIC_ARGS+metrics_number+i], NULL);
    }

    column_alignment(path, output, datasets_number, metrics_number, known_negatives_percentages, weights);
    free(known_negatives_percentages);
    free(weights);

    return 0;
}