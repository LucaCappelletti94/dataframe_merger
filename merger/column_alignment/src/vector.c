//
// Created by Luca Cappelletti on 2019-03-07.
//

#include "vector.h"
#include <stdarg.h>

bool any(bool const* bools, int n){
    for (int i=0; i<n; i++){
        if (bools[i]){
            return true;
        }
    }
    return false;
}

bool all(bool const* bools, int n){
    for (int i=0; i<n; i++){
        if (!bools[i]){
            return false;
        }
    }
    return true;
}

double* doubles_to_vector(va_list al, size_t n, double arg){
    double* args = (double*)malloc(n* sizeof(double));
    args[0] = arg;
    for(int i=1; i<n; i++) {
        args[i] = va_arg(al, double);
    }
    return args;
}

bool* double_vector_bool_callback(double* vector, size_t n, bool(callback)(double)){
    bool* results = (bool*)malloc(n* sizeof(bool));
    for (int i=0; i<n; i++){
        results[i] = callback(vector[i]);
    }
    return results;
}

bool* vector_is_nan(double* vector, size_t n){
    return double_vector_bool_callback(vector, n, &is_nan);
}

bool* vector_is_not_nan(double* vector, size_t n){
    return double_vector_bool_callback(vector, n, &is_not_nan);
}

bool* el_is_nan(size_t n, double arg, ...){
    va_list al;
    va_start(al,arg);
    return vector_is_nan(doubles_to_vector(al, n, arg), n);
}

bool* el_is_not_nan(size_t n, double arg, ...){
    va_list al;
    va_start(al,arg);
    return vector_is_not_nan(doubles_to_vector(al, n, arg), n);
}