import numpy as np
import os
import re

class Result():
    def __init__(self, name):
        self.tao, self.psi = self.readFromFile(name)
        (_, self.filename) = os.path.split(name)
        # f"alpha_{self.alpha}_order_{self.order}_Bo_{self.bo}_DaI_{self.da}.csv"
        self.alpha = re.findall(r"alpha_(.+?)_order", self.filename)[0]
        self.order = re.findall(r"order_(.+?)_Bo", self.filename)[0]
        self.bo = re.findall(r"Bo_(.+?)_DaI", self.filename)[0]
        self.da = re.findall(r"DaI_(.+?).csv", self.filename)[0]


    def readFromFile(self, name):
        tao, psi = np.loadtxt(name, delimiter=",", usecols=(0, 1), unpack=True)
        return tao, psi

    def getLabel(self):
        return f"Bo: {self.bo}"

    def __str__(self) -> str:
        return f"alpha_{self.alpha}_order_{self.order}_Bo_{self.bo}_DaI_{self.da}"


