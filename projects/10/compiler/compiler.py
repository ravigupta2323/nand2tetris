import re
import argparse

ArgPar = argparse.ArgumentParser()
ArgPar


symbol_list = ['(', ')', '{', '}', '[', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurrence single-line comments (//COMMENT\n ) from string
    return string

def Tokenize(string):
    reglist = r'(\()|(\))|(\{)|(\})|(\[)|(\.)|(\,)|(\;)|(\+)|(\-)|(\*)|(\/)|(\&)|(\|)|(\<)|(\>)|(\=)|(\~)|\ '
    a = list(re.split(reglist, string))
    b = [x for x in a if x != None and x!='']
    return b


# # symbol_list = ['(', ')', '{', '}', '[', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
# # e = '\\'   

# # reglist = ""
# # for x in symbol_list:
# #     reglist = reglist +  '(' + e + x + ')' + '|'

# # reglist = r'(\()|(\))|(\{)|(\})|(\[)|(\.)|(\,)|(\;)|(\+)|(\-)|(\*)|(\/)|(\&)|(\|)|(\<)|(\>)|(\=)|(\~)|\ '

# # a = list(re.split(reglist, inputfile))
# # b = [x for x in a if x != None and x!='']



