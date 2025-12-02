from gurobipy import Model, GRB, LinExpr
import numpy as np

class GurobiModelService():
    def __init__(self):
        pass

    # creating model 
    def _create_model(self):
        self.m = Model('Gurobi-Interview')

    # creating set 
    def _create_set(self):
        print("creating sets started ...")

        self.P = [1, 2, 3, 4]            # 1=A, 2=B, 3=C, 4=D
        self.T = range(1, 30 + 1)        # 1..T_max

    def _create_params(self):
        print("setting parameters ...")

        self.capacity = {
            1: 10800,
            2: 10400, 
            3: 5000, # or 9000
            4: 12000
        }

        self.total_demand = 200000 # 假設要產 200000 個產品


    def _set_variables(self):
        self.y = self.m.addVars(self.P, self.T, vtype=GRB.BINARY, name="y") # 是否有開班
        self.x = self.m.addVars(self.P, self.T, vtype=GRB.INTEGER, name="x") # 開班數
        self.q = self.m.addVars(self.P, self.T, vtype=GRB.INTEGER, name="x") # 產出量
        self.s = self.m.addVars(self.P, self.T, vtype= GRB.INTEGER, name="s") # WIP
         

    def _set_objective_func(self):
        # 開班數
        sum_shift = 0
        for p in self.P:
            for t in self.T:
                sum_shift += self.x[p, t]

        self.m.setObjective(sum_shift, GRB.MINIMIZE)

    def _set_constraints(self):
        # constraint 1 
        for p in self.P:
            for t in self.T:
                 self.m.addConstr(self.x[p, t] <= self.y[p, t])

        # constraint 2 : WIP inventory
        for p in self.P:
            for t in self.T:
                if p != 4:
                    self.m.addConstr(self.q[p + 1, t] - self.q[p, t] <= 2 * self.q[p, t])

        # contraint 3: WIP lower bound
        for p in self.P:
            for t in self.T:
                if p != 4:
                    self.m.addConstr(self.q[p + 1, t] >= 1.5 * self.q[p, t])

        
        # constriant 4: capacity 
        for p in self.P:
            for t in self.T:
                 self.m.addConstr(self.capacity[p] * self.x[p, t] >= self.q[p, t])


        # constriant 4: total output 
        self.m.addConstr(
            sum(self.q[4, t] for t in self.T) >= self.total_demand,
        )

 
            
    def _optimize_model(self):
        self.m.optimize()

    def _print_results(self):

        status = self.m.Status
        if status == GRB.OPTIMAL:
            print(f"Optimal objective: {self.m.ObjVal:g}")
        elif status == GRB.INFEASIBLE:
            print("Model is infeasible.")
            return
        elif status == GRB.UNBOUNDED:
            print("Model is unbounded.")
            return
        else:
            print(f"Optimization ended with status {status}")
            return

        # x 
        for p in self.P:
            for t in self.T:
                if self.x[p, t].x > 0:
                    print(f"process {p} open on shift {t}, with quanity {self.q[p, t].x}")
      
    def run(self):
        self._create_model()
        self._create_set()
        self._create_params()
        self._set_variables()
        self._set_constraints()
        self._set_objective_func()
        self._optimize_model()
        self._print_results()

if __name__ == "__main__":
    model_service = GurobiModelService()
    model_service.run()