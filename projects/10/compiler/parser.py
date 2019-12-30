import argparse
from tokenizer import Tokenizer
import sys

parser = argparse.ArgumentParser()
parser.add_argument('nFiles', type = int, help = 'Number of .jack files')
parser.add_argument('files', nargs = '+', help = 'Enter file names!')
args = parser.parse_args()

# for f in args.files:
#     # print(f)
#     file_name = f[:-5] + "test.xml"
#     Tokens = Tokenizer(open(f, 'r').read())
#     token = Tokens.next_token()
#     xml_file = open(file_name, 'w')

#     xml_file.write('<tokens>\n')    
#     while (token != None):
#         # print(token)
#         typ, name = token
#         xml_file.write(' '.join(('<'+ typ + '>', name, '</'+ typ + '>')))
#         xml_file.write('\n')
#         token = Tokens.next_token()

#     xml_file.write('</tokens>\n')

class CompEngine:
    def __init__(self, f):
        self.file_name = f
        self.Tokens = Tokenizer(open(f, 'r').read())
        self.outStr = ''
        self.curr_level = 0

    def get_xml (self):
        return self.outStr
    def PrTkn (self, s):
        for i in range(self.curr_level):
            self.outStr += ' '

        typ, name = s
        self.outStr += ' '.join(('<'+ typ + '>', name, '</'+ typ + '>'))
        self.outStr += '\n'
    def Beg (self, stm):
        for i in range(self.curr_level):
            self.outStr += ' '
        self.outStr += '<' + stm + '>\n'
        self.curr_level+=1
        # print(self.outStr)
    
    def End (self,stm):
        self.curr_level-=1
        for i in range(self.curr_level):
            self.outStr += ' '
        self.outStr += '</' + stm + '>\n'
        # print(self.outStr)



    def eat (self, s):
        # print(self.outStr)
        a = self.Tokens.eat(s)
        if (a):
            self.PrTkn((a, s))
        # print(self.outStr)
    
    def eat_next (self):
        # print(self.outStr)

        a = self.Tokens.next_token()
        if (a):
            self.PrTkn(a)
        # print(self.outStr, 2)



    def compileClass(self):
        self.Beg('class')
        self.eat('class')
        self.eat(self.Tokens.curr_token()[1]) #class Name
        self.eat('{')
        while (self.Tokens.curr_token()[1] in ('static', 'field')):
            self.compileClassVarDec()
        while (self.Tokens.curr_token()[1] in ('constructor', 'function', 'method')):
            self.compileSubroutineDec()
        self.eat('}')
        self.End('class')

    def compileClassVarDec(self):
        self.Beg('classVarDec')
        if (self.Tokens.curr_token()[1] in ('static', 'field')):
            self.eat(self.Tokens.curr_token()[1])
        else:
            print ('Expected: static or field')
            sys.exit()
        if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean')):
            self.eat_next()
        elif (self.Tokens.curr_token()[0] == 'identifier'): #check for class_name
            self.eat_next()
        else:
            print('expected vartype0')
        
        self.compileVarName()
        typ, tok = self.Tokens.curr_token()
        while (tok == ','):
            self.eat(',')
            self.compileVarName()
            typ, tok = self.Tokens.curr_token()

        self.eat(';')
        self.End('classVarDec')

    def compileSubroutineDec(self):
        self.Beg('subroutineDec')
        if (self.Tokens.curr_token()[1] in ( 'function', 'method')):
            self.eat(self.Tokens.curr_token()[1])
        elif (self.Tokens.curr_token()[1] == 'constructor'):
            self.eat_next()
            # self.eat_next() #for new <constructor Square new>
        else:
            print ('Expected: constructor or fucntion or method')
            sys.exit()
        if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean', 'void')):
            self.eat_next()
        elif(self.Tokens.curr_token()[0] == 'identifier'):
            self.eat_next()
        else:
            print('Expected Type, got none')
            sys.exit()

        self.compileSubroutineName()
        self.eat('(')
        self.compileParameterList()
        self.eat(')')
        self.compileSubroutineBody()
        self.End('subroutineDec')
    
    def compileParameterList(self):
        self.Beg('parameterList')
        if (self.Tokens.curr_token()[1] != ')'):
            if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean')):
                self.eat_next()
            elif (self.Tokens.curr_token()[0] == 'identifier'): #check for class_name
                self.eat_next()
            else:
                print("exprected vartype1")
            
            self.compileVarName()
            typ, tok = self.Tokens.curr_token()
            while (tok == ','):
                self.eat(',')
                if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean')):
                    self.eat_next()
                elif (self.Tokens.curr_token()[0] == 'identifier'): #check for class_name
                    self.eat_next()
                else:
                    print("exprected vartype1")
                self.compileVarName()
                typ, tok = self.Tokens.curr_token()

        
        self.End('parameterList')
    
    def compileSubroutineBody(self):
        self.Beg('subroutineBody')
        self.eat('{')
        typ, tok = self.Tokens.curr_token()
        while (tok == 'var'):
            self.compileVarDec()
            typ, tok = self.Tokens.curr_token()


        self.compileStatements()
        self.eat('}')
        self.End('subroutineBody')
    
    def compileVarDec (self):
        self.Beg('varDec')
        self.eat('var')
        if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean')):
            self.eat_next()
        elif (self.Tokens.curr_token()[0] == 'identifier'): #check for class_name
            self.eat_next()
        else:
            print("exprected vartype2, got :", self.Tokens.curr_token()[1])
        self.compileVarName()
        typ, tok = self.Tokens.curr_token()
        while (tok == ','):
            self.eat(',')
            self.compileVarName()
            typ, tok = self.Tokens.curr_token()
        self.eat(';')
        self.End('varDec')

    def compileVarName(self):
        self.eat_next()
    def compileSubroutineName(self):
        self.eat_next()
        
    def compileWhileStatement(self):
        self.Beg('whileStatement')
        self.eat('while')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat ('{')
        self.compileStatements()
        self.eat ('}')
        self.End('whileStatement')
        # while (self.Tokens.next_token() != )

    def compileStatements (self):
        self.Beg('statements')
        while (self.Tokens.curr_token()[1] !=  '}' ):
            self.compileStatement()
           
        self.End('statements')

    def compileStatement (self):
        __, tok = self.Tokens.curr_token()
        if tok == 'let':
            self.compileLet()            
        elif tok == 'if':
            self.compileIf()
        elif tok == 'while':
            self.compileWhileStatement()
        elif tok == 'do':
            self.compileDo()
        elif tok == 'return':
            self.compileReturn()
        else:
            print ("Expected a statement, but not found ")
            sys.exit()

    def compileLet (self):
        self.Beg('letStatement')
        self.eat('let')
        # self.compileVarName()
        self.eat_next()
        if (self.Tokens.curr_token()[1] == '['):
            self.eat('[')
            self.compileExpression()
            self.eat(']')
        
        self.eat('=')
        self.compileExpression()
        self.eat(';')
        self.End('letStatement')
    
    def compileIf (self):
        self.Beg('ifStatement')
        self.eat('if')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')
        self.compileStatements()
        self.eat('}')
        if (self.Tokens.curr_token()[1] == 'else'):
            self.eat('else')
            self.eat('{')
            self.compileStatements()
            self.eat('}')

        self.End('ifStatement')


    def compileDo (self):
        self.Beg('doStatement')
        self.eat('do')
        self.compileSubroutineCall()
        self.eat(';')
        self.End('doStatement')
    def compileReturn (self):
        self.Beg('returnStatement')
        self.eat('return')
        if (self.Tokens.curr_token()[1] != ';'):
            self.compileExpression()
        self.eat(';')
        self.End('returnStatement')
    def compileExpression(self):
        # print(1)
        self.Beg('expression')
        self.compileTerm()
        op = '+-*/|=' 
        sop = ['&gt;', '&lt;', '&amp;']
        # print(self.Tokens.curr_token()[1])
        while (self.Tokens.curr_token()[1] in op or self.Tokens.curr_token()[1] in sop):
            # print(50)
            self.eat(self.Tokens.curr_token()[1])
            self.compileTerm()
        self.End('expression')
    
    def compileTerm (self):
        # there was some confusion here, there is likely to be a bug
        self.Beg('term')
        typ, tok = self.Tokens.curr_token()
        if tok in '-~':
            self.eat_next()
            self.compileTerm()
        elif typ == 'integerConstant' or typ == 'stringConstant' or typ == 'keyword':
            self.eat(tok)
        elif typ == 'identifier':
            ntyp, ntok = self.Tokens.peek_ahead()
            if (ntok == '.' or ntok == '('):
                self.compileSubroutineCall()
            elif (ntok == '['):
                self.compileVarName()
                self.eat('[')
                self.compileExpression()
                self.eat(']')
            else:
                # print(50)
                self.compileVarName()
            
        elif tok == '(':
            self.eat('(')
            self.compileExpression()
            self.eat(')')
        self.End('term')
    
    def compileSubroutineCall(self):
        # self.Beg('subroutineCall')
        typ, tok = self.Tokens.curr_token()
        ntyp, ntok = self.Tokens.peek_ahead()
        if (ntok == '.'):
            self.eat(tok)
            self.eat(ntok)
            self.compileSubroutineName()
        else:
            self.eat_next()
        
        self.eat('(')
        self.compileExpressionList()
        self.eat(')')
        # self.End('subroutineCall')

    def compileExpressionList(self):
        self.Beg('expressionList')
        typ, tok = self.Tokens.curr_token()
        if (tok != ')'):
            self.compileExpression()
            ntyp, ntok = self.Tokens.curr_token()
            while (ntok != ')'):
                self.eat(',')
                self.compileExpression()
                ntyp, ntok = self.Tokens.curr_token()
                # print(ntok)
             
        # print(ntok)
        # sys.exit()    
        self.End('expressionList')


for f in args.files:
    # print(f)
    file_name = f[:-5] + "fin.xml"
    JackAn = CompEngine(f)
    JackAn.compileClass()
    outp = JackAn.get_xml()
    open(file_name, 'w').write(outp)
    # print(outp)
        

            

        







        





