import boto3
import io  # Import StringIO
import pandas as pd  # Import pandas for handling data

# AWS credentials
aws_access_key = "AKIAQKPILR6C4LLEUPO4"
aws_secret_key = "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"

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
bucket_name = 'terpfile'
dataset_key = "terp_FSL_NAPA_SOAS_GoA_mm2nist_2022.06.06.txt"

# Retrieve the file from S3
response = s3.get_object(Bucket=bucket_name, Key=dataset_key)
dataset_content = response['Body'].read().decode('utf-8')

# Default Dictionary
databaseColumns = ["RT1-A", "RT2-A", "Name", "Suspected_matches", "Formula", "MW", "ExactMass", "CAS#", "Derivatization_Agent", "Comments", "Retention_index", "Num Peaks", "X-Values", "Y-Values", "Description", "DB#", "Synon"]
databaseDictionary = {key: [] for key in databaseColumns}

# Adds Values for X-Column and Y-Column
def coordinatesfunction(coordinates):
    xcoords = []
    ycoords = []
    for i in coordinates:
        coordTuple = i.split()
        if len(coordTuple) == 2:
            xcoords.append(float(coordTuple[0]))
            ycoords.append(float(coordTuple[1]))
    databaseDictionary["X-Values"].append(xcoords)
    databaseDictionary["Y-Values"].append(ycoords)

def addNAValues(dic):
    lenValues = len(dic["Name"])
    for keys in dic:
        if len(dic[keys]) != lenValues:
            dic[keys].append("N/A")

# Converts TextFile into dictionary using StringIO
def textdictionary(text_content):
    openfile = io.StringIO(text_content)  # Use StringIO to treat the string as a file-like object
    contentLine = "Start"
    while contentLine:
        contentLine = openfile.readline()
        if not contentLine.strip():
            addNAValues(databaseDictionary)
            continue
        contentList = contentLine.split(":")
        columnnames = contentList[0]
        if columnnames[0].isdigit():
            coordinatesfunction(columnnames.split(";"))
            continue
        columnvalue = contentList[1].strip()
        if columnnames == "Comments":
            metadata = contentList[1].split()
            databaseDictionary["Comments"].append(metadata)
            continue
        if columnvalue == '':
            databaseDictionary[columnnames].append("N/A")
        else:
            databaseDictionary[columnnames].append(columnvalue)
    openfile.close()
    return databaseDictionary   

terp_dict = textdictionary(dataset_content)
terp_dict_length = len(terp_dict["Name"])  # Use len() function

print(terp_dict_length)