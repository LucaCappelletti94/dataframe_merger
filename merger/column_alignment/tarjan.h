//
// Created by Luca Cappelletti on 2019-03-03.
//

#ifndef UNTITLED_TARJAN_H
#define UNTITLED_TARJAN_H

#include "matrix.h"

int*** determine_group_connected_components(Matrix* groups, int groups_number, int* components);
void free_group_connected_components(int*** group_connected_components, int groups_number, int const* components);

#endif //UNTITLED_TARJAN_H
