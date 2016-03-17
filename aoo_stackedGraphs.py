import numpy as np
import pandas as pd
import plotly.plotly as py
py.sign_in('deemariek', 'ep0os2f0m3')
import plotly.graph_objs as go
from collections import OrderedDict


"""
this script to automate graph creation for AoO outputs - stacked bar charts

"""

# update these values each month to reflect the data filenames
roundNumber = '10'
monthYear = 'Feb2016'

fileIn = 'AoO_Round{0}_{1}_Dataset_recode_v2.xlsx'.format(roundNumber, monthYear)
fileSheet = 'AoO_Round10_Feb2016_Dataset'


sector_Qus = {
              'shelter' : {'Shelter/G_QC004_1/QC004_Min_how_much_did_they_pay_per_room', 
                         'Shelter/G_QC004_1/QC004_Max_how_much_did_they_pay_per_room'}
             }
                  

# ################################################


def makeAoOStackedGraphs(df, governorate, values):

    # assign the column names passed as arg tuple
    for v in values:
        if 'Max' in v:
            maxShelter = v
        elif 'Min' in v:
            minShelter = v

    print "\t...{0} data subset ".format(maxShelter.split("/")[0])
    # get subset dataframe for governorate of interest
    df_Graph = df[(df['GEO_Governorate_Assessed_location'] == governorate)]
    df_Graph.set_index(["key"], inplace=False)

    # get average max and min rent values for the governorate
    maxRent = int(df_Graph[maxShelter].mean())
    minRent = int(df_Graph[minShelter].mean())
    maxRentText = 'Governorate average max: {0} SYP'.format(maxRent)
    minRentText = 'Governorate average min: {0} SYP'.format(minRent)

    #  determine which column to select by as Damascus is neighbourhoods not SDs
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
        name = 'Min per room',
        orientation='h',
        marker=dict(
                color='rgb(88,88,90)',
            )
        )
    # max rent bar 
    trace2 = go.Bar(
        x = deltaMaxRent_SDs,
        y = sdNames,
        name = 'Max per room',
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
            l=200,
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

    # add data and layout to Figure
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename='graphs/shelter_{0}.png'.format(governorate))
    print  "Graphs saved"
    #plot_url = py.plot(fig, filename='hello')


# ################################################

def runAoOGraphs(fileIn, fileSheet):
    # load full HSOS dataset
    df = pd.DataFrame()
    data = pd.read_excel(fileIn, fileSheet)
    df = df.append(data) 
    print "Data loaded"
    print
    # get list of all the governorates in the dataset
    govList = pd.unique(df['GEO_Governorate_Assessed_location'].ravel())
    # iterate through each gov, get data and make graph
    for gov in govList:
        #if gov == "Lattakia":
        if gov == "Rural Damascus":
            for key, values in sector_Qus.iteritems():
                print "Processing {0} for  {1}...".format(key, gov)
                graphAoOData = makeAoOStackedGraphs(df, gov, values)
        else:
            pass
    print  "Graphs complete"


# ################################################

runGraphs = runAoOGraphs(fileIn, fileSheet)