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

Matrix init_matrix(int h, int w){
    Matrix matrix;
    matrix.h = h;
    matrix.w = w;
    matrix.M = (double **)malloc(matrix.h * sizeof(double*));
    for(int i = 0; i < matrix.h; i++) matrix.M[i] = (double *)malloc(matrix.w * sizeof(double));
    return matrix;
}

void free_matrix(Matrix matrix){
    for(int i=0; i<matrix.h; i++){
        free(matrix.M[i]);
    }
    free(matrix.M);
}


Matrix fill_nan(Matrix matrix, double fill_value){
    Matrix filled = init_matrix(matrix.h, matrix.w);
    for(int i=0; i<matrix.h; i++){
        for(int j=0; j<matrix.w; j++){
            filled[i][j] = is_nan(matrix.M[i][j])?fill_value:matrix.M[i][j];
        }
    }
    return filled;
}
