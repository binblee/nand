// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@8192
D=A
@num_bytes_screen
M=D             // num_bytes_screen = 8K

@current_color
M=0             // 0 for white, -1 for black

(LOOP)
@KBD
D=M
@NO_INPUT
D;JEQ

@keypressed
M=-1
@DRAW
0;JMP

(NO_INPUT)
@keypressed
M=0

(DRAW)
@current_color
D=M
@keypressed
D=D-M

@CONTINUE_KEYBOARD_PROBE
D;JEQ               // if keypressed == current_color, do nothing

@num_bytes_screen
D=M
@count
M=D                 // set count = 8K

@keypressed
D=M
@current_color
M=D                 // set current_color to value of keypressed, 0 for white, -1 for black

@SCREEN
D=A
@current_byte
M=D                 // screen memory start address

(LOOP_DRAW)

@current_color
D=M

@current_byte
A=M
M=D                 // set color

@current_byte
M=M+1               // move to next 

@count
MD=M-1              // count down

@LOOP_DRAW
D;JGT

(CONTINUE_KEYBOARD_PROBE)
@LOOP
0;JMP       // continue keyboard probe loop

(END)
@END
0;JMP
