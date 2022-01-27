
class ReadSettingFile:

    def read_setting_file(self):

        #읽어드린 파일을 저장할 리스트 선언
        option_list = []

        #settingFile이 있는 폴더 패스 경로
        path="C:/Users/cusoft/Desktop/test/setting/select_setting.txt"

        #while문을 돌면서 읽어드린 파일 option_list에 저장

        f = open(path, 'r')
        while True:
            line = f.readline()
            option_list.append(line)
            if not line: break
            print(line)
        f.close()

        return option_list
