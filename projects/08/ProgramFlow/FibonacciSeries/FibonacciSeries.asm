//push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 1
@SP
AM=M-1
D=M
@4
M=D

//push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop that 0
@THAT
D=M
@0
D=D+A
@SP
A=M
M=D
@SP
A=M-1
D=M
@SP
A=M
A=M
M=D
@SP
M=M-1

//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop that 1
@THAT
D=M
@1
D=D+A
@SP
A=M
M=D
@SP
A=M-1
D=M
@SP
A=M
A=M
M=D
@SP
M=M-1

//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

//pop argument 0
@ARG
D=M
@0
D=D+A
@SP
A=M
M=D
@SP
A=M-1
D=M
@SP
A=M
A=M
M=D
@SP
M=M-1

//label MAIN_LOOP_START
(fn$MAIN_LOOP_START)

//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@fn$COMPUTE_ELEMENT
D;JNE


//goto END_PROGRAM
@fn$END_PROGRAM
0;JMP

//label COMPUTE_ELEMENT
(fn$COMPUTE_ELEMENT)

//push that 0
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push that 1
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M

//pop that 2
@THAT
D=M
@2
D=D+A
@SP
A=M
M=D
@SP
A=M-1
D=M
@SP
A=M
A=M
M=D
@SP
M=M-1

//push pointer 1
@3
D=A
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M

//pop pointer 1
@SP
AM=M-1
D=M
@4
M=D

//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

//pop argument 0
@ARG
D=M
@0
D=D+A
@SP
A=M
M=D
@SP
A=M-1
D=M
@SP
A=M
A=M
M=D
@SP
M=M-1

//goto MAIN_LOOP_START
@fn$MAIN_LOOP_START
0;JMP

//label END_PROGRAM
(fn$END_PROGRAM)

