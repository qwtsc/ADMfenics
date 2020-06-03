import matplotlib.pyplot as plt
from solver import RES_ROOT_DIR

class Displayer():
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def plot(self, expdata):
        self._setLabel()
        self.ax.plot(expdata.tao, 1-expdata.psi, label=expdata.getLabel())

    def plotmany(self, manydata):
        self._setLabel()
        for data in manydata:
            self.ax.plot(data.tao, 1 - data.psi, label=data.getLabel())

    def _setLabel(self):
        self.ax.set_ylabel(r'$1-\psi$')
        self.ax.set_xlabel(r'$\theta_{correct}$')

    def save(self, name):
        self.fig.save(RES_ROOT_DIR+name+".png", dpi=300)

