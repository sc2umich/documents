#include <iostream>
double dot_prod(double* v1, double* v2, int length){
    double sum = 0;
    for (int i=0;i<length;i++){
        sum +=v1[i]*v2[i];
    }
    return sum;
}
int main(){
    int length = 3;
    double* vec1 = new double [3];
    double* vec2 = new double [3];
    for (int i=0;i<length;i++){
        vec1[i]=(double)i+1;
        vec2[i]=((double)i+1)*2;
    }
    double result = dot_prod(vec1,vec2,length);
    std::cout << result <<std::endl;
    return 0;
}