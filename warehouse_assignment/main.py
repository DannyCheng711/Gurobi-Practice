from gurobipy import GRB, Model, LinExpr
import numpy as np 


class GurobiService():
    def __init__(self):
        pass

    def _create_model(self):
        self.m = Model("warehouse_assignment")

    def _create_set(self):
        self.I = {1, 2, 3}
        self.J = {1, 2, 3, 4, 5}

    def _create_params(self):
        self.s = {
            1: 80, 2: 60, 3:50, 
        }
        print(f"s: {self.s}")
        self.d = {
            1: 30, 2: 20, 3: 40, 4: 20, 5:10
        }
        print(f"d: {self.d}")

        self.M = 1e6 

        self.cost = {
            (1, 1): 4,
            (1, 2): 6,
            (1, 3): 9,
            (1, 4): 7, 
            (1, 5): 3,
            (2, 1): 5,
            (2, 2): 4, 
            (2, 3): 7,
            (2, 4): 2,
            (2, 5): 6, 
            (3, 1): 6,
            (3, 2): 8, 
            (3, 3): 3,
            (3, 4): 4,
            (3, 5): 5
        }

    def _set_variables(self):
        self.x = self.m.addVars(self.I, self.J, vtype = GRB.BINARY, name="x")
        self.q = self.m.addVars(self.I, self.J, vtype = GRB.INTEGER, name="q")

    def _set_objectives(self):

        obj = LinExpr(); 
        for k, v in self.cost.items():
            i = k[0] 
            j = k[1] 
            obj += self.q[i, j] * self.cost[i, j]


        self.m.setObjective(obj, GRB.MINIMIZE)

    def _set_constraints(self):

        # constraint 1
        for j in self.J:
            expr = LinExpr()
            for i in self.I:
                expr += self.x[i, j]
        
            self.m.addConstr(expr == 1, name= "constrain 1")

        # constraint 2
        for i in self.I:
            for j in self.J:
                self.m.addConstr(self.M * self.x[i, j] >= self.q[i, j], name= "constrain 2")


        # constraint 3
        for i in self.I:
            expr = LinExpr()
            for j in self.J:
                expr += self.q[i, j]

            self.m.addConstr(expr <= self.s[i], name= "constrain 3")

        # constraint 4
        for j in self.J:
            expr = LinExpr()
            for i in self.I:
                expr += self.q[i, j]

            self.m.addConstr(expr == self.d[j], name= "constrain 4")
        
    def _optimise_model(self):
        
        self.m.setParam('TimeLimit', 600)
        self.m.optimize()


    def _print_result(self):

        status = self.m.Status

        if status == GRB.OPTIMAL:
            print(f"Optimal obj: {self.m.ObjVal:g}")

        else:
            print(f"Status: {status}")


        for i in self.I:
            for j in self.J:
                if self.x[i, j].x > 0:
                    print(f" location {j} is assigned to warehouse {i} ")

        for i in self.I:
            for j in self.J:
                if self.q[i, j].x > 0:
                    print(f" quantity {self.q[i, j].x} is sent from warehouse {i} to location {j} ")
       
            
    
    def run(self):
       self._create_model()
       self._create_set()
       self._create_params()
       self._set_variables()
       self._set_objectives()
       self._set_constraints()
       self._optimise_model()
       self._print_result()


if __name__ == "__main__":

    service = GurobiService()
    service.run()



    