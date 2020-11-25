from expdata import Result
from displayer import Displayer
from solver import Solver

sec = Solver(order=1, dt=1e-3, dz=1e-2, alpha=0.34, da=0.035, bo=0.212, totalTime=200, note="exp")
sec1 = Solver(order=1, dt=1e-3, dz=1e-2, alpha=0.34, da=0.015, bo=0.212, totalTime=200, note="exp")
sec2 = Solver(order=1, dt=1e-3, dz=1e-2, alpha=0.34, da=0.008, bo=0.212, totalTime=200, note="exp")
sec3 = Solver(order=1, dt=1e-3, dz=1e-2, alpha=0.34, da=0.002, bo=0.212, totalTime=200, note="exp")
sec.solve()
sec1.solve()
sec2.solve()
sec3.solve()
result = Result(sec.get_savefile_path())
result1 = Result(sec1.get_savefile_path())
result2 = Result(sec2.get_savefile_path())
result3 = Result(sec3.get_savefile_path())
# result2 = Result(RES_ROOT_DIR + "dt_0.0001_alpha_1_order_1_Bo_100_DaI_0.1.csv")
show = Displayer(0, 45, 0, 1)
show.plotmany([result, result1, result2, result3])
show.save("bo0.212_exp.png")
show.show()
