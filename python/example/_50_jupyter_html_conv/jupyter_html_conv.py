import sys
import re


def write_file(filename, str_data):
    with open(filename, 'w', encoding="utf-8") as fp:
        fp.write(str_data)
        fp.close()


def read_file(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        ret_data = fp.read()
        fp.close()
        return ret_data
    return None


test_str = \
    """
This is test string 
   --jp-cell-prompt-width: 64px; ->   --jp-cell-prompt-width: 0px;
 <div class="jp-InputPrompt jp-InputArea-prompt">In&nbsp;[93]:</div> => remove
 <div class="jp-OutputPrompt jp-OutputArea-prompt">Out[93]:</div> => remove
"""


def conv_main(strdata):
    pattern_re = r'<div class="jp-InputPrompt jp-InputArea-prompt">[\w\d\&\;\[\]\:]*<\/div>' \
                 '|<div class="jp-OutputPrompt jp-OutputArea-prompt">[\w\d\&\;\[\]\:]*<\/div>'
    ret = re.sub(pattern_re, "", strdata)
    ret = ret.replace("--jp-cell-prompt-width: 64px;", "--jp-cell-prompt-width: 0px;")
    return ret


if __name__ == "__main__":
    input_file_name = "dataframe.html"
    if len(sys.argv) != 2:
        print(sys.argv)
    else:
        input_file_name = sys.argv[1]
    print(conv_main(test_str))
    print(f"input file:{input_file_name}")
    indata = read_file(input_file_name)
    indata = conv_main(indata)
    write_file(input_file_name+".html", indata)
