import os
import pandas as pd
pd.core.format.header_style = None
import csv
import operator

"""
this script produces a csv file with a records of each  
Syrian subdistrict and AoO aggregated data for certain questions
"""

roundNumber = '12'
monthYear = 'Apr2016'
monthYearLong = 'April2016'

# filenames for each month's appropriate dataset and sheet name
fileName = 'AoO_Round{0}_{1}_Dataset.xlsx'.format(roundNumber, monthYear)
fileSheet = 'AoO_Round{0}_{1}_Dataset'.format(roundNumber, monthYear)

fileIn = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\Data Collection\\AoO_Script_structure_latest\\AoO_Round12_R_DK_v2\\data_output\\{2}'.format(roundNumber, monthYearLong, fileName)
fileOut = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\Factsheets_governorates\\Table_Database\\AoO_Round{0}_subdistrictAgg1.csv'.format(roundNumber, monthYearLong)

# update each month according to the questions required for the factsheet
aggregateQuestions = [
                      'Displacement/QB001_num_Pre_conf_popul_remained_last_day_prev_month',
                      'Health/QE017_Where_women_delivered_babies',
                      'NFI/QD002_source_electricity_used_most_hours_prev_month',
                      'WASH/QF006_most_way_people_disposed_garbage_prev_month',
                      'Shelter/G_QC001/QC001_most_type_of_housing_this_village_prev_month',
                      'Education/G_QI001/QI001_Primary_school_available_prev_month']

# remove the aggQuestions string so that it's a bit more user friendly
aggregate_Questions = [ 'Displacement_QB001', 'Health_QE017', 'NFI_QD002', 'WASH_QF006', 'Shelter_QC001', 'Education_QI001']

# responses that shouldn't be included in aggregations
noResponse = ['No information', 'No consensus', 'No concensus']

# ################################################

def aggregateToSubDistrict(fileIn, fileSheet):
    """ This function takes a filename and the sheet name as arguments.
    The function aggregates through each SD and aggregated the values for each aggregateQuestion.
    The function returns a list of the aggregated values for each subdistrict.
    """
    # read the data in as a DataFrame
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "{0} loaded".format(fileIn)
    # empty list where the responses will eventually be appended to
    allResponses = []
    # locate the column on which you the script to aggregate, in this case 'Subdistrict_Assessed_location'
    subdistricts = df['Subdistrict_Assessed_location']
    # get list of unique values in the column
    subdistrictList = pd.unique(df.Subdistrict_Assessed_location.ravel())
    # get a Series containing the coverage counts for each subdistrict
    subCounts = subdistricts.value_counts()
    # iterate through the unique subdistrict values
    for sub in subdistrictList:
       # modeResponse is a string to which each subdistricts name, coverage and aggregated values are written to
       modeResponse = "{0},{1},".format(sub, subCounts[sub])
       # iterate through each of the questions of interest and get SD questions and confidence responses
       for aggQ in aggregateQuestions:
           # a list to contain SD responses
           responseList = []
           # a dict to contain SD question and conf responses
           resConfs = {}
           # start to iterate through the dataframe rows
           for index, row in df.iterrows():
              # find rows that relate to our current subdistrict
              if row['Subdistrict_Assessed_location'] == sub:
                   # get the question from the current subdistrict for the current aggQ
                   question = row[aggQ]
                   confidence = row['Conf_'+aggQ]
                   try: 
                     confidence = int(confidence)
                   except ValueError:
                     confidence = 0
                   # append values to list - used below to decide if we need to aggregate or not 
                   responseList.append(str(question))
                   # only include responses on which we want to aggregate
                   if question not in noResponse:
                       # add to dict, add conf value to question key if key already there
                       if question not in resConfs:
                           resConfs[question] = [confidence]
                       else:
                           resConfs[question].append(confidence)
                   else:
                        pass
           ## aggregation starts here             
           # only one response - therefore no need to aggregate
           if len(responseList) == 1:
                # add the response to the modeResponse variable
                modeResponse = modeResponse + "{0},".format(responseList[0])
           # we need to aggregate if there are more two responses for one subdistrict
           elif len(responseList) > 1:
                # check there are responses for that subdistrict, this is just an extra check
                if resConfs:
                    # a dict to contain response and the sum of their confidences
                    maxConfs = {}
                    for key, values in resConfs.iteritems():
                        # get the sum of the values (confidences) for each key (response)
                        sumValue = sum(values)
                        if key not in maxConfs:
                            maxConfs[key] = [sumValue]
                        else:
                            maxConfs[key].append(sumValue)

                    # get max value from confidence sums
                    maxValue = max(maxConfs.iteritems(), key=operator.itemgetter(1))[1]
                    # a list that will contain the final aggregated value for each subdistrict
                    keys = []
                    for key, values in maxConfs.iteritems():
                        if values == maxValue:
                            keys.append(key)
                        keyStr = "/".join(keys)
                    # we don't report on SDs that have more than two equally reported values
                    # if there are more than two items in the keys list then a value of 'No Concensus' is returned
                    if len(keys) <= 2:
                        modeResponse = modeResponse + "{0},".format(keyStr)
                    # return NC (No Concensus) if there are more than two equal options returned 
                    elif len(keys) > 2:
                        modeResponse = modeResponse + "{0},".format("No consensus")
                #if there are no responses, write 'NA' modeResponse
                else:
                    modeResponse = modeResponse + "{0},".format('No information')
           else:
                pass
       # the aggregated values for each aggregateQuestion are appended to allResponses after processing each subdistrict
       allResponses.append(modeResponse)
    print "Aggregated to subdistrict"
    # the full list of SDs and aggregated values is returned by the function
    return allResponses

# ################################################

def writeResponsesToCSV(inputData, outputFile):
    """ This function takes a list of data and an output filename as arguments.
    The function writes the data to the output file.
    districtHeading is the variables declared above.
    questionHeading is a string made from the aggregate_Questions list
    districtHeading and questionHeading become the first line of the text
    the inputData is appended to each line after that
    """
    print "Writing aggregations to {0}".format(outputFile)
    districtHeading = 'Subdistrict_Assessed_location'
    questionHeading = ",".join(aggregate_Questions)
    # create the heading line for the line
    heading = "{0},{1},{2}".format(districtHeading,'coverage',questionHeading)
    with open(outputFile, 'wb') as outFile:
        writer = csv.writer((outFile), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # write the heading line to the file
        writer.writerow([heading])
        # write each SD line to the output file
        for row in inputData:
            writer.writerow([row])
    print "Aggregation file saved"

# ################################################

# return a list of SDs and their aggregated values
aggregation = aggregateToSubDistrict(fileIn, fileSheet)

# write the aggregation list to the outut file
writeToFile = writeResponsesToCSV(aggregation, fileOut)
