import scipy
from gurobipy import *

def init():
    grid = []
    input = open("grid.dat")
    for line in input:
        cur = []
        v = line.split()
        for x in v:
            cur.append(int(x))
        grid.append(cur)

    return grid

def adj(x,y):
    return [(z,w) for (z,w) in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
    if z in range(8) and w in range(8)]


def recurse(length=10):
    grid = init()

#    DP: no.
#    opt = scipy.zeros((8,8,11),int)
#    for l in range(11):
#        for x,row in enumerate(grid):
#            for y,P in enumerate(row):
#                if l == 0:
#                    opt[x,y,l] = 0
#                else:
#                    neighbours = adj(x,y)
#                    opt[x,y,l] = P + max(opt[z,w,l-1] for (z,w) in neighbours)

    best = scipy.zeros((8,8),int)
    optimal_value = 0
    optimal_path = []
    for x,row in enumerate(grid):
        for y,P in enumerate(row):
            #print "Cell:", x,y
            visited = scipy.zeros((8,8),int)
            visited[x,y] = 1
            path = [(x,y)]
            best[x,y], steps = maxprob(x,y,path,length-1,grid)
            if best[x,y] > optimal_value:
                optimal_value = best[x,y]
                optimal_path = steps + [(x,y)]
    
    print "Optimal value:", optimal_value
    
    for x,row in enumerate(grid):
        for y,P in enumerate(row):
            if (x,y) in optimal_path:
                print 1,
            else:
                print 0,
        print ""

# Recursive function that computes the max-cost path with length l starting from x,y
def maxprob(x,y,path,l,grid):
    neighbours = adj(x,y)
    if l==0:
        return grid[x][y], []
    
    # List of optimal paths of length l-1 for each feasible neighbour
    paths = [(maxprob(z,w,path+[(z,w)],l-1,grid),z,w) for (z,w) in neighbours if (z,w) not in path]
    
    # Stuck in a cul-de-sac, can't go on
    if len(paths) == 0:
        return 0,[]

    # Take the neighbour (z,w) with the best l-1 path
    (value,steps),z,w = max(paths)
    
    return value + grid[x][y], steps + [(z,w)]

# Integer linear programming model with Gurobi
def ilp(length=10):
    grid = init()
    m = Model('Lost ship')
    m.setAttr("ModelSense",GRB.MAXIMIZE)
    x,start,end, outgoing,arc,incoming, label = {},{},{},{},{},{},{}
    for i, row in enumerate(grid):
        for j, P in enumerate(row):
            x[i,j] = m.addVar(vtype=GRB.BINARY, obj= P, name='x_%s_%s' % (i, j))
            start[i,j] = m.addVar(vtype=GRB.BINARY, name='start_%s_%s' % (i, j))
            end[i,j] = m.addVar(vtype=GRB.BINARY,  name='end_%s_%s' % (i, j))
            outgoing[i,j] = m.addVar(vtype=GRB.BINARY,  name='outgoing_%s_%s' % (i, j))
            incoming[i,j] = m.addVar(vtype=GRB.BINARY,  name='incoming_%s_%s' % (i, j))
            label[i,j] = m.addVar(vtype=GRB.INTEGER,name='label_%s_%s' % (i, j))
            for (k,l) in adj(i,j):
                    arc[(i,j),(k,l)] = m.addVar(vtype=GRB.BINARY, name='arc_%s,%s_%s,%s' % (i,j,k,l))
    m.update()

    # Constraints
    m.addConstr(quicksum(x[i,j] for i,row in enumerate(grid) for j,P in enumerate(row)) == length, "length")
    
    # One starting and ending cell
    m.addConstr(quicksum(start[i,j] for i,row in enumerate(grid) for j,P in enumerate(row))== 1, "start")
    m.addConstr(quicksum(end[i,j] for i,row in enumerate(grid) for j,P in enumerate(row)) == 1, "end")

    for i, row in enumerate(grid):
        for j, P in enumerate(row):

            # Distinct start and end
            m.addConstr(start[i,j] + end[i,j] <=1)
            # Outgoing and incoming arcs (handy variables, not really necessary)
            m.addConstr(outgoing[i,j] == quicksum((arc[(i,j),(k,l)] for (k,l) in adj(i,j))))
            m.addConstr(incoming[i,j] == quicksum((arc[(k,l),(i,j)] for (k,l) in adj(i,j))))
            # If cell is visited, either there's one outgoing arc or it's the last one
            m.addConstr(outgoing[i,j] + end[i,j]==x[i,j])
            # If cell is visited, either there's one incoming arc or it's the first one
            m.addConstr(incoming[i,j] + start[i,j]==x[i,j])
            # Label each cell in the path from 1 (start) to 'length' (end)
            m.addConstr(label[i,j] >= end[i,j]*length)
            m.addConstr(label[i,j] >= start[i,j])
            m.addConstr(label[i,j] <= length)
            # If not in the solution, set the label to 0
            m.addConstr(label[i,j] <= length*(x[i,j]))
            # If there's an incoming arc from (k,l), the label has to be label(k,l) + 1
            for (k,l) in adj(i,j):
                m.addConstr(label[i,j] >= label[k,l] + 1 - (length+1)*(1-arc[(k,l),(i,j)]))

    m.update()
    m.optimize()
    print "Solution:"
    for i,row in enumerate(grid):
        for j,P in enumerate(row):
            print int(x[i,j].x),
        print ""
    print "Labels:"
    for i,row in enumerate(grid):
        for j,P in enumerate(row):
            print int(label[i,j].x),
        print ""

