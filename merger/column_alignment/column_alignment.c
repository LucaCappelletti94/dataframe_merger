//
// Created by Luca Cappelletti on 2019-03-03.
//

#include <math.h>
#include "column_alignment.h"
#include "utils.h"

int** column_alignment(char* path, size_t datasets_number, size_t metrics_number){
    size_t matrices_number = matrices_number_from_datasets(metrics_number);
    Matrix ** self_matrices_groups = (Matrix**)malloc(metrics_number* sizeof(Matrix*));
    Matrix ** other_matrices_groups = (Matrix**)malloc(matrices_number* sizeof(Matrix*));
}