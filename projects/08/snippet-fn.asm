//call f n=4
//push return address
@LXXX
D=A
@SP 
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - n - 5
@SP
D=M
//@n
@4
D=D-A
@5
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
@f
0;JMP
(LXXX)
@LXXX
0;JMP
//function f m=3:
(f)
@3
D=A
@f.m
M=D
(L2)
@f.m
D=M
@L1
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@f.m
M=M-1
@L2
0;JMP
(L1)
//push result
@5
D=A
@SP
A=M
M=D
@SP
M=M+1
//ret
//frame = LCL
@LCL
D=M
@f.frame
M=D
//ret = *(frame-5)
@f.frame
D=M
@5
D=D-A
A=D
D=M
@f.ret
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
@f.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@f.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@f.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@f.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@f.ret
A=M
0;JMP



