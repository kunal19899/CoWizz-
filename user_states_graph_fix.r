library(plotly)
library(htmlwidgets)

main <- function(fe1, fe2, fig1_nm = "v3/fig1.rds", fig2_nm = "v3/fig2.rds") {
  start.time <- Sys.time()

  fig1 <- readRDS(file = fig1_nm)
  fig2 <- readRDS(file = fig2_nm)

  fig <- subplot(fig1, fig2, shareX=TRUE)

  fig <- layout(
      fig,
      legend=list(orientation='h',
                  yanchor='bottom',
                  y=1.12,
                  xanchor='right',
                  x=0.58,
                  title=list(text='State(s):'),
                  valign='middle',
                  labels=unique(fig$State)
                  ),
      showlegend=TRUE,
      autosize = FALSE,
      height=550,
      width=1400)

  fig <- animation_opts(
    fig,
    frame = 1, 
    transition = 0, 
    redraw = FALSE
  )
  fig <- animation_slider(
    fig,
    currentvalue = list(prefix = 'Date: ', font = list(size=12), visible=TRUE, xanchor='right'),
    yanchor = 'top',
    xanchor = 'left',
    len = 0.9,
    x = 0.075,
    y = -0.17,
  )
  fig <- animation_button(
    fig, x=0, xanchor="left", y=-0.48, yanchor="bottom"
  )

  saveWidget(fig, 'v3/static/animations/graphtest_final.html', selfcontained = F, libdir = 'lib')

  end.time <- Sys.time()
  time.taken <- end.time - start.time

  print(time.taken)
}
