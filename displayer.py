import matplotlib.pyplot as plt
from solver import RES_ROOT_DIR
import numpy as np

class Displayer():
    def __init__(self, xbegin, xend, ybegin, yend):
        self.fig, self.ax = plt.subplots()
        self.xbegin = xbegin
        self.xend = xend
        self.ybegin = ybegin
        self.yend = yend

    def _layout(self):
        self._setLabel()
        self._axial_limit()

    def plot(self, expdata):
        self._layout()
        self.ax.plot(expdata.tao, 1-expdata.psi, 'b', label=expdata.getLabel())
        self.ax.plot(expdata.tao, 1-expdata.truepsi, 'k', label="true")
        self._setlegend()

    def plotmany(self, manydata):
        self._layout()
        for data in manydata:
            self.ax.plot(data.tao, 1 - data.psi, 'b', label=data.getLabel())
            self.ax.plot(data.tao, 1 - data.truepsi, 'k', label=data.getLabel())
        self._setlegend()

    def _setLabel(self):
        self.ax.set_ylabel(r'$1-\psi$')
        self.ax.set_xlabel(r'$\theta_{correct}$')
        self.ax.xaxis.label.set_size(9.5)
        self.ax.yaxis.label.set_size(9.5)
        self.ax.tick_params(labelsize=9)

    def _axial_limit(self):
        self.ax.set_xlim(self.xbegin, self.xend)
        self.ax.set_ylim(self.ybegin, self.yend)
        xticks = np.arange(self.xbegin, self.xend, 5)
        yticks = np.arange(self.ybegin, self.yend, 0.1)
        xtickslabel = [f for f in xticks]
        ytickslabel = [f"{f:.1f}" for f in yticks]
        self.ax.xaxis.set_ticks(xticks)
        self.ax.xaxis.set_ticklabels(xtickslabel)
        self.ax.yaxis.set_ticks(yticks)
        self.ax.yaxis.set_ticklabels(ytickslabel)

    def _setlegend(self):
        self.ax.legend(loc='upper left', ncol=2)

    def show(self):
        plt.show()

    def save(self, name):
        self.fig.savefig(RES_ROOT_DIR+"/fig/"+name, dpi=300)

