//bootstrap
//SP=256
@256
D=A
@SP
M=D
@LCL
D=-A
M=D
@ARG
D=-A
M=D
@THIS
D=-A
M=D
@THAT
D=-A
M=D

//call Sys.init 0
//call f n
//push return address
@__bootstrap___L0
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
@0
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
//@f
@Sys.init
0;JMP
(__bootstrap___L0)

//function Main.fibonacci 0
//function f m
(Main.fibonacci)
@0
D=A
@Main.fibonacci.m
M=D
(Main.vm_L2)
@Main.fibonacci.m
D=M
@Main.vm_L1
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Main.fibonacci.m
M=M-1
@Main.vm_L2
0;JMP
(Main.vm_L1)


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

//lt
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@Main.vm_L3
D;JLT
D=0
@Main.vm_L4
0;JMP
(Main.vm_L3)
D=-1
(Main.vm_L4)
@SP
A=M
A=A-1
M=D

//if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE


//goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP

//label IF_TRUE
(Main.fibonacci$IF_TRUE)

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

//return
//frame = LCL
@LCL
D=M
@Main.fibonacci.frame
M=D
//ret = *(frame-5)
@Main.fibonacci.frame
D=M
@5
D=D-A
A=D
D=M
@Main.fibonacci.ret
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
@Main.fibonacci.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@Main.fibonacci.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@Main.fibonacci.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@Main.fibonacci.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@Main.fibonacci.ret
A=M
0;JMP


//label IF_FALSE
(Main.fibonacci$IF_FALSE)

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

//call Main.fibonacci 1
//call f n
//push return address
@Main.vm_L5
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
@1
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
//@f
@Main.fibonacci
0;JMP
(Main.vm_L5)

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

//call Main.fibonacci 1
//call f n
//push return address
@Main.vm_L6
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
@1
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
//@f
@Main.fibonacci
0;JMP
(Main.vm_L6)

//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M

//return
//frame = LCL
@LCL
D=M
@Main.fibonacci.frame
M=D
//ret = *(frame-5)
@Main.fibonacci.frame
D=M
@5
D=D-A
A=D
D=M
@Main.fibonacci.ret
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
@Main.fibonacci.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@Main.fibonacci.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@Main.fibonacci.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@Main.fibonacci.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@Main.fibonacci.ret
A=M
0;JMP


//function Sys.init 0
//function f m
(Sys.init)
@0
D=A
@Sys.init.m
M=D
(Sys.vm_L8)
@Sys.init.m
D=M
@Sys.vm_L7
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Sys.init.m
M=M-1
@Sys.vm_L8
0;JMP
(Sys.vm_L7)


//push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Main.fibonacci 1
//call f n
//push return address
@Sys.vm_L9
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
@1
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
//@f
@Main.fibonacci
0;JMP
(Sys.vm_L9)

//label WHILE
(Sys.init$WHILE)

//goto WHILE
@Sys.init$WHILE
0;JMP

