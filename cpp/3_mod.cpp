// mod
#include <stdio.h>

#define MOD 34541

void test1()
{
	int i,a,b;
	for(i=0;i<0x7ffffff0;i++){
		a = (i*34500)%MOD;
		b = ((i%MOD)*34500)%MOD;
		if (a!=b) {
			printf("t1 i=%d, %d %d\n",i,a,b);
			printf("error\n");
			break;
		}
	}
}
void test2()
{
	unsigned int i,a,b;
	for(i=0;i<0x7ffffff0;i++){
		a = (i*34500)%MOD;
		b = ((i%MOD)*34500)%MOD;
		if (a!=b) {
			printf("t2 i=%d, %d %d\n",i,a,b);
			printf("error\n");
			break;
		}
	}
}
int main()
{
	printf("%d\n",sizeof(int));
	test1();
	test2();
	return 0;
}
