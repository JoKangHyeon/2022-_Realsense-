import json
import os

dict_list = []


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


createDirectory('./학생정보')
filename = input('반이름 입력 : ')

while True:
    sel = int(input('1번은 학생정보 생성 계속, 2번은 종료 : '))
    if sel == 1:
        print("===== 학생_정보 요소 추가 중 =====")
        my_dict = {}  # empty dictionary
        while True:
            student_number = input('학번 입력 : ')
            student_name = input('이름 입력 : ')
            my_dict[student_number] = student_name
            con = int(input('1번은 학생정보 요소 추가 계속, 2번은 종료 : '))
            if con == 2:
                print("===== 학생정보 요소 추가 끝 =====", end="\n\n")
                break
        dict_list.append(my_dict)
    elif sel == 2:
        print("종료합니다.")
        break
    else:
        print("잘못 선택하셨습니다.")
        break

print("당신이 만든 학생정보 리스트 :", dict_list)


with open('./학생정보/' + filename + '.json', 'w', encoding='cp949') as f:
    json.dump(dict_list, f, indent=4, ensure_ascii=False)