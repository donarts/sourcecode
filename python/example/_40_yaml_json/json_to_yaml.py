import json
import yaml  # pip install pyyaml
import os


def write_file(filename, data):
    format = ''
    if filename.endswith(".json"):
        format = "json"
    if filename.endswith(".yaml"):
        format = "yaml"
    with open(filename, 'w', encoding='utf-8') as fp:
        if format == 'json':
            json.dump(data, fp)
        elif format == 'yaml':
            yaml.dump(data, fp)
        else:
            fp.write(data)
        fp.close()


def read_file(filename):
    format = ''
    if filename.endswith(".json"):
        format = "json"
    if filename.endswith(".yaml"):
        format = "yaml"
    with open(filename, 'r', encoding='utf-8') as fp:
        if format == 'json':
            ret_data = json.load(fp)
        elif format == 'yaml':
            ret_data = yaml.load(fp, Loader=yaml.FullLoader)
        else:
            ret_data = fp.read()
        fp.close()
        return ret_data
    return None


if __name__ == "__main__":
    # make test file
    a = {"a1": [1, 2, 3], "a2": 2}
    write_file("a.json", a)

    b = {"b1": 1, "b2": [2, 3, 4]}
    write_file("b.json", b)

    want_to_folder_name = "."  # 이곳에 원하는 폴더명을 넣으세요
    dirListing = os.listdir(want_to_folder_name)
    for filename in dirListing:
        if filename.endswith(".json"):
            json_data = read_file(filename)
            replaced = filename.replace(".json", ".yaml")
            write_file(replaced, json_data)
            print(f"convert:{filename}->{replaced}")
