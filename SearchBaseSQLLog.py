import pymssql

class SearchBaseSQLLog:

    def connect_search_baseDB(self, DB_info_list):
        print("connect_search_baseDB")

        #select 결과를 담을 리스트 선언
        search_result_List = []


        #파라미터로 넘겨 받은 리스에서 DB 접속에 쓰일 정보 추출하기
        string_ip = DB_info_list[0] #ip
        string_id = DB_info_list[1] #id
        string_pw = DB_info_list[2] #pw
        string_dbn = DB_info_list[3] #DBName

        #pymssql를 이용, MSSQL 접속
        conn = pymssql.connect(server=string_ip, user=string_id, password=string_pw , database=string_dbn)

        #DB 연결
        cur = conn.cursor()

        #DB에서 사용할 View 생성 쿼리문
        createViewSQL = "create view MDView as SELECT M.Id, D.Name as MD FROM [" + string_dbn + "].[MonitorData].[Machine] as M LEFT JOIN [" + string_dbn + "].[MonitorData].[DesktopGroup] as D ON M.DesktopGroupId = D.Id WHERE D.Name IS NOT NULL"

        #DB에 해당 쿼리문 실행
        cur.execute(createViewSQL)

        #데이터를 추출하는 Search 쿼리문 ----> 나중에 오늘날짜 where절 추가 할 수 있는 가능 성 있음
        creatDataSQL1 = "SELECT U.UserName, M.Name,MDV.MD,S.StartDate,S.EndDate,A.Id FROM [" + string_dbn + "].[MonitorData].[Session] S "
        creatDataSQL2 = "LEFT JOIN [" + string_dbn + "].[MonitorData].[Machine] M "
        creatDataSQL3 = "ON S.MachineId = M.Id "
        creatDataSQL4 = "LEFT JOIN [" + string_dbn + "].[MonitorData].[SessionAutoReconnect] A "
        creatDataSQL5 = "ON S.SessionKey = A.SessionKey "
        creatDataSQL6 = "LEFT JOIN [" + string_dbn + "].[MonitorData].[User] U "
        creatDataSQL7 = "ON S.UserId = U.Id "
        creatDataSQL8 = "LEFT JOIN MDView as MDV "
        creatDataSQL9 = "ON S.MachineId = MDV.Id"
        totalSQL = creatDataSQL1 + creatDataSQL2 + creatDataSQL3 + creatDataSQL4 + creatDataSQL5 + creatDataSQL6 + creatDataSQL7 + creatDataSQL8 + creatDataSQL9

        # DB에 select 쿼리문 실행
        cur.execute(totalSQL)
        row = cur.fetchone()

        # while 문을 돌면서 search_result_List 검색값 주입
        while row:

            print(row)
            search_result_List.append(row)
            row = cur.fetchone()

        # 사용한 뷰를 삭제하는 쿼리문
        dropViewSQL = "DROP VIEW MDView"

        # DB에 dropViewSQL 쿼리문 실행
        cur.execute(dropViewSQL)

        # 커넥션 종료
        conn.close()
        return search_result_List
