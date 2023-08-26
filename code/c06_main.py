#!/usr/bin/env python3
# ------------------------------ NOTE -----------------------------

# python 37, sqlite

# cache all the personal data to sql
# more effiency when process with huge data

# -----------------------------------------------------------------

from c04_api import * 

# ------------------------------ VAR ------------------------------

# input
personalDir = "./dataset/personalData"

# output
outputPath =  "./output"

# default - cache location
cacheDir = "./dataset/cache"
cachedb  = 'cache.db'
bool_RefreshCache = True

# ------------------------------ Main ------------------------------

if __name__== "__main__" :

    # init api
    print('-'*20)
    PD = PDapi(personalDir,cacheDir,cachedb,bool_RefreshCache)

    # to query a list of currently supported formats
    print('-'*20)
    PD.PD_supposed_format()

    # add new records
    print('-'*20)
    Name = 'juneleung'
    Address = 'Mars'
    Phone = '(+86) 123-4567'
    newPersonalDataList = [(Name, Address, Phone)]
    PD.PD_add_record(newPersonalDataList)

    # query
    print('-'*20)
    res = PD.PD_search_records() # read all
    res = PD.PD_search_records("name=Aracely*") # fuzzy search: name begin with Aracely 
    print(res)
    res = PD.PD_search_records("name=Aracely Good") # exact search: name is Aracely Good
    print(res)
    res = PD.PD_search_records("address=*NY*") # fuzzy search: address in NY
    print(res)
    res = PD.PD_search_records("phone=(880)*") # fuzzy search: phone begin with (800)
    print(res)
    
    # save html / txt
    print('-'*20)
    PD.PD_display_records(res,outputPath)

    print('-'*20)
