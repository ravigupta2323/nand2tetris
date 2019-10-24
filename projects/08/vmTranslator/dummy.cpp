#include <bits/stdc++.h>

using namespace std;
#define lli short



string toBinary(int n)
{
    std::string r;
    while(n!=0) {r=(n%2==0 ?"0":"1")+r; n/=2;}
    r = "000000000000000000" + r;
    string temp (r.end()-16, r.end());
	return temp;
}


//this class maintains a symbol table and functions to manipulate it. 
class Symbol_table {
private:
	unordered_map <string, int> Table = 
	{
		{"SP", 0},
		{"LCL", 1},
		{"ARG", 2},
		{"THIS", 3},
		{"THAT", 4},
		{"R0", 0},
		{"R1", 1},
		{"R2", 2},
		{"R3", 3},
		{"R4", 4},
		{"R5", 5},
		{"R6", 6},
		{"R7", 7},
		{"R8", 8},
		{"R9", 9},
		{"R10", 10},
		{"R11", 11},
		{"R12", 12},
		{"R13", 13},
		{"R14", 14},
		{"R15", 15},
		{"SCREEN", 16384},
		{"KBD",24576},
	};
	int curr_var_add = 16;
public:
	Symbol_table() {

	};
	int insert (string s, int add) {
		if (Table.find(s) == Table.end())
		{
			Table[s] = add;		
		}
		else
		{
			cout << "Error:You tried insert an already existing element in the Symbol Table" << endl;
			cout << "Check: You code likely has multiple places where (" << s << ") exists. Or you are trying to use reserved sysmbol" << endl;
		}
	}
	int get(string s) {
		if (Table.find(s) == Table.end())
		{
			Table[s] = curr_var_add++;		
		}
		return Table[s];
	}
	// void Print_table () {
	// 	for (auto &l : Table)
	// 		cout << l.first <<" : " << l.second << endl;
	// }

};


//class preprocesses the input file.
class _Parser
{
private:
	string input;
	vector <string> parsed;
	vector <int> ind_to_line;
	bool open (string filepath) {
		ifstream file(filepath);
		if (file.is_open ()) {
			input.clear();
			ostringstream ss;
			ss << file.rdbuf();
			input = ss.str();
			//cout << input << endl;
			return true;
		}
		else {
			cout << "Error in opening file!\nCheck if the filepath passed is correct!";
			return false;
		}
	}
	
	void pre_process() {
		
		// removes all whitespaces 
		input.erase(remove(input.begin(), input.end(), ' '), input.end());
		input.erase(remove(input.begin(), input.end(), '\t'), input.end());
		
		//removing multiline comments; lazy to do it right now,
		//lets do it later
		//if you are reading this mutiline comments are not supported
		{ 
		}

	
		//breaking file into vector of strings
		parsed.clear();
		auto lbegin = input.begin();
		auto lend = input.end();
		if (input.find("\n") != -1)
			lend = input.begin() + input.find("\n");
		int lineno = 0;
		//cout << input;


		while (lbegin != input.end()) {
			
			string temp(lbegin, lend-1);
			//cout << temp << endl;
			if (temp.size() == 0)
			{
				lineno++;
				lbegin = lend + 1;
				lend = input.begin() + input.find("\n", lend-input.begin()+1);
				continue;
			}

		
			if (temp.find("/") != -1) { 
				string temp2 (temp.begin(), temp.begin() + temp.find("//"));
				temp = temp2;
			}
			if (temp.size() == 0)
			{
				lineno++;
				lbegin = lend + 1;
				lend = input.begin() + input.find("\n", lend-input.begin()+1);
				continue;
			}
			
			//cout << temp << endl;
			if (temp[0] == '(')
			{	
				if (temp.size() < 3)
					cout << "Error: Wrong statement at line" << lineno << endl;
				string temp2 (temp.begin() + 1, temp.end() - 1);
				Table.insert(temp2, parsed.size());

			}
			else {
				
				//cout << "i WAS HERE" << endl;
				parsed.push_back(temp);
				ind_to_line.push_back(lineno);
			}
			lineno++;
			lbegin = lend + 1;
			if (input.find("\n") != -1)
				lend = input.begin() + input.find("\n", lend-input.begin()+1);			
			else
				lend = input.end();
		}

	}
	void print_parsed (void){
		//cout << parsed.size();
		for (auto &l : parsed)
			cout << l << endl;
	}
public:
	_Parser (string filepath) {
		open (filepath);
		pre_process();
		//Table.Print_table();
	}
	_Parser (const _Parser & p) {
		input = p.input;
		parsed = p.parsed;
		ind_to_line = p.ind_to_line;
		Table = p.Table;
	}
	Symbol_table Table = Symbol_table();
	vector <string> get_vec () {
		return parsed;
	}
	int get_lineno (int index) {
		return ind_to_line[index];
	}

};

//the class converts instructions to binary.
class Instructions {
private:	
	_Parser parser;
	vector <string> in;
	vector <string> out;
	int index = 0;
	unordered_map <string, string> ALU_table = 
	{
		{"0", "101010"},
		{"1", "111111"},
		{"-1", "111010"},
		{"D", "001100"},
		{"A", "110000"},
		{"!D", "001101"},
		{"!A", "110001"},
		{"-D", "001111"},
		{"-A", "110011"},
		{"D+1", "011111"},
		{"1+D", "011111"},
		{"A+1", "110111"},
		{"1+A", "110111"},
		{"D-1", "001110"},
		{"A-1", "110010"},
		{"D+A", "000010"},
		{"A+D", "000010"},
		{"D-A", "010011"},
		{"A-D", "000111"},
		{"D&A", "000000"},
		{"A&D", "000000"},
		{"D|A", "010101"},
		{"A|D", "010101"},
	};
	



	bool is_A_ins (string s)
	{
		return (s[0] == '@');
	}

	void A_ins (string s) {
		string temp (s.begin() + 1, s.end());
		//out.push_back(temp);
		if (isdigit(s[1]))
			out.push_back(toBinary(stoi(temp)));
		else
			out.push_back(toBinary(parser.Table.get(temp)));
	}
	bool is_C_ins (string s)
	{
		if (s.find(";") != -1 || s.find("=") != -1)
			return true;
		else
			return false;
	}
	string ALU_ins (string s) {
		string temp;
		if (s.find("M") == -1)
		{
			temp = "0";
			if (ALU_table.find (s) != ALU_table.end())
			temp += ALU_table[s];
			else {
				cout << "1-Invalid C Instruction at line ";
				cout << parser.get_lineno(index);
				cout << "; ALU input <" << s << "> not recognized; ";
				cout << endl;
			}
		}
		else {
			temp = "1";
			replace(s.begin(), s.end(), 'M', 'A');
			if (ALU_table.find (s) != ALU_table.end())
			temp += ALU_table[s];
			else {
				replace(s.begin(), s.end(), 'A', 'M');
				cout << "2-Invalid C Instruction at line ";
				cout << parser.get_lineno(index);
				cout << "; ALU input <" << s << "> not recognized; ";
				cout << endl;
			}	
		}
		return temp;
	}
	string jump_ins (string s) {
		string temp (3, '0');
		if (s.size() == 0)
			return "000";
		else if (s[0] != 'J') {
			cout << "3-Invalid Jump Instruction at line ";
			cout << parser.get_lineno(index);
			cout << "; Jump instruction <" << s << "> not recognized; ";
			cout << endl;
		}
		else {
			
			if (s.find("E") != -1)
				temp[1] = '1';
			if (s.find("G") != -1)
				temp[2] = '1';
			if (s.find("L") != -1)
				temp[0] = '1';
			if (s == "JNE")
				temp = "101";
			if (s == "JMP")
				temp ="111";			
		}
		return temp;
	}
	string dest_ins (string s) {
		string temp (3, '0');
		if (s.size() == 0)
			return "000";
		if (s.find("M") != -1)
			temp[2] = '1';
		if (s.find("D") != -1)
			temp[1] = '1';
		if (s.find("A") != -1)
			temp[0] = '1';

		return temp;
	}
	void C_ins (string s) {
		string::iterator ALUib = s.begin(),ALUie = s.end(), desti = s.begin(), jumpi = s.end();
		
		if (s.find(";")!= -1) {
			jumpi = s.begin() + s.find(";") + 1;
			ALUie = s.begin() + s.find(";");
		}
		if (s.find("=") != -1) {
			desti = s.begin() + s.find("="); 
			ALUib = s.begin() + s.find("=") + 1;
		}

		string dest (s.begin(), desti);
		string jump (jumpi, s.end());
		string ALU (ALUib, ALUie);

		out.push_back("111"+ ALU_ins(ALU) + dest_ins(dest) + jump_ins(jump));
	
	}
public:
	Instructions (_Parser inputs) : parser (inputs)
	{
		in = inputs.get_vec();
	}
	vector <string> get_output () {
		for (auto elem: in)
		{
			index++;
			if (is_A_ins(elem)) 
				A_ins(elem);
			else if (is_C_ins(elem))
				C_ins(elem);
			else{
				cout << "4-Invalid Instruction at line ";
				cout << parser.get_lineno(index);
				cout << "ALU input not recognized" << endl;
				cout << elem << endl;

			}
		}
		return out;
	}


};



int main (int argc, char *argv[])
{
	if (argc < 3) {
		cout << "Error: No file name passed\nUsage: ./assembler <INPUT-filepath> <OUTPUT-filepath>" << endl;
		return -1;		
	}
	
	if (strcmp (argv[1], argv[2]) == 0)
	{
		cout << "Warning : Same input and output filepath! Input-File will be overwritten!\n Do you want to continue? (answer in yes or no)" << endl;
		string temp;
		cin >> temp;
		if (temp == "yes");
		else if (temp == "no") return 0;
		else {cout << "Invalid input. Exiting!" << endl;} return -1;

	}
	auto Parser = _Parser(argv[1]);
	auto ins = Instructions(Parser);
	auto out = ins.get_output();

	

	ofstream out_file (argv[2]);
	for (auto elem : out)
		out_file << elem << endl;
	
}


