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


fileIn = 'AoO_Round8_Dec2015_Dataset_Merged_Final.xlsx'
fileOut = 'AoO_Round8_Dec2015_comms_countries.csv'
fileSheet = 'AoO_Round8_Dec2015_Dataset_Merg'

aggregateQuestions = ['Country']

aggregate_Questions = ['Country']


def aggregateToCommunity(fileIn):
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "Data loaded"
    allResponses = []
    subdistricts = df['Village_Assessed_location']
    communityList = pd.unique(df.Village_Assessed_location.ravel())
    for sub in communityList:
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
    questionHeading = ",".join(aggregate_Questions)
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
