import argparse
from tokenizer import Tokenizer

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
    def PrTkn (s):
        for i in range(self.curr_level):
            self.outStr += ' '

        typ, name = s
        self.outStr += ' '.join(('<'+ typ + '>', name, '</'+ typ + '>'))
        self.outStr += '\n'
    def Beg (stm):
        for i in range(self.curr_level):
            self.outStr += ' '
        self.outStr += '<' + stm + '>\n'
        self.curr_level+=1
    def End (stm):
        self.curr_level-=1
        for i in range(self.curr_level):
            self.outStr += ' '
        self.outStr += '</' + stm + '>\n'


    def eat (self, s):
        a = self.Tokens.eat(s)
        if (a):
            PrTkn((a, s))

    
    def compileWhileStatement(self):
        self.Beg('whileStatemet')
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
        self.Beg('Statements')
        while (self.Tokens.next_token() !=  'symbol', '}' ):
            self.compileStatement()
            
        self.End('Statements')

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
            self.compileRetrun()

    def compileLet (self):
        self.Beg('letStatement')
        self.eat('let')
        __, varname = self.Tokens.next_token()
        if (self.Tokens.curr_token()[1] == '['):
            self.eat('[')
            self.compileExpression()
            self.eat(']')
        else:
            self.eat('=')
            self.compileExpression()
            self.eat(';')
        self.End('letStatement'):
    
    def compileIf (self):
        self.Beg('ifStatement')
        self.eat('if')
        self.eat('(')
        self.compileExpression
        self.eat(')')
        self.End('ifStatement')


    def compileDo (self):
        self.Beg('doStatement')
        self.eat('do')
        __, subrCall = self.Tokens.next_token()
        self.eat(';')
        self.End('doStatement')
    def compileReturn (self):
        self.Beg('returnStatement')
        self.eat('return')
        if (self.Tokens.curr_token()[1] != ';')
            self.eat(';')





        





