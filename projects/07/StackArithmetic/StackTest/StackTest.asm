//push constant 17
@17
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 17
@17
D=A
@SP
M=M+1
A=M-1
M=D
//eq
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
M=0
@NEQ0
D;JNE
@SP
A=M-1
M=-1
(NEQ0)
//push constant 17
@17
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 16
@16
D=A
@SP
M=M+1
A=M-1
M=D
//eq
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
M=0
@NEQ1
D;JNE
@SP
A=M-1
M=-1
(NEQ1)
//push constant 16
@16
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 17
@17
D=A
@SP
M=M+1
A=M-1
M=D
//eq
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
M=0
@NEQ2
D;JNE
@SP
A=M-1
M=-1
(NEQ2)
//push constant 892
@892
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 891
@891
D=A
@SP
M=M+1
A=M-1
M=D
//lt
@SP
M=M-1
A=M
D=M
@YLT3
D;JLT
@SP
A=M-1
D=M
@XLTY3
D;JLT
(XMINUSY3)
@SP
A=M-1
D=M
A=A+1
D=D-M
@XLTY3
D;JLT
(XGEY3)
@SP
A=M-1
D=M
M=0
@END3
0;JMP
(YLT3)
@SP
A=M-1
D=M
@XMINUSY3
D;JLT
@XGEY3
0;JMP
(XLTY3)
@SP
A=M-1
M=-1
(END3)
//push constant 891
@891
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 892
@892
D=A
@SP
M=M+1
A=M-1
M=D
//lt
@SP
M=M-1
A=M
D=M
@YLT4
D;JLT
@SP
A=M-1
D=M
@XLTY4
D;JLT
(XMINUSY4)
@SP
A=M-1
D=M
A=A+1
D=D-M
@XLTY4
D;JLT
(XGEY4)
@SP
A=M-1
D=M
M=0
@END4
0;JMP
(YLT4)
@SP
A=M-1
D=M
@XMINUSY4
D;JLT
@XGEY4
0;JMP
(XLTY4)
@SP
A=M-1
M=-1
(END4)
//push constant 891
@891
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 891
@891
D=A
@SP
M=M+1
A=M-1
M=D
//lt
@SP
M=M-1
A=M
D=M
@YLT5
D;JLT
@SP
A=M-1
D=M
@XLTY5
D;JLT
(XMINUSY5)
@SP
A=M-1
D=M
A=A+1
D=D-M
@XLTY5
D;JLT
(XGEY5)
@SP
A=M-1
D=M
M=0
@END5
0;JMP
(YLT5)
@SP
A=M-1
D=M
@XMINUSY5
D;JLT
@XGEY5
0;JMP
(XLTY5)
@SP
A=M-1
M=-1
(END5)
//push constant 32767
@32767
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D
//gt
@SP
M=M-1
A=M
D=M
@YGT6
D;JGT
@SP
A=M-1
D=M
@XGTY6
D;JGT
(XMINUSY6)
@SP
A=M-1
D=M
A=A+1
D=D-M
@XGTY6
D;JGT
(XLEY6)
@SP
A=M-1
D=M
M=0
@END6
0;JMP
(YGT6)
@SP
A=M-1
D=M
@XMINUSY6
D;JGT
@XLEY6
0;JMP
(XGTY6)
@SP
A=M-1
M=-1
(END6)
//push constant 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 32767
@32767
D=A
@SP
M=M+1
A=M-1
M=D
//gt
@SP
M=M-1
A=M
D=M
@YGT7
D;JGT
@SP
A=M-1
D=M
@XGTY7
D;JGT
(XMINUSY7)
@SP
A=M-1
D=M
A=A+1
D=D-M
@XGTY7
D;JGT
(XLEY7)
@SP
A=M-1
D=M
M=0
@END7
0;JMP
(YGT7)
@SP
A=M-1
D=M
@XMINUSY7
D;JGT
@XLEY7
0;JMP
(XGTY7)
@SP
A=M-1
M=-1
(END7)
//push constant 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D
//gt
@SP
M=M-1
A=M
D=M
@YGT8
D;JGT
@SP
A=M-1
D=M
@XGTY8
D;JGT
(XMINUSY8)
@SP
A=M-1
D=M
A=A+1
D=D-M
@XGTY8
D;JGT
(XLEY8)
@SP
A=M-1
D=M
M=0
@END8
0;JMP
(YGT8)
@SP
A=M-1
D=M
@XMINUSY8
D;JGT
@XLEY8
0;JMP
(XGTY8)
@SP
A=M-1
M=-1
(END8)
//push constant 57
@57
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 31
@31
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 53
@53
D=A
@SP
M=M+1
A=M-1
M=D
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
//push constant 112
@112
D=A
@SP
M=M+1
A=M-1
M=D
//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
//neg
@SP
A=M-1
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
M=M+1
A=M-1
M=D
//or
@SP
M=M-1
A=M
D=M
A=A-1
M=D|M
//not
@SP
A=M-1
M=!M
