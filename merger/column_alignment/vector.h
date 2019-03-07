//
// Created by Luca Cappelletti on 2019-03-07.
//

#ifndef UNTITLED_VECTOR_H
#define UNTITLED_VECTOR_H

#include "double.h"
#include <stdlib.h>
bool* el_is_nan(size_t n, double arg, ...);
bool* el_is_not_nan(size_t n, double arg, ...);
bool any(bool const* bools, int n);
bool all(bool const* bools, int n);

#endif //UNTITLED_VECTOR_H
