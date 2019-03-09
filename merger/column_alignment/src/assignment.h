//
// Created by Luca Cappelletti on 2019-03-07.
//

#ifndef ASSIGNMENT_H
#define ASSIGNMENT_H

#include <stdbool.h>

#include "matrix.h"
int**** solve_assignment_problems(Matrix** costs_groups, int groups, int matrices);
void free_assignemnt_groups(int**** assignments_groups, Matrix** costs_groups, int groups, int matrices);

#endif //ASSIGNMENT_H

