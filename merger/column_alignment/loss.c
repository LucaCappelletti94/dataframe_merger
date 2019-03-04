//
// Created by Luca Cappelletti on 2019-03-03.
//

#include <stdbool.h>
#include <math.h>
#include "loss.h"

double loss(bool* y_pred,bool* y_true, int n){
    double loss = 0;
    for(int i=0; i<n; i++){
        loss += y_true[i]!=y_pred[i];
    }
    return loss;
}