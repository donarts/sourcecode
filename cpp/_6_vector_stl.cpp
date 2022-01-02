#include <iostream>
#include <vector>

using namespace std;

int test1()
{
    vector <int> v;

    v.push_back(10);
    v.push_back(20);
    v.push_back(30);
    v.at(0) = 40;
    v[1] = 50;

    int nsize = v.size();
    cout << "size:" << nsize << endl;
    cout << "v = { ";
    for (int i=0 ; i < nsize ; i++) {
        cout << v[i] << ", ";
    }
    cout << "};" << endl;
    return 0;
}
int test2()
{
    vector <int> v;

    v.push_back(10); // index 0
    v.push_back(20); // index 1
    v.push_back(30); // index 2
    cout << "vsize:" << v.size() << endl;
    v[3] = 50;
    cout << "vsize:" << v.size() << " v[3]:" << v[3] << endl;
    v.at(3) = 40;
    cout << "vsize:" << v.size() << " v[3]:" << v[3] << endl;

    int nsize = v.size();
    cout << "size:" << nsize << endl;
    cout << "v = { ";
    for (int i=0 ; i < nsize ; i++) {
        cout << v[i] << ", ";
    }
    cout << "};" << endl;
    return 0;
}
int main()
{
    test1();
    test2();
    return 0;
}