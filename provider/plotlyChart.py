import plotly.plotly as py
from plotly.graph_objs import *
import fitbitAPI as fb
import numpy as np
import npCookbook as npc

py.sign_in('alan.wc.hau', 'gnpl25isfs')

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def plotGraph():
  # gather fitbit data
  fitBitTS = fb.getStepsTimeSeries('3m')

  dt = np.dtype([('dates', 'datetime64[D]'), ('steps', np.int32)])
  TS = np.array(fitBitTS, dtype=dt)
  # print TS
  fb_dates = TS['dates']
  fb_steps = TS['steps']

  fb_steps_ma = npc.smooth(TS['steps'],window_len=11,window='hanning')
  # fb_steps_ma = moving_average(TS['steps'], n=10)
  # print fb_dates, fb_steps 

  surgery_date = np.datetime64('2015-01-18')
  days_since_surgery = fb_dates - surgery_date

  days_since_surgery = days_since_surgery.astype(np.int32)


  # print days_since_surgery

  # prep Time Series for plot
  fitBit_trace = Scatter(
      x=days_since_surgery,
      y=fb_steps,
      name = 'fitBit Step Count',
      line=Line(
        shape='spline',
        smoothing = 10
    )
  )
  # data = Data([trace0])
  fitBit_trace_MA = Scatter(
      x=days_since_surgery,
      y=fb_steps_ma,
      name = 'fitBit Step Count Smoothed 3 day avg',
      line=Line(
        shape='spline',
        smoothing = 10
    )
  )




  data = Data([ fitBit_trace, fitBit_trace_MA ])

  # configure plotly layout:
  layout = Layout(
    title='Step Count Time series ',
    xaxis=XAxis(
        title='Days Since Surgery'

    ),
    yaxis=YAxis(
        title='Step Count'

    )
)

  fig = Figure(data=data, layout=layout)
  unique_url = py.plot(fig, filename = 'CarePigeon-basic-line', auto_open=False)
  # print unique_url
  return unique_url

if __name__ == "__main__":
  
  # b = FatBitAPI.getFloorsTimeSeries()
  # print b
  url = plotGraph()
  print url
