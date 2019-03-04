//
// Created by Luca Cappelletti on 2019-03-03.
//

#include <math.h>
#include "column_alignment.h"
#include "load_csv.h"
#include "solve.h"

int** column_alignment(Matrix costs){
    Matrix filled = fill_nan(costs, INFINITY);
    int** alignment = solve(filled);
    free_matrix(filled);
    return alignment;
}