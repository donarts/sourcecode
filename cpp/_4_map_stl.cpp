// g++ _4_map_stl.cpp
#include <map>
#include <iostream>
#include <string>

using namespace std;


int test1()
{
	// defination key type, value type
	map<int, float> mTest;
	
	// Add item
	mTest.insert(make_pair(1,1.1));
	mTest.insert(make_pair(1,2.1));
	mTest.insert(make_pair(50,3.1));
	mTest[50]=4.11; // 갱신 가능
	mTest.insert(make_pair(50,5.1)); // 갱신이 일어나지 않음
	
	cout << "mTest[50]:" << mTest[50] << endl;
	cout << "mTest.find(50)->first:" << mTest.find(50)->first << endl;
	cout << "mTest.find(50)->second:" << mTest.find(50)->second << endl;
	
	return 0;
}

int test2()
{
	// defination key type, value type
	map<int, float> mTest;
	
	// Add item
	mTest.insert(make_pair(1,1.1));
	mTest.insert(make_pair(1,2.1));
	mTest.insert(make_pair(50,3.1));
	mTest[50]=4.11; // 갱신 가능
	mTest.insert(make_pair(50,5.1)); // 갱신이 일어나지 않음
	
	map<int, float>::iterator iter;
	for(iter = mTest.begin() ; iter!=mTest.end();iter++){
		cout << "iter->first:" << iter->first << endl;
		cout << "iter->second:" << iter->second << endl;
	}
	
	return 0;
}

int test3()
{
	{
		map<const char*, float> mTest;
		
		mTest["abc"]=1.11;
		mTest["ab"]=2.11;
		mTest["bbb"]=3.11;
		
		cout << mTest["ab"] << endl;
	}
	{
		map<char*, float> mTest;
		
		mTest[(char *)"abc"]=1.11;
		mTest[(char *)"ab"]=2.11;
		mTest[(char *)"bbb"]=3.11;
		
		cout << mTest[(char *)"ab"] << endl;
		
		char buf[20];
		buf[0]='a';
		buf[1]='b';
		buf[2]=0;
		cout << buf << endl;
		cout << mTest[buf] << endl;
	}
	
	return 0;
}

int test4()
{
	{
		map<string, float> mTest;
		
		mTest[string("abc")]=1.11;
		mTest[string("ab")]=2.11;
		mTest[string("bbb")]=3.11;
		
		char buf[20];
		buf[0]='a';
		buf[1]='b';
		buf[2]=0;
		cout << buf << endl;
		cout << mTest[string(buf)] << endl;
	}

	return 0;
}
int main()
{
	test1();
	test2();
	test3();
	test4();
	return 0;
}