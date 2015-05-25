import plotly.plotly as py
from plotly.graph_objs import *


class GraphDisplay():

    def __init__(self):
        self._axis_x = [1, 2, 3, 4, 5, 6, 7]
        self._axis_y = []
        self._update_trace()
        py.sign_in('mskec', 'hexnm18mxe')

    def update_data(self, new_data):
        self._axis_y = new_data
        self._update_trace()
        py.plot(Data([self._trace]), filename='parpro-connect4')

    def _update_trace(self):
        self._trace = Scatter(x=self._axis_x, y=self._axis_y)
