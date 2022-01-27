from ReadSettingFile import ReadSettingFile
from ConnectBaseSQL import ConnectBaseSQL
from CreateLogExcelDoc import CreateLogExcelDoc
from SaveDataToDB import SaveDataToDB

class OptionJudgment:

    def option_jud(self):
        # 설정.txt에서 엑셀, DB 설정 옵션 불러오기
        rsf = ReadSettingFile()
        option_dic = rsf.read_setting_file()

        # 설정된 옵션 스트링 파일로 변환 (0은 체크안됨 ,1은 체크됨)
        excel_option = option_dic[0]
        db_option = option_dic[1]

        # 변환된 스트링 파일 :기준으로 마지막 단어 가져오기 ex)Excel:True
        excel_option_result = excel_option.split(':')[1]
        # 변환된 스트링 파일 뒤에 줄바꿈 빼기 ex)True\n
        excel_option_result = excel_option_result.split("\n")[0]
        # 변환된 스트링 파일 :기준으로 마지막 단어 가져오기 ex)Excel:True
        db_option_result = db_option.split(':')[1]
        # 변환된 스트링 파일 뒤에 줄바꿈 빼기 ex)True\n
        db_option_result = db_option_result.split("\n")[0]

        result_dic = {}
        # 로그 정보를 가지고 있는 DB를 정보조회 하는 클래스 객체화
        cbsql = ConnectBaseSQL()
        # 해당 메소드 호출
        result_dic = cbsql.search_logData()

        # if절을 사용해서 알맞는 메소드를 호출
        if excel_option_result == "True":

            ced = CreateLogExcelDoc()
            ced.create_excel_doc_data(result_dic)

        if db_option_result == "True":
            print("DB기록 선택")
            # 딕셔너리에 데이터 리스트 추출
            data_List = result_dic["search_List"]

            # 매일 로그를 저장할 mssql에 접속해서 "A 테이블이 없을경우" 테이블을 생성,아니면 기존 테이블을 이용하는 클래스 객체 생성
            sdtd = SaveDataToDB()
            sdtd.judgement_table(data_List)





