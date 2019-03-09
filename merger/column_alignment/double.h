//
// Created by Luca Cappelletti on 2019-03-07.
//

#ifndef UNTITLED_DOUBLE_H_H
#define UNTITLED_DOUBLE_H_H

#include <stdbool.h>

bool is_nan(double value);
bool is_not_nan(double value);
bool is_infinite(double value);
bool is_not_infinite(double value);
bool tautology(double value);
bool negation(double value);
double max(double a, double b);
double min(double a, double b);
double nan_compare(double a, double b, double (*compare)(double, double));
double nan_min(double a, double b);
double nan_max(double a, double b);
double min_max_norm(double value, double min, double max);
double in_range(double value, double min, double max);


#endif //UNTITLED_DOUBLE_H_H
