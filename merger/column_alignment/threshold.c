//
// Created by Luca Cappelletti on 2019-03-04.
//

#include "threshold.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

int comp (const void * elem1, const void * elem2){
    double f = *((double*)elem1);
    double s = *((double*)elem2);
    if (f > s) return  1;
    if (f < s) return -1;
    return 0;
}

void sort(double* x, size_t size){
    qsort(x, size, sizeof(*x), comp);
}

double determine_threshold(Matrix* matrices, int matrices_number, double known_negatives_percentage){
    size_t vector_size;
    double* flatten = flatten_matrices(matrices, matrices_number, &vector_size);
    qsort(flatten, vector_size, sizeof(*flatten), comp);
    double position = vector_size*(1-known_negatives_percentage);
    int lower=(int)floor(position), upper=(int)ceil(position);
    double threshold = (flatten[lower] + flatten[upper])/2;
    free(flatten);
    return threshold;
}

double* determine_thresholds(Matrix** matrices_groups, int matrices_number, int groups_number, double* known_negatives_percentages){
    double* thresholds = (double *)malloc(groups_number * sizeof(double));
    for(int i=0; i<groups_number; i++){
        thresholds[i] = determine_threshold(matrices_groups[i], matrices_number, known_negatives_percentages[i]);
    }
    return thresholds;
}

Matrix** threshold(Matrix** matrices_groups, int matrices_number, int groups_number, double* known_negatives_percentages, bool inplace){
    double* thresholds = determine_thresholds(matrices_groups, matrices_number, groups_number, known_negatives_percentages);
    Matrix** thresholded_groups;
    if (inplace){
        thresholded_groups = matrices_groups;
    } else {
        thresholded_groups = (Matrix**)malloc(groups_number * sizeof(Matrix*));
        for (int i=0; i<groups_number; i++){
            thresholded_groups[i] = (Matrix*)malloc(groups_number * sizeof(Matrix));
        }
    }

    for (int i=0; i<groups_number; i++){
        for (int j=0; j<matrices_number; j++){
            thresholded_groups[i][j] = fill_above_matrix(matrices_groups[i][j], NAN, thresholds[i], inplace);
        }
    }

    return  thresholded_groups;
}