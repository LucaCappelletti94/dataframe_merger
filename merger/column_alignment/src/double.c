
#include "double.h"

char* double_to_str(double const value){
    int len = (int)((ceil(log10(value+1))+1)*sizeof(char));
    if isinf(value) {
        len = 4;
    }
    if isnan(value) {
        len = 3;
    }
    char* str = (char*)malloc(len* sizeof(char));
    sprintf(str, "%f", value);
    return str;
}

int is_nan(double value){
    return isnan(value);
}

int is_infinite(double value){
    return isinf(value);
}

int is_not_nan(double value){
    return !isnan(value);
}

int is_not_infinite(double value){
    return !isinf(value);
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
    if (isnan(a)){
        return b;
    }
    if (isnan(b)){
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