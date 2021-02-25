import plotly
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
from plotly.subplots import make_subplots

# list of default Plotly colors to color a trace with
DEFAULT_PLOTLY_COLORS=['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                       'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                       'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                       'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                       'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

class graph_test() :
  # Constructor for routes.py to send/receive data
  #   from this program
  def __init__( self, state_list, feature1, feature2) :
    # Stores the states they want to display
    self.states = state_list

    # Stores the first feature user wants to display
    self.f1 = feature1

    # Stores the first feature user wants to display
    self.f2 = feature2
#-------------------------------------------------------------



def main() :
  # Write a list of states to see the Covid data of
  state_list = ['TX', 'FL', 'NJ']

  # Write the name first feature you want to find the data of
  feature1 = 'New Cases'

  # Write the name second feature you want to find the data of
  feature2 = 'New Deaths'

  #-------------------------------------------------------------------------------------
  # Initialize the nGraph object by calling the graph_test constructor
  nGraph = ''

  # Call the feature_graph() function below to create a Graph figure to display
  fig = ''
  
  # Uncomment line below once the fig object is returned from feature_graph() 
  # pio.write_html(fig, file='workshop_graph.html', auto_open=False)
  #-------------------------------------------------------------------------------------



#-------------------------------------------------------------
def feature_graph( states, feature1, feature2 ) :

  #------------------------------------------------------------------------------------
  # Read CSV file generated from Task 1 using the Pandas library
  df = ''
  #------------------------------------------------------------------------------------

  #------------------------------------------------------------------------------------
  # Count the number of days that are available for each state
  # Rather than count it manually, use some of Pandas' built-in functions
  numDays = 0
  #------------------------------------------------------------------------------------

  # frames should correlate to the number of days that pass
  num_frames = numDays

  # lines that appear on the graph, should be one per state chosen
  num_traces = []
  
  #------------------------------------------------------------------------------------
  # Uncomment line below and convert the Date column in the CSV from a Datetime object
  #   to a String object in the form of mm-dd-YYYY format using Pandas
  #df['Date'] = ''
  #------------------------------------------------------------------------------------

  # stores the rows where each state is first used in the CSV file
  axis = []

  for i in range(len(st)) :
    # this value will be used to determine how many lines to draw when the
    #   graph beginning to be generated
    num_traces.append( int(i) )

    #------------------------------------------------------------------------------------
    # Store the indexes at which the state first appears in the CSV file
    axis.append(i)
    #------------------------------------------------------------------------------------

  # creates a figure that will store 2 subgraphs, right next to each other 
  fig = make_subplots(rows=1, cols=2,
                      specs=[[{"secondary_y": True}, {"secondary_y": True}]])

  # only show the state name at the far right of the drawn line (i.e. trace)
  all_text = []

  for j in range(len(axis)) :
    #------------------------------------------------------------------------------------
    # Update x and y values read from a CSV and store those values 
    #   
    # x should be the dates chosen
    # y1 and y2 should be the values for each feature on that day 
    x  = 0
    y1 = 0
    y2 = 0
    #------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------
    # Create a way to only write the state's initials at the final
    #   data point and not on each data point, as is done here
    all_text.append(states[j])
    #------------------------------------------------------------------------------------

    # x & y axis values for the first graph (on the left)
    fig.add_trace(go.Scatter(x = x, y = y1, name=states[j],
                             legendgroup=str(j),
                             marker=dict(color=DEFAULT_PLOTLY_COLORS[j]),
                             mode='lines+text',
                             text=all_text,
                             textposition='middle right'),
                  row=1, col=1, secondary_y=False)
 
    #-------------------------------------------------------------------------------------
    # Repeat process show above but this time to add a trace on
    #   the second subplot
    fig.add_trace()
    #-------------------------------------------------------------------------------------
  

  frames = []

  # want to create enough frames for all the users
  for i in range(num_frames+1) :
    # data is a parameter for Plotly's Frame object
    # it will storedata points what to draw from the dataset
    day_data = []

    for j in range(len(num_traces)) :    
      #------------------------------------------------------------------------------------
      # Update x and y values read from a CSV and store those values 
      #   
      # x should be the dates chosen
      # y1 and y2 should be the values for each feature on that day 
      x  = 0
      y1 = 0
      y2 = 0
      #------------------------------------------------------------------------------------

      day_data.append(go.Scatter(x=x, y=y1,visible=True))
      day_data.append(go.Scatter(x=x, y=y2,visible=True))
 
    # want to make an list of lists to store the different data ranges
    #   to draw from frame to frame
    frames.append(go.Frame(data=day_data,
                           traces=num_traces))

  #------------------------------------------------------------------------------------
  # Create an array of date values from the start date up
  #   and an end date that is numDays after the fact
  dates = []
  #------------------------------------------------------------------------------------

  steps = []
  for i in range(num_frames+1):
    step = dict(
      method="animate",
      
      #--------------------------------------------------------------------------------
      # Update ticks on slider to print out values from dates array
      label=i,
      #--------------------------------------------------------------------------------

      args = [frames[i], dict(frame=dict(duration=500, redraw=False),
                         transition=dict(duration=0),
                         easing='linear',
                         fromcurrent=True,
                         mode='immediate')]
    )
    steps.append(step)

  # Creates button objects to be interactive with the slider
  play_button = dict(label='Play',
                     method='animate',
                     args=[None, dict(frame=dict(duration=500, redraw=False),
                                          transition=dict(duration=0),
                                          easing='linear',
                                          fromcurrent=True,
                                          mode='immediate')])

  pause_button = dict(label='Pause',
                      method='animate',
                      args=[None, dict(frame=dict(duration=0, redraw=False),
                                       transition=dict(duration=0),
                                       mode='immediate')])

  sliders = [dict(yanchor = 'top',
                  xanchor = 'left',
                  currentvalue = {'font': {'size': 20},'prefix': 'Date: ','visible': True,'xanchor': 'right'},
                  transition = {'duration': 0, 'easing': 'linear'},
                  pad = {'b': 10, 't': 50},
                  len = 0.9,
                  x = 0.1,
                  y = 0,
                  steps = []
            )]

  fig.frames=frames
  fig.update_layout(updatemenus=[dict(type='buttons',
                                      showactive=False,
                                      y=-0.1,
                                      x=0.05,
                                      xanchor='right',
                                      yanchor='top',
                                      buttons=[play_button, pause_button])],
                    sliders=sliders)


  #------------------------------------------------------------------------------------
  # Update the y-axes to include the names of the features
  fig.update_yaxes(title_text='Sample 1', row=1, col=1)
  fig.update_yaxes(title_text='Sample 2', row=1, col=2)
  #------------------------------------------------------------------------------------

  return fig
main()
