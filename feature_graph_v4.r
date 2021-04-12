library(plotly)

# list of default Plotly colors to color a trace with
DEFAULT_PLOTLY_COLORS=c('rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                        'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                        'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                        'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                        'rgb(188, 189, 34)', 'rgb(23, 190, 207)')

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

  # retrieve values from the COVID csv file
  df <- read.csv(file = '/Users/kunalsamant/Documents/UTA/ITLab/COVID-19 visualisation/v3/Feb20-USStates-CovidData.csv')

  # store list of all the days each state covers
  dayList <- unique(df$Date)

  # change format of dates from a Date object mm-dd-yy to a String object yyyy-mm-dd
  df$Date <- strptime(as.character(df$Date), '%m/%d/%y')
  df$Date <- format(df$Date, '%Y/%m/%d')

  df_sub <- subset(df, State %in% st, select=c(State,Date,get(fe1),get(fe2)))
  fig <- accumulate_by(df_sub, ~Date)

  fig_min_x <- df_sub[1,2]
  fig_max_x <- tail(df_sub[,2], n=1)
  #fig1_min_y <- min(df_sub$get(fe1))
  #fig1_max_y <- max(df_sub$get(fe1))

  fig1 <- 
    plot_ly(
      fig,
      x = ~Date, 
      y = ~get(fe1),
      split = ~State,
      frame = ~frame, 
      type = 'scatter',
      mode = 'lines', 
      line = list(simplyfy = F,
                  color=DEFAULT_PLOTLY_COLORS[which(st == ~State)]),
      legendgroup=~State
      #legendgroup=DEFAULT_PLOTLY_COLORS[which(st == ~State) - length(st)]
    )
  fig2 <- 
    plot_ly(
      fig,
      x = ~Date, 
      y = ~get(fe2),
      split = ~State,
      frame = ~frame, 
      type = 'scatter',
      mode = 'lines', 
      line = list(simplyfy = F,
                  #color=DEFAULT_PLOTLY_COLORS[which(st == ~State)])
                  color=DEFAULT_PLOTLY_COLORS[which(st == ~State)]),
      legendgroup=~State,
      showlegend=FALSE
    )

  fig1 <- layout(fig1,
    xaxis = list(
      title = 'Date',
      #range = c(as.numeric(as.POSIXct(fig_min_x, format="%Y/%m/%d"))*1000, 
      #          as.numeric(as.POSIXct(fig_max_x, format="%Y/%m/%d"))*1000),
      zeroline = F
    ),
    yaxis = list(
      zeroline = F
      #range = c(fig1_min_y, fig1_max_y)
    )
  )
  fig2 <- layout(fig2,
    xaxis = list(
      title = 'Date',
      #range = c(as.numeric(as.POSIXct(fig_min_x, format="%Y/%m/%d"))*1000, 
      #          as.numeric(as.POSIXct(fig_max_x, format="%Y/%m/%d"))*1000),
      zeroline = F
    ),
    yaxis = list(
      zeroline = F
      #range = c(fig1_min_y, fig1_max_y)
    )
  )
  saveRDS(fig1, file = 'v3/fig1.rds')
  saveRDS(fig2, file = 'v3/fig2.rds')
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  print(time.taken)
}