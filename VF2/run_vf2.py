from VF2.Solver import Solver

def run_vf2(base, target, δ):
    solver = Solver()
    solver.init(1,δ)
    solver.ReadQuery(target)
    solver.input(base, target)
    ids = solver.solve()
    return ids

