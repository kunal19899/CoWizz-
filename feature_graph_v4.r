library(plotly)

# list of default Plotly colors to color a trace with
color_opts <- c('#1f77b4', # blue
                '#ff7f0e', # orange
                '#2ca02c', # green
                '#d62728', # red
                '#9467bd') # purple

accumulate_by <- function(dat, var) {
  var <- lazyeval::f_eval(var, dat)
  lvls <- plotly:::getLevels(var)
  dats <- lapply(seq_along(lvls), function(x) {
    cbind(dat[var %in% lvls[seq(1, x)], ], frame = lvls[[x]])
  })
  dplyr::bind_rows(dats)
}
#st, fe1, fe2

main <- function(st, fe1, fe2) {
  print(fe1)
  print(fe2)
  # hardcoded values for the states and features we want
  #st <- c('Texas', 'Florida', 'New Jersey','Illinois','New Hampshire')
  start.time <- Sys.time()
  # st <- c('Texas', 'Florida', 'New York', 'California', 'Missouri')
  # fe1 <- 'grocery_and_pharmacy_percent_change_from_baseline'
  # fe2 <- 'workplaces_percent_change_from_baseline'

  # condense the color_opts array to only include the number of colors that
  #     correlates to the number states
  color_opts <- color_opts[1:length(st)]

  # set names to map the colors of the lines to the state names
  color_opts <- setNames(color_opts, st)

  # retrieve values from the COVID csv file
  df <- read.csv(file = '/Users/kunalsamant/Documents/UTA/ITLab/COVID-19 visualisation/v3/7Mar2021-USStates-CovidData.csv')

  # obtain the fixed names of the features
  features_df <- read.csv(file = 'features.csv')
  fe1_nm <- features_df[which(fe1 == features_df[1]), 2]
  fe2_nm <- features_df[which(fe2 == features_df[1]), 2]

  # condense the graph to only include the columns we want and the rows we want
  #      ROWS: all instances of rows where the State column aligns with the state in the st set
  #      COLS: the State, Date, and rows related to feature 1 and feature 2
  df_sub <- df %>% subset(State %in% st, select=c(State,Date,get(fe1),get(fe2)))

  # replace any null values with zero in the feature columns
  df_sub[[fe1]][is.na(df_sub[[fe1]])] <- 0
  df_sub[[fe2]][is.na(df_sub[[fe2]])] <- 0

  # change format of dates from a Date object mm-dd-yy to a String object yyyy-mm-dd
  df_sub$Date <- strptime(as.character(df_sub$Date), '%m/%d/%y')
  df_sub$Date <- format(df_sub$Date, '%Y/%m/%d')

  # convert it back to a Date object so we can edit the range of the axis
  df_sub$Date <- as.Date(df_sub$Date)

  # store the number days each state covers
  nDays <- length(unique(df_sub$Date))

  colors_col <- rep(color_opts[1], nDays)

  if(length(st) > 1) {
    rest_colors <- color_opts[2:length(st)]

    for(i in rest_colors) {
      colors_col <- append(colors_col, rep(i, nDays))
    }
  }

  df_sub$Colors <- colors_col

  # creates a cumulative graph that the plots can be animated by
  fig <- df_sub %>% accumulate_by(~Date)

  # sets the minimum and maximum x axis values
  fig_min_x <- df_sub[1,2]
  fig_max_x <- tail(df_sub[,2], n=1)

  # sets the minimum and maximum y axis values for both graphs
  fig1_min_y <- min(df_sub[[fe1]])
  fig1_max_y <- max(df_sub[[fe1]])
  fig2_min_y <- min(df_sub[[fe2]])
  fig2_max_y <- max(df_sub[[fe2]])

  fig1 <- fig %>%
    plot_ly(
      x = ~Date, 
      y = ~get(fe1),
      split = ~State,
      frame = ~frame, 
      type = 'scatter',
      mode = 'lines', 
      text = paste("Date: ", fig$Date,
                   "", fig[[fe1]]),
      hoverinfo = 'text',
      color = ~Colors,
      name = ~State,
      line = list(simplyfy = F),
      legendgroup=~State
    )
  fig2 <- fig %>% 
    plot_ly(
      x = ~Date, 
      y = ~get(fe2),
      split = ~State,
      frame = ~frame, 
      type = 'scatter',
      mode = 'lines', 
      text = paste("Date: ", fig$Date,
                   "", fig[[fe1]]),
      hoverinfo = 'text',
      color = ~Colors,
      name = ~State,
      line = list(simplyfy = F),
      legendgroup=~State,
      showlegend=FALSE
    )

  fig1 <- fig1 %>% layout(
    xaxis = list(
      title = 'Date',
      range = c(as.numeric(as.POSIXct(fig_min_x))*1000, 
                as.numeric(as.POSIXct(fig_max_x))*1000),
      zeroline = F,
      dtick="M1",
      tickformat="%b\n%Y"
    ),
    yaxis = list(
      zeroline = F
      range = c(fig1_min_y, fig1_max_y)
    ),
      annotations=list(list(x=0.40, y = 1.10, text = fe1_nm, showarrow = F, xref='paper', yref='paper'))
  )
  fig2 <- fig2 %>% layout(
    xaxis = list(
      title = 'Date',
      range = c(as.numeric(as.POSIXct(fig_min_x, format="%Y/%m/%d"))*1000, 
                as.numeric(as.POSIXct(fig_max_x, format="%Y/%m/%d"))*1000),
      zeroline = F,
      dtick="M1",
      tickformat="%b\n%Y"
    ),
    yaxis = list(
      zeroline = F
      range = c(fig2_min_y, fig2_max_y)
    ),
    annotations=list(list(x=0.55, y = 1.10, text = fe2_nm, showarrow = F, xref='paper', yref='paper'))
  )
  saveRDS(fig1, file = 'v3/fig1.rds')
  saveRDS(fig2, file = 'v3/fig2.rds')

  end.time <- Sys.time()
  time.taken <- end.time - start.time
  print(time.taken)
}
