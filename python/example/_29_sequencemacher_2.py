from difflib import SequenceMatcher

def get_diff_colored(string1,string2,diff_color):
	reta = ""
	retb = ""
	
	s = SequenceMatcher(None,string1,string2)
	
	for tag,i1,i2,j1,j2 in s.get_opcodes():
		if tag=='equal':
			reta += string1[i1:i2]
			retb += string2[j1:j2]
		else:
			reta += '<span style="color:rgb('+diff_color+');">'+string1[i1:i2]+'</span>'
			retb += '<span style="color:rgb('+diff_color+');">'+string2[j1:j2]+'</span>'
			
	return [reta,retb]

def change_dspace_to_space(string_data):
	while True:
		slen = len(string_data)
		string_data = string_data.replace("  "," ")
		if len(string_data)==slen:
			return string_data

if __name__ == '__main__':
	ret = get_diff_colored("    Hallo   God    Monin  123,  12312, 123,   123,  12312","Hello Good Morning 123 12312,123,123,2312","255,0,0")
	print("<html><body>")
	print(ret[0])
	print("<BR>")
	print(ret[1])
	ret = get_diff_colored(change_dspace_to_space("    Hallo   God    Monin  123,  12312, 123,   123,  12312"),change_dspace_to_space("Hello Good Morning 123 12312,123,123,2312"),"255,0,0")
	print("<BR>")
	print("<BR>")
	print(ret[0])
	print("<BR>")
	print(ret[1])
	print("</body></html>")
