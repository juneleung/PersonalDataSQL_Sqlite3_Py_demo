
# ------------------------------ NOTE -----------------------------

# python 37

# build a simulate dataset from random data 
# and save to json/ yaml/ csv/ xml/ txt format files

# -----------------------------------------------------------------

import os
import hashlib
import json
import yaml
import dicttoxml
from xml.dom.minidom import parseString
import csv

# ------------------------------ VAR ------------------------------

# input
random_Dir = "./dataset/rawData"
random_DirNameTxt = "rdmNameData.txt"
random_DirAddressTxt = "rdmAddressData.txt"
random_DirPhoneTxt = "rdmPhoneData.txt"

# output
OUT_personalDir = "./dataset/personalData"

# the number of personal data files
dataCount = 100

# -----------------------------------------------------------------

def read2List(filePath):
    # read rondom data convert to list
    file = os.path.join(random_Dir,filePath)
    if not os.path.exists(file):
        print(f"ERROR: {file} not exist!")
        return

    file = open(file,"r")
    return file.read().split("\n")



if __name__== "__main__" :
    """ 
        # build a simulate dataset from random data 
        # and save to json/ yaml/ csv/ xml/ txt format files
    """

    # random data -> list:
    nameList = read2List(random_DirNameTxt)
    addList = read2List(random_DirAddressTxt)
    phoneList = read2List(random_DirPhoneTxt)

    if(len(nameList)<dataCount or len(addList)<dataCount or len(phoneList)<dataCount):
        print(f"sim data count less than {dataCount}")
        exit

    if not os.path.exists(OUT_personalDir):
        os.makedirs(OUT_personalDir)

    # make dict and save to different format files:
    genMd5 = hashlib.md5()
    for id in range(dataCount):
        name = nameList[id]
        address = addList[id]
        phone = phoneList[id]

        dict = {'name':name,'address':address,'phone':phone}
        
        genMd5.update(bytes(name+address+phone,encoding="utf-8"))
        hashS = str(genMd5.hexdigest())

        if id in range(int(dataCount*0.2)): # json
            with open(os.path.join(OUT_personalDir,hashS+'.json'), 'w') as f:
                json.dump(dict, f)
        elif id in range(int(dataCount*0.2),int(dataCount*0.4)): # yaml
            with open(os.path.join(OUT_personalDir,hashS+'.yaml'), 'w') as f:
                yaml.dump(dict, f)
        elif id in range(int(dataCount*0.4),int(dataCount*0.6)): # xml
            with open(os.path.join(OUT_personalDir,hashS+'.xml'), 'w') as f:
                xml = dicttoxml.dicttoxml(dict)
                dom = parseString(xml)
                f.write(dom.toprettyxml())
        elif id in range(int(dataCount*0.6),int(dataCount*0.8)): # csv
            with open(os.path.join(OUT_personalDir,hashS+'.csv'), 'w') as f:
                writer = csv.DictWriter(f, fieldnames=list(dict.keys()))
                writer.writeheader()
                writer.writerow(dict)
        else: # txt (sim a not supposed type)
            with open(os.path.join(OUT_personalDir,hashS+'.txt'), 'w') as f:
                json.dump(dict, f)


    print("finish build dataset")
