import base64
import tkinter as tk
import tkinter.ttk as ttk

import chardet
from tkinter import *
from tkinter import filedialog

import self as self

import os
import pandas as pd
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import joblib
import operator, sys
from cryptography.fernet import Fernet
import rsa

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

from services.basicSettingSerivce import *
from services.deobfuscationService import *
from services.mlService import *

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
file_path = ""


# 파일 불러오기 # event loop에서 return값을 못 받아서 이렇게 설정함.
def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[('Text File','.txt')])
    file_path = file_path.replace('\\', '/')
    print("파일 경로 : ", file_path)
    if file_path == '':
        print("파일 경로를 찾을 수 없습니다.")
        exit()
    else:
        print("파일 업로드 완료")
        print("\n")

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        width, height = 800, 800  # 창 크기 값 설정

        self.geometry('{0}x{1}'.format(width, height))  # 창 크기 설정
        self.resizable(False, False)  # 크기 조정 가능 여부

        self.title('어쩔보안')  # 창 제목 설정

        self._frame = None
        self.switch_frame(FileSelectingPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame # 기존 프레임을 제거한다.
        self._frame.pack() # 전달받은 새로운 프레임을 화면에 출력

    def quit(self):
        self.destroy()

class FileSelectingPage(tk.Frame):
    def __init__(self, master):
        # tkinter button에서 return 값 사용하는 법 -> (1) global, (2) lambda 사용
        tk.Frame.__init__(self, master)
        tk.Button(self, text='1. 파일 선택', width=20, height=3,
                  command=lambda: [open_file(), button.config(state=tk.NORMAL)]).pack()

        button = tk.Button(self, text="Go to the deobfuscation", command=lambda: master.switch_frame(DeobfuscationPage), state="disabled")
        button.pack()

        label1 = Label(self, text="파일 업로드 상태 : X", width=30, height=4, fg='blue')
        label1.pack()
        label2 = Label(self, text="비난독화 진행 상태 : X", width=30, height=1, fg='blue')
        label2.pack()
        label2 = Label(self, text="비난독화는 'utf-8, euc-kr, ascii, 16진수'만 가능합니다.", width=50, height=1, fg='red')
        label2.pack()
        label3 = Label(self, text="악성 스크립트 탐지 결과 : 미정", width=30, height=4, fg='blue')
        label3.pack()


    # root.mainloop()

class DeobfuscationPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Button(self, text='2-1. 난독화X', width=20, height=3, command=lambda: [fileRead(file_path), button.config(state=tk.NORMAL)]).pack()  #
        tk.Button(self, text='2-2. 난독화O-Base64', width=20, height=3,
                         command=lambda: decode_base64(file_path)).pack()  #
        tk.Button(self, text='2-2. 난독화O-16진수', width=20, height=3, command=lambda: [decode_hex(file_path), button.config(state=tk.NORMAL)]).pack()
        # my_btn5 = Button(root, text='2-2. 난독화O-XOR_encode', width=20, height=3, command= lambda : xor_encode(file_path)).pack()
        tk.Button(self, text='2-2. 난독화O-XOR_decode', width=20, height=3,
                         command=lambda: [xor_decode(file_path), button.config(state=tk.NORMAL)]).pack()
        # my_btn7 = Button(root, text='2-2. 난독화O-XOR', width=20, height=3, command= lambda : xor(file_path)).pack()
        # my_btn8 = Button(root, text='2-2. 난독화X-대칭키테스트', width=20, height=3, command= lambda : symmetricKey(file_path)).pack()
        tk.Button(self, text='2-2. 난독화X-대칭키-Decode', width=20, height=3,
                         command=lambda: [decode_symmetric(file_path), button.config(state=tk.NORMAL)]).pack()
        tk.Button(self, text='2-2. 난독화X-RSA-Encode', width=20, height=3,
                         command=lambda: [rsaEncode(file_path), button.config(state=tk.NORMAL)]).pack()
        tk.Button(self, text='2-2. 난독화X-RSA-Decode', width=20, height=3,
                         command=lambda: [rsaDecode(file_path), button.config(state=tk.NORMAL)]).pack()

        # my_btn10 = Button(root, text='2-2. 난독화X-XOR-EncodeDecode', width=20, height=3, command= lambda : xor_encode_decode(file_path)).pack()
        button = tk.Button(self, text="Go to the deobfuscation Result", command=lambda: master.switch_frame(DeobfuscationResultPage), state="disabled")
        button.pack()

class DeobfuscationResultPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label1 = Label(self, text="비난독화 결과", width=30, height=1, fg='blue')
        label1.pack()

        tk.Button(self, text="Go to the ML Page", command=lambda: master.switch_frame(MlPage)).pack()


class MlPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        my_btn15 = Button(self, text='3. 악성스크립트 탐지', width=20, height=3, command=lambda : [start, button1.config(state=tk.NORMAL), button2.config(state=tk.NORMAL)]).pack()
        # my_btn3 = Button(root, text='난독화 방식 확인', width=20, height=3, command=identifyObfuscationMethod).pack()
        button1 = tk.Button(self, text="Restart", command=lambda: master.switch_frame(FileSelectingPage), state="disabled")
        button1.pack()

        button2 = tk.Button(self, text='종료', command= master.quit, state="disabled")
        button2.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()