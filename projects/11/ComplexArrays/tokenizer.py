import re
import argparse
import sys

# rgPar = argparse.ArgumentParser()
class Tokenizer:

    def __init__(self, jack_code, err):
        self.err_file = err
        self.curr_count = 0
        self.symbol_list = ['(', ')', '{', '}', '[',']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        self.keyword_list = ['class', 'method', 'function', 'constructor', 'int', 'boolean', 'char', 'void', 'var', 'static', 'field', 'let', 'do', 'if', 'else', 'while', 'return', 'true', 'false', 'null', 'this']
        # print(self.keyword_list)
        cleaned_code = self.removeComments(jack_code)
        self.initial_tokens = self.iTokenize(cleaned_code)
        self.tokens = []
        a = self.__next_token()
        while (a != None):
            self.tokens.append(a)
            a = self.__next_token()
        self.curr_count = 0

    
    
    @staticmethod
    def isIdentifier (s):
        #Checks for valid Identifier.
        isVarRe = re.compile(r'[a-zA-Z_]\w*')
        if (isVarRe.match(s)):
            return isVarRe.match(s).group()==s
        else:
            return False
    
    @staticmethod
    def isInt (s):
        #Checks for valid int.
        isInt = re.compile(r'-?[0-9]+')
        a = isInt.match(s)
        if (a):
            return s == isInt.match(s).group()
        else:
            return False
    
    @staticmethod
    def removeComments(string):
        string = re.sub(re.compile(r"/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile(r"//.*?\n" ) ,"" ,string) # remove all occurrence single-line comments (//COMMENT\n ) from string
        return string

    @staticmethod
    def iTokenize(string):
        #Split at delimiters using Regular Expressions.
        reglist = r'(\()|(\))|(\{)|(\})|(\[)|(\])|(\.)|(\,)|(\;)|(\+)|(\-)|(\*)|(\/)|(\&)|(\|)|(\<)|(\>)|(\=)|(\~)|(\s)|\n|(")'
        a = list(re.split(reglist, string))
        b = [x for x in a if x != None and x!='' and x!='\n']
        return b

    def hasMoreTokens(self):
        return self.curr_count < len(self.tokens)
    def __next_token (self):
        
        # Handles strings seperately as they have different delimiters rules.
        if (self.curr_count < len(self.initial_tokens)):
            if (self.initial_tokens[self.curr_count] == '\"' ):
                s = ''
                self.curr_count += 1
                while (self.initial_tokens[self.curr_count] != '\"'):
                    s = s + self.initial_tokens[self.curr_count]
                    self.curr_count+=1
                self.curr_count+=1
                return 'stringConstant', s
                

            elif (self.initial_tokens[self.curr_count].isspace()):
                self.curr_count+=1
                return self.__next_token()
                
            else:
                self.curr_count+=1
                return self.TokenType(self.initial_tokens[self.curr_count-1])

        else:
            return None
    
    def next_token (self):
        if (self.curr_count < len(self.tokens)):
            self.curr_count+=1
            return self.tokens[self.curr_count-1]

        else:
            return None
    def curr_token (self):
        if (self.curr_count < len(self.initial_tokens)):
            return self.tokens[self.curr_count]
        else:
            return None
    def peek_ahead(self):
        #Allows 1 token look-ahead. (Due to LL1 Jack Grammar)
        if (self.curr_count+1 < len(self.initial_tokens)):
            return self.tokens[self.curr_count+1]
        else:
            return None


    def partial_token(self):
        return self.initial_tokens
    def eat (self, s):
        # This functions checks whether the next token is the one expected or not. If not it throws error.
        typ, token = self.next_token()
        if (token == s):
            return typ
        else:
            extyp = self.TokenType(s)[0]
            if (extyp == typ):
                err_out = 'ERROR: ' + token + '\n'
            else:
                err_out = 'ERROR: Expecting <' + extyp  + '> but ' + token + '\n'     
                
            open(self.err_file, 'w').write(err_out)
            sys.exit()

            return False

    def TokenType (self, s):
        # returns token type
        if (s in self.keyword_list):
            return "keyword", s
        elif (s in self.symbol_list):
            if s == '<':
                s = '&lt;'
            elif s == '>':
                s = '&gt;'
            elif s == '\"':
                s = '&quot;'
            elif s == '&':
                s = '&amp;'
            
            return "symbol", s
        elif (self.isIdentifier(s)):
            return "identifier", s
        elif (self.isInt(s)):
            return "integerConstant", s
        else:

            err_out = 'ERROR: Invalid token ' + s + '\n' 
                
            open(self.err_file, 'w').write(err_out)
            sys.exit()
            return False

      

