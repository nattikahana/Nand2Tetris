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

(STILLWT)
    // Cheks if the keyboard is pressed
    @KBD
    D = M
    @STILLWT
    D;JEQ
    @location
    M = 0
(BLACK)
    // Paint the board to black
    @location
    D = M
    M = M + 1
    
    @SCREEN
    A = A + D
    M = -1
    
    @8191
    D = D - A

    @STILLBLK
    D;JGE

    @BLACK
    0;JMP

(STILLBLK)
    // Cheks if the keyboard is released
    @KBD
    D = M
    @STILLBLK
    D;JNE
    @location
    M = 0

(WHITE)
    // Paint the board to white
    @location
    D = M
    M = M + 1

    @SCREEN
    A = A + D
    M = 0

    @8191
    D = D - A

    @STILLWT
    D;JGE

    @WHITE
    0;JMP
