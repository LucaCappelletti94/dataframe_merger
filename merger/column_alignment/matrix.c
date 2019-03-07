//
// Created by Luca Cappelletti on 2019-03-03.
//

#include <stdbool.h>
#include <math.h>
#include "matrix.h"
#include <stdlib.h>

bool is_nan(double value){
    return value == NAN;
}

Matrix init_matrix(size_t h, size_t w){
    Matrix matrix;
    matrix.h = h;
    matrix.w = w;
    matrix.M = (double **)malloc(matrix.h * sizeof(double*));
    for(int i = 0; i < matrix.h; i++) matrix.M[i] = (double *)malloc(matrix.w * sizeof(double));
    return matrix;
}

Matrix init_matrix_like(Matrix matrix){
    return init_matrix(matrix.h, matrix.w);
}

void free_matrix(Matrix matrix){
    for(int i=0; i<matrix.h; i++){
        free(matrix.M[i]);
    }
    free(matrix.M);
}

Matrix fill_matrix(Matrix matrix, double fill_value, bool (*filter)(double), bool inplace){
    Matrix filled = inplace?matrix:init_matrix_like(matrix);
    for(int i=0; i<matrix.h; i++){
        for(int j=0; j<matrix.w; j++){
            double value = matrix.M[i][j];
            filled.M[i][j] = filter(value)?fill_value:value;
        }
    }
    return filled;
}

Matrix fill_range_matrix(Matrix matrix, double fill_value, double min, double max, bool inplace){
    Matrix filled = inplace?matrix:init_matrix_like(matrix);
    for(int i=0; i<matrix.h; i++){
        for(int j=0; j<matrix.w; j++){
            double value = matrix.M[i][j];
            filled.M[i][j] = (min<= value && value <= max)?fill_value:value;
        }
    }
    return filled;
}

Matrix fill_above_matrix(Matrix matrix, double fill_value, double min, bool inplace){
    return  fill_range_matrix(matrix, fill_value, min, INFINITY, inplace);
}

Matrix fill_below_matrix(Matrix matrix, double fill_value, double max, bool inplace){
    return  fill_range_matrix(matrix, fill_value, -INFINITY, max, inplace);
}

double* flatten_matrices(Matrix* matrices, int matrices_number, size_t* vector_size){
    size_t size=0;
    for(int i=0; i<matrices_number; i++){
        size += matrices[i].h*matrices[i].w;
    }
    *vector_size = size;
    double* flatten = (double *)malloc(size * sizeof(double));
    for(int k=matrices_number-1; k>=0; k--){
        Matrix m = matrices[k];
        for(size_t i=m.h; i>=0; i--){
            for(size_t j=m.w; j>=0; j--){
                flatten[--size] = m.M[i][j];
            }
        }
    }

    return flatten;
}

double* flatten_matrix(Matrix matrix, size_t* vector_size){
    return flatten_matrices(&matrix, 1, vector_size);
}

Matrix fill_nan(Matrix matrix, double fill_value, bool inplace){
    return fill_matrix(matrix, fill_value, &is_nan, inplace);
}