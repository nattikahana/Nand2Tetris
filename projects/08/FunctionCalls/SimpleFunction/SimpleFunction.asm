// initialize the stack pointer to 0x0100
@256
D=A
@SP
M=D
// invoke Sys.init
//call  Sys.init 0
@SimpleFunction.Sys.init$RET.0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(SimpleFunction.Sys.init$RET.0)
//function SimpleFunction.test 2
(SimpleFunction.test)
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//push local 1
@LCL
D=M
@1
A=D+A
D=M
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
//not
@SP
A=M-1
M=!M
//push argument 0
@ARG
D=M
@0
A=D+A
D=M
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
//push argument 1
@ARG
D=M
@1
A=D+A
D=M
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
//return
@LCL
D=M
@R15
M=D
@5
D=A
@R15
D=M-D
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R15
A=M-1
D=M
@THAT
M=D
@R15
D=M
@2
A=D-A
D=M
@THIS
M=D
@R15
D=M
@3
A=D-A
D=M
@ARG
M=D
@R15
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP