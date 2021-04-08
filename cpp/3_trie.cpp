#include <stdio.h>

#define ALPHA 26
#define MAX_TRIE_VERTEX 100

typedef struct {
	int child[ALPHA];
	int done;
}trie_type;

trie_type trie[MAX_TRIE_VERTEX];
int trie_count = 1;

int init()
{
	int i,j;
	trie_count = 1; // for root node
	for(i=0;i<MAX_TRIE_VERTEX;i++){
		for(j=0;j<ALPHA;j++){
			trie[i].child[j] = 0;
		}
		trie[i].done = 0;
	}
}

void trie_insert(const char data[])
{
	int i;
	int node_vertex = 0; // 0 : root node
	int next_node_vertex = 0;
	for(i=0;;i++){
		if (data[i]==0) break;
		
		next_node_vertex = trie[node_vertex].child[data[i]-'a'];
		if( next_node_vertex == 0 ){
			// empty chiled need to add
			trie[node_vertex].child[data[i]-'a'] = trie_count;
			node_vertex = trie_count;
			trie_count++;
		}else{
			node_vertex = next_node_vertex;
		}
	}
	if(node_vertex!=0){
		// string end
		trie[node_vertex].done = 1;
	}
}

int trie_search(const char data[])
{
	int i;
	int node_vertex = 0; // 0 : root node
	int next_node_vertex = 0;
	for(i=0;;i++){
		if (data[i]==0) break;
		
		next_node_vertex = trie[node_vertex].child[data[i]-'a'];
		if( next_node_vertex == 0 ){
			// empty child 
			return 0;
		}else{
			node_vertex = next_node_vertex;
		}
	}
	if(node_vertex!=0){
		if (trie[node_vertex].done==1) return 1;
	}
	return 0;
}

int main()
{
	init();
	trie_insert("abc");
	trie_insert("ksg");
	trie_insert("abefg");
	trie_insert("tg");
	
	printf("%d\n",trie_search("abf"));//0
	printf("%d\n",trie_search("ksg"));//1
	printf("%d\n",trie_search("abdfg"));//0
	printf("%d\n",trie_search("abefg"));//1
	printf("%d\n",trie_search("ab"));//0
}
