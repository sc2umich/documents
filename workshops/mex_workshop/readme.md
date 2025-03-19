# Step 0: Prerequisites

### MATLAB 64-bit 2023a or newer
If you have an older version (2017a or newer) or a different OS you can still work with MEX files, but you will need to manually configure your compiler.

-For Windows OS with older versions of MATLAB, see the information in the MinGW-w64 Add On page linked below.
-For other OS, see the information linked [here](https://www.mathworks.com/support/requirements/supported-compilers-mac.html)

### Install MinGW-w64 Support from Add-On Explorer
[MinGW-w64 Add-On](https://www.mathworks.com/matlabcentral/fileexchange/52848-matlab-support-for-mingw-w64-c-c-fortran-compiler?s_tid=srchtitle_support_results_1_mingw64)
If you have issues, try launching MATLAB with administrator privileges.

Simply click "Install" in the upper right of the download page and the compiler will automatically configure itself. This may take a few minutes.

Here is a [link](https://www.mathworks.com/help/matlab/matlab_external/integrate-matlab-with-external-programming-languages-and-systems.html) to an overview of using external languages with MATLAB (includes both compiled and runtime use cases).


# Step 1: Write your code in the language of your choice

MEX files can be created from C,C++, or FORTRAN files. C++ is generally recommended over C, but to keep our example simple we will use C.

[C](https://www.mathworks.com/help/matlab/cc-mx-matrix-library.html)

[C++](https://www.mathworks.com/help/matlab/cpp-mex-file-applications.html)

[FORTRAN](https://www.mathworks.com/help/matlab/call-mex-fortran.html)

Here is our [example C file](./hello.cpp)

 ```c
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

```

With the C API, we simply need a function called "mexFunction". The inputs for the function are

	nlhs: The number of returned objects by our MATLAB function
	plhs: The pointers to the returned objects of the MATLAB function
	nrhs: The number of inputs being passed to the function in MATLAB
	prhs: The pointers to the inputs we pass the MATLAB function

Here's what the code does:

First, if no inputs are given, say "Hello World!"


```c
	if(nrhs==0) {
        	 mexPrintf("Hello, World!\n");
    	}
```

If an input is provided, make sure it has the char type and not a null pointer. Then, greet our new friend!

```c
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

```


Notice we can print directly to the MATLAB console from our MEX file as well as throw errors inside MATLAB. If we want to return a value, the method is similar to how we handled the inputs.

If you want to include outputs, the process is similar to the way we handled inputs. First, you would create the object to return and then assign the variable plhs[i] that object as a value. The links above have several useful examples covering how to handle inputs, different data types, and many other common situations.

# Step 2: Compiling your code
To compile hello.cpp into a MEX file, we will need to use the [mex](https://www.mathworks.com/help/matlab/ref/mex.html?s_tid=srchtitle_site_search_1_mex) command. For our simple example, if hello.cpp is in your working directory or on your MATLAB path, you can use type the following into your MATLAB terminal: 

```
    mex hello.cpp
```
This will compile hello.cpp and create a file called "hello.mexw64". 

Our example is pretty simple. For a realistic project, you might need to use compiler flags. For example, if you type

```
mex hello.cpp -output "greeting"
```
then the MEX file will instead be called "greeting.mexw64". See the mex documentation linked about for the full list of supported compiler options.

# Step 3: Calling your code

From here, as long as the compiled file is in your current working directory or the MATLAB path, you can use it just like any other MATLAB command. Let's try out a few different cases:

```
hello()
hello('Alice')
hello(0)
```

