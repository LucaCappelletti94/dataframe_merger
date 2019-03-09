#include "double.h"
#include <math.h>

bool is_nan(double value){
    return value == NAN;
}

bool is_not_nan(double value){
    return !is_nan(value);
}

bool is_infinite(double value){
    return value == INFINITY;
}

bool is_not_infinite(double value){
    return !is_infinite(value);
}

bool tautology(double value){
    return true;
}

bool negation(double value){
    return false;
}

double max(double a, double b){
    return a>b?a:b;
}

double min(double a, double b){
    return a<b?a:b;
}

double in_range(double value, double min, double max){
    return value > min && value < max;
}

double nan_compare(double a, double b, double (*compare)(double, double)){
    if (is_nan(a)){
        return b;
    }
    if (is_nan(b)){
        return a;
    }
    return compare(a,b);
}

double nan_min(double a, double b){
    return nan_compare(a, b, &min);
}

double nan_max(double a, double b){
    return nan_compare(a, b, &max);
}

double min_max_norm(double value, double min, double max){
    return (value-min)/(max==0?1:max);
}