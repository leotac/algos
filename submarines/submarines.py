from gurobipy import *
import string, math

def readFile():
   subs = []
   ships = []
   datafile = open("grid.dat")
   for line in datafile:
      if line[0] == '#':
         continue
      v = line.split()
      sub = (v[0],v[1])
      ship = (v[2],v[3])
      subs.append(sub)
      ships.append(ship)

   return subs, ships 

def computeDistances(subs, ships):
   dist = []
   for (i,sub) in enumerate(subs):
      dist.append([math.sqrt(((string.uppercase.index(sub[0])-string.uppercase.index(ship[0]))**2 +  (int(sub[1])-int(ship[1]))**2)) for ship in ships])
   return dist

# Integer linear programming model with Gurobi
def ilp():
    subs,ships = readFile()
    dist = computeDistances(subs,ships)
    m = Model('Submarines')
    m.setAttr("ModelSense",GRB.MINIMIZE)
    x = {}
    for i,sub in enumerate(subs):
        for j, ship in enumerate(ships):
            # Assign submarine i to ship j
            x[i,j] = m.addVar(vtype=GRB.BINARY, obj=dist[i][j] , name='x_%s_%s' % (i, j))
    m.update()

    # Constraints
    for i,sub in enumerate(subs):    
        m.addConstr(quicksum(x[i,j] for j,ship in enumerate(ships)) == 1, "each sub -> only one ship")
    for j,ship in enumerate(ships):    
        m.addConstr(quicksum(x[i,j] for i,sub in enumerate(subs)) == 1, "each ship <- only one sub")

    m.update()
    m.optimize()
    print "Solution:"
    for i,sub in enumerate(subs):
        for j,ship in enumerate(ships):
            if int(x[i,j].x) == 1:
                print sub,"->",ship
        print ""

