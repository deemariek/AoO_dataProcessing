import pandas as pd

# global variables
confSheet = 'Sheet1'

# set file paths and sheet names
confMatrix = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round8_December2015\\Data Collection\\headings.xlsx'
output = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round8_December2015\\Data Collection\\headings_output.xlsx'

questions = ['Displacement', 'Health', 'NFI', 'WASH', 'Shelter', 'Education', 'Food_Security', 'Livelihoods']


# ########################################################


def readConfMatrix(confMatrix, confSheet):

	# read in a store the list of ordinal variables
    df = pd.DataFrame()
    data_conf = pd.read_excel(confMatrix, confSheet)
    df = df.append(data_conf) 
    print "{0} loaded".format(confMatrix)

    # test = df_conf["Displacement QB001"]
    # print test

    # for index, row in df.iterrows():
    #     print row
    #     df.loc[x, 'type'] = row

    cols = list(df.columns)
    # select the column from where will we will generate further columns
    colTypes = df['key']
    # iterate through the length of the 'type' column and 
    # append data into question_type and choices as appropriate
    for x in range(0, len(colTypes)):
        qType = colTypes[x]
        if qType.startswith("Conf_"):
            df.loc[x, 'type'] = " "
        #if qtSplit[0]:
        else:
            splitLine = qType.split("/")
            if len(splitLine) > 2:
                if splitLine[0] in questions:
                    lastIndex = len(splitLine)-1
                    optionEntry = splitLine[lastIndex].replace("_", " ")
                    df.loc[x, 'type'] = optionEntry
                    #print optionEntry
            

    #print df

    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer, sheet_name='survey', index=False)

    
# ########################################################


runConfMatrix = readConfMatrix(confMatrix, confSheet)