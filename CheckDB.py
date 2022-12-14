import csv
import os
import datetime


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


createDirectory('./출결')

if __name__ == '__main__':
    student_number = ['학생1', '학생2', '학생3', '학생4']
    student_name = ['선택안함', '출석', '지각', '결석']  # Nominal
    dt = dict(zip(student_number, student_name))
    print(dt)

    filename = datetime.datetime.now().strftime("%Y-%m-%d")

    with open('./출결/' + filename + '.csv', 'w', encoding='cp949') as f:
        w = csv.writer(f)
        w.writerow(dt.keys())
        w.writerow(dt.values())