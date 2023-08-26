import os
import sqlite3
from sqlite3 import OperationalError
import c01_readPersonalDataUtils as readPsnData

class cacheModule:
    """ 
        cache all the personal data to sql
        more effiency when process with huge data

        support input data format : ".yaml" ,".json", ".xml", ".csv"

        running with python 37, sqlite
    """

    # default - Parm
    formatFilter = (".yaml" ,".json", ".xml", ".csv")# ".txt"
    personalDir = ""

    def __init__(self,cacheDir,cachedb):
        self.cacheDir = cacheDir
        self.cachedb = cachedb

    def supposedFormat(self):
        print(self.formatFilter)
        return self.formatFilter

    def cache_sql_createTable(self):
        if not os.path.exists(self.cacheDir):os.makedirs(self.cacheDir)
        conn = sqlite3.connect(os.path.join(self.cacheDir,self.cachedb))  
        cur = conn.cursor()
        try:
            sql = """CREATE TABLE personaldata (   
                    id INTEGER PRIMARY KEY AUTOINCREMENT,   
                    name TEXT NOT NULL,   
                    address TEXT NOT NULL,   
                    phone TEXT NOT NULL,
                    UNIQUE (name, address, phone)
                    );"""
            cur.execute(sql)
            print("create table success")
            return 0
        except OperationalError as o:
            if str(o) == "table personaldata already exists":
                cur.execute("SELECT COUNT(*) FROM personaldata")  
                row = cur.fetchone()
                count = row[0]
                return count
            print("OpErr: "+str(o))
            return -1
        except Exception as e:
            print("ExcErr: "+e)
            return -1
        finally:
            cur.close()
            conn.close()

    def cache_sql_add(self,data_list):
        conn = sqlite3.connect(os.path.join(self.cacheDir,self.cachedb))  
        cur = conn.cursor()
        try:
            insert_datas = """INSERT INTO personaldata(name,address,phone) values(?,?,?);"""
            cur.executemany(insert_datas, data_list)
            conn.commit()
            print("add success")
            return 1
        except Exception as e:
            if("UNIQUE constraint failed" in str(e)):
                print("this data has already exists") 
                return -1
            print(str(e))
            ("error when add new data")
            return 0
        finally:
            cur.close()
            conn.close()


    def cache_sql_read(self, condition=""):
        conn = sqlite3.connect(os.path.join(self.cacheDir,self.cachedb))  
        cur = conn.cursor()
        try:
            if(condition == ""):
                sql = "SELECT * FROM personaldata;"
            else:
                condition = condition.replace("="," like '").replace("*","%") # fuzzy search
                sql = "SELECT * FROM personaldata WHERE "+condition+"';"
            cur.execute(sql)
            res =  cur.fetchall()
            conn.commit()
            return res
        except Exception as e:
            print(str(e))
        finally:
            cur.close()
            conn.close()


    def listPersonalData(self,filePath):
        # list PersonalData 
        result = [] 
        if not os.path.exists(filePath): 
            return result
        file_list = os.listdir(filePath)
        for file in file_list:
            if file.endswith(self.formatFilter):
                result.append(os.path.join(filePath,file))
        return result

    def readDataList(self,DataFileList):
        DataList = []
        for file in DataFileList:
            if(file.endswith(".yaml")):
                DataList.append(readPsnData.readyaml(file))
            if(file.endswith(".json")):
                DataList.append(readPsnData.readjson(file))
            if(file.endswith(".xml")):
                DataList.append(readPsnData.readxml(file))
            if(file.endswith(".csv")):
                DataList.append(readPsnData.readcsv(file))

        return DataList


    def cacheSQL_main(self,personalDir):
        # get perosnal data
        self.personalDir = personalDir
        personalDataFileList = self.listPersonalData(personalDir)

        # cache data in db for fast process in future
        createRes = self.cache_sql_createTable() 
        if createRes < 0: 
            print("cache sql db failed")
            return 

        # skip if cached before ( a trick by files number only ) 
        if createRes != len(personalDataFileList):
            DataList = self.readDataList(personalDataFileList) 
            self.cache_sql_add(DataList) # [('Marley Tucker', '807 Oakwood St. Jamestown, NY 14701', '(286) 278-4025')]


