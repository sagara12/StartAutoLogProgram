from ReadSaveDBSettingFile import ReadSaveDBSettingFile
from DBDataEncoding import DBDataEncoding
from ConnectSaveDBSQL import ConnectSaveDBSQL

class SaveDataToDB():

    def judgement_table(self,result_dic):
        csdq = ConnectSaveDBSQL()
        csdq.insert_data(result_dic)




