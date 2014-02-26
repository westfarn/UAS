#this is another test
#https://developers.google.com/maps/documentation/elevation/

import urllib.parse
import urllib.request
import simplejson
import math


def get_chart(chartData, chartDataScaling="-500,5000", chartType="lc",chartLabel="Elevation in Meters",chartSize="500x160",chartColor="orange", **chart_args):
    chart_args.update({
        'cht': chartType,
        'chs': chartSize,
        'chl': chartLabel,
        'chco': chartColor,
        'chds': chartDataScaling,
        'chxt': 'x,y',
        'chxr':'1,-500,5000'
        })

    dataString = "t:" + ','.join(str(x) for x in chartData)
    chart_args['chd'] = dataString.strip(',')
    URL_BASE = 'http://chart.apis.google.com/chart'
    URL = URL_BASE + "?" + urllib.parse.urlencode(chart_args)
    print('--------')
    print(URL)
    print('--------')

def get_elevation(path, samples="100", sensor="false",**elvtn_args):
    elvtn_args.update({
        'path':path,
        'samples':samples,
        'sensor':sensor
        })

    URL_BASE = 'http://maps.googleapis.com/maps/api/elevation/json'
    URL = URL_BASE + "?" + urllib.parse.urlencode(elvtn_args)
    print(URL)


    response = simplejson.load(urllib.request.urlopen(URL))

    #create a directory for each result[] object
    elevationArray = []

    for resultset in response['results']:
        elevationArray.append(resultset['elevation'])
    print(elevationArray)
    get_chart(chartData=elevationArray)

def get_values(uavPosition, targetPosition):

def get_position(args):
    #step 1
    #R = h * tan(90 - theta
    R =args['alt'](math.radians(90 - math.abs(args['pitch'])))

    #step 2
    # DTED values at some interval along the line traced out by distance R.  Also find the vehicle's lcoal
    values = get_values((args['lat'],args['long'],args['alt']),())

    #Step 3
    #Calculate R' values for each h' value using
    #R' = R(1 - (h'/h))

    #Step 4
    
    startPt = "36.578581,-118.291994"
    endPt = "36.23998,-116.83171"
    path = startPt +"|"+endPt
    get_elevation(path)
    
if __name__ == "__main__":
    args.update({
        'lat':0
        'long':0
        'alt':100
        'pitch':45
        })
    get_position()
    
