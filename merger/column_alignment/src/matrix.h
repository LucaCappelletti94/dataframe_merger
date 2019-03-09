//
// Created by Luca Cappelletti on 2019-03-03.
//

#ifndef UNTITLED_MATRIX_H
#define UNTITLED_MATRIX_H

#include <stdbool.h>
#import <stdlib.h>

typedef struct matrix_struct {
    size_t h;
    size_t w;
    double **M;
} Matrix;

Matrix init_matrix(size_t h, size_t w);
Matrix init_matrix_like(Matrix matrix);
void free_matrix(Matrix matrix);
Matrix fill_above_matrix(Matrix *matrix, double fill_value, double min, bool inplace);
Matrix fill_below_matrix(Matrix *matrix, double fill_value, double max, bool inplace);
double* flatten_matrices(Matrix const *matrices, int matrices_number, size_t * vector_size);
Matrix fill_nan(Matrix matrix, double fill_value, bool inplace);
Matrix min_max_matrix_norm(Matrix *matrix, bool inplace);
Matrix* groups_to_adjacency_matrix(Matrix ** groups, int **** groups_masks, int groups_number, int matrices);

#endif //UNTITLED_MATRIX_H
