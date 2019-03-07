#include "hungarian/hungarian.h"
#include "load_csv.h"
#include "solve.h"
#include <stdlib.h>

int** solve(Matrix costs){
    hungarian_problem_t p;
    hungarian_init(&p, costs.M, (int)costs.h, (int)costs.w, HUNGARIAN_MODE_MINIMIZE_COST);
    int ** assignment = (int **)malloc(costs.h * sizeof(int*));
    for(int i=0; i<costs.h; i++){
        assignment[i] = (int *)malloc(costs.w * sizeof(int));
        for(int j=0; j<costs.w; j++){
            assignment[i][j] = p.assignment[i][j];
        }
    }
    hungarian_solve(&p);
    hungarian_free(&p);
    return assignment;
}