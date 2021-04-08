
#include <stdio.h>

#define N_MAX 10

int data[]={9,3,1,4,5,3,4,6,2,4};

void swap(int i,int j)
{
	int temp;
	temp = data[i];
	data[i]=data[j];
	data[j]=temp;
}

void print()
{
	int i;
	for(i=0;i<N_MAX;i++){
		printf("%d ",data[i]);
	}
	printf("\n");
}

int main()
{
	int i,j;
	for(i=0;i<N_MAX;i++){
		for(j=i+1;j<N_MAX;j++){
			if(data[i]>data[j]){
				swap(i,j);
			}		 
		}
	}
	
	print();
	return 0;
}