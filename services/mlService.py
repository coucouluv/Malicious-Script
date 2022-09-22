import os
import subprocess
import joblib

# 비난독화된 파일(txt) -> textPsParser 실행
def run_psparser(directory):
    # PATH에 자기가 위치하고 있는 곳 경로 추가
    curpath = os.getcwd() + ';'
    env = os.environ
    path = curpath + env['PATH']
    env['PATH'] = path
    # textPsParser.exe는 파이썬 코드와 같은 위치에 있어야함

    #script = read_file(directory) # 확인용
    #print("psParser1.txt 내용 확인 : ", script) # 확인용

    # 이전 파일에서 자동으로 업로드가 안되어서 있는지 확인하고 삭제하기
    file_path = "result/psParser1.txt.txt"
    if os.path.exists(file_path):
        os.remove(file_path)

    result = subprocess.run(['textPsParser.exe', directory])


# textPsParser 실행 후 만들어진 txt 파일
# 여기서 매개변수로 txt파일 경로를 넘겨주자
def read_file(directory):
    script = ""
    try:
        f = open(directory, 'r')
        script += f.read()
    except UnicodeDecodeError as e:
        print(directory)
        script += "None"
    return script


# 소문자로 바꾸기, 길이 1 제거
def lower_case(script):
    words = script.lower().split()
    lower_line = []
    for word in words:
        if len(word) >= 2:
            lower_line.append(word)
    result = []
    result.append(' '.join(lower_line))
    return result


def print_result(outputdata):
    ret = ""
    if outputdata[0][0] > outputdata[0][1]:
        ret = "정상 스크립트입니다.\n\n확률(%) : " + str(round(outputdata[0][0] * 100, 1))
    else:
        ret = "악성 스크립트입니다.\n\n확률(%) : " + str(round(outputdata[0][1] * 100, 1))

    f_decoding = open("mlResult.txt", 'w')
    f_decoding.write(ret)
    f_decoding.close()


def start():
    directory = "psParser1.txt"  # 확인하고 싶은 스크립트 파일 경로 # "./psParser1.txt"

    # 실행 전에 파일이 txt인지 확인하기 v

    if '.txt' in directory:
        # textPsParser 실행
        run_psparser(os.path.join(directory))

        directory = "result/psParser1.txt.txt"  # psParser돌리고 난 파일 경로 # "./result/psParser1.txt.txt"
        # txt파일 읽기
        script = read_file(directory)

        if script == 'None':
            print("파일에 잘못된 값이 존재")
            ret = "파일에 잘못된 값이 존재합니다"
            f_decoding = open("mlResult.txt", 'w')
            f_decoding.write(ret)
            f_decoding.close()
        elif len(script) == 0:
            outputdata = [[0.999, 0.001]]
            print_result(outputdata)
        else:
            script = lower_case(script)  # 소문자로 바꾸기, 길이 1 제거
            count = joblib.load('countvector.pkl') # 'countvector.pkl'
            inputdata = count.transform(script)
            model = joblib.load('model.pkl') # './model.pkl'
            outputdata = model.predict_proba(inputdata)
            print_result(outputdata)

    else:
        print("파일 형식이 잘못되었습니다.")