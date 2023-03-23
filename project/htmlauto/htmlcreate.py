import os
import sys
import stat
import re
from PIL import Image


# 두개 인자 값 받음 (이미지 구분 확장자, 결과 html 파일명)
if __name__ == '__main__':
    argument = sys.argv
    del argument[0]			# 첫번째 인자는 실행시킨 파일명
    # file_ext = argument[0]
    result_file_name = argument[0]

    tpl_path = '/NAS2/KHL/tpl/'
    before_path = "/NAS2/KHL/before/"
    after_path = "/NAS2/KHL/after/"
    resize_path = "/NAS2/KHL/resizeImg/"
    resize_popup_path = "/NAS2/KHL/resizeFullImg/"
    txtfile_path = "/NAS2/KHL/"+result_file_name
    head_lines = ''
    body_new_line = ''
    end_lines = ''

    beforeList = os.listdir(before_path)
    afterList = os.listdir(after_path)

    # 정렬
    beforeList.sort(key=lambda f: int(re.sub('\D', '', f)))
    afterList.sort(key=lambda f: int(re.sub('\D', '', f)))

    # 폴더내 파일명 변경
    for i in range(0, len(beforeList)):
        if beforeList[i] in afterList:
            os.rename(
                before_path+beforeList[i], before_path+'img_' + str(i) + beforeList[i][-4:])
            os.rename(
                after_path+beforeList[i], after_path+'img_' + str(i) + beforeList[i][-4:])

    # 이미지 사이즈 조절
    for i in range(0, len(beforeList)):
        img_after = Image.open(after_path+beforeList[i])  # display size
        img_resize_a = img_after.resize((300, 200))
        img_resize_a.save(resize_path+'after/'+beforeList[i])

        img_after = Image.open(after_path+beforeList[i])  # popup size
        img_resizefull_a = img_after.resize((1300, 880))
        img_resizefull_a.save(resize_popup_path+'contour/'+beforeList[i])

        img_before = Image.open(before_path+beforeList[i])
        img_resizefull_b = img_before.resize((1300, 880))
        img_resizefull_b.save(resize_popup_path+'origin/'+beforeList[i])

    # 폴더별 image name mapping
    for i in range(0, len(beforeList)):
        # if beforeList[i].split('.')[0]+'_'+file_ext+'.'+beforeList[i].split('.')[1] in afterList:
        #     b_file_name = beforeList[i]
        #     a_file_name = beforeList[i].split('.')[0]+'_'+file_ext+'.'+beforeList[i].split('.')[1]

        # body 부분 반복 추가
        with open(tpl_path+'body.txt', 'r') as f:
            lines = f.readlines()
            for j, l in enumerate(lines):
                if j == 0:
                    new_line0 = l.strip().replace('xxx', str(i))
                    body_new_line += '\n' + new_line0
                elif 'filename' in l and 'after' in l:
                    new_line1 = l.strip().replace(
                        'testblack.jpg', beforeList[i])
                    body_new_line += new_line1 + '\n'
                elif 'filename' in l and 'origin' in l:
                    new_line2 = l.strip().replace('origin.jpg', afterList[i])
                    body_new_line += new_line2 + '\n'
                elif 'filename' in l and 'contour' in l:
                    new_line3 = l.strip().replace('contour.jpg', afterList[i])
                    body_new_line += new_line3 + '\n'
                elif 'test.png' in l:
                    new_line4 = l.strip().replace('test.png', beforeList[i])
                    body_new_line += new_line4 + '\n'
                else:
                    body_new_line += l
        f.close()

    with open(tpl_path+'head.txt', 'r') as f:
        head_line = f.readlines()
        for i in head_line:
            head_lines += i
    f.close()

    with open(tpl_path+'end.txt', 'r') as f:
        end_line = f.readlines()
        for i in end_line:
            end_lines += i
    f.close()

    os.umask(0)

    with open(txtfile_path, mode='w', encoding='utf-8', newline='') as f:
        print('filepath:', txtfile_path)
        os.chmod(txtfile_path, 0o777)
        f.write(head_lines)
        f.write(body_new_line)
        f.write(end_lines)
    f.close()
