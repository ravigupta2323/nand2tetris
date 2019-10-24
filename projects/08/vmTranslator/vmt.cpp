#include <bits/stdc++.h>

using namespace std;
#define lli int

class _Parser
{
private:
	string input;
	vector <vector <string>> parsed;
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
		// input.erase(remove(input.begin(), input.end(), ' '), input.end());
		// input.erase(remove(input.begin(), input.end(), '\t'), input.end());
		
		//removing multiline comments; lazy to do it right now,
		//lets do it later
		//if you are reading this mutiline comments are not supported

	
		//breaking file into vector of strings
		parsed.clear();
		auto lbegin = input.begin();
		auto lend = input.end();
		if (input.find("\n") != -1)
			lend = input.begin() + input.find("\n");
		int lineno = 0;
		//cout << input;

		while (lbegin != input.end()) {
			
			string temp(lbegin, lend);
			//cout << temp << endl;
			if (temp.find("//") != -1) { 
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
			istringstream bufs(temp);
			vector <string> tempv;

			while (bufs >> temp) {
				tempv.push_back(temp);
			}

			if (tempv.size() > 0) {
				//cout << "i WAS HERE" << endl;
				parsed.push_back(tempv);
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
	
public:
	_Parser (string filepath) {
		if (open(filepath));
		pre_process();
		//Table.Print_table();
	}
	vector <vector <string>> parsed_vec () {
		return parsed;
	}
	int get_lineno (int index) {
		return ind_to_line[index];
	}


};
class assembly_code {
private:
	//static lli loop_no;
	map <string, string> Arithemetic;
	set <string> Comp;
	map <string, string> segment_map1;
	map <string, lli> segment_map2;
	string file_name;
public:
		void __init__ (string fn) {
		Arithemetic["add"] = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n";
		Arithemetic["sub"] = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n";
		Arithemetic["and"] = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n";
		Arithemetic["or"] = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n";
		Arithemetic["neg"] = "@SP\nA=M-1\nM=-M\n";
		Arithemetic["not"] = "@SP\nA=M-1\nM=!M\n";
		Comp.insert("eq");
		Comp.insert("gt");
		Comp.insert("lt");
		segment_map1["argument"] = "ARG";
		segment_map1["local"] = "LCL";
		segment_map1["this"] = "THIS";
		segment_map1["that"] = "THAT";
		segment_map1["local"] = "LCL";
		segment_map2["constant"] = 0;
		segment_map2["pointer"] = 3;
		segment_map2["temp"] = 5;
		segment_map2["static"] = -1;
		file_name = fn.substr(0, fn.find('.'));

	}

	bool isArith (vector <string> s) {
		return s.size() == 1 && Arithemetic.find(s[0])!= Arithemetic.end();
	}
	bool isComp (vector <string> s) {
		return s.size() == 1 && Comp.find(s[0])!= Comp.end();
	}
	bool isPush (vector <string> s) {
		return s.size() == 3 && s[0] == "push";
	} 
	bool isPop (vector <string> s) {
		return s.size() == 3 && s[0] == "pop";	
	}
	bool isPrf (vector <string> s) {
		return s.size() == 2 && (s[0] == "label" || s[0] == "goto" || s[0] == "if-goto");
	}
	bool isFunc (vector <string> s) {
		return s.size() == 3 && s[0] == "function";
	}
	bool isCall (vector <string> s) {
		return s.size() == 3 && s[0] == "call";
	}
	bool isRet (vector <string> s) {
		return s.size() == 1 && s[0] == "return";
	}
	string compins (string in) { 
		static int loop_no = 0;
		for (auto &e:in) e+='A'-'a';
		string temp = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@IFEQ" + to_string (loop_no) + "\nD;J" + in + "\n@SP\nA=M-1\nM=0\n(IFEQ" + to_string (loop_no) + ")\n";
		loop_no++;  
		return temp;
	}

	string pushins (string segment, string ind_string) {
			if (segment_map1.find(segment) != segment_map1.end()) {
				string seg = segment_map1[segment];
				string temp = "@" + ind_string + "\nD=A\n@" + seg + "\nA=M+D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\nA=A+1\n";
				return temp;
			}
			else if (segment_map2.find(segment) != segment_map2.end()) {
				lli ind = stoi(ind_string) + segment_map2[segment];
				string seg = to_string(ind);
				if (segment == "static") {
					seg = file_name + "." + ind_string;
				}
				string temp = "@" + seg + "\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\nA=A+1\n";
				if (segment == "constant")
					temp = "@" + seg + "\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\nA=A+1\n";
				return temp;
			}
			else {
				cout << "Wrong push command Segment Name: " << segment << endl;
				return "\nError while Interpreting\n";
			}
	}
	string popins (string segment, string ind_string) {
			if (segment_map1.find(segment) != segment_map1.end()) {
				string seg = segment_map1[segment];
				string temp = "@" + ind_string + "\nD=A\n@" + seg + "\nD=M+D\n@SP\nM=M-1\nA=M+1\nM=D\nA=A-1\nD=M\nA=A+1\nA=M\nM=D\n";
				return temp;
			}
			else if (segment_map2.find(segment) != segment_map2.end()) {
				lli ind = stoi(ind_string) + segment_map2[segment];
				string seg = to_string(ind);
				if (segment == "static") {
					seg = file_name + "." + ind_string;
				}
				string temp = "@SP\nAM=M-1\nD=M\n@" + seg + "\nM=D\n";
				return temp;
			}
			else {
				cout << "Wrong pop command Segment Name: " << segment << endl;
				return "\nError while Interpreting\n";
			}
	}
	string arithins (string s) {
		return Arithemetic[s];
	}
	string labelins (string ins, string label) {
		// label = file_name + "_" + label; 
		if (ins == "label")
			return "(" + label +  ")\n";
		else if (ins == "goto")
			return "@" + label + "\n0;JMP\n";
		else if (ins == "if-goto") {
			string s = "@SP\nAM=M-1\nD=M\n@";
			s += label + "\nD;JNE\n";

			return s;
		}
	}
	string FuncIns (string f, string lvar) {
		// f = f;
		if (lvar == "0") {
			return 	"(" + f + ")\n";
		}
		string s = "(" + f + ")\n@" + lvar + "\nD=A\n@SP\nAM=M+D\n(LOOP_FOR_" + f + ")\n";
		s += "A=A-1\nD=D-1\nM=0\n@LOOP_FOR_" + f + "\nD;JGT\n";
		return s; 
	}

	string CallIns (string f, string nargs) {
		static int rnum = 0;
		// f = f;
		string s = "@5\n D=A\n @SP\n M=M+D\n D=M-D\n ";
		string ret = "retAddOf_" + f + to_string (rnum);
		s += "@" + ret+ "\n";
		s +=  "D=D+A\n A=D-A\n M=D-A\n D=A+1\n";
		string t = "D=D+M\n A=D-M\n M=D-A\n D=A+1\n";
		s += "@LCL\n" + t;
		s += "@ARG\n" + t;
		s += "@THIS\n" + t;
		s += "@THAT\n" + t;
		s += "@LCL\nM=D\n";
		s += "@" + to_string(5 + stoi (nargs)) + "\nD=D-A\n@ARG\nM=D\n";
		s += "@" + f + "\n0;JMP\n(" + ret + ")\n";		
		rnum++;

		return s;
	}

	string returnIns () {
		string s = "@LCL\nD=M\n@R13\nM=D\n";
		s += "@R13\nD=M\n@5\nA=D-A\nD=M\n@R14\nM=D\n";
		s += "@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n";
		s += "@ARG\nD=M+1\n@SP\nM=D\n";
		s += "@R13\nAM=M-1\nD=M\n@THAT\nM=D\n";
		s += "@R13\nAM=M-1\nD=M\n@THIS\nM=D\n";
		s += "@R13\nAM=M-1\nD=M\n@ARG\nM=D\n";
		s += "@R13\nAM=M-1\nD=M\n@LCL\nM=D\n";
		s += "@R14\nA=M\n0;JMP\n";

		return s;
	}
	void Err (vector <string> v) {
		cout << "Error in " + file_name << endl << "Command:<";
		for (auto e : v) {
			cout << e << " ";
		}
		cout << "> is not recognised.\n";
	}


};



class convert_to_assembly {
private:
	vector <vector <string>> input;
	string output;
	assembly_code ac;

	void run() {
		for (auto in : input) {
			if (ac.isArith(in)) {
				output += ac.arithins(in[0]);
			}
			else if (ac.isComp(in)) {
				output += ac.compins(in[0]);
			}
			else if (ac.isPop(in)) {
				output += ac.popins(in[1], in[2]);
			}
			else if (ac.isPush(in)) {
				output += ac.pushins (in[1], in[2]);
			}
			else if (ac.isPrf(in)) {
				output += ac.labelins(in[0], in[1]);
			}
			else if (ac.isFunc(in)) {
				output += ac.FuncIns(in[1], in[2]);
			}
			else if (ac.isRet(in)) {
				output += ac.returnIns();
			}
			else if (ac.isCall(in)) {
				output += ac.CallIns(in[1], in[2]);
			}
			else {
				ac.Err(in);
			}

		}
	}
public:
	convert_to_assembly (vector <vector <string>> a, string file_name) {
		input = a;
		ac.__init__(file_name);
		run();
		
	}

	string get_out() {
		return output;
	}




};






int main (int argc, char *argv[])
{
	if (argc < 2) {
		cout << "Error: No file name passed\nUsage: ./assembler <INPUT-filepath1> <INPUT-filepath2>....." << endl;
		return -1;		
	}
	
	// if (strcmp (argv[1], argv[2]) == 0)
	// {
	// 	cout << "Warning : Same input and output filepath! Input-File will be overwritten!\n Do you want to continue? (answer in yes or no)" << endl;
	// 	string temp;
	// 	cin >> temp;
	// 	if (temp == "yes");
	// 	else if (temp == "no") return 0;
	// 	else {cout << "Invalid input. Exiting!" << endl;} return -1;

	// }

	string temp;
	bool includeBSC = false;
	cout << "Do you wish to include BootStrap Code in the Assembly file? (y or n)" << endl;
	cin >> temp;
	if (temp == "y")
		includeBSC = true;
	
	string output;
	string out_file_name;

	for (int i = 1; i < argc; i++) {
		string file_name (argv[i]);


		string mod_file_name (file_name.begin(), find(file_name.begin(), file_name.end(), '.'));
		out_file_name = mod_file_name + ".asm";
		auto Parser = _Parser(argv[i]);

		auto intermediate = Parser.parsed_vec();

		convert_to_assembly res (intermediate, mod_file_name);
		output += res.get_out();
	}
	
	if  (includeBSC)
		output = "@261\nD=A\n@0\nM=D\n@1\nM=D\n@2\nM=D\n@3\nM=D\n@4\nM=D\n@Sys.init\n0;JMP\n" + output;
	
	
	
	if (argc > 2) 
		out_file_name = "out.asm";
	
	ofstream file (out_file_name);
	
	file << output << endl;
}


