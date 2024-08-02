#Default Dictionary
databaseColumns = ["RT1-A", "RT2-A", "Name", "Suspected_matches", "Formula", "MW", "ExactMass", "CAS#", "Derivatization_Agent", "Comments", "Retention_index", "Num Peaks", "X-Values", "Y-Values", "Description", "DB#", "Synon"]
databaseDictionary = {key: [] for key in databaseColumns}

#Adds Values for X-Column and Y-Column
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


#Converts TextFile into dictionary which is then passed into pandas to create data frame (see pandas documentation)
def textdictionary(textfile):
    openfile = open(textfile, "r", encoding = "cp1252")
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
        if columnvalue ==  '':
            databaseDictionary[columnnames].append("N/A")
        else:
            databaseDictionary[columnnames].append(columnvalue)
    openfile.close()
    return databaseDictionary   

terp_dict = textdictionary("./terp_FSL_NAPA_SOAS_GoA_mm2nist_2022.06.06.txt")
terp_dict_length = terp_dict["Name"].__len__()


