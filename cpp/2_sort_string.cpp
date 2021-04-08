
#include <stdio.h>

#define N_MAX 10

char data[N_MAX][80]={
	"hello","abc","a","cdef","cdef","zzzz","bbb","ba","bc","ab"
	};

int diff(char *a,char *b){
	int i;
	for(i=0;;i++){
		if(a[i]==0 && b[i]==0)return 0;
		if(a[i]==0)return -1;
		if(b[i]==0)return 1;
		if(a[i]-b[i]>0)return 1;
		if(a[i]-b[i]<0)return -1;
	}
	return 0;
}
void cpy(char *dst,char *src)
{
	int i;
	for(i=0;;i++){
		dst[i] = src[i];
		if(dst[i]==0)break;
	}
}
void swap(int i,int j)
{
	char temp[80];
	cpy(temp,data[i]);
	cpy(data[i],data[j]);
	cpy(data[j],temp);
}

void print()
{
	int i;
	for(i=0;i<N_MAX;i++){
		printf("%s\n",data[i]);
	}
}

int main()
{
	int i,j;
	for(i=0;i<N_MAX;i++){
		for(j=i+1;j<N_MAX;j++){
			if(diff(data[i],data[j])>0){
				swap(i,j);
			}
		}
	}
	
	print();
	return 0;
}