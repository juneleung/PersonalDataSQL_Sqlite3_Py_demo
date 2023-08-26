import os
import c01_readPersonalDataUtils as readPsnData
import c02_cacheSQLUtils as cacheSQL
import c03_saveModuleUtils as saveMod
import shutil

class PDapi:
    def __init__(self,personalDir,cacheDir,cachedb,bool_RefreshCache):
        self.personalDir = personalDir
        self.cacheDir = cacheDir
        self.cachedb = cachedb
        self.bool_RefreshCache = bool_RefreshCache

        if self.bool_RefreshCache and os.path.exists(cacheDir):
            shutil.rmtree(cacheDir)
        if not os.path.exists(personalDir): print("not exist personal data folder")
        cacheMod = cacheSQL.cacheModule(cacheDir,cachedb)
        cacheMod.cacheSQL_main(personalDir)

        self.cacheMod = cacheMod

    def PD_supposed_format(self):
        self.cacheMod.supposedFormat() 
        # print with : ('.yaml', '.json', '.xml', '.csv')

    def PD_add_record(self, newPersonalDataList):
        self.cacheMod.cache_sql_add(newPersonalDataList)  # add in sql 
        saveMod.saveToJson([('-',)+newPersonalDataList[0]] ,self.personalDir) # add in json

    def PD_search_records(self, cond=""):
        res = self.cacheMod.cache_sql_read(cond)
        return res
    
    def PD_display_records(self,record,outputPath):
        print('*'*50 + "\n" + "---- display records ----\n")
        print(record)
        if not os.path.exists(outputPath):os.makedirs(outputPath)
        saveMod.saveToTxt(record,outputPath)
        saveMod.saveToHTML(record,outputPath)

    def PD_convert_records(self,outputpath):
        res = self.cacheMod.cache_sql_read()
        saveMod.saveToJson(res,outputpath)