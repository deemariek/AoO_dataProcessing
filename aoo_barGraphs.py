import numpy as np
import pandas as pd
import plotly.plotly as py
py.sign_in('deemariek', 'ep0os2f0m3')
import plotly.graph_objs as go
from collections import OrderedDict


"""
this script to automate graph creation for AoO outputs - bar charts

"""

# update these values each month to reflect the data filenames
roundNumber = '10'
monthYear = 'Feb2016'

fileIn = 'AoO_Round{0}_{1}_Dataset_recode_v2.xlsx'.format(roundNumber, monthYear)
fileSheet = 'AoO_Round10_Feb2016_Dataset'

sector_Qus = {
              'livelihoods' : {'Livelihoods/QH004_coping_strategies_lack_of_income_resrc_pre_m/'},
              'education': {'Education/QI002_rzn_school_aged_children_not_attend_pre_m/'},
              'wash1': {'WASH/QF005_problems_latrine_toilet_pre_m/'},
              'food1': {'Food_Security/QG001_How_people_obtain_food_pre_m/'},
              'food2': {'Food_Security/QG003_rzn_difficulties_access_enough_food_pre_m/'},
              'health': {'Health/QE007_most_health_problems_reported_pre_m/'},
               }

columnDict = {  #QH004 
                'Children_sent_to_work_or_beg': 'Children sent to<br>work or beg', 
                'Taking_loans_buying_on_credit_informal_formal': 'Taking loans/<br>buying on credit', 
                'Borrowing_money_from_family_friends': 'Borrowing money<br>from family friends',
                'High_risk_illegal_work': 'High risk<br>illegal work', 
                'Looking_for_food_in_garbage': 'Looking for food<br>in garbage', 
                'Adults_begging': 'Adults begging', 
                'Selling_household_assets': 'Selling<br>household assets', 
                'Skipping_meals': 'Skipping meals', 
                'Reducing_size_of_meals': 'Reducing size<br>of meals', 
                'Spending_days_without_eating': 'Spending days<br>without eating', 
                'Eating_weeds': 'Eating weeds', 
                #QI002
                'Services_exist_but_are_not_accessible': 'Services exist but<br>are not accessible',
                'Distance_to_services_is_too_far': 'Distance to<br>services is too far', 
                'due_to_destruction_of_facilities': 'Due to destruction<br>of facilities', 
                'Route_to_services_is_unsafe': 'Route to services<br>is unsafe', 
                'due_to_lack_of_school_supplies': 'Due to lack of<br>school supplies', 
                'Parents_do_not_approve_of_curriculum': 'Parents do not<br>approve of curriculum', 
                'due_to_lack_of_teaching_staff': 'Due to lack of<br>teaching staff', 
                'All_children_access_education_services': 'All children access<br>education services',
                'Services_have_0_spaces_available' : 'Services have no<br>spaces available',
                #QF005
                'Too_crowded_not_sufficient': 'Too crowded/<br>not sufficient', 
                'not_clean': 'Not clean', 
                'Connection_to_sewage_blocked': 'Connection to<br>sewage blocked', 
                'Cannot_empty_septic_tank': 'Cannot empty<br>septic tank', 
                'no_water_to_flush': 'No water<br>to flush', 
                'There_are_no_problems': 'There are<br>no problems',
                #QG001
                'Received_from_others_relatives_friends': 'Received from others<br>relatives friends', 
                'Received_through_food_distributions': 'Received through<br>food distributions', 
                'Bartering': 'Bartering', 
                'Own_production': 'Own production', 
                'Purchased': 'Purchased',
                #QG003
                'Local_food_production_has_decreased': 'Local food production<br>has decreased', 
                'There_were_no_challenges': 'There were<br>no challenges', 
                'Lack_of_access_to_market': 'Lack of access<br>to market', 
                'lack_of_availability_of_cooking_fuel': 'Lack of availability<br>of cooking fuel', 
                'Some_food_items_not_available_on_market': 'Some food items <br>unavailable on market', 
                'lack_of_resources_to_buy_food_available_in_the_markets': 'Lack of resources<br>to buy available food', 
                'Some_types_of_foods_too_expensive': 'Some types of foods<br>too expensive',
                'lack_of_access_to_available_cooking_fuel': 'Lack of access to <br>available cooking fuel',
                #QE007 
                'Skin_disease': 'Skin disease',
                'Fever': 'Fever',
                'Symptoms_of_psychological_trauma' : 'Symptoms of<br>psychological trauma',
                'Communicable_diseases': 'Communicable<br>diseases',
                'Disabilities': 'Disabilities',
                'Injuries': 'Injuries',
                'Maternal_health_issues': 'Maternal health<br>issues',
                'Severe_diseases_affecting_those_aged_less_than_5': 'Severe diseases affecting<br>those aged < 5',
                'Malnutrition' : 'Malnutrition',
                'Diarrhea' : 'Diarrhea',
                'Acute_respiratory_Infections': 'Acute respiratory<br>infections',
                'Chronic_diseases_no_access_medicine': 'Chronic diseases (no<br>access medicine)',
                'Pregnancy_related_diseases' : 'Pregnancy related<br>diseases',
                'Polio' : 'Polio',
                # others
                'Other': 'Other',
                'other': 'Other',
                }                    

# ################################################


def getAoOGraphData(df, governorate, sector):

    print "\t...{0} data subset ".format(sector.split("/")[0])
    df_Graph = df[(df['GEO_Governorate_Assessed_location'] == governorate)]
    df_Graph.set_index(["key"], inplace=False)

    dataset_columns = df_Graph.columns.tolist()
    responseDict = {}
    for d in dataset_columns:
    	if d.startswith(sector):
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
        obText = columnDict[key]
        objects.append(obText)
        for v in values:
            performance.append(v)

    return (objects, performance, communitiesNumber)

# ################################################

def makeGraph(graphAoOData, governorate, key):

    numberText = '# of communities reported<br>(of {0} assessed)'.format(graphAoOData[2])
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
    # text annotation with number of assessed communities
    annotations2 = [dict(
                    x=0.99,
                    y=0.1,
                    xref='paper',
                    yref='paper',
                    text=str(numberText),
                    font=dict(family="Arial",size=20),
                    xanchor='right',
                    yanchor='center',
                    showarrow=False,
                )]
    # labels at start of bars
    annotations3 = [dict(
                    x=-0.02,
                    y=yi,
                    xref='paper',
                    yref='paper',
                    align='right',
                    text=str(yi),
                    font=dict(family="Arial",size=18),
                    xanchor='right',
                    yanchor='center',
                    showarrow=False,
                ) for xi, yi in zip(performance, objects)]
    annotations = annotations1 + annotations2 + annotations3
    data = [
        go.Bar(
            x=performance,
            y=objects,
            name='sectorGraph',
            orientation='h',
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
    #plot_url = py.plot(fig, filename='{0}_{1}'.format(key, governorate))
    py.image.save_as(fig, filename='graphs/{0}_{1}.png'.format(key, governorate))
    #py.image.save_as(fig, filename='hello.png')
    print "\t...Loading graph..."

# ################################################

def runAoOGraphs(fileIn, fileSheet):
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "Data loaded"
    print
    govList = pd.unique(df['GEO_Governorate_Assessed_location'].ravel())
    for gov in govList:
        if gov == "Idleb":
            print "Processing {0}...".format(gov)
            for key, values in sector_Qus.iteritems():
                for v in values:
                    graphAoOData = getAoOGraphData(df, gov, v)
                    makeAoOGraph = makeGraph(graphAoOData, gov, key)
        else:
            pass
    print  "Graphs complete"


# ################################################

runGraphs = runAoOGraphs(fileIn, fileSheet)