(BEGIN)
	@KBD
	D = M;
	@WHITE
	D; JEQ
	@BLACK
	D;JNE
(WHITE)
	@SCREEN
	D = A;
	@a
	M = D;
(LOOPB)
	@SCREEN
	D = A;
	@a
	D = M - D;
	@BEGIN
	D;JGE
	@a
	A = M;
	M = 0;
	@a
	M = M + 1;
	@LOOPB
	0; JMP
(BLACK)
	@SCREEN
	D = A;
	@a
	M = D;
(LOOPW)
	@SCREEN
	D = A;
	@a
	D = M - D;
@BEGIN
	D;JGE
	@a
	A = M;
	M = -1;
	@a
	M = M + 1;
@LOOPW
	0; JMP

