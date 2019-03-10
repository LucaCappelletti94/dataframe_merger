//
// Created by Luca Cappelletti on 2019-03-07.
//

#include "vector.h"

int any(int const* bools, int n){
    for (int i=0; i<n; i++){
        if (bools[i]){
            return 1;
        }
    }
    return 0;
}

int all(int const* bools, int n){
    for (int i=0; i<n; i++){
        if (!bools[i]){
            return 0;
        }
    }
    return 1;
}

double* doubles_to_vector(va_list al, size_t n, double arg){
    double* args = (double*)malloc(n* sizeof(double));
    args[0] = arg;
    for(int i=1; i<n; i++) {
        args[i] = va_arg(al, double);
    }
    return args;
}

int* double_vector_bool_callback(double* vector, size_t n, int(callback)(double)){
    int* results = (int*)malloc(n* sizeof(int));
    for (int i=0; i<n; i++){
        results[i] = callback(vector[i]);
    }
    return results;
}

int* vector_is_nan(double* vector, size_t n){
    return double_vector_bool_callback(vector, n, &is_nan);
}

int* vector_is_not_nan(double* vector, size_t n){
    return double_vector_bool_callback(vector, n, &is_not_nan);
}

int* el_is_nan(size_t n, double arg, ...){
    va_list al;
    va_start(al,arg);
    return vector_is_nan(doubles_to_vector(al, n, arg), n);
}

int* el_is_not_nan(size_t n, double arg, ...){
    va_list al;
    va_start(al,arg);
    return vector_is_not_nan(doubles_to_vector(al, n, arg), n);
}