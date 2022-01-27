from datetime import datetime
from ReadBaseDBSettingFile import ReadBaseDBSettingFile
from DBDataEncoding import DBDataEncoding
from SearchBaseSQLLog import SearchBaseSQLLog

class ConnectBaseSQL:

    def search_logData(self):

        #txt 파일에서 조회된 DB 로그인 정보를 저장할 리스트 생성
        login_info_list = []

        #ReadBaseDBSettingFile 객체 생성
        rbdf = ReadBaseDBSettingFile()
        login_info_list = rbdf.read_setting_file()

        #리스트에 담겨진 DB 정보 스트링으로 변환
        ip_string = login_info_list[0] # DB IP
        id_string = login_info_list[1] # DB ID
        pw_string = login_info_list[2] # 암호화된 패스 워드
        dbn_string = login_info_list[3] # 데이터베이스 명

        #스트링으로 된 정보에서 로그인에 필요한 정보 선별 ex)IP:192.168.0.214

        # 1) ip정보
        ip_string = ip_string.split(":")[1] # :를 기준으로 실제 필요한 정보인 리스트의 [0]의 값 취득
        ip_string = ip_string.split("\n")[0] # 뒤에 줄바꿈 부분 삭제

        # 2) id정보
        id_string = id_string.split(":")[1] # :를 기준으로 실제 필요한 정보인 리스트의 [0]의 값 취득
        id_string = id_string.split("\n")[0]  # 뒤에 줄바꿈 부분 삭제

        # 3) 암호화된 패스워드 정보
        pw_string = pw_string.split(":")[1] # :를 기준으로 실제 필요한 정보인 리스트의 [0]의 값 취득
        pw_string = pw_string.split("\n")[0] # 뒤에 줄바꿈 부분 삭제

        # 4) 데이터베이스 명
        dbn_string = dbn_string.split(":")[1] # :를 기준으로 실제 필요한 정보인 리스트의 [0]의 값 취득
        dbn_string = dbn_string.split("\n")[0]  # 뒤에 줄바꿈 부분 삭제

        # 암호화된 정보를 복호화 해줄 클래스 객체화
        dbe = DBDataEncoding()
        decoding_ip = dbe.decrypt(ip_string)
        decoding_id = dbe.decrypt(id_string)
        decoding_password = dbe.decrypt(pw_string)
        decoding_dbn = dbe.decrypt(dbn_string)


        # 변환된 정보를 이용해서 SQL에 접속해서 오늘 날짜에 해당 되는 로그 값 검색해서 가져오기

        # 1. 변환된 정보를 담을 리스트 생성해서 해당 정보 리스트에 담기
        base_DB_info_List = []

        base_DB_info_List.append(decoding_ip)
        base_DB_info_List.append(decoding_id)
        base_DB_info_List.append(decoding_password)
        base_DB_info_List.append(decoding_dbn)


        # 2. 검색된 로그 값을 저장할 리스트 생성
        search_List = []

        # 3. 해당 클래스 객체 생성후 데이터 주입
        sbq = SearchBaseSQLLog()
        search_List = sbq.connect_search_baseDB(base_DB_info_List)

        # DB 및 Excel에서 사용할 컬럼 리스트 생성
        colum_List = []

        colum_List.append("Associated User")
        colum_List.append("Machine Name")
        colum_List.append("Delivery Group")
        colum_List.append("Session Start Time")
        colum_List.append("Session End Time")
        colum_List.append("session Duration(hh:mm)")
        colum_List.append("session Auto Reconnect Count")

        return_dic = {'colum_List':colum_List, 'search_List':search_List}
        return return_dic
