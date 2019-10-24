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


int main (void) {
	lli n;
	cin >> n;

	cout << toBinary (n) << endl;

}