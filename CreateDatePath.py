import datetime
import os

class CreateDatePath:

    def create_folder(self):

        # path를 저장할
        path_list = []

        path = "C:/Users/cusoft/Desktop/test/setting/excel_setting.txt"

        f = open(path, 'r')

        while True:
            line = f.readline()
            path_list.append(line)
            if not line: break
            print(line)
        f.close()

        # path_list에서 string_path로 주입(현재는 텍스트 파일이 한 줄이기 때문에 [0]를 이용해서 불러드림)
        string_path = path_list[0]
        # 경로 부분만 가져와서 저장
        string_path = string_path.split(':',maxsplit=1)[1]

        # 경로 부분에서 \n 부분 제거 해서 저장
        string_path = string_path.split('\n')[0]

        # 현재 날짜 불러오기기
        datetime_now = datetime.datetime.now()

        # 현자 날짜 형식 변환 ex) 2021/12/22
        datetime_now = datetime_now.strftime('%Y/%m/%d')
        print(datetime_now)

        # 경로 설정에 필요한 년, 월 스트링으로 저장
        string_year = datetime_now[0:4] # ex)2021
        string_month = datetime_now[6:7] # ex) 12

        # 년도가 바뀌는 경우 새로운 년도의 폴더 생성

        # 1. 현재 년/월에 맞는 경로 생성
        excel_path = string_path+"/"+string_year+"/"+string_month
        print(excel_path)

        # 2. 해당 패스가 없을 경우 패스 생성
        if not os.path.isdir(excel_path):
            os.makedirs(excel_path)

        return excel_path