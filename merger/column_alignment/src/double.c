
#include <string.h>
#include "double.h"

char* double_to_str(double const value){
    int len = (int)((ceil(log10(value+1))+1)*sizeof(char));
    if isinf(value) {
        len = 4;
    }
    if isnan(value) {
        len = 3;
    }
    if (value==0) {
        len = 1;
    }
    char* str = (char*)malloc(len* sizeof(char));
    if (value==0) {
        sprintf(str, "%d", (int)value);
    } else {
        sprintf(str, "%f", value);
    }
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
    return (value-min)/((max-min)==0?1:max-min);
}

void print_2d_double_array(double** M, int h, int w){
    size_t * max_sizes = (size_t*)malloc(w* sizeof(size_t));
    for(int i=0; i<w; i++){
        max_sizes[i] = 0;
        for(int j=0; j<h; j++){
            size_t e = strlen(double_to_str(M[j][i]));
            max_sizes[i] = e>max_sizes[i]?e:max_sizes[i];
        }
    }
    for(int i=0; i<h; i++){
        for(int j=0; j<w; j++){
            size_t e = strlen(double_to_str(M[i][j]));
            int padding = (int)(max_sizes[j] - e);
            if (j!=w-1){
                printf("%f,%.*s", M[i][j], padding+1, "                                             ");
            } else {
                printf("%f%.*s", M[i][j], padding, "                                             ");
            }

        }
        printf("\n");
    }
    printf("\n");
    free(max_sizes);
}