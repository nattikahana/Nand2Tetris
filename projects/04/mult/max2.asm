    @R1
    D = M
    @R2
    D = D - M
    @LARGER
    D;JGT
    @R2
    D = M
    @R0
    M = D
    @END
    0;JMP
(LARGER)
    @R1
    D = M
    @R0
    M = D
(END)
    @END
    0;JMP
