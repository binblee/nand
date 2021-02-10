//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@StackTest.vm_L0
D;JEQ
D=0
@StackTest.vm_L1
0;JMP
(StackTest.vm_L0)
D=-1
(StackTest.vm_L1)
@SP
A=M
A=A-1
M=D

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@StackTest.vm_L2
D;JEQ
D=0
@StackTest.vm_L3
0;JMP
(StackTest.vm_L2)
D=-1
(StackTest.vm_L3)
@SP
A=M
A=A-1
M=D

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@StackTest.vm_L4
D;JEQ
D=0
@StackTest.vm_L5
0;JMP
(StackTest.vm_L4)
D=-1
(StackTest.vm_L5)
@SP
A=M
A=A-1
M=D

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
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
@StackTest.vm_L6
D;JLT
D=0
@StackTest.vm_L7
0;JMP
(StackTest.vm_L6)
D=-1
(StackTest.vm_L7)
@SP
A=M
A=A-1
M=D

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 892
@892
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
@StackTest.vm_L8
D;JLT
D=0
@StackTest.vm_L9
0;JMP
(StackTest.vm_L8)
D=-1
(StackTest.vm_L9)
@SP
A=M
A=A-1
M=D

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
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
@StackTest.vm_L10
D;JLT
D=0
@StackTest.vm_L11
0;JMP
(StackTest.vm_L10)
D=-1
(StackTest.vm_L11)
@SP
A=M
A=A-1
M=D

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@StackTest.vm_L12
D;JGT
D=0
@StackTest.vm_L13
0;JMP
(StackTest.vm_L12)
D=-1
(StackTest.vm_L13)
@SP
A=M
A=A-1
M=D

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@StackTest.vm_L14
D;JGT
D=0
@StackTest.vm_L15
0;JMP
(StackTest.vm_L14)
D=-1
(StackTest.vm_L15)
@SP
A=M
A=A-1
M=D

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@StackTest.vm_L16
D;JGT
D=0
@StackTest.vm_L17
0;JMP
(StackTest.vm_L16)
D=-1
(StackTest.vm_L17)
@SP
A=M
A=A-1
M=D

//push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 53
@53
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

//push constant 112
@112
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

//neg
@SP
A=M
A=A-1
M=-M

//and
@SP
M=M-1
A=M
D=M
A=A-1
M=D&M

//push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

//or
@SP
M=M-1
A=M
D=M
A=A-1
M=D|M

//not
@SP
A=M
A=A-1
M=!M

