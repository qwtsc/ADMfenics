import numpy as np
from fenics import *
from fenics import dx
from exceptions import CFLError

BOUNDARY_ERROR = 1e-14
PICARD_ERROR = 1e-6
PICARD_MAX_COUNT = 100
RES_ROOT_DIR = "/home/fenics/ADMresults/"

class Solver():
    def __init__(self, order, dt, dz, alpha, da, bo, totalTime=50, note="exp", steady=False):
        self.order = order
        if (dt/dz>1):
            raise CFLError("dt should be less than dz since the max velocity is 1")
        self.time_step = dt
        self.length_interval = dz
        self.alpha = alpha
        self.da = da
        self.bo = bo
        self.totalTime = totalTime
        self.prefix = note
        self.steady= steady

    def solve(self):
        set_log_active(False)
        if self.order==1:
            self._solve_firstOrder()
        elif self.order==2:
            self._solve_secondOrder()
        else:
            raise NotImplementedError

    def _solve_firstOrder(self):
        right, V, left, bcp, u_n, w, w_0 = self._define_firstOrderReaction()
        # running
        u = Function(V)
        t = 0
        ulastl = []
        for n in range(int(self.totalTime / self.time_step)):
            t += self.time_step
            u.t = t
            if (not self.steady) and t > 2:  # start to change the velocity, t is dimensionless residence time.
                w_0.params = t - 2
                w.interpolate(w_0)
            solve(left == right, u, bcp)
            ulastl.append(u.vector().get_local()[0])
            # Update previous solution
            u_n.assign(u)
        if self.steady:
            self._save_steady(u.vector().get_local())
        else:
            self._save_res(ulastl)

    def _solve_secondOrder(self):
        # Create mesh and define function space
        right, V, left, bcp, du, u_n, w, w_0 = self._define_secondOrderReaction()
        # running
        u = Function(V)
        t = 0
        ulastl = []
        for n in range(int(self.totalTime/self.time_step)):
            t += self.time_step
            u.t = t
            count = 0
            if (not self.steady) and t > 2: # start to change the velocity, t is dimensionless residence time.
                w_0.params = t - 2
                w.interpolate(w_0)
            # picard iteration!
            while count < PICARD_MAX_COUNT:
                solve(left == right, u, bcp)
                nonlinearerror = errornorm(du, u, 'L2')
                count += 1
                du.assign(u)
                if nonlinearerror < PICARD_ERROR:
                    # print(f"ok!, after {count} the error is {nonlinearerror}")
                    break
            # picard finish!ls
            ulastl.append(u.vector().get_local()[0])
            # Update previous solution
            u_n.assign(u)
        if self.steady:
            self._save_steady(u.vector().get_local())
        else:
            self._save_res(ulastl)

    def _define_firstOrderReaction(self):
        V, bcp, u_0, u_n, w, w_0, v, u, eps, da = self._prepare_define()
        F = (u - u_n) / self.time_step * v * dx + eps * w[0] * w[0] *dot(grad(u), grad(v)) * dx + dot(w, grad(
            u)) * v * dx + da * u * v * dx
        left, right = self._split_function(F)
        return right, V, left, bcp, u_n, w, w_0

    def _define_secondOrderReaction(self):
        V, bcp, u_0, u_n, w, w_0, v, u, eps, da = self._prepare_define()
        du = interpolate(u_0, V)
        F = (u - u_n) / self.time_step * v * dx + eps * w[0] * w[0] * dot(grad(u), grad(v)) * dx + dot(w, grad(
            u)) * v * dx + da * du * u * v * dx
        left, right = self._split_function(F)
        return right, V, left, bcp, du, u_n, w, w_0

    def _prepare_define(self):
        mesh = IntervalMesh(int(1 / self.length_interval), 0, 1)
        W = VectorFunctionSpace(mesh, 'P', 1)
        V = FunctionSpace(mesh, 'P', 1)
        # boundary condition
        bcp = self._boundary_condition(V)
        # initial condition
        u_0 = Expression('0', degree=0)
        u_n = interpolate(u_0, V)
        w = Function(W)  # velocity space
        w_0 = self.velocityExp(0, self.alpha)  # initial velocity is 1 which is maximum value.
        w.interpolate(w_0)
        v = TestFunction(V)
        u = TrialFunction(V)
        # Define variational problem
        eps = Constant(1 / self.bo)
        da = Constant(self.da)
        return V, bcp, u_0, u_n, w, w_0, v, u, eps, da

    def _split_function(self, F):
        left, right = lhs(F), rhs(F)
        return left, right

    def _boundary_condition(self, V):
        # the dimensionless concentration in the inlet is 1
        def boundary_D(x, on_boundary):
            return on_boundary and near(x[0], 0, BOUNDARY_ERROR)
        return DirichletBC(V, Constant(1), boundary_D)

    def getRealTao(self, time):
        S = 1 - np.exp(-self.alpha)
        tao = S * (1 / self.alpha + time - 2)
        return tao

    class velocityExp(UserExpression):
        def __init__(self, params, alpha, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.params = params
            self.alpha = alpha
        def eval(self,values,x):
            values[0] = 1.0/(1+self.alpha*self.params)
            # values[1] = 1.0*random() + 0.25`
        def value_shape(self):
            return(1,)

    def _save_res(self, ulastl):
        with open(RES_ROOT_DIR + f"{self.prefix}_dt_{self.time_step}_alpha_{self.alpha}_order_{self.order}_Bo_{self.bo}_DaI_{self.da}.csv", "w") as f:
            for t, u in enumerate(ulastl):
                tao = self.getRealTao(t * self.time_step)
                if tao<1: continue
                f.write(f"{tao}, {u}"+"\n")
            f.flush()

    def _save_steady(self, lastrun):
        with open(RES_ROOT_DIR + f"{self.prefix}_dt_{self.time_step}_alpha_{self.alpha}_order_{self.order}_Bo_{self.bo}_DaI_{self.da}.csv", "w") as f:
            for z, u in enumerate(lastrun[::-1]):
                f.write(f"{z*self.length_interval}, {u}"+"\n")
            f.flush()

    def get_savefile_path(self):
        return RES_ROOT_DIR + f"{self.prefix}_dt_{self.time_step}_alpha_{self.alpha}_order_{self.order}_Bo_{self.bo}_DaI_{self.da}.csv"

if __name__ == '__main__':
    from expdata import Result
    from displayer import Displayer
    sec = Solver(order=2, dt=1e-2, dz=1e-1, alpha=1, da=0.05, bo=10, totalTime=40, note="testnorm")
    sec.solve()
    result = Result(sec.get_savefile_path())
    # result2 = Result(RES_ROOT_DIR + "dt_0.0001_alpha_1_order_1_Bo_100_DaI_0.1.csv")
    show = Displayer(0, 30, 0, 1)
    show.plotmany([result])
    show.save("testnorm.png")
    show.show()

