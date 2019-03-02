typedef struct matrix {
    int h;
    int w;
    double **M;
} Matrix;

Matrix load_csv(char* path);