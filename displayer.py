import matplotlib.pyplot as plt
from solver import RES_ROOT_DIR

class Displayer():
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def plot(self, expdata):
        self._setLabel()
        self.ax.plot(expdata.tao, 1-expdata.psi, 'b', label=expdata.getLabel())
        self.ax.plot(expdata.tao, 1-expdata.truepsi, 'k', label=expdata.getLabel())

    def plotmany(self, manydata):
        self._setLabel()
        for data in manydata:
            self.ax.plot(data.tao, 1 - data.psi, 'b', label=data.getLabel())

    def _setLabel(self):
        self.ax.set_ylabel(r'$1-\psi$')
        self.ax.set_xlabel(r'$\theta_{correct}$')

    def _setlegend(self):
        self.ax.legend()

    def show(self):
        plt.show()

    def save(self, name):
        self.fig.savefig(RES_ROOT_DIR+"/fig/"+name+".png", dpi=300)

