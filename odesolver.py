from solver import Solver
import numpy as np
import matplotlib.pyplot as plt

sec = Solver(order=1, dt=1e-3, dz=1e-3, alpha=1, da=3, bo=10, totalTime=2, note="steady", steady=True)
sec.solve()

zeta, psi = np.loadtxt(sec.get_savefile_path(), delimiter=",", usecols=(0, 1), unpack=True)
plt.plot(zeta, psi)
plt.show()