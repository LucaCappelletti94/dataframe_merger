//
// Created by Luca Cappelletti on 2019-03-07.
//

#ifndef UNTITLED_VECTOR_H
#define UNTITLED_VECTOR_H

#include "double.h"
#include <stdarg.h>
#include <stdlib.h>

int* el_is_nan(size_t n, double arg, ...);
int* el_is_not_nan(size_t n, double arg, ...);
int* vector_is_nan(double* vector, size_t n);
int any(int const* bools, int n);
int all(int const* bools, int n);

#endif //UNTITLED_VECTOR_H
