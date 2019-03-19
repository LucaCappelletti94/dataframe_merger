//
// Created by Luca Cappelletti on 2019-03-07.
//

#ifndef UNTITLED_DOUBLE_H_H
#define UNTITLED_DOUBLE_H_H


#include <math.h>
#include <stdio.h>
#include <stdlib.h>


int is_nan(double value);
int is_infinite(double value);
int is_not_nan(double value);
int is_not_infinite(double value);
double max(double a, double b);
double min(double a, double b);
char* double_to_str(double value);
double nan_compare(double a, double b, double (*compare)(double, double));
double nan_min(double a, double b);
double nan_max(double a, double b);
double min_max_norm(double value, double min, double max);
double in_range(double value, double min, double max);
void print_2d_double_array(double** M, int h, int w);

#endif //UNTITLED_DOUBLE_H_H
