
# Project: [Numeric Matrix Processor](https://hyperskill.org/projects/96)

## Stage 1: Addition

### Objectives

In this stage, you should write a program that:
 1. Reads matrix **A** from the input.
 2. Reads matrix **B** from the input.
 3. Outputs their sum if it is possible to add them. Otherwise, 
    it should output the `ERROR` message.

Each matrix in the input is given in the following way: the first line 
contains the number of rows ***n*** and the number of columns ***m***. 
Then ***n*** lines follow, each containing ***m*** integers representing 
one row of the matrix.

Output the result in the same way but don't print the dimensions of the 
matrix.


## Stage 2: Multiplication by number

### Objectives

Write a program that reads a matrix and a constant and outputs 
the result of their multiplication.


## Stage 3: Matrix by matrix multiplication 

 - [x] [3Blue1Brown: Essence of linear algebra (15 chapters)][Essence of linear algebra]

### Objectives

Write a program that does the following:
 1. Prints a menu consisting of 4 options and reads the user's choice.
 2. Reads all data (matrices, constants) needed to perform the chosen 
    operation.
 3. Calculates the result and outputs it.
 4. Repeats all these steps until the `"Exit"` option is chosen.


## Stage 4: Transpose 

### Objectives
 1. Add an option to transpose matrices.
 2. If the user chooses this option, program should provide them with 4 
    types of transposition and ask them to choose one.
 3. Then it should read the matrix, transpose it, and output the result.


## Stage 5: Determined! 

 - [x] Youtube: [Minors and Cofactors][Matrices – Minors and Cofactors]

### Objectives
 1. Add support calculating the determinant of a matrix.


## Stage 6: Inverse matrix

 - [x] Youtube: [Inverse of a Matrix][]
 - [x] Youtube: [Inverse of a 2x2 Matrix using Adjoint][]
 - [x] Youtube: [Inverse of a 3x3 Matrix using Adjoint][]

### Objectives
 1. Add support finding the inverse of a matrix
 2. Implement a method that prints a matrix in a readable way so that 
    every column is correctly aligned and all elements are rounded 
    to a fixed number of digits.


[Essence of linear algebra]: https://www.youtube.com/watch?v=fNk_zzaMoSs&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
[Matrices – Minors and Cofactors]: https://www.youtube.com/watch?v=KMKd993vG9Q

[Inverse of a Matrix]: https://www.youtube.com/watch?v=AMLUikdDQGk
[Inverse of a 2x2 Matrix using Adjoint]: https://www.youtube.com/watch?v=HYWeEx21WWw
[Inverse of a 3x3 Matrix using Adjoint]: https://www.youtube.com/watch?v=xfhzwNkMNg4
