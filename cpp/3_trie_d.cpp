#include <stdio.h>
#include <stdlib.h>

#define ALPHA 26

typedef struct trie_type_s{
	struct trie_type_s *child[ALPHA];
	int done;
}trie_type;

trie_type trie;

void dfs_free(trie_type *node)
{
	int i;
	trie_type *cur_node = node;
	trie_type *child_node;
	for(i=0;i<ALPHA;i++){
		child_node = cur_node->child[i];
		if( child_node != 0 ){
			dfs_free(child_node);
		}
	}
	if( &trie==cur_node ){
		for(i=0;i<ALPHA;i++){
			cur_node->child[i] = 0;
		}
		cur_node->done = 0;
	}else{
		free(cur_node);
	}
}

int init()
{
	dfs_free(&trie);
	return 0;
}

void trie_insert(const char data[])
{
	int i;
	trie_type *cur_node = &trie;
	trie_type *next_node;
	for(i=0;;i++){
		if (data[i]==0) break;
		
		next_node = cur_node->child[data[i]-'a'];
		if( next_node == 0 ){
			// empty child need to add
			trie_type *new_node = (trie_type *)malloc(sizeof(trie_type));
			cur_node->child[data[i]-'a'] = new_node;
			for(int j=0;j<ALPHA;j++){
				new_node->child[j]=0;
			}
			new_node->done = 0;
			cur_node = new_node;
		}else{
			cur_node = next_node;
		}
	}
	if(cur_node!=&trie){
		// string end
		cur_node->done = 1;
	}
}

int trie_search(const char data[])
{
	int i;
	trie_type *cur_node = &trie;
	trie_type *next_node;
	for(i=0;;i++){
		if (data[i]==0) break;
		
		next_node = cur_node->child[data[i]-'a'];
		if( next_node == 0 ){
			// empty child 
			return 0;
		}else{
			cur_node = next_node;
		}
	}
	if(cur_node!=&trie){
		if (cur_node->done==1) return 1;
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
	
	init();
	trie_insert("abcadfae");
	trie_insert("ksasdfg");
	trie_insert("abadfefg");
	trie_insert("tgadf");
	
	printf("%d\n",trie_search("abf"));//0
	printf("%d\n",trie_search("ksasdfg"));//1
	printf("%d\n",trie_search("abdfg"));//0
	printf("%d\n",trie_search("abadfefg"));//1
	printf("%d\n",trie_search("ab"));//0
	
	init();
}
