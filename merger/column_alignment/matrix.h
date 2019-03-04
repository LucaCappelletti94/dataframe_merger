//
// Created by Luca Cappelletti on 2019-03-03.
//

#ifndef UNTITLED_MATRIX_H
#define UNTITLED_MATRIX_H

typedef struct matrix_struct {
    int h;
    int w;
    double **M;
} Matrix;

Matrix init_matrix(int h, int w);
void free_matrix(Matrix matrix);
Matrix fill_nan(Matrix matrix, double fill_value);

#endif //UNTITLED_MATRIX_H
