import os
import shutil


def recursive_searching_dir(depth,
                            search_path,
                            cb_fun):
    abs_path = os.path.abspath(search_path)
    full_file_list = []
    base_file_list = []
    full_folder_list = []
    base_folder_list = []
    all_list = os.listdir(abs_path)
    for file_name in all_list:
        full_path = os.path.join(abs_path, file_name)
        if os.path.isdir(full_path):
            full_folder_list.append(full_path)
            base_folder_list.append(file_name)
        elif os.path.isfile(full_path):
            full_file_list.append(full_path)
            base_file_list.append(file_name)
    cb_fun(depth, abs_path, base_file_list,
           full_file_list, base_folder_list,
           full_folder_list)

    for folder in full_folder_list:
        recursive_searching_dir(depth + 1, folder, cb_fun)


def print_filename_cb(depth,
                      abs_path,
                      base_file_list,
                      full_file_list,
                      base_folder_list,
                      full_folder_list):
    print(f"depth #{depth} //{abs_path}")
    print(f"base_file_list:{base_file_list}")
    print(f"full_file_list:{full_file_list}")
    print(f"base_folder_list:{base_folder_list}")
    print(f"full_folder_list:{full_folder_list}")
    print("\n")


def searching_filename_cb(depth,
                          abs_path,
                          base_file_list,
                          full_file_list,
                          base_folder_list,
                          full_folder_list):
    print(f"depth #{depth} //{abs_path}")
    print(f"base_file_list:{base_file_list}")
    print(f"full_file_list:{full_file_list}")
    for fn in base_file_list:
        if fn.startswith("a"):
            print("!!! find !!!:" + fn)

    print("\n")


def makefolder(folder_name):
    if folder_name != '' and \
            not os.path.exists(folder_name):
        os.makedirs(folder_name)


def write_file(filename, str_data):
    with open(filename, 'w') as fp:
        fp.write(str_data)
        fp.close()


if __name__ == "__main__":
    shutil.rmtree("temp", ignore_errors=True)
    makefolder("temp/a/b/c/d")
    makefolder("temp/b/e/f")
    makefolder("temp/g/h")
    write_file("temp/a/abc.txt", "Hello ABC")
    write_file("temp/b/e/f/acc.txt", "Hello ACC")

    recursive_searching_dir(0, ".", print_filename_cb)
    recursive_searching_dir(0, ".", searching_filename_cb)

    shutil.rmtree("temp", ignore_errors=True)

