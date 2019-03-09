//
// Created by Luca Cappelletti on 2019-03-08.
//


#include "int.h"

char* int_to_str(int const value){
    char* str = (char*)malloc((int)((ceil(log10(value))+1)*sizeof(char))* sizeof(char));
    sprintf(str, "%d", 42);
    return str;
}