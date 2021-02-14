//function SimpleFunction.test 2
//function f m
(SimpleFunction.test)
@2
D=A
@SimpleFunction.test.m
M=D
(SimpleFunction.vm_L1)
@SimpleFunction.test.m
D=M
@SimpleFunction.vm_L0
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@SimpleFunction.test.m
M=M-1
@SimpleFunction.vm_L1
0;JMP
(SimpleFunction.vm_L0)


//push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push local 1
@LCL
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

//not
@SP
A=M
A=A-1
M=!M

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

//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M

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

//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

//return
//frame = LCL
@LCL
D=M
@fn.frame
M=D
//ret = *(frame-5)
@fn.frame
D=M
@5
D=D-A
A=D
D=M
@fn.ret
M=D
// *ARG = pop()
@SP
AM=M-1
D=M
@ARG
A=M
M=D
// SP = ARG+1
@ARG
D=M+1
@SP
M=D
// THAT=*(frame-1)
@fn.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@fn.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@fn.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@fn.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@fn.ret
A=M
0;JMP


