//
// Created by Luca Cappelletti on 2019-03-04.
//

#include "threshold.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <assert.h>

int comp (const void * elem1, const void * elem2){
    double f = *((double*)elem1);
    double s = *((double*)elem2);
    if (f > s) return  1;
    if (f < s) return -1;
    return 0;
}

double determine_threshold(Matrix const* matrices, int const matrices_number, double const known_negatives_percentage){
    size_t vector_size;
    double* flatten = flatten_matrices_drop_nan_identity(matrices, matrices_number, &vector_size);
    if (vector_size==0){
        return INFINITY;
    }
    qsort(flatten, vector_size, sizeof(*flatten), comp);
    double position = (vector_size-1)*known_negatives_percentage;
    int lower=(int)floor(position), upper=(int)ceil(position);
    double lower_value = flatten[lower];
    double upper_value = flatten[upper];
    double threshold = (lower_value + upper_value)/2;
    free(flatten);
    return threshold;
}

double* determine_thresholds(Matrix ** matrices_groups, int const matrices_number, int const groups_number, double const* known_negatives_percentages){
    double* thresholds = (double *)malloc(groups_number * sizeof(double));
    for(int i=0; i<groups_number; i++){
        thresholds[i] = determine_threshold(matrices_groups[i], matrices_number, known_negatives_percentages[i]);
    }
    return thresholds;
}

void apply_threshold(Matrix** matrices_groups, int const matrices_number, int const groups_number, double const* thresholds){
    for (int i=0; i<groups_number; i++){
        for (int j=0; j<matrices_number; j++){
            fill_above_matrix(&matrices_groups[i][j], NAN, thresholds[i], true);
            min_max_matrix_norm(&matrices_groups[i][j], true);
        }
    }
}

void threshold(Matrix ** self_matrices_groups, int  const self_matrices_number, Matrix** other_matrices_groups, int const other_matrices_number, int const groups_number, double const* known_negatives_percentages){
    double* thresholds = determine_thresholds(self_matrices_groups, self_matrices_number, groups_number, known_negatives_percentages);
    apply_threshold(other_matrices_groups, other_matrices_number, groups_number, thresholds);
    free(thresholds);
}