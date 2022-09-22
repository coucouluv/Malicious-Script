import os
import sys
import tkinter as tk

from tkinter import filedialog, E, END, HORIZONTAL

from services.basicSettingSerivce import fnAlert, fileRead
from services.deobfuscationService import decode_base64, decode_hex
from services.mlService import start

file_path = ""
print("is it working?1")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 파일 불러오기 # event loop에서 return값을 못 받아서 main에 두기.
def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[('Text File','.txt')])
    file_path = file_path.replace('\\', '/')
    if file_path == '':
        print("파일 경로를 찾을 수 없습니다.")
        exit()
    else:
        print("파일 업로드 완료")

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        width, height = 600, 400  # 창 크기 값 설정

        self.geometry('{0}x{1}'.format(width, height))  # 창 크기 설정
        # self.geometry("800x400")
        self.resizable(False, False)  # 크기 조정 가능 여부

        self.title('TEAM_어쩔보안')  # 창 제목 설정

        self.iconbitmap(resource_path('main_image.ico'))

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
        tk.Frame.__init__(self, master)

        #진행 바
        process_btn1 = tk.Button(self, text="파일 선택", width=20, bg="LightSteelBlue3")
        process_btn1.grid(row=0, column=0, columnspan=2)
        process_btn2 = tk.Button(self, text="비난독화 방식 선택", width=20, state="disabled", relief="ridge")
        process_btn2.grid(row=0, column=2, columnspan=2)
        process_btn3 = tk.Button(self, text="비난독화 결과 확인", width=20, state="disabled", relief="ridge")
        process_btn3.grid(row=0, column=4, columnspan=2)
        process_btn4 = tk.Button(self, text="악성 스크립트 결과 확인", width=20, state="disabled", relief="ridge")
        process_btn4.grid(row=0, column=6, columnspan=2)

        self.grid_rowconfigure(1, minsize=20) # 칸 띄우기

        file_button = tk.Button(self, text='파일 선택', width=40, height=4, bg="LightSteelBlue1",
                  command=lambda: [open_file(), button.config(state=tk.NORMAL, text="다음 단계로 넘어가기", bg="LightSteelBlue1", fg="blue")
                      , file_button.config(text="파일 재선택", bg="gainsboro")])
        file_button.grid(row=2, column=2, columnspan=4)

        self.grid_rowconfigure(3, minsize=20)

        button = tk.Button(self, text="파일을 먼저 선택 하세요", command=lambda: master.switch_frame(DeobfuscationPage), state="disabled")
        button.grid(row=4, column=3, columnspan=2)

        self.grid_rowconfigure(5, minsize=200)

        #알림창
        vBtn = tk.Button(self, text="❓", command=fnAlert, bg="gray90")
        vBtn.grid(row=6, column=7, sticky=E)

class DeobfuscationPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 진행 바
        process_btn1 = tk.Button(self, text="파일 선택", width=20, command=lambda: master.switch_frame(FileSelectingPage), bg="LightSteelBlue3", fg="gray")
        process_btn1.grid(row=0, column=0, columnspan=2)
        process_btn2 = tk.Button(self, text="비난독화 방식 선택", width=20, bg="LightSteelBlue3")
        process_btn2.grid(row=0, column=2, columnspan=2)
        process_btn3 = tk.Button(self, text="비난독화 결과 확인", width=20, state="disabled", relief="ridge")
        process_btn3.grid(row=0, column=4, columnspan=2)
        process_btn4 = tk.Button(self, text="악성 스크립트 결과 확인", width=20, state="disabled", relief="ridge")
        process_btn4.grid(row=0, column=6, columnspan=2)

        self.grid_rowconfigure(1, minsize=20)

        button1 = tk.Button(self, text='Base64 비난독화', width=40, height=4, bg="LightSteelBlue1",
                            command=lambda: [decode_base64(file_path),
                                               button.config(state=tk.NORMAL, text="Base64 비난독화 진행", bg="LightSteelBlue1", fg="blue"),
                                               button1.config(bg="LightSteelBlue1", relief="sunken"), button2.config(bg="gainsboro", relief="raised"),
                                               button3.config(bg="gainsboro", relief="raised")])
        button1.grid(row=2, column=2, columnspan=4)
        self.grid_rowconfigure(3, minsize=20)

        button2 = tk.Button(self, text='16진수 비난독화', width=40, height=4, bg="LightSteelBlue1",
                            command=lambda: [decode_hex(file_path),
                                             button.config(state=tk.NORMAL, text="16진수 비난독화 진행", bg="LightSteelBlue1", fg="blue"),
                                             button1.config(bg="gainsboro", relief="raised"),
                                             button2.config(bg="LightSteelBlue1", relief="sunken"),
                                             button3.config(bg="gainsboro", relief="raised")])
        button2.grid(row=4, column=2, columnspan=4)
        self.grid_rowconfigure(5, minsize=20)

        button3 = tk.Button(self, text='비난독화 진행 X', width=40, height=4, bg="LightSteelBlue1",
                            command=lambda: [fileRead(file_path),
                                             button.config(state=tk.NORMAL, text="ML으로 넘어가기", bg="LightSteelBlue1", fg="blue"),
                                             button1.config(bg="gainsboro", relief="raised"),
                                             button2.config(bg="gainsboro", relief="raised"),
                                             button3.config(bg="LightSteelBlue1", relief="sunken")])
        button3.grid(row=6, column=2, columnspan=4)
        self.grid_rowconfigure(7, minsize=20)

        button = tk.Button(self, text="비난독화 방식 선택", command=lambda: master.switch_frame(DeobfuscationResultPage), state="disabled")
        button.grid(row=8, column=3, columnspan=2)
        self.grid_rowconfigure(9, minsize=20)

        # 뒤로 가기
        backBtn = tk.Button(self, text="◀", bg="gray90", command=lambda: master.switch_frame(FileSelectingPage))
        backBtn.grid(row=10, column=0, sticky='w')

        # 알림창
        vBtn = tk.Button(self, text="❓", bg="gray90", command=fnAlert)
        vBtn.grid(row=10, column=7, sticky='e')


class DeobfuscationResultPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 진행 바
        process_btn1 = tk.Button(self, text="파일 선택", width=20,
                                 command=lambda: master.switch_frame(FileSelectingPage), bg="LightSteelBlue3", fg="gray")
        process_btn1.grid(row=0, column=0, columnspan=2)
        process_btn2 = tk.Button(self, text="비난독화 방식 선택", width=20,
                                 command=lambda: master.switch_frame(DeobfuscationPage), bg="LightSteelBlue3", fg="gray")
        process_btn2.grid(row=0, column=2, columnspan=2)
        process_btn3 = tk.Button(self, text="비난독화 결과 확인", width=20, bg="LightSteelBlue3")
        process_btn3.grid(row=0, column=4, columnspan=2)
        process_btn4 = tk.Button(self, text="악성 스크립트 결과 확인", width=20, state="disabled", relief="ridge")
        process_btn4.grid(row=0, column=6, columnspan=2)

        self.grid_rowconfigure(1, minsize=20)  # 칸 띄우기

        scrollbar = tk.Scrollbar(self)
        scrollbar1 = tk.Scrollbar(self)

        list = tk.Listbox(self, yscrollcommand=scrollbar.set, xscrollcommand=scrollbar1.set, width= 60, height= 12)

        # my_btn15의 config 설정을 위해서 여기서 초기값 설정
        my_btn15 = tk.Button(self, text='악성스크립트 탐지', width=20, height=3, bg="LightSteelBlue1",
                             command=lambda: [start(), master.switch_frame(MlResultPage)])

        f = open(resource_path("psParser1.txt"), 'r')
        while True:
            line = f.readline()
            if(line.find("비난독화가 올바르게 진행되지 않았습니다.") != -1):
                my_btn15.config(text="비난독화 재실행")
                my_btn15.config(command=lambda: [master.switch_frame(DeobfuscationPage)])


            if not line:
                break
            list.insert(END, line)

        f.close()

        list.grid(row=2, column=1, columnspan=6)
        scrollbar.config(command=list.yview)
        scrollbar.grid(row=2, column=7, rowspan=1, sticky='ns')

        scrollbar1.config(command=list.xview, orient=HORIZONTAL, width=20)
        scrollbar1.grid(row=3, column=1, columnspan=6, sticky='we')



        label1 = tk.Label(self, text="<비난독화 결과>", width=20, height=1)
        label1.grid(row=4, column=3, columnspan=2)

        self.grid_rowconfigure(5, minsize=20)

        my_btn15.grid(row=6, column=2, columnspan=4)

        # 뒤로 가기
        backBtn = tk.Button(self, text="◀", bg="gray90", command=lambda: master.switch_frame(DeobfuscationPage))
        backBtn.grid(row=7, column=0, sticky='w')

        # 알림창
        vBtn = tk.Button(self, text="❓", bg="gray90", command=fnAlert)
        vBtn.grid(row=7, column=7, sticky='e')


class MlResultPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 진행 바
        process_btn1 = tk.Button(self, text="파일 선택", width=20, command=lambda: master.switch_frame(FileSelectingPage), bg="LightSteelBlue3", fg="gray")  # disabled이면 fg가 안 먹음
        process_btn1.grid(row=0, column=0, columnspan=2)
        process_btn2 = tk.Button(self, text="비난독화 방식 선택", width=20, command=lambda: master.switch_frame(DeobfuscationPage), bg="LightSteelBlue3", fg="gray")
        process_btn2.grid(row=0, column=2, columnspan=2)
        process_btn3 = tk.Button(self, text="비난독화 결과 확인", width=20, command=lambda: master.switch_frame(DeobfuscationResultPage), bg="LightSteelBlue3", fg="gray")
        process_btn3.grid(row=0, column=4, columnspan=2)
        process_btn4 = tk.Button(self, text="악성 스크립트 결과 확인", width=20, bg="LightSteelBlue3")
        process_btn4.grid(row=0, column=6, columnspan=2)

        self.grid_rowconfigure(1, minsize=40)

        label1 = tk.Label(self, text="<정상 vs 악성>", width=25, height=1, font=(20))
        label1.grid(row=2, column=2, columnspan=4)

        self.grid_rowconfigure(3, minsize=20)

        context = open(resource_path("mlResult.txt"), 'r').read()
        label2 = tk.Label(self, width = 25, text=context, height=5, font=(20))
        if(context.find("정상") != -1): #정상인 경우
            label2.config(bg="LightSteelBlue1")
        else:
            label2.config(bg="red", fg='yellow')
        label2.grid(row=4, column=2, columnspan=4)

        button1 = tk.Button(self, text="Restart", command=lambda: master.switch_frame(FileSelectingPage), width=10, height=2, bg="SlateGray1")
        button1.grid(row=6, column=2, columnspan=1, rowspan=2, sticky='w')

        button2 = tk.Button(self, text='종료', command=master.quit, width=10, height=2, bg="SlateGray1")
        button2.grid(row=6, column=5, columnspan=1, rowspan=2, sticky='e')

        self.grid_rowconfigure(7, minsize=140)

        # 뒤로 가기
        backBtn = tk.Button(self, text="◀", bg="gray90", command=lambda: master.switch_frame(DeobfuscationResultPage))
        backBtn.grid(row=8, column=0, sticky='w')

        # 알림창
        vBtn = tk.Button(self, text="❓", bg="gray90", command=fnAlert)
        vBtn.grid(row=8, column=7, sticky='e')

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()