// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@num_negative
M=0

@count
M=0

// if r0 == 0 then
//    r2 = 0
//    jmp to end
// else if r0 < 0 then
//    num_negative = num_negative + 1, r2=-r0
// else
//    r2 = r0
// end

@R0
D=M
@EQ_ZERO
D;JEQ

@R0_LT_ZERO
D;JLT

// r0 > 0
@R0
D=M
@R2
M=D         //r2=r0
@CHECK_R1
0;JMP

(R0_LT_ZERO)
@num_negative
M=M+1
@R0
D=-M
@R2
M=D         // r2=r0

// if r1 == 0 then
//    r2 = 0
//    jmp to end
// else if r1 < 0 then
//   num_negative = num_negative + 1, count=-r1
// else
//   count = r1
// end

(CHECK_R1)
@R1
D=M
@EQ_ZERO
D;JEQ

@R1_LT_ZERO
D;JLT

// r1 > 0
@R1
D=M
@count
M=D         // count=r1
@LOOP
0;JMP

(R1_LT_ZERO)
@num_negative
M=M+1
@R1
D=-M
@count
M=D         // count = -r1

// loop while count > 0
//   r2 = r2 + r0
(LOOP)
@count
MD=M-1
@NEGATIVE_OR_NOT
D;JEQ
@R0
D=M
@R2
M=D+M
@LOOP
0;JMP

// if num_negative -1 == 0 then
//    r2 = -r2
(NEGATIVE_OR_NOT)
@num_negative
D=M
@1
D=D&A   // num_negative & 0x01
@END
D;JEQ   // if num_negative & 1 == 0, means result is positive number

@R2
M=-M

@END
0;JMP

(EQ_ZERO)
@R2
M=0

// end of program
(END)
@END
0;JMP      
