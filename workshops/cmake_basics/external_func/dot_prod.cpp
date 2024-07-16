double dot_prod(double* v1, double* v2, int length){
    double sum = 0;
    for (int i=0;i<length;i++){
        sum +=v1[i]*v2[i];
    }
    return sum;
}