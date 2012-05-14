import heapq
from gurobipy import *

## Exact IP formulation
def exact(F, C, f, c):
    m = Model('MUFL')
    
    # Variables
    x,y = {},{}
    for i in F:
        for j in C:
            x[i,j] = m.addVar(vtype=GRB.BINARY, obj=c[i,j], name='x_%s_%s' % (i, j))
    for i in F:
        y[i] = m.addVar(vtype=GRB.BINARY, obj=f[i], name='y_%s' % (i))
                    
    m.update()
    # Constraints
    for j in C:
        m.addConstr(quicksum(x[i,j] for i in F) >= 1, 'covering_%s' % (i))
    for i in F:
        for j in C:
            m.addConstr(y[i] - x[i,j] >= 0, 'open_%s%s' % (i,j))
     
    m.optimize()
    assign, I = {},{}
    for i in F:
        if y[i].x == 1:
            I.append(i)
        for j in C:
             if x[i,j].x == 1:
                  print i, '->', j, ':', x[i,j].x
                  assign[j]=i

    costo = sum([f[x] for x in I]) + sum([c[assign[x],x] for x in C])
    print costo, assign
    return costo
    
    
# Primal-dual 3-approximation algorithm for Metric Uncapacitated Facility Location  [Jain, Vazirani 2001]  
def primaldual(F, C, f, c):

    #beta
    beta = dict.fromkeys([(i,j) for i in F for j in C],0)

    #queue with edge costs
    edges = [(value,key) for key,value in c.iteritems()]
    heapq.heapify(edges)
    
    #queue with anticipated time for each facility
    time = dict.fromkeys(F,(float('inf')))
    timeq = [(float('inf'), x) for x in F]
    heapq.heapify(timeq)

    #cities already connected
    connected = dict.fromkeys(C,False)

    #temporarily open facility
    opened = dict.fromkeys(F,False)

    #number of contributors at current instant
    contributors = dict.fromkeys(F,0)

    #list of facilities with contribution from a city
    from collections import defaultdict 
    contrib = defaultdict(list) 

    ## First Phase

    while len(edges)>0 and len(timeq)>0:
        if edges[0][0]<=timeq[0][0]:
            smaller = heapq.heappop(edges)

            value, edge = smaller
            fac = edge[0]
            city = edge[1]
            if connected[city]==False:
                if opened[fac] == False:
                    #facility not yet completed: start contributing
                    #update anticipated time
                    if contributors[fac]>0:
                        remaining = (time[fac] - value)*contributors[fac]
                    else:
                        remaining = f[fac]
                    contrib[city].append(fac)
                    contributors[fac]+=1
                    time[fac] = value + float(remaining/contributors[fac])

                    #update queue
                    timeq = [(time[x], x) for x in F if opened[x]==False]
                    heapq.heapify(timeq)
                else:
                    #facility already completed: stop contributing to other facilities (past contributions remain)
                    connected[city]=True
                    for x in contrib[city]:
                        if x != fac:
                            remaining = (time[x] - value)*contributors[x]
                            contributors[x]-=1
                            
                            if contributors[x]>0:
                                time[x] = value + float(remaining/contributors[x])
                            else:
                                time[x] = float('Inf')

                            beta[(x,city)] = value - c[(x,city)]        

                            timeq = [(time[y], y) for y in F if opened[y]==False]
                            heapq.heapify(timeq)
                    contrib[city]=[fac]

        else:
            #facility completed: stop cities from contributing to other facilities
            smaller = heapq.heappop(timeq)
            value, fac = smaller
            
            opened[fac] = True
            for city in C:
                if fac in contrib[city] and connected[city]==False:
                        for x in contrib[city]:
                            beta[(x,city)] = value - c[(x,city)]  
                            if x != fac:
                                remaining = (time[x] - value)*contributors[x]
                                contributors[x]-=1
                                if contributors[x]>0:
                                    time[x] = value + float(remaining/contributors[x])
                                else:
                                    time[x] = float('Inf')

                                timeq = [(time[y], y) for y in F if opened[y]==False]
                                heapq.heapify(timeq)

                        contrib[city]=[fac]

    ## Second Phase
                        
    adj={}
    Ft = [y for y in F if opened[y]==True]

    #build adjacency list
    for x in C:
        A=[y for y in Ft if beta[(y,x)]>0]
        for a in A:
            adj.setdefault(a,set())
            adj[a] = adj[a].union(A)
    #Build maximal independent set
    I=[]
    free=dict.fromkeys(Ft,True)
    for x in Ft:
        if free[x]==True:
            I.append(x)
            for i in adj.setdefault(x,[]):
                free[i]=False
    assign={}
    for x in C:
        special=[y for y in I if beta[(y,x)]>0]
        if len(special)>0: #if the city has contributed to at least 1 open facility, pick one
            assign[x]=special[0]
        elif contrib[x][0] in I: #else, pick witness if in I
            assign[x]=contrib[x][0]
        else: #if witness is not in I, pick an adjacent facility in I (indirect connection) -> here goes the 3-approximation factor
            a = [i for i in I if i in adj[contrib[x][0]]]
            assign[x] = a[0]

    costo = sum([f[x] for x in I]) + sum([c[assign[x],x] for x in C])
    print costo, assign
    return costo
            


def main():
##  Example
##    facilities = ['Storage A', 'Storage B', 'Storage C']
##    cities = ['Roma', 'Firenze', 'Bologna', 'Pisa']
##
##    cost= {('Storage A','Roma'):20,
##           ('Storage A','Firenze'):40,
##           ('Storage A','Bologna'):70,
##           ('Storage A','Pisa'):50,
##           ('Storage B','Roma'):60,
##           ('Storage B','Firenze'):20,
##           ('Storage B','Bologna'):40,
##           ('Storage B','Pisa'):30,
##           ('Storage C','Roma'):90,
##           ('Storage C','Firenze'):40,
##           ('Storage C','Bologna'):20,
##           ('Storage C','Pisa'):50}
##    
##    fixedcost = {'Storage A':100,'Storage B':130,'Storage C':120}

##  Tight example (with epsilon=0.05)
    facilities = ['F1','F2']
    cities = ['1', '2', '3', '4','5']

    cost= {('F1','1'):1,
           ('F1','2'):3,
           ('F1','3'):3,
           ('F1','4'):3,
           ('F1','5'):3,
           ('F2','1'):1,
           ('F2','2'):1,
           ('F2','3'):1,
           ('F2','4'):1,
           ('F2','5'):1}
         
    fixedcost = {'F1':0.05,'F2':0.05*(6)}

    

    primaldual(facilities, cities, fixedcost, cost)
    exact(facilities, cities, fixedcost, cost)

