//
// Created by Luca Cappelletti on 2019-03-07.
//

#include "utils.h"

size_t matrices_number_from_datasets(size_t datasets){
    size_t sum=0;
    for (size_t i=0; i<datasets; i++, sum+=i);
    return sum;
}