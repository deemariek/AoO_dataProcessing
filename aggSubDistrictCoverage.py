import os
import pandas as pd
import xlrd
from collections import Counter
pd.core.format.header_style = None
import csv
import operator

"""
this script produces a csv file with a records of each assessed 
Syrian subdistrict and the country/countries that collected data there
and number of communities assessed there
"""

# update these values each month to reflect the data filenames
roundNumber = '12'
monthYear = 'Apr2016'
monthYearLong = 'April2016'

# filenames for each month's appropriate dataset and sheet name
fileName = 'AoO_Round{0}_{1}_Dataset_Merged_FINAL.xlsx'.format(roundNumber, monthYear)
fileSheet = 'AoO_Round{0}_{1}_Dataset_Mer'.format(roundNumber, monthYear)

#fileIn = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\Data Collection\\AoO_Round{0}_R\\{2}'.format(roundNumber, monthYearLong, fileName)foe
fileIn = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round12_April2016\\Data Collection\\AoO_Script_structure_latest\\AoO_Round12_R_DK_v3\\raw_data\\AoO_Round{0}_{1}_Dataset_Merged_FINAL.xlsx'.format(roundNumber, monthYear)

# output file info
fileOutName = 'AoO_Round{0}_SD_country.csv'.format(roundNumber)
fileOut = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\Coverage_analysis\\Table_database\\{2}'.format(roundNumber, monthYearLong, fileOutName)

aggregateQuestions = ['Country']

#country = 'IRQ'
#fileIn = "C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\Data Collection\\AoO_Round{0}_Data\\dataCleaning\\{0}_KI_Village_Level_Monitoring_Tool_Feb16_coded.csv".format(country)


# ################################################

def aggregateToSubDistrict(fileIn):
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "Data loaded"
    allResponses = []
    subdistricts = df['Subdistrict_Assessed_location']
    subdistrictList = pd.unique(df.Subdistrict_Assessed_location.ravel())
    # get a Series containing the coverage counts for each subdistrict
    subCounts = subdistricts.value_counts()
    for sub in subdistrictList:
       modeResponse = "{0},{1},".format(sub, subCounts[sub])
       for aggQ in aggregateQuestions:
           responseList = []
           for index, row in df.iterrows():
               if row['Subdistrict_Assessed_location'] == sub:
                   question = row[aggQ]
                   responseList.append(str(question))
           uniqueResponses = set(responseList)
           keys = []
           for key in uniqueResponses:
               keys.append(key)
               keyStr = "/".join(keys)

           modeResponse = modeResponse + "{0},".format(keyStr)

       allResponses.append(modeResponse)
    print "Aggregated coverage to subdistrict"
    return allResponses

# ################################################

def writeResponsesToCSV(inputData, outputFile):
    print "Writing aggregations to the output file"
    districtHeading = 'Subdistrict_Assessed_location'
    questionHeading = ",".join(aggregateQuestions)
    heading = "{0},coverage,{1}".format(districtHeading, questionHeading)
    with open(outputFile, 'wb') as outFile:
        writer = csv.writer((outFile), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([heading])
        for row in inputData:
            writer.writerow([row])
    print "Coverage file saved"

# ################################################

aggregation = aggregateToSubDistrict(fileIn)

writeToFile = writeResponsesToCSV(aggregation, fileOut)

