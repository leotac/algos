def buildTable(totalFuel, totalCars, capacity):
   L = {}
   p = {}
   for K in range(totalCars,0,-1): #from totalCars to 1
      L[K] = {}
      for F in range(totalFuel,-1,-1): #from totalFuel to 0
         move = 0
         sendBack = 0
         if (F+2*K) <= totalFuel:
            if F + 2*K + K*L[K][F+2*K] <= K*capacity:
               move = 1 + L[K][F+2*K]
         if K+1 <= totalCars:
            sendBack = L[K+1][F]
         L[K][F] = max(move,sendBack)
         if move>=sendBack and move>0:
            p[(K,F)] = ((K,F+2*K),move)
         elif sendBack>0:
            p[(K,F)] = ((K+1,F),sendBack)
         else:
            p[(K,F)] = (0)
         print "L["+str(K)+","+str(F)+"]="+str(L[K][F])
   return L,p


def path(L,p,K,F):
   state = (K,F)
   while p[state] != 0:
      print "L["+str(state)+"]= "+str(p[state][1])#+" <- "+ str(p[state][0])
      state = p[state][0]
   print "p["+str(state)+"]= "+str(p[state])
   
