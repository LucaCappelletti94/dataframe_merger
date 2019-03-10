//
// Created by Luca Cappelletti on 2019-03-03.
//

#include <stdlib.h>
#include <limits.h>
#include <printf.h>
#include "tarjan.h"
#include "canterbury/graphalg/sc.h"
#include "double.h"

dgraph_t* incidence_matrix_to_dgraph(Matrix incidence_matrix){
    dgraph_t* graph= dgraph_blank((int)incidence_matrix.h);
    for(int i=0; i<incidence_matrix.h; i++){
        for(int j=0; j<incidence_matrix.h; j++){
            if(is_not_infinite(incidence_matrix.M[i][j])){
                long distance = (long)(incidence_matrix.M[i][j]*LONG_MAX);
                add_new_edge(&graph->vertices[i], j, distance);
            }
        }
    }
    return graph;
}

int** tarjan_result_to_components(sc_result_t * result, int* component_number, int** components_elements){
    int** components = (int **)malloc(result->n_sets * sizeof(int*));
    *components_elements = (int *)malloc(result->n_sets * sizeof(int));
    *component_number = result->n_sets;
    for(int i=0; i<result->n_sets; i++){
        components[i] = (int *)malloc((result->sets_f[i] - result->sets_s[i]+1) * sizeof(int));
        (*components_elements)[i] = result->sets_f[i] - result->sets_s[i]+1;
        for(int j=result->sets_s[i], k=0; j<=result->sets_f[i]; j++, k++){
            components[i][k] = result->vertices[j];
        }
    }
    return components;
}

int** determine_connected_components(Matrix incidence_matrix, int* component_number, int** components_elements){
    dgraph_t* graph = incidence_matrix_to_dgraph(incidence_matrix);
    sc_result_t* result = sc(graph, 0);
    int** components = tarjan_result_to_components(result, component_number, components_elements);
    sc_result_free(result);
    dgraph_free(graph);
    return components;
}

void free_group_connected_components(int*** group_connected_components, int groups_number, int const* components){
    for(int i=0; i<groups_number; i++){
        for(int j=0; j<components[i]; j++){
            free(group_connected_components[i][j]);
        }
        free(group_connected_components[i]);
    }
    free(group_connected_components);
}

int*** determine_group_connected_components(Matrix* groups, int groups_number, int* components_number, int** components_elements_number){
    int*** group_connected_components = (int***)malloc(groups_number* sizeof(int**));
    for(int i=0; i<groups_number; i++){
        group_connected_components[i] = determine_connected_components(groups[i], &components_number[i], &components_elements_number[i]);
    }
    return group_connected_components;
}