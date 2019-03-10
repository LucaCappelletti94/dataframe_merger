//
// Created by Luca Cappelletti on 2019-03-03.
//


#include <printf.h>
#include <string.h>
#include "matrix.h"
#include "double.h"
#include "vector.h"
#include "int.h"


Matrix init_matrix(size_t const h, size_t const w){
    Matrix matrix;
    matrix.h = h;
    matrix.w = w;
    matrix.M = (double **)malloc(matrix.h * sizeof(double*));
    for(int i = 0; i < matrix.h; i++) matrix.M[i] = (double *)malloc(matrix.w * sizeof(double));
    return matrix;
}

Matrix init_matrix_like(Matrix const matrix){
    return init_matrix(matrix.h, matrix.w);
}

Matrix fill_identity(size_t const n, double const diagonal, double const standard){
    Matrix I = init_matrix(n, n);
    for(size_t i=0; i<n; i++) {
        for(size_t j=0; j<n; j++) {
            I.M[i][j] = i==j?diagonal:standard;
        }
    }
    return I;
}

void free_matrix(Matrix matrix){
    for(int i=0; i<matrix.h; i++){
        free(matrix.M[i]);
    }
    free(matrix.M);
}


void print_matrix(Matrix matrix){
    size_t * max_sizes = (size_t*)malloc(matrix.w* sizeof(size_t));
    for(int i=0; i<matrix.w; i++){
        max_sizes[i] = 0;
        for(int j=0; j<matrix.h; j++){
            size_t e = strlen(double_to_str(matrix.M[j][i]));
            max_sizes[i] = e>max_sizes[i]?e:max_sizes[i];
        }
    }
    for(int i=0; i<matrix.h; i++){
        for(int j=0; j<matrix.w; j++){
            size_t e = strlen(double_to_str(matrix.M[i][j]));
            int padding = (int)(max_sizes[j] - e);
            if (j!=matrix.w-1){
                printf("%f,%.*s", matrix.M[i][j], padding+1, "                                             ");
            } else {
                printf("%f%.*s", matrix.M[i][j], padding, "                                             ");
            }

        }
        printf("\n");
    }
    printf("\n");
    free(max_sizes);
}

Matrix fill_matrix(Matrix matrix, double const fill_value, int (*filter)(double), bool const inplace){
    Matrix filled = inplace?matrix:init_matrix_like(matrix);
    for(int i=0; i<matrix.h; i++){
        for(int j=0; j<matrix.w; j++){
            double value = matrix.M[i][j];
            filled.M[i][j] = filter(value)?fill_value:value;
        }
    }
    return filled;
}

Matrix fill_range_matrix(Matrix *matrix, double const fill_value, double const min, double const max, bool const inplace){
    Matrix filled = inplace?*matrix:init_matrix_like(*matrix);
    for(int i=0; i<filled.h; i++){
        for(int j=0; j<filled.w; j++){
            double value = (*matrix).M[i][j];
            filled.M[i][j] = in_range(value, min, max)?fill_value:value;
        }
    }
    return filled;
}

Matrix fill_above_matrix(Matrix *matrix, double fill_value, double const min, bool const inplace){
    return  fill_range_matrix(matrix, fill_value, min, INFINITY, inplace);
}

double* flatten_matrices_drop_nan_identity(Matrix const *matrices, int const matrices_number, size_t * vector_size){
    size_t size=0;
    for(int i=0; i<matrices_number; i++){
        size += matrices[i].h*matrices[i].w;
        for(int j=0; j<matrices[i].h; j++){
            for(int k=0; k<matrices[i].w; k++){
                size -= isnan(matrices[i].M[j][k]) || j==k;
            }
        }
    }
    *vector_size = size;
    double* flatten = (double *)malloc(size * sizeof(double));
    for(int k=matrices_number-1; k>=0; k--){
        Matrix m = matrices[k];
        for(int i=(int)m.h-1; i>=0; i--){
            for(int j=(int)m.w-1; j>=0; j--){
                if (is_not_nan(m.M[i][j]) && i!=j){
                    flatten[--size] = m.M[i][j];
                }
            }
        }
    }

    return flatten;
}

void matrix_nan_min_max(Matrix const matrix, double *min, double *max){
    *min=*max=NAN;
    for (int i=0; i<matrix.h; i++){
        for (int j=0; j<matrix.w; j++){
            double value = matrix.M[i][j];
            *min = nan_min(*min, value);
            *max = nan_max(*max, value);
        }
    }
}

Matrix min_max_matrix_norm(Matrix *matrix, bool const inplace){
    double min, max;
    matrix_nan_min_max(*matrix, &min, &max);
    if(any(el_is_nan(2, min, max), 2)){
        return *matrix;
    }
    Matrix normalized = inplace?*matrix:init_matrix_like(*matrix);
    for (int i=0; i<normalized.h; i++){
        for (int j=0; j<normalized.w; j++){
            normalized.M[i][j] = min_max_norm((*matrix).M[i][j], min, max);
        }
    }
    return normalized;
}

size_t extrapolate_group_size(Matrix const* group, int const submatrices){
    size_t sum=group[0].w;
    for (int i=0; i<submatrices; i++){
        sum+=group[i].h;
    }
    return sum;
}

Matrix group_to_adjacency_matrix(Matrix const* group, int *** group_masks, int matrices){
    Matrix I = fill_identity(extrapolate_group_size(group, matrices), 0, INFINITY);
    size_t offset_x = 0, offset_y=0;
    for(int sub=matrices, total_sub=0; sub>0; sub--){
        offset_y+=group[total_sub].w;
        for (size_t k=0, starting_offset_y=offset_y; k<sub; k++, starting_offset_y+=group[total_sub].h, total_sub++){
            for(size_t i=0; i<group[total_sub].h; i++){
                for (int j = 0; j < group[total_sub].h; j++) {
                    if (group_masks[total_sub][i][j]){
                        I.M[offset_x+i][offset_y+j]= I.M[offset_y+j][offset_x+i] = group[total_sub].M[i][j];
                    }
                }
            }
        }
        offset_x=offset_y;
    }
    return I;
}

Matrix* groups_to_adjacency_matrix(Matrix ** groups, int **** groups_masks, int groups_number, int matrices){
    Matrix* adjacency_matrices = (Matrix*)malloc(groups_number*sizeof(Matrix));
    for(int i=0; i<groups_number; i++){
        adjacency_matrices[i] = group_to_adjacency_matrix(groups[i], groups_masks[i], matrices);
    }
    return adjacency_matrices;
}

Matrix fill_nan(Matrix matrix, double const fill_value, bool const inplace){
    return fill_matrix(matrix, fill_value, &is_nan, inplace);
}