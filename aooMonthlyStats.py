import numpy as np
import pandas as pd
import os


"""
this script to automate stats for monthly data collection

"""

# update these values each month to reflect the data filenames
roundNumber = '10'
monthYear = 'Feb2016'

# fileInApril = 
fileInMay = 'C:\\REACH\SYR\\Projects\\13BVJ_AoO\\Activities\\Round2_May2015\\AoO_Round2_Data\\AoO_Round2_Final_Datasets_Packages\\AoO_Round2_May2015_Dataset_Clean_Agregated_NonAnonymised.xlsx'
fileInJune = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round3_June2015\\AoO_Round3_Data\\AoO_Round3_Final_Datasets_Packages\\AoO_Round3_June2015_Dataset_Clean_Agregated_NonAnonymised.xlsx'
fileInJuly = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round4_July2015\\AoO_Round4_July2015_Dataset_Clean_Agregated_NonAnonymised.xlsx'
fileInSept = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round5_September2015\\AoO_Round5_Sept2015_Dataset_Clean_Aggregated_NonAnoymised.xlsx'
fileInOct = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round6_October2015\\Data Collection\\AoO_Round6_Oct2015_Data_Package_Clean_Agregated_NonAnonymised\\AoO_Round6_Oct2015_Dataset_Clean_Agregated_NonAnonymised.xlsx'
fileInNov = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round7_November2015\\Data Collection\\AoO_Round7_Final_Datasets_Packages\\AoO_Round7_Nov2015_Data_Package_NonAnonymised\\AoO_Round7_Nov2015_Dataset_NonAnonymised.xlsx'
fileInDec = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round8_December2015\\Data Collection\\AoO_Round8_Final_Datasets_Packages\\AoO_Round8_Dec2015_Data_Package_NonAnonymised\\AoO_Round8_Dec2015_Dataset_NonAnon.xlsx'
fileInJan = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round9_January2016\\Data Collection\\AoO_Round9_Final_Datasets_Packages\\AoO_Round9_Jan2016_Data_Package_NonAnonymised\\AoO_Round9_Jan2016_Dataset_NonAnonymised.xlsx'
fileInFeb = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round10_February2016\\Data Collection\\AoO_Round10_Final_Dataset_Packages\\AoO_Round10_Feb2016_Data_Package\\AoO_Round10_Feb2016_Dataset.xlsx'

#fileSheet = 'AoO_Round1_April2015_Dataset'
#fileSheet = 'AoO_Round{0}'.format(roundNumber)
#fileSheet = 'AoO_full2015-10-13_FINAL'
#fileSheet = 'AoO_Round6_Oct2015_Dataset_Clea'
#fileSheet = 'AoO_Round7_Nov2015_Dataset_NonA'
#fileSheet = 'AoO_Round8_Dec2015_Dataset_NonA'
#fileSheet = 'AoO_Round9_Jan2016_Dataset_NonA'
fileSheet = 'AoO_Round10_Feb2016_Dataset'

# ################################################

def runAoOStats(fileIn, fileSheet):
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "{0} data".format(monthYear)
    print
    govList = pd.unique(df['Governorate_Assessed_location'].ravel())
    SDList = pd.unique(df['Subdistrict_Assessed_location'].ravel())
    commList = df['GEO_Village_Assessed_location'].ravel()

    print "Governorates covered: {0}".format(len(govList))
    print "Sub-districts covered: {0}".format(len(SDList))
    print "Communities covered: {0}".format(len(commList))


# ################################################


def gatherDuplicates(fileIn, fileSheet):
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "{0} data".format(monthYear)
    print
    sdList = list(pd.unique(df['Subdistrict_Assessed_location'].ravel()))
    print sdList
    commList = list(df['GEO_Village_Assessed_location'].ravel())
    print commList

    with open("subdistrictsFeb2016.txt", "a") as sdfile:
        for sd in sdList:
            sdfile.write('{0}\n'.format(sd))

    with open("communitiesFeb2016.txt", "a") as commfile:
        for comm in commList:
            commfile.write('{0}\n'.format(comm))


# ################################################

def removeDuplicatedEntries():

    months = ['April2015', 'May2015', 'June2015', 'July2015', 'Sept2015', 'Oct2015', 'Nov2015', 'Dec2015', 'Jan2016', 'Feb2016']

    with open("communitiesApril_Feb.txt", "a") as allFile:
        for month in months:
            sdFile = "communities{0}.txt".format(month)
            print sdFile
            with open(sdFile, 'r') as readFile:
                for line in readFile:
                    allFile.write('{0}'.format(line))


# ################################################

#runGraphs = runAoOStats(fileIn, fileSheet)

#getDuplicates = gatherDuplicates(fileInFeb, fileSheet)

removeDuplicates = removeDuplicatedEntries()

