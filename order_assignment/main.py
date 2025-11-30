from gurobipy import *
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

        self.orders = set([1, 2, 3, 4, 5, 6, 7, 8])
        self.trucks = set([1, 2, 3, 4])

    def _create_params(self):
        print("setting parameters ...")
        self.demand = {
            1: 4, 
            2: 6, 
            3: 3, 
            4: 7, 
            5: 2, 
            6: 5, 
            7: 4, 
            8: 8
        }

        self.capacity = {
            1: 10,
            2: 12, 
            3: 15, 
            4: 8
        }

        self.fixed_cost = {
            1: 100,
            2: 120, 
            3: 130,
            4: 90
        }

        self.cost = {
            (1,1): 30, (1,2): 28, (1,3): 35, (1,4): 40,
            (2,1): 40, (2,2): 32, (2,3): 30, (2,4): 50,
            (3,1): 20, (3,2): 25, (3,3): 22, (3,4): 30,
            (4,1): 50, (4,2): 38, (4,3): 36, (4,4): 55,
            (5,1): 18, (5,2): 16, (5,3): 20, (5,4): 25,
            (6,1): 35, (6,2): 30, (6,3): 28, (6,4): 42,
            (7,1): 24, (7,2): 26, (7,3): 27, (7,4): 33,
            (8,1): 60, (8,2): 48, (8,3): 45, (8,4): 55,
        }

        """
        self.graph = dict()
        self.t_cost = dict()

        for k, v in self.cost.items():
            origin = k[0]
            dest = k[1]
            if origin not in self.graph:
                self.graph[origin] = set()
                self.t_cost[origin] = dict()
            else:
                self.graph[origin].add(dest)
                self.t_cost[origin][dest] = v

        print("graph: ", self.graph)
        print("cost:" , self.t_cost)
        """
        
        self.penalty = {
            1: 80,
            2: 100,
            3: 60,
            4: 120,
            5: 50,
            6: 90,
            7: 70,
            8: 150,
        }

    def _set_variables(self):
        self.x = self.m.addVars(self.orders, self.trucks, vtype=GRB.BINARY, name="x")
        self.y = self.m.addVars(self.trucks, vtype=GRB.BINARY, name="y")
        self.z = self.m.addVars(self.orders, vtype=GRB.BINARY, name="z")


    def _set_objective_func(self):
        # summation fixed cost + transportation cost + penalty
        sum_fixed_cost = 0
        for h in self.trucks:
            sum_fixed_cost += self.fixed_cost[h] * self.y[h]
        
        sum_trans_cost = 0
        for h in self.trucks:
            for i in self.orders:
                sum_trans_cost += self.cost[i, h] * self.x[i, h]
        
        sum_penalty = 0
        for i in self.orders:
            sum_penalty += self.penalty[i] * self.z[i]

        self.m.setObjective(sum_fixed_cost + sum_trans_cost + sum_penalty, GRB.MINIMIZE)
         

    def _set_constraints(self):
        # constraint 1 
        for i in self.orders: 
            order_assign_expr = LinExpr()
            for h in self.trucks:
                order_assign_expr += self.x[i, h]

            self.m.addConstr(order_assign_expr + self.z[i] == 1, "order_assign")

        # constraint 2 
        for h in self.trucks:
            truck_cap_expr = LinExpr()
            for i in self.orders:
                truck_cap_expr+= self.demand[i] * self.x[i, h]
            
            self.m.addConstr(truck_cap_expr <= self.capacity[h], "truck_assign")

        # constraint 3 
        for i in self.orders:
            for h in self.trucks:
                self.m.addConstr(self.x[i, h] <= self.y[h])

    def _optimize_model(self):
        self.m.setParam('TimeLimit', 600)
        self.m.optimize()

    def _print_results(self):

        # x 
        for i in self.orders:
            for h in self.trucks:
                if self.x[i, h].x > 0:
                    print(f"truck {h} carry the order {i}")
        # y
        for h in self.trucks:
            if self.y[h].x > 0:
                print(f"truck {h} is assigned")
        
        # p
        for i in self.orders:
            if self.z[i].x > 0:
                print(f"order {i} is dropped, so the penalty occurs")


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