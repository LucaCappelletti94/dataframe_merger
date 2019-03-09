//
// Created by Luca Cappelletti on 2019-03-03.
//

#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "column_alignment.h"
#include "load_csv.h"
#include "int.h"
#include "threshold.h"
#include "double.h"
#include "assignment.h"
#include "tarjan.h"

bool self_loading_rule(int i, int j){
    return i==j;
}

bool other_loading_rule(int i, int j){
    return i<j;
}

char* format_path(char* path, int metric, int df1, int df2){
    char* str_metric = int_to_str(metric);
    char* str_df1 = int_to_str(df1);
    char* str_df2 = int_to_str(df2);
    char* formatted_path = (char*)malloc((strlen(path)+strlen(str_metric)+strlen(str_df1)+strlen(str_df2)+7)* sizeof(char));
    snprintf(formatted_path, sizeof formatted_path, "%s/%s/%s-%s.csv", path, str_metric, str_df1, str_df2);
    free(str_metric);
    free(str_df1);
    free(str_df2);
    return formatted_path;
}

int matrices_number(int datasets, bool (*loading_rule)(int, int)){
    int matrices = 0;
    for (int i=0; i<datasets; i++){
        for (int j=0; j<datasets; j++){
            if (loading_rule(i,j)){
                matrices++;
            }
        }
    }
    return  matrices;
}

int self_matrices_number(int datasets){
    return matrices_number(datasets, &self_loading_rule);
}

int other_matrices_number(int datasets){
    return matrices_number(datasets, &other_loading_rule);
}

Matrix** load_groups(char* path, int metrics, int datasets, int matrices, bool (*loading_rule)(int, int)){
    Matrix** groups = (Matrix**)malloc(metrics* sizeof(Matrix*));
    for (int metric=0; metric<metrics; metric++){
        groups[metric] = (Matrix*)malloc(matrices* sizeof(Matrix));
        for (int df1=0, matrix=0; df1<datasets; df1++){
            for (int df2=0; df2<datasets; df2++){
                if (loading_rule(df1, df2)){
                    char* formatted_path = format_path(path, metric, df1, df2);
                    groups[metric][matrix++] = load_csv(formatted_path);
                    free(formatted_path);
                }
            }
        }
    }
    return groups;
}

Matrix** load_self_groups(char* path, int metrics, int datasets, int matrices){
    return load_groups(path, metrics, datasets, matrices, &self_loading_rule);
}

Matrix** load_other_groups(char* path, int metrics, int datasets, int matrices){
    return load_groups(path, metrics, datasets, matrices, &other_loading_rule);
}

void free_groups(Matrix** groups, int metrics, int datasets, bool (*loading_rule)(int, int)){
    for (int metric=0; metric<metrics; metric++){
        for (int df1=0, matrix=0; df1<datasets; df1++){
            for (int df2=0; df2<datasets; df2++){
                if (loading_rule(df1, df2)){
                    free_matrix(groups[metric][matrix++]);
                }
            }
        }
        free(groups[metric]);
    }
    free(groups);
}

void free_self_groups(Matrix ** groups, int metrics, int datasets){
    return free_groups(groups, metrics, datasets, &self_loading_rule);
}

void free_other_groups(Matrix ** groups, int metrics, int datasets){
    return free_groups(groups, metrics, datasets, &other_loading_rule);
}

Matrix* groups_nan_composition(Matrix** groups, double const* weights, int metrics, int matrices){
    Matrix* groups_composition = (Matrix *)malloc(matrices* sizeof(Matrix));
    for (int i=0; i<matrices; i++){
        groups_composition[i]=init_matrix_like(groups[0][i]);
        for (int j = 0; j < groups_composition[i].h; j++) {
            for (int k = 0; k < groups_composition[i].w; k++) {
                groups_composition[i].M[j][k] = 0;
                for (int metric = 0; metric < metrics; metric++) {
                    if(is_not_nan(groups[metric][i].M[j][k])){
                        groups_composition[i].M[j][k] += weights[i]*groups[metric][i].M[j][k];
                    }
                }
            }
        }
    }
    return groups_composition;
}


int** column_alignment(char* path, char* output, int datasets, int metrics, double const* known_negatives_percentages,  double const* weights){
    int self_matrices = self_matrices_number(datasets);
    int other_matrices = other_matrices_number(datasets);
    Matrix ** self_matrices_groups = load_self_groups(path, metrics, datasets, self_matrices);
    Matrix ** other_matrices_groups = load_other_groups(path, metrics, datasets, other_matrices);
    // Apply thresholds to matrices.
    // Values above thresholds are set to NAN, then matrices are max_min normalized in a NAN-aware fashion.
    threshold(self_matrices_groups, self_matrices, other_matrices_groups, other_matrices, metrics, known_negatives_percentages);
    // Build weighted matrices
    Matrix * groups_composition = groups_nan_composition(other_matrices_groups, weights, metrics, other_matrices);
    // Solve assignment problems using hungarian algorithm
    int*** composition_assignment = *solve_assignment_problems(&groups_composition, 1, other_matrices);
    int**** other_assignment = solve_assignment_problems(other_matrices_groups, metrics, other_matrices);
    // Build weighted adjacency matrix
    Matrix composition_adjacency_matrix = *groups_to_adjacency_matrix(&groups_composition, &composition_assignment, 1, other_matrices);
    Matrix* other_adjacency_matrix = groups_to_adjacency_matrix(other_matrices_groups, other_assignment, metrics, other_matrices);
    // Free assignments
    free_assignemnt_groups(&composition_assignment, &groups_composition, 1, other_matrices);
    free_assignemnt_groups(other_assignment, other_matrices_groups, metrics, other_matrices);
    // Run Tarjan on the weighted adjacency matrix
    int* composition_components_number = (int*)malloc(sizeof(int));
    int* other_components_number = (int*)malloc(metrics*sizeof(int));
    int** composition_connected_components = *determine_group_connected_components(&composition_adjacency_matrix, 1, composition_components_number);
    int*** other_connected_components = determine_group_connected_components(other_adjacency_matrix, metrics, other_components_number);
    // Free groups
    free_self_groups(self_matrices_groups, metrics, datasets);
    free_other_groups(self_matrices_groups, metrics, datasets);
    // Save and return the components

    // Free connected components
    free_group_connected_components(&composition_connected_components, 1, composition_components_number);
    free_group_connected_components(other_connected_components, metrics, other_components_number);
}