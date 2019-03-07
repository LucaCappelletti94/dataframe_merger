//
// Created by Luca Cappelletti on 2019-03-04.
//

#ifndef UNTITLED_THRESHOLD_H
#define UNTITLED_THRESHOLD_H

#include <stdbool.h>
#include "matrix.h"

Matrix** threshold(Matrix** matrices_groups, int matrices_number, int groups_number, double* known_negatives_percentages, bool inplace);
#endif //UNTITLED_THRESHOLD_H
