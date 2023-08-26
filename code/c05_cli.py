#!/usr/bin/env python3

import os,sys
import argparse
from c04_api import * 

# ------------------------------ VAR ------------------------------

# input
personalDir = "./dataset/personalData"

# output
outputPath =  "./output"

# default - cache location
cacheDir = "./dataset/cache"
cachedb  = 'cache.db'


# ------------------------------ Main ------------------------------

if __name__== "__main__" :

    parser = argparse.ArgumentParser(description='personal data cmd')
    parser.add_argument('--add', '-a', nargs="+", help="""add data to personal data; 
                                                    format: --add Name Address Phone; 
                                                    example1: --add juneleung BJChina +861234
                                                    example2: --add juneleung BJChina +861234 juneleung2 BJ2China +8612345
                                                """)
    parser.add_argument('--query', '-q', type=str, default= None, help="""query personal data
                                                    format: --query condiciton; 
                                                    example1: --query ""
                                                    example2: --query "name=june"
                                                    example3: --query "name=june*"
                                                    example4: --query "address=*NY*"
                                                    example5: --query "phone=(880)*"
                                                """)
    parser.add_argument('--convert', type=str, help="""convert all data to json format
                                                    format: --convert outputpath; 
                                                    example1: --convert ./output/convert 
                                                """)
    parser.add_argument('--display','-d', nargs="+", help="""display data in html/txt
                                                    format: --display condiction outputpath; 
                                                    example1: --display "" ./output 
                                                    example2: --display "address=*NY*" ./output 
                                                """)

    args = parser.parse_args()

    if len(sys.argv) > 1: # use cmd 
        print("use cmd mode")
        if args.add:
            print("add data")
            info = args.add
            if len(info)%3:
                print("The input information is incomplete, -h for help")
                exit(0)
            else: 
                newPersonalDataList = [info[i:i+3] for i in range(0,len(info),3)]
                PD = PDapi(personalDir,cacheDir,cachedb)
                PD.PD_add_record(newPersonalDataList)

        if args.query is not None:
            print("query data")
            info = str(args.query)
            PD = PDapi(personalDir,cacheDir,cachedb)
            res = PD.PD_search_records(info)
            print(res)

        if args.convert:
            print("convert data")
            outpath = str(args.convert)
            PD = PDapi(personalDir,cacheDir,cachedb)
            PD.PD_convert_records(outpath)

        if args.display:
            print("display data")
            info = args.display
            if len(info) != 2:
                print("display param number error, -h for help ")
                exit(0)
            else: 
                PD = PDapi(personalDir,cacheDir,cachedb)
                res = PD.PD_search_records(str(info[0]))
                PD.PD_display_records(res,info[1])