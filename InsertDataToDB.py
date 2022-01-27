import datetime

import pymssql


class InsertDataToDB:

    def insert_data_to_DB(self,DB_para_dic):
        search_table = []

        # DB_para_dic에서 담겨진 DB_info_list 추출

        DB_base_list = DB_para_dic["result_dic"]
        DB_info_list = DB_para_dic["save_DB_info_List"]
        col_info_list = DB_para_dic["colum_List"]

        # 파라미터로 넘겨 받은 리스에서 DB 접속에 쓰일 정보 추출하기
        string_ip = DB_info_list[0]  # ip
        string_id = DB_info_list[1]  # id
        string_pw = DB_info_list[2]  # pw
        string_dbn = DB_info_list[3]  # DBName

        # pymssql를 이용, MSSQL 접속
        conn = pymssql.connect(server=string_ip, user=string_id, password=string_pw, database=string_dbn)

        # DB 연결
        cur = conn.cursor()

        # 현재 날짜 받아오기 (now_date 부분 입력할때 필요)
        datetime_now = datetime.datetime.now()

        # 현자 날짜 형식 변환 ex) 2021/12/22
        datetime_now = datetime_now.strftime('%Y/%m/%d/ %H:%M:%S')
        print(datetime_now)

        # 시차 반영 및 duration 계산을 하는 리스트 선언
        calculate_list = []

        # j번째에 데이터를 바꿔주는
        update_data_list = []

        # UTC기준이므로 9시 더하기
        for i in range(len(DB_base_list)):

            data_list  = DB_base_list[i]

            for j in range(len(data_list)):


                if j == 3:

                    nine_add_later_start = data_list[j] + datetime.timedelta(hours=9)
                    update_data_list.append(nine_add_later_start)

                elif j == 4:

                # 데이터 리스트의 i번째 값이 NoneType인지 아닌지 판별하는 if 절 ( 만약 서버가 계속 돌아가는 경우 end Time에 NoneType이 들어감)
                # end Time이 빈칸이 이 아닐경우 UTC기준 서버 종료 시간이 들어가 있으므로 
                    print(type(data_list[j]))
                    if (str(type(data_list[j])) != "<class 'NoneType'>"):

                        nine_add_later_end = data_list[j] + datetime.timedelta(hours=9)
                        server_running_time = data_list[4] - data_list[3]
                        update_data_list.append(nine_add_later_end)
                        update_data_list.append(server_running_time)

                    else:

                        nine_add_later_end = "running"
                        server_running_time = "calculating"
                        update_data_list.append(nine_add_later_end)
                        update_data_list.append(server_running_time)

                else:
                        update_data_list.append(data_list[j])

            calculate_list.append(update_data_list)
            update_data_list=[]

        DB_base_list = calculate_list
        # 포문을 돌면서 List에 datetime_now 데이터 넣기
        for i in range(len(DB_base_list)):
            # DB_info_list[i].insert(0,datetime_now)
            list_value = DB_base_list[i]
            #튜플 리스트로 변환
            list_value = list(list_value)
            list_value.insert(0,datetime_now)
            DB_base_list[i] = list_value


        # 쿼리문 생성에 사용될 변수 생성
        str_total_value = ""
        total_value = ""
        total_value_all = ""
        Insert_sql_value = ""
        Insert_sql_value_total = ""

        # 쿼리문 생성
        Insert_sql_querry1 = "INSERT INTO Log_History"
        Insert_sql_querry2 = " VALUES"


        for i in range(len(DB_base_list)):
            str_parentheses_open = ""
            str_total_value = ""
            str_parentheses_close = ")"

            if i == 0:
                str_parentheses_open = "("

            else:
                str_parentheses_open = ",("


            db_list = DB_base_list[i]

            for j in range(len(db_list)):

                if j != (len(db_list)-1):

                    if j == 0:

                        str_comma = ","
                        str_sec = ".000"
                        total_value = total_value + str_parentheses_open
                        str_value = db_list[j]
                        str_value = str_value.replace("/", "-",2)
                        str_value = str_value.replace("/", "")
                        str_value = "'" + str_value + str_sec + "'"
                        str_value = str_value + str_comma
                        total_value = total_value + str_value

                    str_value = db_list[j]
                    print(str(type(str_value)) + "타입 STR")

                    if (str(type(str_value)) == "<class 'datetime.datetime'>"):

                        format = '%Y-%m-%d %H:%M:%S'
                        str_value = datetime.datetime.strftime(str_value, format)
                        print(str_value)
                        str_value = "'"+str_value+"'"
                        str_value = str_value + str_comma
                        total_value = total_value + str_value
                        str_value = ""


                    elif (str(type(str_value)) == "<class 'datetime.timedelta'>"):

                        str_comma = ","
                        str_value = str(str_value)
                        print(str_value)
                        str_value = "'" + str_value + "'"
                        str_value = str_value + str_comma
                        total_value = total_value + str_value
                        str_value = ""


                    else:

                        if j != 0:

                            str_comma = ","
                            print(str_value)
                            str_value = "'" + str_value + "'"
                            str_value = str_value + str_comma
                            total_value = total_value + str_value
                            str_value = ""


                else :

                    str_value = db_list[j]

                    if (str(type(str_value)) == "<class 'NoneType'>"):

                        str_value = "0"

                    total_value = total_value + str_value + str_parentheses_close

                    str_value = ""

                total_value_all = total_value_all + total_value
                total_value = ""


            Insert_sql_value_total = Insert_sql_value + total_value_all
            Insert_sql_value = ""

        Insert_sql_querry3 = Insert_sql_value_total

        Insert_sql_querry = Insert_sql_querry1+ Insert_sql_querry2 + " " + Insert_sql_querry3

        print(Insert_sql_querry)
        cur.execute(Insert_sql_querry)
        conn.commit()


