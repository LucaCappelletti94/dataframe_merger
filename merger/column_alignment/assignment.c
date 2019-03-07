#include "hungarian/hungarian.h"
#include "assignment.h"

#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

int** solve_assignment_problem(Matrix costs){
    hungarian_problem_t p;
    fill_nan(costs, INFINITY, true);
    hungarian_init(&p, costs.M, (int)costs.h, (int)costs.w, HUNGARIAN_MODE_MINIMIZE_COST);
    hungarian_solve(&p);
    int ** assignment = (int **)malloc(costs.h * sizeof(int*));
    for(int i=0; i<costs.h; i++){
        assignment[i] = (int *)malloc(costs.w * sizeof(int));
        for(int j=0; j<costs.w; j++){
            assignment[i][j] = p.assignment[i][j];
        }
    }
    hungarian_free(&p);
    return assignment;
}