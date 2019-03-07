//
// Created by Luca Cappelletti on 2019-03-04.
//

#ifndef UNTITLED_THRESHOLD_H
#define UNTITLED_THRESHOLD_H

#include <stdbool.h>
#include "matrix.h"
void threshold(Matrix const** self_matrices_groups, size_t self_matrices_number, Matrix** other_matrices_groups, size_t other_matrices_number, size_t groups_number, double const* known_negatives_percentages);
#endif //UNTITLED_THRESHOLD_H
