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

//function Class1.set 0
//function f m
(Class1.set)
@0
D=A
@Class1.set.m
M=D
(Class1.vm_L2)
@Class1.set.m
D=M
@Class1.vm_L1
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Class1.set.m
M=M-1
@Class1.vm_L2
0;JMP
(Class1.vm_L1)


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

//pop static 0
@SP
AM=M-1
D=M
@Class1.vm.0
M=D

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

//pop static 1
@SP
AM=M-1
D=M
@Class1.vm.1
M=D

//push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

//return
//frame = LCL
@LCL
D=M
@Class1.set.frame
M=D
//ret = *(frame-5)
@Class1.set.frame
D=M
@5
D=D-A
A=D
D=M
@Class1.set.ret
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
@Class1.set.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@Class1.set.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@Class1.set.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@Class1.set.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@Class1.set.ret
A=M
0;JMP


//function Class1.get 0
//function f m
(Class1.get)
@0
D=A
@Class1.get.m
M=D
(Class1.vm_L4)
@Class1.get.m
D=M
@Class1.vm_L3
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Class1.get.m
M=M-1
@Class1.vm_L4
0;JMP
(Class1.vm_L3)


//push static 0
@Class1.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1

//push static 1
@Class1.vm.1
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
@Class1.get.frame
M=D
//ret = *(frame-5)
@Class1.get.frame
D=M
@5
D=D-A
A=D
D=M
@Class1.get.ret
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
@Class1.get.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@Class1.get.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@Class1.get.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@Class1.get.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@Class1.get.ret
A=M
0;JMP


//function Sys.init 0
//function f m
(Sys.init)
@0
D=A
@Sys.init.m
M=D
(Sys.vm_L6)
@Sys.init.m
D=M
@Sys.vm_L5
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Sys.init.m
M=M-1
@Sys.vm_L6
0;JMP
(Sys.vm_L5)


//push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Class1.set 2
//call f n
//push return address
@Sys.vm_L7
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
@2
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
@Class1.set
0;JMP
(Sys.vm_L7)

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

//push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Class2.set 2
//call f n
//push return address
@Sys.vm_L8
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
@2
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
@Class2.set
0;JMP
(Sys.vm_L8)

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

//call Class1.get 0
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
@Class1.get
0;JMP
(Sys.vm_L9)

//call Class2.get 0
//call f n
//push return address
@Sys.vm_L10
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
@Class2.get
0;JMP
(Sys.vm_L10)

//label WHILE
(Sys.init$WHILE)

//goto WHILE
@Sys.init$WHILE
0;JMP

//function Class2.set 0
//function f m
(Class2.set)
@0
D=A
@Class2.set.m
M=D
(Class2.vm_L12)
@Class2.set.m
D=M
@Class2.vm_L11
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Class2.set.m
M=M-1
@Class2.vm_L12
0;JMP
(Class2.vm_L11)


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

//pop static 0
@SP
AM=M-1
D=M
@Class2.vm.0
M=D

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

//pop static 1
@SP
AM=M-1
D=M
@Class2.vm.1
M=D

//push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

//return
//frame = LCL
@LCL
D=M
@Class2.set.frame
M=D
//ret = *(frame-5)
@Class2.set.frame
D=M
@5
D=D-A
A=D
D=M
@Class2.set.ret
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
@Class2.set.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@Class2.set.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@Class2.set.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@Class2.set.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@Class2.set.ret
A=M
0;JMP


//function Class2.get 0
//function f m
(Class2.get)
@0
D=A
@Class2.get.m
M=D
(Class2.vm_L14)
@Class2.get.m
D=M
@Class2.vm_L13
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@Class2.get.m
M=M-1
@Class2.vm_L14
0;JMP
(Class2.vm_L13)


//push static 0
@Class2.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1

//push static 1
@Class2.vm.1
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
@Class2.get.frame
M=D
//ret = *(frame-5)
@Class2.get.frame
D=M
@5
D=D-A
A=D
D=M
@Class2.get.ret
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
@Class2.get.frame
AM=M-1
D=M
@THAT
M=D
// THIS=*(frame-2)
@Class2.get.frame
AM=M-1
D=M
@THIS
M=D
// ARG=*(frame-3)
@Class2.get.frame
AM=M-1
D=M
@ARG
M=D
// LCL=*(frame-4)
@Class2.get.frame
AM=M-1
D=M
@LCL
M=D
// goto return address
@Class2.get.ret
A=M
0;JMP


