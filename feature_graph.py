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
  def __init__( self, state_list, start_date, num_days, feature1, feature2) :
    # Stores the states they want to display
    self.states = state_list

    # Stores the number of days the user wants to cover
    self.start = start_date

    # Stores the number of days the user wants to cover
    self.days = int(num_days)

    # Stores the first feature user wants to display
    self.f1 = feature1

    # Stores the first feature user wants to display
    self.f2 = feature2
#-------------------------------------------------------------



def main(states, fe1, fe2) :
  # Read a file with a list of all the known features CoWiz supports

  nGraph = graph_test( states, '01-08-2021', 10, fe1, fe2 )

  fig = feature_graph(nGraph.states, nGraph.start, nGraph.days, 
                      nGraph.f1, nGraph.f2)

  #states_list = '_'.join(states)
  link_name = 'v3/static/animations/graphtest.html'
  
  pio.write_html(fig, file=link_name, auto_open=False)



#-------------------------------------------------------------
def feature_graph( st, sDate, nDays, fe1, fe2 ) :
  num_frames = nDays

  # lines that appear on the graph, should be one per state chosen
  num_traces = []

  df = pd.read_csv('v3/sample_test.csv')

  # casts the date parameter from the csv into a Date object so it
  #   can be readable by the program
  df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

  # x & y axis values for each date and feature for both visible graphs 
  axis = []

  for i in range(len(st)) :
    # this value will be used to determine how many lines to draw when the
    #   graph beginning to be generated
    num_traces.append( int(i) )

    # finds the index for where the state and the date selected align
    # tolist() is used to cast a Int64Index type to an integer type
    strt_idx = df[ (df['state']==st[i]) & (df['date']==sDate) ].index.tolist()

    # tolist() turns the object into a list object, since it will only
    #   store one value (the row number in the CSV file where the data 
    #   we're searching appears) we'll only need to access the value
    #   at the first index of the list
    axis.append(strt_idx[0])

  # creates a figure that will store 2 subgraphs, right next to each other 
  fig = make_subplots(rows=1, cols=2,
                      specs=[[{"secondary_y": True}, {"secondary_y": True}]])

  for j in range(len(axis)) :
    # only show the state name at the far right of the drawn line (i.e. trace)
    all_text = []

    for k in range(nDays + 1) :
      if k == nDays :
        all_text.append(st[j])
      else :
        all_text.append('')

    # represents the index at each iteration, used for convenience
    cur_idx = axis[j]

    # x values are range of dates starting from the start date to the amount
    #   of days the users chooses to look ahead (i.e. nDays)
    x = df['date'][cur_idx:cur_idx + nDays + 1]

    # y values for each feature chosen by the user
    y1 = df[fe1][cur_idx:cur_idx+nDays + 1]
    y2 = df[fe2][cur_idx:cur_idx+nDays + 1]

    
    # x & y axis values for the first graph (on the left)
    fig.add_trace(go.Scatter(x = x, y = y1, name=st[j],
                             legendgroup=str(j),
                             marker=dict(color=DEFAULT_PLOTLY_COLORS[j]),
                             mode='lines+text',
                             text=all_text,
                             textposition='middle right'),
                  row=1, col=1, secondary_y=False)
 
    # x & y axis values for the second graph (on the right)
    fig.add_trace(go.Scatter(x = x, y = y2, name=st[j], 
                             legendgroup=str(j),
                             marker=dict(color=DEFAULT_PLOTLY_COLORS[j]),
                             mode='lines+text',
                             text=all_text,
                             textposition='middle right',
                             showlegend=False),
                  row=1, col=2, secondary_y=False)
  

  # data is a parameter for Plotly's Frame object
  # it will determine what do draw from the given range in the dataset
  data = []

  # want to create enough frames for all the users
  for i in range(num_frames+1) :
    day_data = []
    for j in range(len(num_traces)) :
      cur_idx = axis[j]

      # x values are range of dates starting from the start date to the amount
      #   of days the users chooses to look ahead (i.e. nDays)
      x = df['date'][cur_idx:cur_idx + i+1].tolist()

      # y values for each feature chosen by the user
      y1 = df[fe1][cur_idx:cur_idx + i+1].tolist()
      y2 = df[fe2][cur_idx:cur_idx + i+1].tolist()

      day_data.append(go.Scatter(x=x, y=y1,visible=True))
      day_data.append(go.Scatter(x=x, y=y2,visible=True))
 
    # want to make an list of lists to store the different data ranges
    #   to draw from frame to frame
    data.append(day_data)   

  # Update the number of traces by two since there are two graphs
  for i in range(len(num_traces), len(num_traces)*2) :
    num_traces.append( int(i) )

  frames =[go.Frame(data=data[k],
                    traces=num_traces) for k in range(num_frames+1)]   # define the number of frames

  # will store all the frames where a line is drawn
  sFrame = []

  # Plotly will take drawing the dot as the first line of input
  # This will not be considered, we want to start with a line already drawn
  for i in range(num_frames+1):
    if i == 0 :
      sFrame.append(None)
    else :
      sFrame.append(frames[i]) 

  # get a range of dates to display on the slider
  dates = df['date'][axis[0]:axis[0] + (nDays+1)].tolist()

  steps = []
  for i in range(num_frames+1):
    step = dict(
      method="animate",
      label=dates[i],
      args = [sFrame[i], dict(frame=dict(duration=500, redraw=False),
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
                  transition = {'duration': 500, 'easing': 'linear'},
                  pad = {'b': 10, 't': 50},
                  len = 0.9,
                  x = 0.1,
                  y = 0,
                  steps = steps
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

  # rather than update the graphs day-by-day, this updates the traces over a fixed range of days
  fig.update_xaxes(range=[ (pd.to_datetime(dates[0], format='%Y-%m-%d') - pd.Timedelta(days=1)), 
                           (pd.to_datetime(dates[len(dates)-1], format='%Y-%m-%d') + pd.Timedelta(days=1)) ],
                   row=1, col=1)

  fig.update_xaxes(range=[ (pd.to_datetime(dates[0], format='%Y-%m-%d') - pd.Timedelta(days=1)), 
                           (pd.to_datetime(dates[len(dates)-1], format='%Y-%m-%d') + pd.Timedelta(days=1)) ],
                   row=1, col=2)

  # include the y axis titles for each subplot
  fig.update_yaxes(title_text=fe1, row=1, col=1)
  fig.update_yaxes(title_text=fe2, row=1, col=2)

  return fig
