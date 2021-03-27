#include <stdio.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0
#define MAX_VERTICES 20
#define MAX_ALIST    20

typedef struct{
	int in;
	int out;
}adj_info;

adj_info adj_alist[MAX_ALIST+1];
int edge_count = 0;

int visited[MAX_VERTICES+1];

void graph_init()
{
	int i;
	for (i = 0; i<MAX_ALIST; i++){
		adj_alist[i].in = 0;
		adj_alist[i].out = 0;
	}
	edge_count=0;
}

void insert_edge(int u, int v)
{
	// 간선 정보 u->v
	adj_alist[edge_count].in = u;
	adj_alist[edge_count].out = v;
	edge_count++;
}

// 간단 queue
typedef int element;
int  front, rear;
element  queue[MAX_VERTICES+2];

void init()
{
	front = rear = 0;
}

int is_empty()
{
	return (front == rear);
}

void enqueue(element item)
{
	rear++;
	queue[rear] = item;
}

element dequeue()
{
	front++;
	return queue[front];
}

// BFS 이해가 쉽게 인접 행렬로 구현
void bfs_list(int v)
{
	int w;
	init();
	visited[v] = TRUE;
	printf("%d ", v); 
	enqueue(v);
	while (!is_empty()) {
		v = dequeue();
		for (w = 0; w < edge_count; w++ ){
			if (adj_alist[w].in==v && !visited[adj_alist[w].out]) {
				visited[adj_alist[w].out] = TRUE;
				printf("%d ", adj_alist[w].out);
				enqueue(adj_alist[w].out);
			}
		}
	}
}

main()
{
	int i;

	graph_init();

	insert_edge(1, 9);
	insert_edge(1, 5);
	insert_edge(1, 2);
	insert_edge(2, 3);
	insert_edge(3, 4);
	insert_edge(5, 8);
	insert_edge(5, 6);
	insert_edge(6, 7);
	insert_edge(9, 10);
	bfs_list(1);
}