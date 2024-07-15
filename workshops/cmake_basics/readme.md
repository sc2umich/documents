# Part 0: Prerequisites

### Have CMAKE Installed

[Install here](https://cmake.org/download/)

### Have Git Installed
If you are using MacOS or Linux, it is probably already installed.

[Install here](https://git-scm.com/)

### Have a C++ Compiler iInstalled
If you are using MacOS or Linux, it is probably already installed.

For windows, you can use visual studio's compiler, or emulate a another

- [w64devkit](https://github.com/skeeto/w64devkit/releases) (This is what I have)
- [cygwin64](https://cygwin.com/)

If you are relying on visual studio, it can be difficult to use from the command line.


# Part 1: Look at someone else's CMAKE:

In this part of the workshop, we will use cmake to configure blender before compiling from scratch.

git clone https://projects.blender.org/blender/blender.git


# Part 2: Life without CMAKE
### compile a simple program

We will create a simple program that computes the dot product of two vectors

$$
\left[\begin{array}{c c c}
    1 &2 &3
\end{array}\right]*\left[\begin{array}{c}
    2\\4\\6
\end{array}\right]=28
$$

We will begin by defining our main function and declaring some variables we will need. This script will be in the `simple` folder and we will name it `fun_math.cpp`

    int main(){
        int length = 3;
        double* vec1 = new double [3];
        double* vec2 = new double [3];
        return 0;
    }

Then, we can fill in the values for our vectors

    for (int i=0;i<length;i++){
        vec1[i]=(double)i+1;
        vec2[i]=((double)i+1)*2;
    }

Next, we can write a function to compute a dot product:
    double dot_prod(double* v1, double* v2, int length){
        double sum = 0;
        for (int i=0;i<length;i++){
            sum +=v1[i]*v2[i];
        }
        return sum;
    }

Finally, we can return the output so we know its working:
    #include <iostream>
    std::cout << result <<std::endl;

This can be simply compiled from the root directory:

    g++ ./simple/fun_math.cpp -o fun_math

Now we can run it

    ./simple/fun_math.exe
### Put function in separate file
The previous example works well for when the program is simple, but when there are multiple functions, it is better to split them into multiple scripts. We will do this for our dot product function. In a folder named `external_func`, create a file called `dot_prod.cpp`, then copy the function into it. our old `main` function into a new file as well in this folder. We can name it `fun_math_lib.cpp`. `fun_math_lib.cpp` should look like this

    #include <iostream>

    int main(){
        int length = 3;
        double* vec1 = new double [3];
        double* vec2 = new double [3];
        for (int i=0;i<length;i++){
            vec1[i]=(double)i+1;
            vec2[i]=((double)i+1)*2;
        }
        double result = dot_prod(vec1,vec2,length);
        std::cout << result;
        return 0;
    }

and `dot_prod.cpp` should look like this

    double dot_prod(double* v1, double* v2, int length){
        double sum = 0;
        for (int i=0;i<length;i++){
            sum +=v1[i]*v2[i];
        }
        return sum;
    }

We are still calling dot_prod ino our main function, but the function is no longer defined in that script. We will have to tell the compiler what that function looks like. The main way of doing this is with header files. Lets create a header file named `dot_prod.hpp`:

    double dot_prod(double* v1, double* v2, int length);

Then we add `#include "dot_prod.hpp` into one of the top lines of our main file.

Now our project is organized into two nice files. To compile, we need to tell the compiler about both of them.

    g++ ./external_func/fun_math_lib.cpp ./external_func/dot_prod.cpp -o fun_math

You can see how this starts to get difficult when you have more files. Run the file to make sure it works.
### Put function in library

You will likely need to incorporate an external library into your project at some point. One common example is a library called BLAS, which gives a bunch of linear algebra subroutines. So instead of having to write a dot product (for exmaple) function ourselves, we can use the one in the library. A library is essentially a big collection of those function scripts. 

Instead of using the BLAS library, we will turn our function script into a library. In a new folder called `library`, copy all the scripts from our previous folder. First, we will need to make an "object" file from our function script

    g++ -c ./library/dot_prod.cpp -0 ./library/dot_prod

Then, we can turn this object file into a library using ar

    ar rvs ./library/dot_prod.a ./library/dot_prod.o

usually, you would put many object files into a library. To compile our main function with the library, we can run

    g++ ./library/fun_math_lib.cpp -L./library/ -l:dot_prod.a -o fun_math

Typically in project, you'll want to use many libraries, so we need a good way to keep track of them and our supporting scripts. This brings us to CMAKE
# Part 3: Introducing CMAKE
### Just the basics
To start using cmake, we will go back to our simple folder and begin with the basics. cmake is driven from instructions located in `CMakeLists.txt` files. First, we will create one of these files in our `simple` folder. There are three main items needed in this file, as shown below:

    cmake_minimum_required(VERSION 3.20)

    project(fun_math VERSION 0.1.0 LANGUAGES CXX)

    add_executable(fun_math fun_math.cpp)

Once we add these to our `CMakeLists.txt` file, we are pretty much ready to use cmake. First let us create a build directory. Cmake creates a lot of files and you dont want them to pollute your working area.

    mkdir build
    cd build

Now we can run cmake, the first argument of the command is the directory where the `CMakeLists.txt` is located

    cmake ..\simple

Depending on how your system is set up, a few things could have happened. If you are on windows, a bunch of visual studio files were probably created. If you are on linux or mac, make files were probably created. These are both files for your "build system" They explain the configuration of your project and everything needed to run. They are basically scripts that will compile your code for you. An easy way to run them is by using

    cmake --build .

This will create your fun_math executable. The location of it may vary. For me, I have to run

    ./Debug/fun_math.exe

### Filling out more detail

Now we will get more into the things you can specify. For starters, you can specify the minimum version of C++

    set(CMAKE_CXX_STANDARD 11)
    set(CMAKE_CXX_STANDARD_REQUIRED True)

You can also define many complier options, such as how much optimization you want or which compiler flags to use. For example,

    set(CMAKE_CXX_COMPILER \path\to\compiler)

[warning](https://stackoverflow.com/questions/45933732/how-to-specify-a-compiler-in-cmake)

### Incorporating source code libraries

We can also specify c++ files that we want to include as libraries. Lets copy our current `CMakeLists.txt` file to the `external_func` folder and add the following lines.

    add_library(dot_prod dot_prod.cpp)
    target_link_libraries(fun_math PUBLIC dot_prod)
    target_include_directories(fun_math PUBLIC "${PROJECT_SOURCE_DIR}")

Breaking this down, the `add_library` command tells cmake that we want to make a library out of the `dot_prod.cpp` file. This is similar to how we made a library with the `ar` command. The `target_link_libraries` command tells cmake to link in that library when compiling the fun_math target. Since we created the library in the line above, cmake knows were to look for the library. Finally, the `target_include_directories` tells cmake where to look for our header files, since it will not know that by default. Conveniently, CMake has special variables to refer to special parts of your project directory. `"${PROJECT_SOURCE_DIR}"` refers to the directory where the `project` function was last called.

It is worth noting that while we have all these files in the same directory, it is customary to separate library, header, and main files into their own directories. see [here](https://github.com/bloomberg/bde/wiki/Home/3479ade9835be24db1a8cb8eeba3033e781db46b) if you are curious.

Now lets test out our new cmake file. First clear out the contents of our last build. For powershell, we can use

    rm *

Then

    cmake ../external_func
    cmake --build .
    ./Debug/fun_math.exe

### Incorporating already built libraries

From what I have seen, the most common incorporation of external libraries is by the previous method, or by using the `find_package`, which we wont get into. However, there is another way to incorporate static libraries like the one we have already created. Lets copy our current `CMakeLists.txt` file to the `library` folder and add the following lines.

    target_link_libraries(fun_math "${CMAKE_SOURCE_DIR}/dot_prod.a")

remove these lines

    add_library(dot_prod dot_prod.cpp)
    target_link_libraries(fun_math PUBLIC dot_prod)

Now, instead of creating a library then adding it to the library, we are just simply adding one that has already been created. There is a [catch](https://stackoverflow.com/a/66516012) to this though. The compiler we used to create the library likely has to be the same compiler used by cmake or else the linking will fail. Now, I will get to show you what it looks like to use makefiles as the build system instead of visual studio's system. First, clean out the build folder like last time. If you have mingw64 gnu compilers, you can type:

    cmake -G "MinGW Makefiles" ..\library

If you have another version on windows, you will need to use a different argument. If you are on linux or mac, you probably dont need an argument at all. You also might get an error and notification about viruses on windows. Windows detects executables being copied by cmake and deletes them, causing the errors and notifications. When this happens, I run the command again without errors. If we look at our build folder now, it is much cleaner. To build the project, we can simply type:

    make
    .\fun_math.exe

# Part 4: Changing functionality with compile definitions

Finally, we can change how our program runs based on what happens in CMake.

For example, you might want to use `find_package` to see if a certain library is available. If it isn't, you change your source code to use homemade functions instead of those provided by the library.

    find_package(BLAS)
     
    if (BLAS_FOUND) 
    add_compile_definitions(BLAS_FOUND=1)
    else ()
    add_compile_definitions(BLAS_FOUND=0)
    endif()

Then in the source code or headers

    #if BLAS_FOUND
    #include <cblas.h>
    #else
    #include <dot_prod.hpp>
    #endif

You would then need to add similar branching statements to you function calls or make both functions have the same interface.


