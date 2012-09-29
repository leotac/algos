import scipy

def init():
    grid = []
    input = open("grid.dat")
    allTheLetters = string.ascii_lowercase
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


def main():
    grid = init()

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
            print "Starting cell:", x,y
            visited = scipy.zeros((8,8),int)
            visited[x,y] = 1
            path = [(x,y)]
            best[x,y], steps = maxprob(x,y,path,9,grid)
            if best[x,y] > optimal_value:
                optimal_value = best[x,y]
                optimal_path = steps
    return best, optimal_value, optimal_path

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

