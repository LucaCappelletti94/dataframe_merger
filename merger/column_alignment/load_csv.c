#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <stdbool.h>
#include "csvparser.h"
#include "load_csv.h"

int get_rows_number(char *path){
    CsvParser *csvparser = CsvParser_new(path, ",", 1);
    int n;
    for (n = 0 ; CsvParser_getRow(csvparser); n++);
    CsvParser_destroy(csvparser);
    return n;
}

int get_columns_number (char *path){
    CsvParser *csvparser = CsvParser_new(path, ",", 1);
    CsvRow *row = CsvParser_getRow(csvparser);
    int columns_number = CsvParser_getNumFields(row) - 1;
    CsvParser_destroy_row(row);
    CsvParser_destroy(csvparser);
    return columns_number;
}

bool is_empty(const char *string){
    return string[0] == '\0';
}

Matrix init_matrix(char *path){
    Matrix matrix;
    matrix.h = get_rows_number(path);
    matrix.w = get_columns_number(path);
    matrix.M = (double **)malloc(matrix.h * sizeof(double*));
    for(int i = 0; i < matrix.h; i++) matrix.M[i] = (double *)malloc(matrix.w * sizeof(double));
    return matrix;
}

Matrix load_csv(char* path){
    CsvParser *csvparser = CsvParser_new(path, ",", 1);
    Matrix matrix = init_matrix(path);
    for(int i=0; i<matrix.h; i++) {
        CsvRow *row = CsvParser_getRow(csvparser);
        const char **rowFields = CsvParser_getFields(row);
        for (int j = 0; j < matrix.w; j++) {
            matrix.M[i][j] = is_empty(rowFields[j+1]) ? NAN:strtod(rowFields[j+1], NULL);
        }
        CsvParser_destroy_row(row);
    }
    CsvParser_destroy(csvparser);
    return matrix;
}