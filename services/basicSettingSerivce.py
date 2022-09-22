# 난독화가 안된 경우 # 비난독화를 하는 대신 해당 파일을 psParser1.txt에 저장해야 함.
import os
import sys
import tkinter.messagebox as msgbox

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def fileRead(path_origin):
    f_origin = open(path_origin, 'r')
    f_decoding = open(resource_path("psParser1.txt"), 'w')
    while True:
        line = f_origin.readline()
        if not line: break
        f_decoding.write(line)
        f_decoding.write("\n")

    f_origin.close()
    f_decoding.close()

def fnAlert():
    msgbox.showinfo("안내", "[프로그램 설명]\n해당 프로그램은 난독화된 스크립트를 비난독화하고 스크립트에 악성 코드가 포함되어 있는지를 판단합니다.\n\n"
                          "비난독화는 Base64와 16진법을 이용한 인코딩 방식의 복호화를 지원합니다.\n"
                          "악성 스크립트 탐지는 downloader, shellcode inject, keylogger 등 다양한 파워셸 공격을 찾아냅니다.\n\n"
                          "[사용법]\n1. 스크립트가 포함된 txt파일을 선택한다.\n2. 비난독화를 진행할 방식을 선택한다.\n3. 비난독화 결과를 확인 후 악성스크립트 탐지 버튼을 클릭한다.\n4. 악성 스크립트 탐지 결과를 확인한다.\n\n"
                          "[개발자]\n김서영 - ksy654333@gmail.com\n박지연 - oy5325@naver.com\n최연재 - duswo0624@naver.com\n\n"
                          "[출시일]\n2022.09.30\n\n"
                          "[버전정보]\nv1.0.0")

