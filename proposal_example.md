# SC2 Project Proposal
Project Name: automatic-differentiation-library-1
## Background
Machine learning and artificial intelligence has become very prevelant recently thanks to an increase in data, an increase in computational power, and improvement in optimization methods. Deep neural networks are the basis for many popular models like chatGPT and stable diffusion models. To train these models the error from predictions must be back-propagated throughout the model. This requires the derivative of each of the millons of parameters in a deep neural network to be taken with respect to the error. Computing the derivative analytically for each weight and bias would be intractable. Thus, one of the revolutional algorithms that made deep learning much more feasible was automatic differentiation. An algorithm that could algorithmically compute the value of each weigth and bias's derivative. In fact, automatic differentiation is one of the main features of popular machine learning libraries, like tensorflow or pytorch. 

In general, the algorithm works by adding and multiplying special objects instead of plain integers or floats. In doing this, each object can keep track of the one that came before it and what operation was used. By programming basic derivative rules, derivative values can be propagated backwards starting from the loss and ending at the beginning weights and biases.

This project would begin to create the mathematical objects required for automatic differentiation and implement the addition and multiplication routines. This project will be implemented in C++

This guide is helpful

https://towardsdatascience.com/build-your-own-automatic-differentiation-program-6ecd585eec2a

## Duration
I plan for this project to take one month

## Example Tasks
1. Create a "Tensor" object: the basis of this algorithm are special objects that can trace where they came from. This task will focus on creating these objects and defining the attributes they would required.

2. add the addition operation to the tensor object: we will need to specify what happens when two "Tensor" operations are added together. It will likely include producing a new "Tensor" object which has pointers to the tensors that were added together.

3. Create an automatic differentiation example to show to the club: We will create an example of a function with many additions and multiplications and compute its derivative's values.

## Extra Resourses Required
This project requires no extra resourses