#include "mex.h"

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {
    if(nrhs==0) {
         mexPrintf("Hello, World!\n");
    }
    if(nrhs==1) {
        if (!mxIsChar(prhs[0])) {
        mexErrMsgIdAndTxt("helloworld:notString", "Input must be a string.");
        }
    
        // Get the input string
        char *inputString = mxArrayToString(prhs[0]);
        if (inputString == nullptr) {
            mexErrMsgIdAndTxt("helloworld:conversionFailed", "String conversion failed.");
        }
    
        // Print "Hello, <name>"
        mexPrintf("Hello, %s!\n", inputString);
    }
}

