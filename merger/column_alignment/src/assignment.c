#include "hungarian/hungarian.h"
#include "assignment.h"
#include "int.h"

#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <printf.h>

int** problem_result_to_integer_matrix(hungarian_problem_t p, Matrix costs){
    int ** assignment = (int **)malloc(p.num_rows * sizeof(int*));
    for(int i=0; i<p.num_rows; i++){
        assignment[i] = (int *)malloc(p.num_cols * sizeof(int));
        for(int j=0; j<p.num_cols; j++){
            assignment[i][j] = isinf(costs.M[i][j])?0:p.assignment[i][j];
        }
    }
    return assignment;
}

int** solve_assignment_problem(Matrix costs){
    hungarian_problem_t p;
    Matrix hungarian_costs = fill_nan(costs, HUNGARIAN_INFINITY, false);
    fill_nan(costs, INFINITY, true);
    hungarian_init(&p, hungarian_costs.M, (int)costs.h, (int)costs.w, HUNGARIAN_MODE_MINIMIZE_COST);
    hungarian_solve(&p);
    int ** assignment = problem_result_to_integer_matrix(p, costs);
    hungarian_free(&p);
    free_matrix(hungarian_costs);
    return assignment;
}

void free_assignemnt_groups(int**** assignments_groups, Matrix** costs_groups, int groups, int matrices){
    for(int i=0; i<groups; i++){
        for(int j=0; j<matrices; j++){
            for(int k=0; k<costs_groups[i][j].h; k++){
                free(assignments_groups[i][j][k]);
            }
            free(assignments_groups[i][j]);
        }
        free(assignments_groups[i]);
    }
    free(assignments_groups);
}

int**** solve_assignment_problems(Matrix** costs_groups, int groups, int matrices){
    int**** assignments_groups = (int****)malloc(groups* sizeof(int***));
    for(int i=0; i<groups; i++){
        assignments_groups[i] = (int***)malloc(matrices* sizeof(int**));
        for(int j=0; j<matrices; j++){
            assignments_groups[i][j] = solve_assignment_problem(costs_groups[i][j]);
        }
    }
    return assignments_groups;
}