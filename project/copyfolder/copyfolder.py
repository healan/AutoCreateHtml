import os, sys, time
import shutil
from distutils.dir_util import copy_tree
import errno
import filecmp


def get_dir_size(path):
    total = 0
    for p in os.listdir(path):
        full_path = os.path.join(path, p)
        if os.path.isfile(full_path):
            total += os.path.getsize(full_path)
        elif os.path.isdir(full_path):
            total += get_dir_size(full_path)
    return total

if __name__ == '__main__':
    argument = sys.argv
    del argument[0]			
    from_folder = argument[0]
    dest_folder = argument[1]

    path = '/NAS2/KHL/copyfolder/'
    from_path = path + from_folder
    dest_path = path + dest_folder

    try:
        copy_tree(from_path, dest_path)
        a_cnt = len(os.listdir(from_path))
        b_cnt = len(os.listdir(dest_path))
        a_size = get_dir_size(from_path) 
        b_size = get_dir_size(dest_path)
        print(a_cnt, b_cnt, a_size, b_size)

        # 폴더 검증
        # diff = filecmp.dircmp(from_path, dest_path).report()
        # print(diff)
        files = os.listdir(from_path)

        if a_cnt == b_cnt:
            for i in range(0, a_cnt-1):
                a_file_date = time.ctime(os.path.getmtime(from_path + '/' +files[i]))
                b_file_date = time.ctime(os.path.getmtime(dest_path + '/' +files[i]))
                
                a_file_size = os.path.getsize(from_path + '/' +files[i])
                b_file_size = os.path.getsize(dest_path + '/' +files[i])

                if a_file_date == b_file_date:
                    if a_file_size == b_file_size:
                        pass
                    else:
                        print('please check filesize')
                        break

                else:
                    print('please check filedate')
                    break
        else:
            print('please check filecount.')

    except OSError as err:
        if err.errno == errno.ENOTDIR:
            shutil.copy2(from_path, dest_path)
        else:
            print("Error: % s" % err)

   
