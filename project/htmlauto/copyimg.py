import os
import sys
import stat
import re
from PIL import Image
import shutil


# 두개 인자 값 받음 (이미지 구분 확장자, 결과 html 파일명)
if __name__ == '__main__':

    before_path = "/NAS2/KHL/before/"
    after_path = "/NAS2/KHL/after/"

    beforeList = os.listdir(before_path)
    afterList = os.listdir(after_path)

    for j in range(0, len(beforeList)):
        c_f = len(beforeList)
        from_path = before_path+beforeList[j]
        to_path = from_path.split('_')[0]+'_'+str(c_f+j)+'.jpg'
        print('f:', from_path)
        print('t:', to_path)
        # shutil.copyfile(from_path, to_path)
