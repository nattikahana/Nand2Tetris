// initialize the stack pointer to 0x0100
@256
D=A
@SP
M=D
// invoke Sys.init
//call  Sys.init 0
@Sys.Sys.init$RET.0
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
(Sys.Sys.init$RET.0)
//function Sys.init 0
(Sys.init)
//push constant 4000
@4000
D=A
@SP
M=M+1
A=M-1
M=D
//pop pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
//push constant 5000
@5000
D=A
@SP
M=M+1
A=M-1
M=D
//pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
//call  Sys.main 0
@Sys.Sys.main$RET.1
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
@Sys.main
0;JMP
(Sys.Sys.main$RET.1)
//pop temp 1
@R5
D=A
@1
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//label LOOP
(Sys.init$LOOP)
//goto LOOP
@Sys.init$LOOP
0;JMP
//function Sys.main 5
(Sys.main)
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
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 4001
@4001
D=A
@SP
M=M+1
A=M-1
M=D
//pop pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
//push constant 5001
@5001
D=A
@SP
M=M+1
A=M-1
M=D
//pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
//push constant 200
@200
D=A
@SP
M=M+1
A=M-1
M=D
//pop local 1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//push constant 40
@40
D=A
@SP
M=M+1
A=M-1
M=D
//pop local 2
@LCL
D=M
@2
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//push constant 6
@6
D=A
@SP
M=M+1
A=M-1
M=D
//pop local 3
@LCL
D=M
@3
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//push constant 123
@123
D=A
@SP
M=M+1
A=M-1
M=D
//call  Sys.add12 1
@Sys.Sys.add12$RET.2
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
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys.Sys.add12$RET.2)
//pop temp 0
@R5
D=A
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
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
//push local 2
@LCL
D=M
@2
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//push local 3
@LCL
D=M
@3
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//push local 4
@LCL
D=M
@4
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
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
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
//function Sys.add12 0
(Sys.add12)
//push constant 4002
@4002
D=A
@SP
M=M+1
A=M-1
M=D
//pop pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
//push constant 5002
@5002
D=A
@SP
M=M+1
A=M-1
M=D
//pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
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
//push constant 12
@12
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
