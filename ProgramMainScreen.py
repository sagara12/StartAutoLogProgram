from tkinter import *
from tkinter import messagebox
from OptionJudgment import OptionJudgment
from threading  import Thread
import pythoncom


class ProgaramMainScreen:

    def __init__(self):

        self.window = Tk()
        self.window.title("Auto SQL")  # 메인 화면 타이틀 제목 설정
        self.window.geometry("800x500")  # 메인 화면 크기 설정
        self.window.resizable(False, False)  # 가로값 x 세로값 변경 불가
        self.window.configure(background ='#e5e5e5') # rgb코드로 색상 변경


        # 라벨 생성

        # 메인 화면 라벨 설정
        mainLabel = Label(self.window, text="로그 데이터를 처리중 입니다. 잠시만 기다려 주세요", bg = '#e5e5e5')  # 데이터 베이스 IP 라벨
        mainLabel.place(x=260, y=60)  # mainLabel의 위치

        bottomLabel = Label(self.window, text=" ※ 로그 데이터를 처리가 완료되면 프로그램이 자동으로 종료 됩니다 ", bg='#e5e5e5')  # 데이터 베이스 IP 라벨
        bottomLabel.place(x=220, y=400)  # mainLabel의 위치


        # gif 파일 재생
        frameCnt = 30
        frames = [PhotoImage(file='C:/Users/cusoft/Desktop/LoadingMark/bufferMark2.gif', format='gif -index %i' % (i)) for i in
                  range(frameCnt)]

        # frame을 after메서드를 사용해서 업데이트
        label = Label(self.window, bg = '#e5e5e5')
        label.place(x=300, y=140)



        def update(ind):

            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            label.configure(image=frame)
            self.window.after(50, update, ind)

        def main_event_hangdling():

            pythoncom.CoInitialize()

            oj = OptionJudgment()
            oj.option_jud()
            pythoncom.CoInitialize()
            self.window.destroy()

        th1 = Thread(target=main_event_hangdling)
        th1.start()
        self.window.after(0, update, 0)
        self.window.mainloop()




#메인 화면 호출
ms = ProgaramMainScreen()
