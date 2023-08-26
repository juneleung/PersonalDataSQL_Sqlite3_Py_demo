import os
import hashlib
import json

def saveToJson(res,OUToutputPath):
    #save json
    if not os.path.exists(OUToutputPath): os.makedirs(OUToutputPath)
    genMd5 = hashlib.md5()
    for data in res:
        dict = {'name':data[1],'address':data[2],'phone':data[3]}
        genMd5.update(bytes(str(data[1])+str(data[2])+str(data[3]),encoding="utf-8"))
        hashS = str(genMd5.hexdigest())
        with open(os.path.join(OUToutputPath,hashS+'.json'), 'w') as f:
            json.dump(dict, f)
    print(f"data file has saved to {OUToutputPath}")

def saveToTxt(res,OUToutputPath):
    with open(os.path.join(OUToutputPath,'result.txt'), 'w') as f:
        f.write("Name\tAddress\tPhone\n")
        for res_ in res:
            f.write(str(res_[1])+"\t"+str(res_[2])+"\t"+str(res_[3])+"\n")

def saveToHTML(res,OUToutputPath):
    with open(os.path.join(OUToutputPath,'result.html'), 'w') as f:
        html = """
        <!DOCTYPE html>  
        <html>  
        <head>  
            <title>result</title>  
            <style>  
                table {  
                    border-collapse: collapse;  
                    margin: auto;  
                    width: 80%;  
                }

                th, td {  
                    border: 1px solid black;  
                    padding: 8px;  
                    text-align: left;  
                }

                th {  
                    background-color: #ddd;  
                }  
            </style>  
        </head>  
        <body>  
            <table>  
            <tr>  
                <th>No</th>  
                <th>Name</th>  
                <th>Address</th>  
                <th>Phone</th>  
            </tr>  """
        f.write(html)

        No = 0 
        for res_ in res:
            No = No+1
            f.write("""<tr>  
			<td>"""+str(No).zfill(4)+"""</td>  
			<td>"""+str(res_[1])+"""</td>  
			<td>"""+str(res_[2])+"""</td>  
			<td>"""+str(res_[3])+"""</td>  
		</tr>  """)
            
        html="""    
            </table>  
        </body>  
        </html>  """
        f.write(html)

