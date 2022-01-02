#include <string>
#include <iostream> 

using namespace std;

int main()
{
    string str("Hello World!!");
    string str2("Wor");
 
    size_t found = str.find(str2);
    if (found != string::npos)
        cout << "first 'Wor' found at: " << found << '\n';

    str.replace(str.find(str2), str2.length(), "XXX");
    cout << str << '\n';

    return 0;
}
