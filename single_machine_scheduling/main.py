from gurobipy import GRB, LinExpr, Model


class GurobiService():
    def __init__(self):
        pass
    
    def _create_model(self):
        self.m = Model('Gurobi_Exercise')

    def _create_set(self):
        self.J = {1, 2, 3, 4, 5, 6}

    def _set_params(self):
        self.p = {
            1: 4, 
            2: 3,
            3: 6, 
            4: 2,
            5: 5, 
            6: 3
        }

        self.d = {
            1: 10, 
            2: 8,
            3: 15, 
            4: 9,
            5: 20, 
            6: 12
        }

        self.w = {
            1: 3, 
            2: 2,
            3: 4, 
            4: 1,
            5: 5, 
            6: 2
        }

        self.M = 1e3

    def _set_variables(self):
        self.s = self.m.addVars(self.J, vtype=GRB.INTEGER, name = 's')
        self.c = self.m.addVars(self.J, vtype=GRB.INTEGER, name = 'c')
        self.t = self.m.addVars(self.J, vtype=GRB.INTEGER, name = 't')
        self.y = self.m.addVars(self.J, self.J, vtype=GRB.BINARY, name = 'y')

    def _set_objectives(self):
        
        obj = LinExpr()
        for j in self.J:
            obj += self.w[j] * self.t[j]
        
        self.m.setObjective(obj, GRB.MINIMIZE)

    def _set_constraint(self):

        # constraint 1 
        for j in self.J: 
            self.m.addConstr(self.c[j] == self.s[j] + self.p[j])

        # constraint 2 
        for j in self.J:
            self.m.addConstr(self.t[j] >= self.c[j] - self.d[j])

        # constraint 3
        for j in self.J:
            self.m.addConstr(self.t[j] >= 0)

        # constraint 4 
        for i in self.J:
            for j in self.J:
                if i != j: 
                    self.m.addConstr(
                        self.s[j] >= self.c[i] - self.M * (1 - self.y[i, j]))
                    self.m.addConstr(self.s[i] >= self.c[j] - self.M * (self.y[i, j]))

        for i in self.J:
            for j in self.J:
                if i < j:
                    self.m.addConstr(self.y[i,j] + self.y[j,i] == 1, 
                                    name=f"order_{i}_{j}")

    def _model_optimize(self):
        self.m.optimize()

    def _print_results(self):
        status = self.m.Status

        if status == GRB.OPTIMAL:
            print(f"optimal obj: {self.m.ObjVal:g}")
        
        elif status == GRB.INFEASIBLE:
            print("model is infeasible")

        else:
            print(f"error status is: {status}")

        
        task_sequence = []
        for i in self.J:
            task_sequence.append((i, self.s[i].x, self.c[i].x))
        
        task_sequence = sorted(task_sequence, key=lambda item: item[1])

        for task in task_sequence:
            print(
                f"task {task[0]} start time is {task[1]}, complete time is {task[2]}")

    
    def run(self):
        self._create_model()
        self._create_set()
        self._set_params()
        self._set_variables()
        self._set_objectives()
        self._set_constraint()
        self._model_optimize()
        self._print_results()


if __name__ == "__main__":
    service = GurobiService()
    service.run()




        

           



    