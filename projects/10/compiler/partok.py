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



