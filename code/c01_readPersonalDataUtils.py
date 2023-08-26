

# ------------------------------ NOTE -----------------------------

# python 37

# read json yaml xml csv file

# -----------------------------------------------------------------

import json
import yaml
import xmltodict
import xml
import csv

def readyaml(file):
    with open(file, 'r') as f:
        data = yaml.load(f.read(),Loader=yaml.Loader)
    return (data['name'],data['address'],data['phone'])

def readjson(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return (data['name'],data['address'],data['phone'])

def readxml(file):
    with open(file, 'r') as f:
        data = xmltodict.parse(f.read())
    return (data['root']['name']['#text'],data['root']['address']['#text'],data['root']['phone']['#text'])

def readcsv(file):
    with open(file, 'r') as f:
        for data in csv.DictReader(f, skipinitialspace=True): # one line one file only
            return (data['name'],data['address'],data['phone'])