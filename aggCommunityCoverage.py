import os
import pandas as pd
import xlrd
from collections import Counter
pd.core.format.header_style = None
import csv
import operator

"""
this script produces a csv file with a records of each  
Syrian community and the country that collected data there 

"""

# update these values each month to reflect the data filenames
roundNumber = '12'
monthYear = 'Apr2016'
monthYearLong = 'April2016'

# maintain accurate filename and the directory where the unaggregated data sits
fileName = 'AoO_Round{0}_{1}_Dataset_Merged_FINAL.xlsx'.format(roundNumber, monthYear)
fileIn = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\Data Collection\\AoO_Script_structure_latest\\AoO_Round{0}_R_DK_v3\\raw_data\\{2}'.format(roundNumber, monthYearLong, fileName)
fileSheet = 'AoO_Round{0}_{1}_Dataset_Mer'.format(roundNumber, monthYear)

# output file info - filename and directory where new file will be written to
fileOutName = 'AoO_Round{0}_community_country.csv'.format(roundNumber)
fileOut = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\Coverage_analysis\\Table_database\\{2}'.format(roundNumber, monthYearLong, fileOutName)

aggregateQuestions = ['Country']

# ################################################


def aggregateToCommunity(fileIn):
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "Data loaded"
    allResponses = []
    communityList = pd.unique(df.Village_Assessed_location.ravel())
    for sub in communityList:
       # this 'C' is to account for there being no 'C' in the AoO pcodes
       # if this issue is resolved and there is a 'C' in AoO pcodes then use this line of code instead:
       # modeResponse = "{0},".format(sub)
       modeResponse = "C{0},".format(sub)
       for aggQ in aggregateQuestions:
           responseList = []
           for index, row in df.iterrows():
               if row['Village_Assessed_location'] == sub:
                   question = row[aggQ]
                   responseList.append(str(question))
           uniqueResponses = set(responseList)
           keys = []
           for key in uniqueResponses:
               keys.append(key)
               keyStr = "/".join(keys)

           modeResponse = modeResponse + "{0},".format(keyStr)

       allResponses.append(modeResponse)
    print "Aggregated to subdistrict"
    return allResponses

# ################################################

def writeResponsesToCSV(inputData, outputFile):
    print "Writing aggregations to the output file"
    districtHeading = 'Village_Assessed_location'
    questionHeading = ",".join(aggregateQuestions)
    heading = "{0},{1}".format(districtHeading, questionHeading)
    with open(outputFile, 'wb') as outFile:
        writer = csv.writer((outFile), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([heading])
        for row in inputData:
            writer.writerow([row])
    print "Aggregation file saved"

# ################################################

aggregation = aggregateToCommunity(fileIn)
writeToFile = writeResponsesToCSV(aggregation, fileOut)
