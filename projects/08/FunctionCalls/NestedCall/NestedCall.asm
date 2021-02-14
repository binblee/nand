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

//function Sys.init 0
//function f m
(Sys.init)
@0
D=A
@Sys.init.m
M=D
(Sys.vm_L2)
@Sys.init.m
D=M
@Sys.vm_L1
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Sys.init.m
M=M-1
@Sys.vm_L2
0;JMP
(Sys.vm_L1)


//push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 0
@SP
AM=M-1
D=M
@3
M=D

//push constant 5000
@5000
D=A
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

//call Sys.main 0
//call f n
//push return address
@Sys.vm_L3
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
@Sys.main
0;JMP
(Sys.vm_L3)

//pop temp 1
@5
D=A
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

//label LOOP
(Sys.init$LOOP)

//goto LOOP
@Sys.init$LOOP
0;JMP

//function Sys.main 5
//function f m
(Sys.main)
@5
D=A
@Sys.main.m
M=D
(Sys.vm_L5)
@Sys.main.m
D=M
@Sys.vm_L4
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Sys.main.m
M=M-1
@Sys.vm_L5
0;JMP
(Sys.vm_L4)


//push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 0
@SP
AM=M-1
D=M
@3
M=D

//push constant 5001
@5001
D=A
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

//push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop local 1
@LCL
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

//push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop local 2
@LCL
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

//push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop local 3
@LCL
D=M
@3
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

//push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Sys.add12 1
//call f n
//push return address
@Sys.vm_L6
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
@Sys.add12
0;JMP
(Sys.vm_L6)

//pop temp 0
@5
D=A
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

//push local 2
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push local 3
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push local 4
@LCL
D=M
@4
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

//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M

//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M

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
@Sys.main.frame
M=D
//ret = *(frame-5)
@Sys.main.frame
D=M
@5
D=D-A
A=D
D=M
@Sys.main.ret
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
@Sys.main.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@Sys.main.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@Sys.main.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@Sys.main.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@Sys.main.ret
A=M
0;JMP


//function Sys.add12 0
//function f m
(Sys.add12)
@0
D=A
@Sys.add12.m
M=D
(Sys.vm_L8)
@Sys.add12.m
D=M
@Sys.vm_L7
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Sys.add12.m
M=M-1
@Sys.vm_L8
0;JMP
(Sys.vm_L7)


//push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 0
@SP
AM=M-1
D=M
@3
M=D

//push constant 5002
@5002
D=A
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

//push constant 12
@12
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

//return
//frame = LCL
@LCL
D=M
@Sys.add12.frame
M=D
//ret = *(frame-5)
@Sys.add12.frame
D=M
@5
D=D-A
A=D
D=M
@Sys.add12.ret
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
@Sys.add12.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@Sys.add12.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@Sys.add12.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@Sys.add12.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@Sys.add12.ret
A=M
0;JMP


