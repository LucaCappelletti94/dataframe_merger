//
// Created by Luca Cappelletti on 2019-03-03.
//

#include "tarjan.h"
#include "canterbury/graphalg/sc.h"

dgraph_t* incidence_matrix_to_dgraph(int** incidence_matrix, int V){
    dgraph_t* graph= dgraph_blank(V);
    for(int i=0; i<V; i++){
        for(int j=0; j<V; j++){
            if(incidence_matrix[i][j]){
                add_new_edge(&graph->vertices[i], j, 1);
            }
        }
    }
    return graph;
}

int** tarjan_result_to_components(sc_result_t * result){

}

int** tarjan(int** incidence_matrix, int V){
    dgraph_t* graph = incidence_matrix_to_dgraph(incidence_matrix, V);
    sc_result_t* result = sc(graph, 0);
    int** components = tarjan_result_to_components(result);
    sc_result_free(result);
    dgraph_free(graph);
    return  components;
}