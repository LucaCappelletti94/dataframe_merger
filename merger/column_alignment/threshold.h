//
// Created by Luca Cappelletti on 2019-03-04.
//

#ifndef UNTITLED_THRESHOLD_H
#define UNTITLED_THRESHOLD_H

#include <stdbool.h>
#include "matrix.h"
void threshold(Matrix ** self_matrices_groups, int self_matrices_number, Matrix** other_matrices_groups, int other_matrices_number, int groups_number, double const* known_negatives_percentages);
#endif //UNTITLED_THRESHOLD_H
