import sys

def one_open_replace_save(infile,outfile,find_str,replace_str,encoding=None):
	fp = open(infile, 'r', encoding=encoding)
	data = fp.read()
	fp.close()
	
	instr = str(data)
	
	instr = instr.replace(find_str,replace_str)
	
	fp = open(outfile, 'w', encoding=encoding)
	fp.write(instr)
	fp.close()
	
if __name__ == "__main__":
	if len(sys.argv)==6:
		one_open_replace_save(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],encoding=sys.argv[5])
	else:
		print("argment error")
		print("I run one_open_replace_save('9_mul_sub_txt_replace_test_in.txt','9_mul_sub_txt_replace_test_out.txt','Hello','Hi',encoding='utf-8')")
		one_open_replace_save("9_mul_sub_txt_replace_test_in.txt","9_mul_sub_txt_replace_test_out.txt","Hello","Hi",encoding='utf-8')
