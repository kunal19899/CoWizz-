# Library that gives us the functions to create
#   the map
import plotly.io as pio

# Reads csv files and sorts the states by their
#   fips codes
import pandas as pd

# Object that will be used to execute the 
#   map creation features 
import plotly.express as px

# Reads the map data from a website to help
#   generate the map
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# To find the proper path to find the html file we want to display
import os

# Used to import and run the C++ program to generate CSV files
import subprocess

# Calculate the elapsed time for each check for a map or csv file
import timeit


class map_test() :
  # Constructor
  def __init__( self, interval, sDate, fDate, rates ) :
    # Stores the number of days the user chooses
    self.interval = interval

    # Stores the start date
    self.sDate = sDate

    # Stores the final date
    self.fDate = fDate

    # Stores the rates of change
    self.rates = rates

    # Make mapHash() a global variable
    self.mapHash = {}

  # Runs entire checks for generating map
  def main( self ) :
    # Reads in user input from the website
    options = [ self.interval, self.sDate,
                self.fDate, self.rates ]
                
    if int(options[3]) == int(8) :
      options[3] = 'ALL'

    # Stores the name of the temporary key
    tempKey = ''

    # Creates a key using the user input
    for i in range( len(options) ) :
      tempKey = tempKey + str( options[i] )

      # Separates each element in the key by a hyphen
      if i != len(options) - 1 :
        tempKey = tempKey + '-' 

    # Reformats the key to be easier to read with the file names
    key = self.createKey( tempKey )

    # Each element is separated into
    keys = key.split( '-' )

    # Concatenates the strings that will be used for filename
    fName = ( keys[0] + '-CommID-Cases-' +
              keys[1] + '-' + keys[2] + '-' +
              keys[3] + 'vs' + keys[4] + '-' +
              keys[5] + '-' + keys[6] + 
              '-intDays' + keys[7] )
    
    # Creates a subdirectory for the data set if it doesn't exist
    subName = ( 'Cases-'+ keys[1] + '-' +
                keys[2] + '-' + keys[3] + 
                'vs' + keys[4] + '-' +
                keys[5] + '-' + keys[6] + 
                '-intDays' + keys[7] )

    # Calculate to generate map hash table
    start_time = timeit.default_timer()

    # Initialize the hash tables for
    #   the maps files
    self.mapHash = self.initMapHash()

    # End timer 
    elapsed = timeit.default_timer() - start_time

    # Calculate to generate map hash table
    start_time = timeit.default_timer()

    # Initialize the hash tables for
    #   the CSV files
    csvHash = self.initCSVHash()

    # End timer 
    elapsed = timeit.default_timer() - start_time

    # Check if there is a map for this dataset
    if self.mapHash.get( key ) == None :
      #print( "map key: %s does exist" % key )
      #fName = './v2/static/maps/' + subName + '/' + self.mapHash[key]
    #else :
      if csvHash.get( key ) == None :
        # Rewrite the configuration file with the csv information
        #   we want to read in
        with open( '/var/www/demosite/Covid19/v2/csvLayers/Covid19Period.conf', 'r' ) as fp :
          allLines = fp.readlines()
        fp.close()

        allLines[1] = (str(options[0])+'\r\n')  # Update new interval choice
        nDate = self.fixDate(options[1])
        allLines[3] = (nDate + '\r\n')     # Update new start date
        nDate = self.fixDate(options[2])
        allLines[5] = (nDate + '\r\n')     # Update new second date

        with open( '/var/www/demosite/Covid19/v2/csvLayers/Covid19Period.conf', 'w' ) as fp :
          fp.writelines(allLines)
        fp.close()
       
        subprocess.call(["/var/www/demosite/Covid19/v2/csvLayers/csvGenerator"])
        #print( "csv key: %s doesn't exist" % key ) 
      #print( "map key: %s doesn't exist" % key )

      # Creates a file path for where to store the map html files
      mapPath = '/var/www/demosite/Covid19/v2/static/maps/'+ subName
    
      # Checks if a directory for the map data set exists
      # If not, then we create one
      if not os.path.isdir( mapPath ) :
        try :
          os.mkdir( mapPath )
        except OSError :
          print ("Command mkdir for directory %s has failed." % mapPath)

      fig = self.generateMap( subName, fName )

      # Add key and value to the HTML hash table 
      with open( '/var/www/demosite/Covid19/v2/maptest/tables/html_table.txt', 'a' ) as fp :
        if fig is None :
          fp.write( key + ',' + '../default.html\r\n' )
        else :
          fp.write( key + ',' + fName + '.html\r\n' )

      fp.close()

      # Update the map hash table
      if fig is None :
        self.mapHash[key] = ( '../default.html' )
      else :
        self.mapHash[key] = ( fName + '.html' )

    return key
#-------------------------------------------------------------



  # Takes a filename and generates the map requested by the user 
  def generateMap( self, dirName, fName ) :
    """
    TODO: Create a way to parse a folder from filename

    """
    path = ( '/var/www/demosite/Covid19/v2/csvLayers/'+ dirName + 
             '/' + fName + '.csv' )

    # Reads in the info from our COVID data set
    df = pd.read_csv(path, dtype={"FIPS": str}, encoding='UTF-8')

    # Counts the number of lines in the CSV
    numLines = len(df.index)
 
    # If there are counties that have this change, we
    #   don't want to generate an html file, just use
    #   default.html
    if numLines == 0 :
      return None

    # We manually insert the CommunityID column in the DataFrame
    #   object so it is compatible with the cholopleth parameter
    if fName[:3] != 'ALL' :
      # The color parameter in the choropleth function
      #   only takes in int data types
      df.loc[:,'CommunityID'] = int( fName[0] )

    df['text'] = '<b>' + df['Area_Name'] + ', ' + df['State'] + '</b>'
    #             'Pop. Density per Square Mile: ' + str(df['DensityPerSquaremileOfLandarea-Population']) + '<br>' + \
    #             'Median Household Income in 2018: ' + str(df['Median_Household_Income_2018']) + '<br>' + \
    #             '% Adults with High School Diplomas: ' + str(df['Percent_of_adults_with_a_high_school_diploma_only_2014-18'])

    text = df['text'].tolist()

    # Creates the map object and fills it with 
    #   information
    # ASantra[11/15]: Added hovername for the County,State
    # ASantra[11/15]: Updated hover_data with dict specfying which columns to display. CommunityID error solved
    fig = px.choropleth(df, geojson=counties, locations='FIPS', color='CommunityID',
                               range_color=[1,7],
                               # color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                               # color_continuous_scale=px.colors.sequential.OrRd,
                               #color_continuous_scale=([(0.000, 'rgb(175, 45, 36)'), (0.142,'rgb(175, 45, 36)'), # dark red
                               #                          (0.142, 'rgb(193, 78, 79)'), (0.285,'rgb(193, 78, 79)'), # light red
                               #                          (0.285, 'rgb(202, 122, 92)'), (0.428,'rgb(202, 122, 92)'), # nude
                               #                          (0.428, 'rgb(211, 166, 88)'), (0.571,'rgb(211, 166, 88)'), # mustard
                               #                          (0.571, 'rgb(183, 192, 85)'), (0.714,'rgb(183, 192, 85)'), # olive 
                               #                          (0.714, 'rgb(143, 174, 98)'), (0.857,'rgb(143, 174, 98)'), # light green
                               #                          (0.857, 'rgb(119, 163, 111)'), (1.000,'rgb(119, 163, 111)')]), # green apple
                               color_continuous_scale=(['rgb(119, 163, 111)', # green apple
                                                        'rgb(143, 174, 98)', # light green
                                                        'rgb(183, 192, 85)', # olive
                                                        'rgb(211, 166, 88)', # mustard
                                                        'rgb(202, 122, 92)', # nude 
                                                        'rgb(193, 78, 79)', # light red
                                                        'rgb(175, 45, 36)']), # dark red
                               scope="usa",
                               labels={'State':'State',
                                       'Area_Name':'County',
                                       'text':'County, State',
                                       'Change%':'Change%',
                                       'DensityPerSquaremileOfLandarea-Population':'Pop. Density / Sq. Mile',
                                       'Median_Household_Income_2018':'Med. Household Income',
                                       'Percent_of_adults_with_a_high_school_diploma_only_2014-18':'% High School Graduates',
                                       'FIPS':'',
                                       'CommunityID':''},
                               hover_data={'Change%':True,
                                           'DensityPerSquaremileOfLandarea-Population':True, 
                                           'Median_Household_Income_2018':True, 
                                           'Percent_of_adults_with_a_high_school_diploma_only_2014-18':True,
                                           'CommunityID':False,
                                           'FIPS':False},
                               hover_name="text")
                               #hover_data=["text"])

    # Fixes and displays the legend to the 
    #   right of the map
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      coloraxis_colorbar = dict(
                        title = dict( 
                          text = "<b>Severity Rate<b><br>",
                          font = dict(
                            size = 13)),
                        ticks = 'inside',
                        tickvals = [1, 2, 3, 4, 5, 6, 7],
                        ticktext = ['<b>BIG DIP<b><br>-100%', '<b>DOWNTICK<b><br>(-100%,50%]', 
                                    '<b>DECREASE<b><br>(-50%, 0%)', '<b>FLAT<b><br>0%',
                                    '<b>INCREASE<b><br>(0%, 50%)', '<b>UPTICK<b><br>[50%, 100%)', 
                                    '<br><b>SPIKE<b><br>>=100%'],
                        tickfont = dict(
                          size = 9),
                        thickness = 35,
                        xpad = 5,
                        len = 0.85))

    # Displays the figure when program is executed    
    #fig.show()
 
    # Path to the specific directory the file is stored in 
    nDir  = ( '/var/www/demosite/Covid19/v2/static/maps/' + dirName + '/' )

    # Path to where to store the file for the hash table
    nFile = fName + '.html'

    # Creates an html file of the map
    pio.write_html(fig, file= nDir + nFile, auto_open=False)

    return fig
#-------------------------------------------------------------


  # Convert 3 character month to a 2 digit month
  def fixDate( self, dateVal ) :
    newMon = dateVal[3:6]

    if newMon == 'JAN' :
      newMon = dateVal[:3] + '01' + dateVal[-3:]
    elif newMon == 'FEB' :
      newMon = dateVal[:3] + '02' + dateVal[-3:]
    elif newMon == 'MAR' :
      newMon = dateVal[:3] + '03' + dateVal[-3:]
    elif newMon == 'APR' :
      newMon = dateVal[:3] + '04' + dateVal[-3:]
    elif newMon == 'MAY' :
      newMon = dateVal[:3] + '05' + dateVal[-3:]
    elif newMon == 'JUN' :
      newMon = dateVal[:3] + '06' + dateVal[-3:]
    elif newMon == 'JUL' :
      newMon = dateVal[:3] + '07' + dateVal[-3:]
    elif newMon == 'AUG' :
      newMon = dateVal[:3] + '08' + dateVal[-3:]
    elif newMon == 'SEP' :
      newMon = dateVal[:3] + '09' + dateVal[-3:]
    elif newMon == 'OCT' :
      newMon = dateVal[:3] + '10' + dateVal[-3:]
    elif newMon == 'NOV' :
      newMon = dateVal[:3] + '11' + dateVal[-3:]
    else :
      newMon = dateVal[:3] + '12' + dateVal[-3:]

    return( newMon )
#-------------------------------------------------------------



  # Initializes the CSV Hash Table
  def initCSVHash( self ) :
    # The dictionary that stores all the keys to
    #   the csv file we want to generate maps from
    csvHash = {}

    # Empties out the file before we store new values
    open( '/var/www/demosite/Covid19/v2/maptest/tables/csv_table.txt', 'w+' ).close()

    # Walks through each subdirectory in /cases/ and
    #   stores the names of the CSVs in csv_table.txt
    # ASantra: Other .csv may be present, need to ignore those
    for path, subd, files in os.walk( '/var/www/demosite/Covid19/v2/csvLayers/' ) :
      for names in files :
        # Only look for .csv files to store in our hash
        if (names[-3:] == 'csv'):
          keys = names.replace( '.', '-' ).split( '-' )

          # Only the keys and CSV files will be stored 
          #   in csv_table.txt
          if (len(keys) == 10) and (keys[-1] == 'csv'):
            # Creates the key for each value in the
            #   CSV hash table
            key = ( keys[0] + '-' + keys[3] + 
                    '-' + keys[4] + '-' + keys[5][:2] +
                    '-' + keys[5][-2:] + '-' + keys[6] +
                    '-' + keys[7] + '-' + keys[-2][7:] )
          
            # Writes the values to csv_table.txt
            with open( '/var/www/demosite/Covid19/v2/maptest/tables/csv_table.txt', 'a+' ) as fp :
              fp.write( key + ',' + names + '\r\n' )
          
            fp.close()

    with open( '/var/www/demosite/Covid19/v2/maptest/tables/csv_table.txt', 'r' ) as fp :
      lines = fp.read().replace( '\r', '' ).split( '\n' )

    # Checks if the file is not empty
    if lines[0] != '' :
      for line in lines :
        line = line.split( ',' )

        key = line[0]

        # Indicates an end of file
        if key == '' :
          val = ''
        else :
          val = line[1]

        csvHash[key] = val
  
    return csvHash
#-------------------------------------------------------------



  # Initializes the Map Hash Table
  def initMapHash( self ) : 
    # The dictionary that stores all the keys to
    #   the html file we want to display to the
    #   home page iframe
    mHash = {}

    with open( '/var/www/demosite/Covid19/v2/maptest/tables/html_table.txt', 'r' ) as fp :
      lines = fp.read().replace( '\r', '' ).split( '\n' )

    fp.close()

    # Checks if the file is not empty
    if lines[0] != '' :
      for line in lines :
        line = line.split( ',' )

        key = line[0]

        # Indicates an end of file
        if key == '' :
          val = ''
        else :
          val = line[1]

        mHash[key] = val
  
    return mHash
#-------------------------------------------------------------



  # Formats the key of the hash table to be similar
  #   the names of all the .csv and .html files 
  def createKey( self, tempKey ) :
    key = ''
    front = ''
    middle = ''
    end = ''

    if( tempKey.endswith('ALL') ) :
      # Holds the ALL part of the string to be moved
      #   to the front of a key
      front = tempKey[-3:]

      if tempKey[1] == '-' :
        # Rearranges the string for key in order for
        #   it to fit the format of each files that
        #   will need to be read in
        middle = tempKey[1:-3]
        end    = tempKey[:1]
      else : 
        middle = tempKey[2:-3]
        end = tempKey[:2]
    else :
      # Otherwise, last element in the key will be 
      #   a single digit
      front = tempKey[-1:]

      if tempKey[1] == '-' :
        middle = tempKey[1:-1]
        end = tempKey[:1]
      else :
        middle = tempKey[2:-1]
        end = tempKey[:2]

    key = front + middle + end

    return key
#-------------------------------------------------------------



  def get_maphash( self ) :
    return self.mapHash
#-------------------------------------------------------------

# This is how you'll call the class
# test = map_test( 7, '04-JUL-20', '04-AUG-20', 2 )
# test = map_test( 30, '04-JUL-20', '04-AUG-20', 8 )
# key = test.main()

