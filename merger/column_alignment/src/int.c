//
// Created by Luca Cappelletti on 2019-03-08.
//


#include <string.h>
#include "int.h"

char* int_to_str(int const value){
    int len = (int)((ceil(log10(value+1))+1)*sizeof(char));
    if (isinf(value) || value> 1000000000){
        len = 4;
    }
    if isnan(value) {
        len = 3;
    }
    char* str = (char*)malloc(len* sizeof(char));
    sprintf(str, "%d", value);
    return str;
}


void print_2d_int_array(int** M, int h, int w){
    size_t * max_sizes = (size_t*)malloc(w* sizeof(size_t));
    for(int i=0; i<w; i++){
        max_sizes[i] = 0;
        for(int j=0; j<h; j++){
            size_t e = strlen(int_to_str(M[j][i]));
            max_sizes[i] = e>max_sizes[i]?e:max_sizes[i];
        }
    }
    for(int i=0; i<h; i++){
        for(int j=0; j<w; j++){
            size_t e = strlen(int_to_str(M[i][j]));
            int padding = (int)(max_sizes[j] - e);
            if (j!=w-1){
                printf("%d,%.*s", M[i][j], padding+1, "                                             ");
            } else {
                printf("%d%.*s", M[i][j], padding, "                                             ");
            }

        }
        printf("\n");
    }
    printf("\n");
    free(max_sizes);
}