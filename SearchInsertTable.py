import pymssql


class SearchInsertTable:

    def search_table(self,DB_para_dic):
        # select 결과를 담을 리스트 선언
        search_table = []

        # DB_para_dic에서 담겨진 DB_info_list 추출
        DB_info_list = DB_para_dic["save_DB_info_List"]
        col_info_list = DB_para_dic["colum_List"]


        # DB_para_dic에서 담겨진


        # 파라미터로 넘겨 받은 리스에서 DB 접속에 쓰일 정보 추출하기
        string_ip = DB_info_list[0]  # ip
        string_id = DB_info_list[1]  # id
        string_pw = DB_info_list[2]  # pw
        string_dbn = DB_info_list[3]  # DBName

        print(string_ip +"ip")
        print(string_id +"id")
        print(string_pw +"pw")
        print(string_dbn + "dbn")

        # pymssql를 이용, MSSQL 접속
        conn = pymssql.connect(server=string_ip, user=string_id, password=string_pw, database=string_dbn)

        # DB 연결
        cur = conn.cursor()

        # 검색 할 테이블명 저장

        table_name = "Log_History"

        # 테이블 검색 SQL 쿼리문 작성
        search_talbe_quarry = "select * from sys.tables where name ='"+table_name+"'"
        print(search_talbe_quarry)

        # 데이터 베이스에 해당테이블이 있는지 검색
        search_table=[]
        cur = conn.cursor()
        cur.execute(search_talbe_quarry)
        row = cur.fetchone()

        # 데이테 베이스에 테이블이 없으면 None
        if row is None:

            create_flag = 1


        else:

            create_flag = 2


        #해당하는 테이블이 없을때
        if create_flag == 1:
            # 파티션 함수를 생성
            string_partition_fuc_1 = "CREATE PARTITION FUNCTION pf_LogDate ( datetime )"
            string_partition_fuc_2 = "AS RANGE RIGHT"
            string_partition_fuc_3 = " FOR VALUES ("
            string_partition_fuc_4 = "'2021'"
            string_partition_fuc_5 = ",'2022'"
            string_partition_fuc_6 = ",'2023'"
            string_partition_fuc_7 = ")"

            string_partition_fuc = (string_partition_fuc_1+string_partition_fuc_2+
                                    string_partition_fuc_3+string_partition_fuc_4+string_partition_fuc_5+
                                    string_partition_fuc_6+string_partition_fuc_7)

            print(string_partition_fuc)
            cur.execute(string_partition_fuc)
            conn.commit()


            # 파티션 스키마를 생성
            string_partition_sche1 = "CREATE PARTITION SCHEME ps_LogDate"
            string_partition_sche2 = " AS PARTITION pf_LogDate"
            string_partition_sche3 = " TO([primary], [primary], [primary], [primary])"

            string_partition_sche = (string_partition_sche1 + string_partition_sche2 + string_partition_sche3)

            print(string_partition_sche)
            cur.execute(string_partition_sche)
            conn.commit()

            # 2. 테이블을 생성하는 쿼리문 작성

            string_creat_table1 = "CREATE TABLE [dbo].[Log_History]("
            string_creat_table2 = "[Colum_Number] [int] IDENTITY(1,1) NOT NULL,"
            string_creat_table3 = "[Now_Date] [datetime] NOT NULL,"
            string_creat_table4 = "[Associated_User] [varchar](500) NOT NULL,"
            string_creat_table5 = "[Machine_Name] [varchar](500) NOT NULL,"
            string_creat_table6 = "[Delivery_Group] [varchar](500) NOT NULL,"
            string_creat_table7 = "[Session_Start_Time] [datetime] NOT NULL,"
            string_creat_table8 = "[Session_End_Time] [datetime] NOT NULL,"
            string_creat_table9 = "[Session_Duration(hh:mm)] [varchar](500) NOT NULL,"
            string_creat_table10 = "[Session_Auto_Reconnect_Count] [int] NOT NULL"
            string_creat_table11 = " )ON ps_LogDate ( Now_Date )"

            string_creat_table = (string_creat_table1+string_creat_table2+string_creat_table3+string_creat_table4
                                  +string_creat_table5+string_creat_table6+string_creat_table7+string_creat_table8
                                  +string_creat_table9+string_creat_table10+string_creat_table11
                                  )

            cur.execute(string_creat_table)
            conn.commit()
            cur.close()
            conn.close()

