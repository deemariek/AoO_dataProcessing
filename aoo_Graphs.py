import numpy as np
import pandas as pd
import plotly.plotly as py
py.sign_in('deemariek', 'ep0os2f0m3')
import plotly.graph_objs as go
from collections import OrderedDict


"""
this script to automate graph creation for AoO outputs - bar and stacked charts

"""

# update these values each month to reflect the data filenames
roundNumber = '12'
monthYear = 'Apr2016'
monthYearLong = 'April2016'

# directory where the output files will be saved
graphDir = 'C:\\REACH\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\Factsheets_governorates\\Graphic\\Graphs'.format(roundNumber, monthYearLong)

# the filename of the recoded datatset, make sure it matches
fileIn = 'AoO_Round{0}_{1}_DatasetRC.xlsx'.format(roundNumber, monthYear)
fileSheet = 'AoO_Round{0}_{1}_Dataset'.format(roundNumber, monthYear)

# the variable containing all the AoO questions that we want to make graphs of
sector_Qus = {
              # bar charts
              'livelihoods' : {'Livelihoods/QH004_coping_strategies_lack_of_income_resrc_prev_month/'},
              'education': {'Education/QI002_rzn_school_aged_children_not_attend_prev_month/'},
              'wash1': {'WASH/QF005_problems_latrine_toilet_prev_month/'},
              'food1': {'Food_Security/QG001_How_people_obtain_food_prev_month/'},
              'food3': {'Food_Security/QG003_rzn_difficulties_access_enough_food_prev_month/'},
              'health': {'Health/QE007_most_health_problems_reported_prev_month/'},

              # stacked bar charts
              'shelter' : {'Shelter/G_QC004_1/QC004_Min_how_much_did_they_pay_per_room', 
                           'Shelter/G_QC004_1/QC004_Max_how_much_did_they_pay_per_room'},
              'disp2' : {'Displacement/G_QB014/QB014_1_min_paid_for_transport_from_village_to_border',
                         'Displacement/G_QB014/QB014_2_max_paid_for_transport_from_village_to_border'}
               }

columnRecode = { #QH004 
                'Children_sent_to_work_or_begRC': 'Children sent to<br>work or beg', 
                'Taking_loans_buying_on_credit_informal_formalRC': 'Taking loans/<br>buying on credit', 
                'Borrowing_money_from_family_friendsRC': 'Borrowing money<br>from family friends',
                'High_risk_illegal_workRC': 'High risk<br>illegal work', 
                'Looking_for_food_in_garbageRC': 'Looking for food<br>in garbage', 
                'Adults_beggingRC': 'Adults begging', 
                'Selling_household_assetsRC': 'Selling<br>household assets', 
                'Skipping_mealsRC': 'Skipping meals', 
                'Reducing_size_of_mealsRC': 'Reducing size<br>of meals', 
                'Spending_days_without_eatingRC': 'Spending days<br>without eating', 
                'Eating_weedsRC': 'Eating weeds', 
                #QI002
                'Services_exist_but_are_not_accessibleRC': 'Services exist but<br>are not accessible',
                'Distance_to_services_is_too_farRC': 'Distance to<br>services is too far', 
                'due_to_destruction_of_facilitiesRC': 'Due to destruction<br>of facilities', 
                'Route_to_services_is_unsafeRC': 'Route to services<br>is unsafe', 
                'due_to_lack_of_school_suppliesRC': 'Due to lack of<br>school supplies', 
                'Parents_do_not_approve_of_curriculumRC': 'Parents do not<br>approve of curriculum', 
                'due_to_lack_of_teaching_staffRC': 'Due to lack of<br>teaching staff', 
                'All_children_access_education_servicesRC': 'All children access<br>education services',
                'Services_have_no_spaces_availableRC' : 'Services have no<br>spaces available',
                #QF005
                'Too_crowded_not_sufficientRC': 'Too crowded/<br>not sufficient', 
                'not_cleanRC': 'Not clean', 
                'Connection_to_sewage_blockedRC': 'Connection to<br>sewage blocked', 
                'Cannot_empty_septic_tankRC': 'Cannot empty<br>septic tank', 
                'no_water_to_flushRC': 'No water<br>to flush', 
                'There_are_no_problemsRC': 'There are<br>no problems',
                #QG001
                'Received_from_others_relatives_friendsRC': 'Received from others<br>relatives friends', 
                'Received_through_food_distributionsRC': 'Received through<br>food distributions', 
                'BarteringRC': 'Bartering', 
                'Own_productionRC': 'Own production', 
                'PurchasedRC': 'Purchased',
                #QG003
                'Local_food_production_has_decreasedRC': 'Local food production<br>has decreased', 
                'There_were_no_challengesRC': 'There were<br>no challenges', 
                'Lack_of_access_to_marketRC': 'Lack of access<br>to market', 
                'lack_of_availability_of_cooking_fuelRC': 'Lack of availability<br>of cooking fuel', 
                'Some_food_items_not_available_on_marketRC': 'Some food items <br>unavailable on market', 
                'lack_of_resources_to_buy_food_available_in_the_marketsRC': 'Lack of resources<br>to buy available food', 
                'Some_types_of_foods_too_expensiveRC': 'Some types of foods<br>too expensive',
                'lack_of_access_to_available_cooking_fuelRC': 'Lack of access to <br>available cooking fuel',
                #QE007 
                'Skin_diseaseRC': 'Skin disease',
                'FeverRC': 'Fever',
                'Symptoms_of_psychological_traumaRC' : 'Symptoms of<br>psychological trauma',
                'Communicable_diseasesRC': 'Communicable<br>diseases',
                'DisabilitiesRC': 'Disabilities',
                'InjuriesRC': 'Injuries',
                'Maternal_health_issuesRC': 'Maternal health<br>issues',
                'Severe_diseases_affecting_those_aged_less_than_5RC': 'Severe diseases affecting<br>those aged < 5',
                'MalnutritionRC' : 'Malnutrition',
                'DiarrheaRC' : 'Diarrhea',
                'Acute_respiratory_InfectionsRC': 'Acute respiratory<br>infections',
                'Chronic_diseases_no_access_medicineRC': 'Chronic diseases (no<br>access medicine)',
                'Pregnancy_related_diseasesRC' : 'Pregnancy related<br>diseases',
                'PolioRC' : 'Polio',
                # others
                'OtherRC': 'Other',
                'otherRC': 'Other',
                }                    



# ################################################


def makeAoOStackedGraphs(df, governorate, values, graphName):

    # assign the column names passed as arg tuple
    for v in values:
        if 'Max' in v or 'max' in v:
            maxShelter = v
        elif 'Min' in v or 'min' in v:
            minShelter = v

    print "\t...{0} data subset ".format(maxShelter.split("/")[0])
    # get subset dataframe for governorate of interest
    df_Graph = df[(df['GEO_Governorate_Assessed_location'] == governorate)]
    df_Graph.set_index(["key"], inplace=False)

    maxMean = df_Graph[maxShelter].mean()
    minMean = df_Graph[minShelter].mean()

    # get average max and min rent values for the governorate
    if maxMean > 1:
        maxRent = int(maxMean)
    else:
        maxRent = 0
    if maxMean > 1:
        minRent = int(minMean)
    else:
        minRent = 0
    maxRentText = 'Governorate average max: {0} SYP'.format(maxRent)
    minRentText = 'Governorate average min: {0} SYP'.format(minRent)

    #  determine which column to select by, as Damascus its by neighbourhoods not SDs
    if governorate == 'Damascus':
        selection = 'GEO_Village_Assessed_location'
    else:
        selection = 'GEO_Subdistrict_Assessed_location'

    rentDict = {}
    # get list of subdistricts within the governorate of interest
    SDList = pd.unique(df_Graph[selection].ravel())
    for sd in SDList:
        # create smaller subset dataframe for the subdistrict/neighbourhood of interest
        df_SD = df_Graph[(df_Graph[selection] == sd)]
        # get max and min rent values for each subdistrict/neighbourhood
        sd_maxRent = df_SD[maxShelter].mean()
        sd_minRent = df_SD[minShelter].mean()
        # edit the name value for Damascus neighbourhoods
        if sd.startswith("Damascus"):
            sd = sd.replace("Damascus (", " ")
            sd = sd.replace(")", " ")
        # exclude subdistricts with 'nan' - no information
        if sd_maxRent > 1:
            # add subdistricts as keys to rentDict with max and min rent as values - important max is added first
            if sd not in rentDict:
                rentDict[sd] = [sd_maxRent,sd_minRent]
            else:
                rentDict[sd].append(sd_maxRent, sd_minRent)
        else:
            pass

    # sort subdistricts based on max rent value
    rentOrdered = OrderedDict(sorted(rentDict.items(), key=lambda t: t[1][0]))
    
    sdNames = []                # list of SD/neighbourhood names
    maxRent_SDs = []            # list of max rent prices
    minRent_SDs = []            # list of min rent prices
    deltaMaxRent_SDs = []       # list of delta between max and min rent prices - used to show max in graphs
    avgMaxRent = []             # list of avg max rent prices - repeats avg price for every SD entry - used to plot avg line on graph
    avgMinRent = []             # list of avg min rent prices - repeats avg price for every SD entry - used to plot avg line on graph

    # create separate lists of the SD name, max rent and min rent values
    for key, values in rentOrdered.iteritems():
        sdNames.append(key)
        maxRent_SDs.append(values[0])
        minRent_SDs.append(values[1])
        delta = values[0]-values[1]
        deltaMaxRent_SDs.append(delta)
        # also append max/min rent values to separate lists
        avgMaxRent.append(maxRent)
        avgMinRent.append(minRent)

    # text for maxRent
    annotations1 = [dict(
                    x=0.5,
                    y=1.05,
                    xref='paper',
                    yref='paper',
                    text=str(maxRentText),
                    font=dict(family="Arial",size=18),
                    xanchor='center',
                    yanchor='bottom',
                    showarrow=False,
                )]
    # text for minRent
    annotations2 = [dict(
                    x=0.5,
                    y=0.98,
                    xref='paper',
                    yref='paper',
                    text=str(minRentText),
                    font=dict(family="Arial",size=18),
                    xanchor='center',
                    yanchor='bottom',
                    showarrow=False,
                )]

    # text annotation with names of assessed SD/neighbourhoods
    annotations3 = [dict(
                    x=-0.02,
                    y=yi,
                    xref='paper',
                    # yref='paper',
                    align='right',
                    text=str(yi),
                    font=dict(family="Arial",size=18),
                    xanchor='right',
                    yanchor='center',
                    showarrow=False,
                ) for xi, yi in zip(minRent_SDs, sdNames)]

    annotations = annotations1+annotations2+annotations3
    
    # min rent bar
    trace1 = go.Bar(
        x = minRent_SDs,
        y = sdNames,
        showlegend=False,
        name = 'Min paid for room',
        orientation='h',
        marker=dict(
                color='rgb(88,88,90)',
            )
        )
    # max rent bar 
    trace2 = go.Bar(
        x = deltaMaxRent_SDs,
        y = sdNames,
        showlegend=False,
        name = 'Max paid for room',
        orientation='h',
        marker=dict(
                color='rgb(237,87,88)',
            )
        )
    # min rent line
    trace3 = go.Scatter(
        x = avgMinRent,
        y = sdNames,
        showlegend=False,
        name = "Avg min rent",
        mode='lines',
        line=dict(
                color='rgb(0,0,0)',
            )
        )
    # max rent line
    trace4 = go.Scatter(
        x = avgMaxRent,
        y = sdNames,
        showlegend=False,
        name = "Avg max rent",
        mode='lines',
        line=dict(
                color='rgb(0,0,0)',
            )
        )

    # add data 
    data = [trace1, trace2, trace3, trace4]
    
    # graph layout
    layout = go.Layout(
        barmode='stack',
        height=400,
        width=600,
        margin=dict(
            l=150,
            r=40,
            t=40,
            b=40,
            pad=10
        ),
        showlegend=True,
        legend=dict(
                x=0.95,
                y=0.1,
                xanchor="right",
                yanchor="bottom",
                font=dict(family="Arial",size=16)),
        xaxis=dict(
            showgrid=False,
            showline=True,
            ticks="outside",
            showticklabels=True,
            ticksuffix=' SYP',
            zeroline=False,
                ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            tickfont=dict(
                size=14)
                ),
            annotations=annotations,
        )

    # add data and layout to Figures
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename='{1}/{2}_{0}.png'.format(governorate, graphDir, graphName))
    #py.image.save_as(fig, filename='graphs2/{1}_{0}.png'.format(governorate, graphName))
    print  "\t...Graph saved"


# ################################################


def getAoOGraphData(df, governorate, sector):

    df_Graph = df[(df['GEO_Governorate_Assessed_location'] == governorate)]
    df_Graph.set_index(["key"], inplace=False)

    dataset_columns = df_Graph.columns.tolist()
    responseDict = {}
    for d in dataset_columns:
    	if d.startswith(sector) and d.endswith("RC"):
           communitiesNumber = int(df_Graph[d].count())
           columnValue = int(df_Graph[d].sum())
           if columnValue > 0:
            response = str(d.split("/")[2])
            if response not in responseDict:
                responseDict[response] = [columnValue]
            else:
                responseDict[response].append(columnValue)
           else:
            pass

    responseOrdered = OrderedDict(sorted(responseDict.items(), key=lambda t: t[1]))
    objects = []
    performance = []
    for key, values in responseOrdered.iteritems():
        obText = columnRecode[key]
        objects.append(obText)
        for v in values:
            performance.append(v)

    return (objects, performance, communitiesNumber)

# ################################################

def makeGraph(graphAoOData, governorate, key):

    #numberText = '# of communities reported<br>(of {0} assessed)'.format(graphAoOData[2])
    performance = graphAoOData[1]
    objects = graphAoOData[0]

    # dynamically create the height for the graph
    countObjects = len(objects)
    height = 100*countObjects
    if height > 600:
        height = 600

    # the numbers at the end of the bars
    annotations1 = [dict(
                    x=xi+0.25,
                    y=yi,
                    text=str(xi),
                    font=dict(family="Arial",size=20),
                    xanchor='left',
                    yanchor='center',
                    showarrow=False,
                ) for xi, yi in zip(performance, objects)]
    annotations2 = [dict(
                    x=-0.02,
                    y=yi,
                    # xref='paper',
                    # yref='paper',
                    align='right',
                    text=str(yi),
                    font=dict(family="Arial",size=18),
                    xanchor='right',
                    yanchor='center',
                    showarrow=False,
                ) for xi, yi in zip(performance, objects)]
    annotations = annotations1 + annotations2
    data = [
        go.Bar(
            x=performance,
            y=objects,
            name='sectorGraph',
            orientation='h',
            showlegend=False,
            marker=dict(
                    color='rgb(237,87,88)',
            )
        )
    ]
    layout = go.Layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        #barmode='stack',
        height=height,
        width=600,
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(255,255,255)',
        margin=dict(
            l=2,
            r=2,
            t=2,
            b=2,
            pad=2
        ),
        showlegend=False,
        annotations=annotations    
    )

    fig = go.Figure(data=data, layout=layout)
    governorate = governorate.replace("-", " ")
    py.image.save_as(fig, filename='{2}/{0}_{1}.png'.format(key, governorate, graphDir))
    #py.image.save_as(fig, filename='graphs2/{0}_{1}.png'.format(key, governorate, graphDir))
    print "\t...{0} graph saved...".format(key)

# ################################################

def runAoOGraphs(fileIn, fileSheet):
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "Data loaded"
    print
    govList = pd.unique(df['GEO_Governorate_Assessed_location'].ravel())
    for gov in govList:
        print "Processing {0}...".format(gov)
        for key, values in sector_Qus.iteritems():
            if len(values) == 1 :
                for v in values:
                    graphAoOData = getAoOGraphData(df, gov, v)
                    makeAoOGraph = makeGraph(graphAoOData, gov, key)
            if len(values) == 2:
                #print "Processing {0} for {1}...".format(key, gov)
                graphAoOData = makeAoOStackedGraphs(df, gov, values, key)
 

    print  "Graphs complete"


# ################################################

runGraphs = runAoOGraphs(fileIn, fileSheet)