#include <stdio.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0
#define MAX_VERTICES 20

typedef struct AdjNode
{
	int vertex;
	struct AdjNode *link;
} AdjNode;

typedef struct GraphType {
	int n;
	AdjNode *adj_list[MAX_VERTICES];
	int visited[MAX_VERTICES];
} GraphType;

void graph_init(GraphType *g)
{
	int v;
	g->n = 0;
	for (v = 0; v<MAX_VERTICES; v++){
		g->adj_list[v] = NULL;
		g->visited[v] = 0;
	}
}

void insert_vertex(GraphType *g, int v)
{
	if (((g->n) + 1) > MAX_VERTICES) {
		printf("error");
		return;
	}
	g->n++;
}

void insert_edge(GraphType *g, int u, int v)
{
	AdjNode *AdjNode;
	if (u > g->n || v > g->n) {
		printf("error");
		return;
	}
	AdjNode = (struct AdjNode *)malloc(sizeof(AdjNode));
	AdjNode->vertex = v;
	// 이전에 저장된 주소는 제일 마지막에 연결되었던 AdjNode이므로 이 주소를 지금 생성한 AdjNode의 link에 연결하여 인접 리스트를 구성한다.
	AdjNode->link = g->adj_list[u];
	// 새로 추가되는 AdjNode를 adj_list를 이용해서 access 가능하도록 저장
	g->adj_list[u] = AdjNode;

}

#define MAX_QUEUE_SIZE 100
typedef int element;
typedef struct {
	element  queue[MAX_QUEUE_SIZE];
	int  front, rear;
} QueueType;

void error(char *message)
{
	fprintf(stderr, "%s\n", message);
	exit(1);
}

void init(QueueType *q)
{
	q->front = q->rear = 0;
}

int is_empty(QueueType *q)
{
	return (q->front == q->rear);
}

int is_full(QueueType *q)
{
	return ((q->rear + 1) % MAX_QUEUE_SIZE == q->front);
}

void enqueue(QueueType *q, element item)
{
	if (is_full(q))printf("q full");
	q->rear = (q->rear + 1) % MAX_QUEUE_SIZE;
	q->queue[q->rear] = item;
}

element dequeue(QueueType *q)
{
	if (is_empty(q))printf("q empty");
	q->front = (q->front + 1) % MAX_QUEUE_SIZE;
	return q->queue[q->front];
}

void bfs_list(GraphType *g, int v)
{
	AdjNode *w;
	QueueType q;
	init(&q);
	g->visited[v] = TRUE;
	printf("%d ", v); 
	enqueue(&q, v);
	while (!is_empty(&q)) {
		v = dequeue(&q);
		for (w = g->adj_list[v]; w; w = w->link)
			if (!g->visited[w->vertex]) {
				g->visited[w->vertex] = TRUE;
				printf("%d ", w->vertex);
				enqueue(&q, w->vertex);
			}
	}
}

main()
{
	int i;
	GraphType g;

	graph_init(&g);

	for (i = 1; i<=10; i++)
		insert_vertex(&g, i);
	insert_edge(&g, 1, 9);
	insert_edge(&g, 1, 5);
	insert_edge(&g, 1, 2);
	insert_edge(&g, 2, 3);
	insert_edge(&g, 3, 4);
	insert_edge(&g, 5, 8);
	insert_edge(&g, 5, 6);
	insert_edge(&g, 6, 7);
	insert_edge(&g, 9, 10);
	bfs_list(&g, 1);
}