import argparse
from tokenizer import Tokenizer
import sys


#Next few lines parse the command line arguments. Number of Jack files (1st Argumument) is essentially ignored, and the rest of the arguments are proccessed as files.
parser = argparse.ArgumentParser()
parser.add_argument('nFiles', type = int, help = 'Number of .jack files')
parser.add_argument('files', nargs = '+', help = 'Enter file names!')
args = parser.parse_args()

class CompEngine:
    def __init__(self, f):
        self.file_name = f
        self.err_file = f[:-5] + '.err'
        self.Tokens = Tokenizer(open(f, 'r').read(), self.err_file)
        self.outStr = ''
        self.curr_level = 0
        self.class_symbol_table = {}
        self.field_count = 0
        self.static_count = 0
        self.class_name = ''
        self.vmCode = ''
        self.numLabels = 0
        self.op_table = {
            '+': 'add', '-': 'sub', '&amp;': 'and', '|': 'or', 
            '&lt;': 'lt', '&gt;': 'gt', '=': 'eq', '*' : 'call Math.multiply 2', '/': 'call Math.divide 2'
        }
        self.subR_symbol_table = {}
        self.lcl_count = 0
        self.arg_count = 0



    def add_class_var(self, name, kind, typ):
        # Adds a variable to the class symbol table. 
        
        if (kind == 'static'):
            self.class_symbol_table[name] = {'kind':kind, 'type': typ,  'index':self.static_count}
            self.static_count+=1
        elif (kind == 'field'):
            self.class_symbol_table[name] = {'kind':kind, 'type': typ,  'index':self.field_count}
            self.field_count+=1

    def add_subR_var(self, name, kind, typ):
        # Adds a variable to the subroutine symbol table.
        if (kind == 'argument'):
            self.subR_symbol_table[name] = {'kind':kind, 'type': typ,  'index':self.arg_count}
            self.arg_count+=1
        elif (kind == 'local'):
            self.subR_symbol_table[name] = {'kind':kind, 'type': typ,  'index':self.lcl_count}
            self.lcl_count+=1


    def get_xml (self):
        return self.outStr

    def get_vm (self):
        return self.vmCode
   
    def PrTkn (self, s):
        #This was a helper function for the XML file to get the proper indentation.
        for i in range(self.curr_level):
            self.outStr += ' '

        typ, name = s
        self.outStr += ' '.join(('<'+ typ + '>', name, '</'+ typ + '>'))
        self.outStr += '\n'
    
    def Beg (self, stm):
        #This was a helper function for the XML file to print the staring of a new instance eg. <whileStament>.
        for i in range(self.curr_level):
            self.outStr += ' '
        self.outStr += '<' + stm + '>\n'
        self.curr_level+=1
        
    
    def End (self,stm):
        #This was a helper function for the XML file to print the ending of a new instance eg. </whileStament>.
        self.curr_level-=1
        for i in range(self.curr_level):
            self.outStr += ' '
        self.outStr += '</' + stm + '>\n'
        



    def eat (self, s):
        # Calls the eat function of the Tokenizer.
        #  (That functions compares the next token with the expected token <s>, and throws an error in case of a mismatch)
        a = self.Tokens.eat(s)
        if (a):
            self.PrTkn((a, s))
        
    
    def eat_next (self):
        # Moves the tokenizer, to the next token. 
        a = self.Tokens.next_token()
        if (a):
            self.PrTkn(a)
    



    def compileClass(self):
        self.Beg('class')
        self.eat('class')
        self.class_name = self.Tokens.curr_token()[1]
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
        kind = self.Tokens.curr_token()[1] 
        if (self.Tokens.curr_token()[1] in ('static', 'field')):
            kind = self.Tokens.curr_token()[1]
            self.eat(self.Tokens.curr_token()[1])
        else:
            err_out = 'ERROR: Expected <keyword> but ' + kind + '.\n'  
            open(self.err_file, 'w').write(err_out)
            sys.exit()

        
        typ = self.Tokens.curr_token()[1]
        if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean')):
            self.eat_next()
        elif (self.Tokens.curr_token()[0] == 'identifier'): #check for class_name
            self.eat_next()
        else:
            err_out = 'ERROR: Expected <variable type> but ' + typ + '.\n'  
            open(self.err_file, 'w').write(err_out)
            sys.exit()

        varN = self.Tokens.curr_token()[1]
        self.compileVarName()
        self.add_class_var(varN, kind, typ)
        tok = self.Tokens.curr_token()[1]
        while (tok == ','):
            self.eat(',')
            varN = self.Tokens.curr_token()[1]
            self.compileVarName()
            self.add_class_var(varN, kind, typ)
            tok = self.Tokens.curr_token()[1]

        self.eat(';')
        self.End('classVarDec')

    def compileSubroutineDec(self):
        self.Beg('subroutineDec')
        self.arg_count = 0
        self.lcl_count = 0
        self.subR_symbol_table = {}
        s = self.Tokens.curr_token()[1]
        if (self.Tokens.curr_token()[1] in ('constructor', 'function', 'method')):
            self.currSubRoutineType = self.Tokens.curr_token()[1]
            self.eat(self.Tokens.curr_token()[1])
        else:
            err_out = 'ERROR: Expected <keyword> but ' + s + '.\n'  
            open(self.err_file, 'w').write(err_out)
            sys.exit()
        self.currSubRoutineReturnType = self.Tokens.curr_token()[1]
        s = self.Tokens.curr_token()[1]

        if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean', 'void')):
            self.eat_next()
        elif(self.Tokens.curr_token()[0] == 'identifier'):
            self.eat_next()
        else:
            err_out = 'ERROR: Expected <keyword> but ' + s + '.\n'  
            open(self.err_file, 'w').write(err_out)
            sys.exit()
            return False


       
        
        self.currSubRoutineName = self.Tokens.curr_token()[1]
        self.compileSubroutineName()
        if (self.currSubRoutineType =='method'):
                self.add_subR_var('this', 'argument', self.class_name)
        self.eat('(')
        self.compileParameterList()
        self.eat(')')
        self.compileSubroutineBody()
        
        self.End('subroutineDec')
    
    def compileParameterList(self):
        self.Beg('parameterList')
        if (self.Tokens.curr_token()[1] != ')'):
            varType = self.Tokens.curr_token()[1]
            if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean')):
                self.eat_next()
            elif (self.Tokens.curr_token()[0] == 'identifier'): #check for valid identifier.
                self.eat_next()
            else:
                print("exprected vartype1")
                err_out = 'ERROR: ' + varType + '.\n'  
                open(self.err_file, 'w').write(err_out)
                sys.exit()
                print("exprected vartype1")
            
            varName = self.Tokens.curr_token()[1]
            self.add_subR_var(varName, 'argument', varType)
            self.compileVarName()
            typ, tok = self.Tokens.curr_token()
            while (tok == ','):
                self.eat(',')
                varType = self.Tokens.curr_token()[1]
                if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean')):
                    self.eat_next()
                elif (self.Tokens.curr_token()[0] == 'identifier'): #check for valid identifier.
                    self.eat_next()
                else:
                    err_out = 'ERROR: ' + varType + '.\n'  
                    open(self.err_file, 'w').write(err_out)
                    sys.exit()
                    print("exprected vartype1")
                
                varName = self.Tokens.curr_token()[1]
                self.add_subR_var(varName, 'argument', varType)
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

        self.vmCode += 'function ' + self.class_name + '.' + self.currSubRoutineName + ' ' + str(self.lcl_count) + '\n'
        if (self.currSubRoutineType == 'constructor'):
            self.vmCode += 'push constant ' + str(self.field_count) + '\n'
            self.vmCode += 'call Memory.alloc 1\n'
            self.vmCode += 'pop pointer 0\n'
        elif (self.currSubRoutineType == 'method'):
            self.vmCode += 'push argument 0\n'
            self.vmCode += 'pop pointer 0\n'
    

        self.compileStatements()
        self.eat('}')

        self.End('subroutineBody')
    
    def compileVarDec (self):
        self.Beg('varDec')
        self.eat('var')
        varType = self.Tokens.curr_token()[1]
        if (self.Tokens.curr_token()[1] in ('char', 'int', 'boolean')):
            self.eat_next()
        elif (self.Tokens.curr_token()[0] == 'identifier'): #check for class_name
            self.eat_next()
        else:
            print("exprected vartype2, got :")
            err_out = 'ERROR:' + s + '\n'  
            open(self.err_file, 'w').write(err_out)
            sys.exit()
        
        varName = self.Tokens.curr_token()[1]
        self.add_subR_var(varName, 'local', varType)
        self.compileVarName()
        typ, tok = self.Tokens.curr_token()
        while (tok == ','):
            self.eat(',')
            varName = self.Tokens.curr_token()[1]
            self.add_subR_var(varName, 'local', varType)
            self.compileVarName()
            typ, tok = self.Tokens.curr_token()
        self.eat(';')
        self.End('varDec')

    def compileVarName1(self):
        #This functions checks for the varName in the symbol table and if it doesn't exist, throws an error.
        typ, varName = self.Tokens.curr_token()
        varKind, varIndex, varType = 0, 0, 0
        id1 = varName
        if (varName in self.subR_symbol_table.keys()):
            varKind, varIndex, varType= self.subR_symbol_table[id1]['kind'] , self.subR_symbol_table[id1]['index'] , self.subR_symbol_table[id1]['type']
        elif (varName in self.class_symbol_table.keys()):
            varKind, varIndex, varType = self.class_symbol_table[id1]['kind'] , self.class_symbol_table[id1]['index'], self.class_symbol_table[id1]['type']
        elif(typ == 'identifier'):
            print('Variable', varName, 'used but was undeclared')
            err_out = 'Declaration error: ' + varName + ' undeclared.'
            open(self.err_file, 'w').write(err_out)

            sys.exit()
        else:
            print('Expected identifier, but got', typ)
            err_out = 'ERROR: Expecting <identifier> but ' + varName + '\n'     
            open(self.err_file, 'w').write(err_out)
            sys.exit()
        self.eat_next()
        return varName, varKind, varType, varIndex
        
    def compileVarName(self):
        #Initially this function had a more useful role, but now it doesn't serve much purpose.
        self.eat_next()


    def compileSubroutineName(self):
        #Initially this function had a more useful role, but now it doesn't serve much purpose.
        self.eat_next()
        
    def compileWhileStatement(self):
        tLabel = self.numLabels
        self.numLabels += 2
        self.Beg('whileStatement')
        self.eat('while')
        self.eat('(')
        self.vmCode += 'label ' + self.class_name + '_' + str(tLabel) + '\n'
        self.compileExpression()
        self.vmCode += 'not\n'
        self.vmCode += 'if-goto ' + self.class_name + '_' + str(tLabel+1) + '\n'
        self.eat(')')
        self.eat ('{')
        self.compileStatements()
        self.eat ('}')
        self.vmCode += 'goto ' + self.class_name + '_' + str(tLabel) + '\n'
        self.vmCode += 'label ' + self.class_name + '_' + str(tLabel+1) + '\n'
        self.End('whileStatement')
        
    
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
            err_out = 'ERROR: Expected <keyword> but ' + tok + '.\n'  
            open(self.err_file, 'w').write(err_out)
            sys.exit()

    def compileLet (self):
        self.Beg('letStatement')
        self.eat('let')
        
        varName, varKind, varType, varIndex =  self.compileVarName1()
         
        if (self.Tokens.curr_token()[1] == '['):
            self.eat('[')
            self.compileExpression()
            self.eat(']')
            if (varKind == 'field'):
                varKind = 'this'
            self.vmCode += 'push ' + varKind + ' ' + str(varIndex) +'\n'
            self.vmCode += 'add\n'
            self.eat('=')
            
            self.compileExpression()
            self.vmCode += 'pop temp 0\n'
            self.vmCode += 'pop pointer 1\n'
            self.vmCode += 'push temp 0\n'
            self.vmCode += 'pop that 0\n'
            self.eat(';')
        else:
            self.eat('=')
            self.compileExpression()
            if (varKind == 'field'):
                varKind = 'this'
            self.vmCode += 'pop ' + varKind + ' ' + str(varIndex) +'\n'
            self.eat(';')

        
        
        self.End('letStatement')
    
    def compileIf (self):
        tLabel = self.numLabels
        self.numLabels += 2

        self.Beg('ifStatement')
        self.eat('if')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')
        self.vmCode += 'not\n'
        self.vmCode += 'if-goto ' + self.class_name + '_' + str(tLabel) + '\n'
        
        self.compileStatements()
        self.eat('}')
        self.vmCode += 'goto ' + self.class_name + '_' + str(tLabel+1) + '\n'
        self.vmCode += 'label ' + self.class_name + '_' + str(tLabel) + '\n'


        if (self.Tokens.curr_token()[1] == 'else'):
            self.eat('else')
            self.eat('{')
            self.compileStatements()
            self.eat('}')

        self.vmCode += 'label ' + self.class_name + '_' + str(tLabel+1) + '\n'

            
        self.End('ifStatement')


    def compileDo (self):
        self.Beg('doStatement')
        self.eat('do')
        self.compileSubroutineCallDo()
        self.eat(';')
        self.End('doStatement')
    def compileReturn (self):
        self.Beg('returnStatement')
        self.eat('return')
        if (self.Tokens.curr_token()[1] != ';'):
            self.compileExpression()
        else:
            self.vmCode += 'push constant 0\n'
        self.eat(';')
        self.vmCode += 'return\n'
        self.End('returnStatement')
    def compileExpression(self):
        self.Beg('expression')
        self.compileTerm()
        opr = '+-*/|=' 
        sop = ['&gt;', '&lt;', '&amp;']
        while (self.Tokens.curr_token()[1] in opr or self.Tokens.curr_token()[1] in sop):
            op = self.op_table[self.Tokens.curr_token()[1]]
            self.eat(self.Tokens.curr_token()[1])
            self.compileTerm()
            self.vmCode += op + '\n'
        self.End('expression')
    
    def compileTerm (self):
        #I have implemented this function slightly differently than in slides.
        #  I have split it's functionality between this function and compileSubroutineTerm.
        self.Beg('term')
        typ, tok = self.Tokens.curr_token()
        if tok in '-~':
            self.eat_next()
            self.compileTerm()
            if (tok == '-'):
                self.vmCode += 'neg\n'
            elif (tok == '~'):
                self.vmCode += 'not\n'
        elif typ == 'integerConstant':
            self.eat(tok)
            self.vmCode += 'push constant ' + str(tok) + '\n'
        elif typ == 'stringConstant':
            self.eat(tok)
            strlen = len(tok)
            self.vmCode += 'push constant ' + str(strlen) + '\n'
            self.vmCode += 'call String.new 1\n'
            for i in range(strlen):
                self.vmCode += 'push constant ' + str(ord(tok[i])) + '\n'
                self.vmCode += 'call String.appendChar 2\n'

        elif typ == 'keyword':
            self.eat_next()
            if tok == 'true':
                self.vmCode += 'push constant 0\n'
                self.vmCode += 'not\n'
            elif tok == 'false' or tok == 'null':
                self.vmCode += 'push constant 0\n'
            elif tok == 'this':
                self.vmCode += 'push pointer 0\n'
            else:
                err_out = 'ERROR: Expecting <keywordConstant> but ' + tok + '\n'     
                open(self.err_file, 'w').write(err_out)
                sys.exit()        
        elif typ == 'identifier':
            ntyp, ntok = self.Tokens.peek_ahead()
            if (ntok == '.' or ntok == '('):
                self.compileSubroutineCallTerm()
            elif (ntok == '['):
                varName, varKind, varType, varIndex = self.compileVarName1()
                if (varKind == 'field'):
                    varKind = 'this'
                self.eat('[')
                self.compileExpression()
                self.vmCode += 'push ' + varKind + ' ' +  str(varIndex) + '\n' #Check next 2 lines, different from slides
                self.vmCode += 'add\n'
                self.vmCode += 'pop pointer 1\n'
                self.vmCode += 'push that 0\n'
               
                self.eat(']')
            else:
                varName, varKind, varType, varIndex = self.compileVarName1()
                if (varKind == 'field'):
                    varKind = 'this'    
                self.vmCode += 'push ' + varKind + ' ' + str(varIndex) + '\n'
            
        elif tok == '(':
            self.eat('(')
            self.compileExpression()
            self.eat(')')
        self.End('term')
    
    def compileSubroutineCallDo(self):
        # self.Beg('subroutineCall')
        typ, tok = self.Tokens.curr_token()
        ntyp, ntok = self.Tokens.peek_ahead()
        id1 = tok
        obKind, obIndex, obType = 0, 0, 0    
        id2 = ''
        if (ntok == '.'):
            self.eat(tok)
            self.eat(ntok)
            __, id2 = self.Tokens.curr_token()
            
            if (id1 in self.subR_symbol_table.keys()):
                obKind, obIndex,obType= self.subR_symbol_table[id1]['kind'] , self.subR_symbol_table[id1]['index'] , self.subR_symbol_table[id1]['type']
                if (obKind == 'field'):
                    obKind = 'this'
                self.vmCode += 'push ' + obKind + ' ' + str(obIndex) + '\n'   
            elif (id1 in self.class_symbol_table.keys()):
                obKind, obIndex,obType = self.class_symbol_table[id1]['kind'] , self.class_symbol_table[id1]['index'], self.class_symbol_table[id1]['type']
                if (obKind == 'field'):
                    obKind = 'this'
                self.vmCode += 'push ' + obKind + ' ' + str(obIndex) + '\n'   
            self.compileSubroutineName()
        else:
            self.eat_next()
            self.vmCode += 'push pointer 0\n'
        
        self.eat('(')
        nP = self.compileExpressionList()
        
        self.eat(')')
        if (ntok == '.'):
            if (obKind != 0):
                self.vmCode += 'call ' + obType + '.' + id2 + ' ' + str(nP+1) + '\n'               
            else:
                self.vmCode += 'call ' + id1 + '.' + id2 + ' ' + str(nP) + '\n'
        else:
            self.vmCode += 'call ' + self.class_name + '.' + id1 + ' ' + str(nP+1) + '\n'
           
            

        self.vmCode += 'pop temp 0\n'
        # self.End('subroutineCall')

    def compileSubroutineCallTerm(self):
         # self.Beg('subroutineCall')
        typ, tok = self.Tokens.curr_token()
        ntyp, ntok = self.Tokens.peek_ahead()
        id1 = tok
        obKind, obIndex, obType = 0, 0, 0       
        if (ntok == '.'):
            self.eat(tok)
            self.eat(ntok)
            __, id2 = self.Tokens.curr_token()
            
            if (id1 in self.subR_symbol_table.keys()):
                obKind, obIndex,obType= self.subR_symbol_table[id1]['kind'] , self.subR_symbol_table[id1]['index'] , self.subR_symbol_table[id1]['type']
                if (obKind == 'field'):
                    obKind = 'this'
                self.vmCode += 'push ' + obKind + ' ' + str(obIndex) + '\n'   
            elif (id1 in self.class_symbol_table.keys()):
                obKind, obIndex,obType = self.class_symbol_table[id1]['kind'] , self.class_symbol_table[id1]['index'], self.class_symbol_table[id1]['type']
                if (obKind == 'field'):
                    obKind = 'this'
                self.vmCode += 'push ' + obKind + ' ' + str(obIndex) + '\n'   
            self.compileSubroutineName()
        else:
            self.eat_next()
            self.vmCode += 'push pointer 0\n'
        
        self.eat('(')
        nP = self.compileExpressionList()
        
        self.eat(')')
        if (ntok == '.'):
            if (obKind != 0):
                self.vmCode += 'call ' + obType + '.' + id2 + ' ' + str(nP+1) + '\n'               
            else:
                self.vmCode += 'call ' + id1 + '.' + id2 + ' ' + str(nP) + '\n'
        else:
            self.vmCode += 'call ' + self.class_name + '.' + id1 + ' ' + str(nP+1) + '\n'
            
            

        # self.End('subroutineCall')

    def compileExpressionList(self):
        self.Beg('expressionList')
        typ, tok = self.Tokens.curr_token()
        numEx = 0
        if (tok != ')'):
            self.compileExpression()
            numEx+=1
            ntyp, ntok = self.Tokens.curr_token()
            while (ntok != ')'):
                self.eat(',')
                self.compileExpression()
                numEx+=1
                ntyp, ntok = self.Tokens.curr_token()
                
             
            
        self.End('expressionList')
        return numEx


for f in args.files:
    #Final output file-name.
    file_name = f[:-5] + ".vm"
    JackAn = CompEngine(f)
    JackAn.compileClass()
    #Gets the compiled vmCode from the compilation engine.
    outp = JackAn.get_vm()
    open(file_name, 'w').write(outp)
    
    #Compilation engine also generates XML output. You can ask for that string by calling the method get_xml.
        

            

        







        





