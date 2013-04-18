#!/usr/bin/env python
from gurobipy import *

# Data

# Sets
T = range(1,25)
#I = ['heatpump','turbine']
S = [1,2,3]

# Parameters
I, c_OM, c_delta, c_f, b, q_u, q_l, e_u, e_l, K_1, K_2, K_3, max_starts = multidict({\
   'heatpump': \
   [0.1,      10,   0,   3,2500, 400,   0,   0,   0,   3,  0,   5],\
   'turbine':\
   [0.4,      50,0.06,   8,3100,1300,4500,2200,0.16,   0,0.21,  3],\
    'turbine2':\
   [0.4,      50,0.06,   8,3100,1300,4500,2200,0.16,   0,0.21,  3]
   })

# Break symmetry between turbines?
#print I,S,T
c_p = 0.09
nu = 4
loss = 0.05
max_storage = 2000

d_q = {}
#        1     2    3    4    5    6   7    8    9    10   11   12 
d_q[1] = [ 200, 200, 200, 200, 200, 500,2000,2000,2000,3000,2000,2000,\
        2000,2000,4000,100,2000,2000,2000,2000, 500, 300, 200, 200]

d_q[2] = [ 200, 200, 200, 300, 500, 2000,3000,2000,2000,2000,400,2000,\
        2000,2000,2000,2000,2000,2000,2000,2500, 300, 200, 100, 100]

d_q[3] = [ 200, 300, 300, 200, 200, 500,2000,3000,6000,2000,4000,4000,\
        3000,1400,1200,1500,2000,4000,4000,3500,1500, 400, 300, 200]

d_e = {}
#        1     2    3    4    5    6   7    8    9    10   11   12 
d_e[1] = [ 200, 200, 800, 1000, 900, 500,2000,2000,3000,2000,2000,2000,\
        4000,4000,4000,5000,2000,2000,2000,2000, 500, 300, 200, 200]

d_e[2] = [ 200, 200, 200, 300, 500, 2000,3000,2000,2000,4000,2000,2000,\
        2000,2000,2000,2000,2000,2000,2000,2500, 300, 200, 100, 100]

d_e[3] = [ 200, 300, 300, 200, 200, 500,5000,5000,2000,2000,7000,2000,\
        6000,2000,2000,2000,2000,2000,2009,900, 500, 400, 300, 200]

m = Model('rdcogen')

z,y,q,e,f,p,u,delta,v = {},{},{},{},{},{},{},{},{}
for i in I:
        for t in T:
            z[i,0,t] = m.addVar(vtype=GRB.BINARY, obj=c_OM[i], name='z_%s_%s_%s'%(i,0,t))
            for s in S:
                z[i,s,t] = m.addVar(vtype=GRB.BINARY, name='z_%s_%s_%s'%(i,s,t))
                delta[i,s,t] = m.addVar(vtype=GRB.BINARY, name='delta_%s_%s_%s'%(i,s,t))
                y[i,s,t] = m.addVar(vtype=GRB.INTEGER, ub=1,lb=-1, name='y_%s_%s_%s'%(i,s,t))
                v[i,s,t] = m.addVar(vtype=GRB.BINARY, name='v_%s_%s_%s'%(i,s,t))
                #print "added v_%s_%s_%s"%(i,s,t)
                q[i,s,t] = m.addVar(lb=0,ub=q_u[i], name='q_%s_%s_%s'%(i,s,t))
                e[i,s,t] = m.addVar(lb=0,ub=e_u[i], name='e_%s_%s_%s'%(i,s,t))
                f[i,s,t] = m.addVar(lb=0, name='f_%s_%s_%s'%(i,s,t))
                p[i,s,t] = m.addVar(lb=0, name='p_%s_%s_%s'%(i,s,t))


for t in T:
    for s in S:
        u[s,t] = m.addVar(lb=0,ub=max_storage, name='u_%s_%s'%(s,t))

eta = m.addVar(lb=0,name='eta',obj=1)
totcost={}
for s in S:
    totcost[s] = m.addVar(lb=0, name='totcost_%s'%(s),obj=0.000001)
m.update()


for s in S:
    m.addConstr(quicksum(v[i,s,t] for i in I for t in T) <= nu)
    m.addConstr(eta>=totcost[s])
    m.addConstr(totcost[s]==quicksum((c_f[i]*f[i,s,t] + c_p*p[i,s,t] + c_OM[i]*y[i,s,t] + c_delta[i]*delta[i,s,t] + b[i]*v[i,s,t]) for i in I for t in T))

for i in I:
    for t in T:
        for s in S:
            m.addConstr(z[i,s,t] == z[i,0,t] + y[i,s,t])
            m.addConstr(v[i,s,t] >= y[i,s,t])
            m.addConstr(v[i,s,t] >= -y[i,s,t])
            if 'turbine' in i:
                m.addConstr(q[i,s,t] <= K_1[i]*f[i,s,t])
                m.addConstr(e[i,s,t] <= K_3[i]*f[i,s,t])
            else:
                m.addConstr(q[i,s,t] <= K_2[i]*p[i,s,t])
            
            m.addConstr(q[i,s,t] <= q_u[i]*z[i,s,t])
            m.addConstr(q[i,s,t] >= q_l[i]*z[i,s,t])
            
            m.addConstr(e[i,s,t] <= e_u[i]*z[i,s,t])
            m.addConstr(e[i,s,t] >= e_l[i]*z[i,s,t])

for t in range(1,24):
    for s in S:
        m.addConstr(quicksum(q[i,s,t] for i in I) + u[s,t]*(1-loss) - u[s,t+1]>=d_q[s][t-1])

#Q: WHY t-1? A: d_q[s] is an array, not a dict. starts from 0..
for s in S:
    m.addConstr(u[s,1]==0)
    m.addConstr(quicksum(q[i,s,24] for i in I) + u[s,24]*(1-loss) #- u[s,1]
            >=d_q[s][24-1])

for t in T:
    for s in S:
        #print s,t
        m.addConstr(quicksum((e[i,s,t]-p[i,s,t]) for i in I) >= d_e[s][t-1])

for i in I:
    for t in range(2,25):
        for s in S:
            m.addConstr(delta[i,s,t] >= z[i,s,t] - z[i,s,t-1])
            m.addConstr(delta[i,s,t] <= z[i,s,t])
            m.addConstr(delta[i,s,t] <= 1 - z[i,s,t-1])

for i in I:
        for s in S:
            m.addConstr(delta[i,s,1] >= z[i,s,1]) # - z[i,s,24])
            m.addConstr(delta[i,s,1] <= z[i,s,1])
            #m.addConstr(delta[i,s,1] <= 1 - z[i,s,24])
            m.addConstr(quicksum(delta[i,s,t] for t in T)<=max_starts[i])

m.optimize()

print m.status
print m.getObjective().getValue()
#print z,y

