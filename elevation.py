#this is another test
#https://developers.google.com/maps/documentation/elevation/

import urllib.parse
import urllib.request
import simplejson
import math
import sys
import webbrowser

debug = False

def is_not_white(rgb):
    return not is_white(rgb)

def is_white(rgb):
    if rgb[0] == 255 and rgb[1] == 255 and rgb[2] == 255:
        return True
    return False

def is_a_shade_of_green(rgb):
    if rgb[1] > rgb[0] and rgb[1] > rgb[2]:
        return True
    return False


def analyize_picture(filename):
    pixelList = []
    im = Image.open(filename)
    image_height = im.size[1]
    image_width = im.size[0]
    pixels = list(im.getdata())
    info = []
    if(im.mode == "RGB"):
        for x in range(image_width):
            temp_lst = []
            for y in range(image_height):
                offset = x * image_height + 7
                if is_a_shade_of_green(pixels[offset]):
                    temp_list.append(1)
                else:
                    temp_list.append(0)
            info.append(temp_list)
    else:
        print("ERROR: the im.mode is not RGB")
    


#---------------------------------------------------------------
# Targeting Algorithm Stuff
#---------------------------------------------------------------
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

    elevationArray = []
    for resultset in response['results']:
        elevationArray.append(resultset['elevation'])
    get_chart(chartData=elevationArray)

'''------get_values-----
    purpose: gets our dted data from google maps api
    input:  uav position information, target position information
    output: dted data
'''
def get_values(uavPosition, targetPosition):

    path = str(uavPosition[0]) + ',' + str(uavPosition[1]) + "|"+ str(targetPosition[0]) +','+ str(targetPosition[1])
    URL_BASE = 'http://maps.googleapis.com/maps/api/elevation/json'
    elvtn_args = {'path':path,'samples':"100",'sensor':"false"}
    URL = URL_BASE + "?" + urllib.parse.urlencode(elvtn_args)
    response = simplejson.load(urllib.request.urlopen(URL))
    terrainInfo = []
    if response['status'] == 'OK':
        for resultset in response['results']:
            tempArr = [resultset['elevation'],resultset['location']['lat'],resultset['location']['lng']]
            terrainInfo.append(tempArr)
        return terrainInfo
    else:
        print("there was an error")
    return None

'''------print_stuff-----
    purpose: gets rid of all values equal to zero.
             this is a translation of a MATLAB funciton
    input:  a list of values
    output: a sub list of valuea
'''
def find(values):
    for item in values:
        if item == 0:
            values.remove(item)
    return values

'''------print_stuff-----
    purpose: prints information verbosly
    input:  title of the information, the information
    output: none
'''
def print_stuff(title,msg):
    global debug
    if debug:
        print('---%s---' % title)
        print(msg)
        print('-------------')

'''------get_updated_position-----
    purpose: finds the real distance of the target
    input:  uav position information, target position information, dted data, the distance, a threshold value
    output: returns the distace in degrees on the surface of the earth
'''
def get_updated_position(uavPosition,targetPosition,dted,distance,threshold):
    possible_target_values = []
    for value in dted:
        temp_height = value[0] - targetPosition['ground_elevation']
        temp_distance = distance*(1-(uavPosition['alt']/temp_height))

        error = math.tan(math.degrees(90 - math.fabs(uavPosition['pitch'])) - ((distance - temp_distance)/temp_height))
        possible_target_values.append((temp_distance,temp_height,math.fabs(error)))
    min_value = 100000000
    for pair in possible_target_values:
        #print("pair[0]: %f | pair[1]: %f | pair[2] :%f" % (pair[0],pair[1],pair[2]))
        if pair[2] < min_value and pair[0] > 0:
            min_value = pair[2]
            distance = pair[0]
            targetPosition['ground_elevation'] = pair[1]

    print_stuff("Real Distance",distance)

    return distance

'''------get_degrees-----
    purpose: converts the give distance to degrees on the surface of the earth
    input:  the distance
    output: returns the distace in degrees on the surface of the earth
'''
def get_degrees(distance):
    #print(math.degrees(math.atan(distance/6371000)))
    
    return math.degrees(math.atan(distance/6371000))

'''------get_position-----
    purpose: finds the lat and long of the target
    input:  uav position information, target position information
    output: updated target position information
'''
def get_position(uavPosition,targetPosition):

    
    #step 1
    #R = h * tan(90 - theta
    # R = distance.  R is an awful variable name  same with Psi and theta
    #figure out which one is right
    distance = uavPosition['alt'] * math.tan(math.radians(90 - math.fabs(uavPosition['pitch'])))
    #print("distance: %f" % distance)

    #step 2
    # DTED values at some interval along the line traced out by distance R.  Also find the vehicle's lcoal
    #sin = y
    #cos = x
    #target = {'lat':0,'long':0}
    targetPosition['lat'] = uavPosition['lat'] + get_degrees(distance * math.sin(math.radians(uavPosition['heading'])))
    
    targetPosition['long'] = uavPosition['long'] + get_degrees(distance * math.cos(math.radians(uavPosition['heading'])))
    print_stuff('target latitude',targetPosition['lat'])
    print_stuff('target longitude',targetPosition['long'])
    dted = get_values((uavPosition['lat'],uavPosition['long']),(target['lat'],target['long']))
    uavPosition['ground_elevation'] = dted[0][0]
    print_stuff('uav ground elevation', uavPosition['ground_elevation'])
    
    slopes = []
    dx = distance/100.0 # this is a distance interval
    print_stuff('dx',dx)
    #print("\n\n\n" , dted)
    total = 0
    for i,item in enumerate(dted):
        if i == 0:
            continue
        #print("(%f - %f)/%f = %f" % (item[0],dted[i-1][0],dx,((item[0] - dted[i-1][0])/dx)))
        slopes.append((item[0] - dted[i-1][0])/dx)
        total += (item[0] - dted[i-1][0])/dx
    print_stuff('slopes',slopes)
    average = total/len(slopes)
    
    #print("total: %f" % total)
    #print("Average: %f" % average)
    
    if average > 0:
        
        #targetPosition['ground_elevation'] = 0 
        distance =  get_updated_position(uavPosition,targetPosition,dted,distance,1)
    elif average < 0:
        
        #targetPosition['ground_elevation'] = 0
        distance = get_updated_position(uavPosition,targetPosition,dted,distance,0.1)
    elif average == 0:
        pass# distance
    targetPosition['lat'] = uavPosition['lat'] + get_degrees(distance * math.cos(math.degrees(uavPosition['heading'])))
    targetPosition['long'] = uavPosition['long'] + get_degrees(distance + math.sin(math.degrees(uavPosition['heading'])))
    
    print("Longitude: %f" % targetPosition['long'])
    print("Latitude: %f" % targetPosition['lat'])
    return targetPosition

def parse_line(text,keyword,value):
    index = text.find(keyword)
    return text[:index+2] + str(value)
    

def write_webpage(uavPosition,targetPosition,webpage_filename):
    
    template_filename = 'Template.html'

    template = open(template_filename,'r')
    webpage = open(webpage_filename,'w')
    for line in template:
        if 'uavLat' in line and "Position" not in line:
            line = parse_line(line,'=',uavPosition['lat'])
            line += '\n'
        if 'uavLng' in line and "Position" not in line:
            line = parse_line(line,'=',uavPosition['long'])
            line += '\n'
        if 'targetLat' in line and "Position" not in line:
            line = parse_line(line,'=',targetPosition['lat'])
            line += '\n'
        if 'targetLng' in line and "Position" not in line:
            line = parse_line(line,'=',targetPosition['long'])
            line += '\n'
            
        webpage.write(line)
    template.close()
    webpage.flush()
    webpage.close()

'''------display_map-----
    purpose: displays a map with target information
    input:  target position information
    output: none
'''
def display_map(uavPosition,targetPosition):
    webpage_filename = 'webpage.html' #will change file name with date info
    write_webpage(uavPosition,targetPosition,webpage_filename)

    #now display the map
    webbrowser.open_new(webpage_filename)

if __name__ == "__main__":
    test_target = True
    test_picture = False
    filename = 'test.jpg'
    args = {}
    target = {}
    #units are in meters
    args.update({
        'lat':43.0000000,
        'long':-73.0000000,
        'alt':50,
        'pitch':-45,
        'heading':269,
        'ground_elevation':0
        })
    target.update({
        'lat':0.0000000,
        'long':0.0000000,
        'alt':0, 
        'pitch':0,
        'heading':0,
        'ground_elevation':0
        })
    if test_picture:
        analyize_picture(filename)
    if test_target:
        target = get_position(args,target)
        display_map(args,target)
    

        

