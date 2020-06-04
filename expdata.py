import numpy as np
import os
import re
from displayer import Displayer
from solver import RES_ROOT_DIR

class Result():
    def __init__(self, name):
        self.tao, self.psi = self.readFromFile(name)
        (_, self.filename) = os.path.split(name)
        # f"alpha_{self.alpha}_order_{self.order}_Bo_{self.bo}_DaI_{self.da}.csv"
        self.alpha = re.findall(r"alpha_(.+?)_order", self.filename)[0]
        self.order = re.findall(r"order_(.+?)_Bo", self.filename)[0]
        self.bo = re.findall(r"Bo_(.+?)_DaI", self.filename)[0]
        self.da = re.findall(r"DaI_(.+?).csv", self.filename)[0]
        self.truepsi = self.getTruePsi()

    def readFromFile(self, name):
        tao, psi = np.loadtxt(name, delimiter=",", usecols=(0, 1), unpack=True)
        return tao, psi

    def getLabel(self):
        return f"Bo: {self.bo}"

    def __str__(self) -> str:
        return f"alpha_{self.alpha}_order_{self.order}_Bo_{self.bo}_DaI_{self.da}"

    def getTruePsi(self):
        if int(self.order)==1:
            return 1/np.exp(float(self.da) * self.tao)
        elif int(self.order)==2:
            return 1 / (1 + float(self.da) * self.tao)
        else:
            raise NotImplementedError

if __name__ == '__main__':

    resname = [
               "dt_0.1_alpha_1_order_1_Bo_100_DaI_0.1",
               ]

    show = Displayer()
    for name in resname:
        res = Result(RES_ROOT_DIR+name+".csv")
        show.plot(res)
        show.save(name)
    show.show()

