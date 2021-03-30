library(plotly)
library(htmlwidgets)

start.time <- Sys.time()

fig <- subplot(fig1, fig2, shareX=TRUE)

fig <- fig %>% layout(
    legend=list(orientation='h',
                yanchor='bottom',
                y=1.12,
                xanchor='right',
                x=0.58,
                title=list(text='State(s):'),
                valign='middle'
                ),
    annotations = list(list(x = 0.125, y = 1.05, text = fe1, showarrow = F, xref='paper', yref='paper'),
                       list(x = 0.875, y = 1.05, text = fe2, showarrow = F, xref='paper', yref='paper')),
    autosize = FALSE,
    height=550,
    width=1400)

fig <- fig %>% animation_opts(
  frame = 1, 
  transition = 0, 
  redraw = FALSE
)
fig <- fig %>% animation_slider(
  currentvalue = list(prefix = 'Date: ', font = list(size=12), visible=TRUE, xanchor='right'),
  yanchor = 'top',
  xanchor = 'left',
  len = 0.8,
  x = 0.1,
  y = -0.15,
)
fig <- fig %>% animation_button(
  x = 1, xanchor = "right", y = 0, yanchor = "bottom"
)

saveWidget(fig, 'graphtest_final.html', selfcontained = F, libdir = 'lib')

end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)