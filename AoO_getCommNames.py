import os
import pandas as pd
import csv
import operator
import numpy as np
from StringIO import StringIO
# this makes the header style not bold
pd.core.format.header_style = None

dirPath = "C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round10_February2016\\Data Collection\\AoO_Round10_Python"

AoO_inputDataset = os.path.join(dirPath,'AoO_Round10_Feb2016_Dataset_Merged.xlsx')
dataSheet = 'All_KI_Village_Level_Monitoring'

AoO_geoOutput = os.path.join(dirPath,'AoO_Round10_Feb2016_Dataset_Merged_Geo.xlsx')

# Geo data - pcodes
geoData = os.path.join(dirPath,'SYRadmin.xlsx')

# ########################################################

def insertGeoData(inputFile):
    """
    Add in the geo data for each response based on the pcode provided
    Return a dataFrame with no other changes except new 'GEO_' columns and entries
    """

    print "Inserting GEO_ data into the dataFrame"
    # load pcode file as dataFrame
    df_Geo = pd.DataFrame()
    data_Geo = pd.read_excel(geoData, "SYRadmin")
    df_Geo = df_Geo.append(data_Geo) 
    print "{0} loaded".format(geoData)

    # load AoO dataFrame
    df = pd.DataFrame()
    data = pd.read_excel(inputFile, dataSheet)
    df = df.append(data) 
    print "{0} loaded".format(inputFile)

    # insert the GEO column to the dataFrame, the insert location is hard coded
    df.insert(12, "GEO_Village_Assessed_location", "No information")            # Name_Eng    

    # iterate through all the dataframe rows and locate each response's village location info 
    # then iterate through the pcode dataframe and locate the relevant hierarchical codes
    for index, row in df.iterrows():
        p = row['Village_Assessed_location']
        subLoc = row['Subdistrict_Assessed_location']
        # if the village location is a correct 'XXXX' community level pcode
        if type(p) == int:
            for row in df_Geo.itertuples():
                if row[2] == p:
                    df.loc[index, "GEO_Village_Assessed_location"] = row[1]
                else:
                    pass
        # if the village location is given as 'other'
        elif str(p) == 'other':
            for row in df_Geo.itertuples():
                if row[4] == subLoc:
                    df.loc[index, "GEO_Village_Assessed_location"] = "other"
                else:
                    pass
        # else if village location starts with 'SY'
        elif p.startswith("SY"):
            for row in df_Geo.itertuples():
                if row[2] == p:
                    df.loc[index, "GEO_Village_Assessed_location"] = row[1]
        else:
            print "Error processing geodata for {0}".format(p)

    # save the non-duplicates dataframe
    with pd.ExcelWriter(AoO_geoOutput) as writer:
        df.to_excel(writer, sheet_name='dataset_Geo', index=True)
    
    print "Saved file {0} with geo data".format(AoO_geoOutput)



# ########################################################



# update the dataFrame to have the GEO data according to its pcode and SYRadmin file
addGeoData = insertGeoData(AoO_inputDataset)