(SimpleFunction.SimpleFunction.test)
@2
D=A
@SP
AM=M+D
(LOOP_FOR_SimpleFunction.SimpleFunction.test)
A=A-1
D=D-1
M=0
@LOOP_FOR_SimpleFunction.SimpleFunction.test
D;JLE
@0
D=A
@LCL
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
A=A+1
@1
D=A
@LCL
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
A=A+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
@SP
A=M-1
M=!M
@0
D=A
@ARG
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
A=A+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
@1
D=A
@ARG
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
A=A+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
@LCL
D=M
@R13
M=D
@R13
D=M
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP

