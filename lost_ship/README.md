Lost at sea
----------

Searching for a lost ship at sea is a time sensitive
task that requires skill and urgency. Quickly finding
a lost ship can mean the difference between life and
death.

The following grid shows a section of ocean
divided into 64 cells. Somewhere in this grid, a ship
has been lost. Each cell has a number that represents the probability of finding the lost ship when
that cell is searched (based on last known position,
ocean currents and debris sightings). For example,
if you searched cell (0,0), you would have a 3 percent
chance of finding the lost ship there.

3 0 0 3 2 4 2 3  
3 3 3 1 2 4 1 4  
0 4 0 1 2 3 4 0  
1 1 0 3 4 1 1 0  
1 1 3 3 1 2 2 4  
0 2 3 3 3 0 2 4  
2 3 2 4 2 4 1 1  
2 1 2 2 2 4 1 3  


As the leader of the search and rescue team,
your goal is to find the ship with all survivors. Unfortunately, it takes you one day to search a cell, and
the lost sailors have only enough food and water to survive for 10 days. This allows you to search a total of 10 cells before the lost sailors perish.
You may start your search in any of the 64 cells.
You are only allowed to move to adjacent cells (you
cannot move diagonally), and you are not allowed
to revisit any cells. Add up the percentages in the
10 cells you have searched to get the probability of
finding the lost ship.

**QUESTION:**
What is the greatest probability of finding the lost ship?

###~~First idea: Dynamic Programming~~


Bellman equation:

OPT(i,l) = P(i) + max{j in adj(i)}OPT(j,l-1)  
OPT(i,1) = P(i) or, equivalently, OPT(i,0) = 0

A node is a coordinate pair (x,y).  
Given i = (x,y), the neighbouring cells are adj(i) = {(x+1,y), (x-1,y), (x,y+1), (x,y-1)} (provided that the element is in the grid).

Then, just build the table OPT = card(i) x length = 64 x 10

Nope, scratch this. We can't use twice the same cell,
and there is no direction we have to follow, so DP is not as
straightforward as it seemed.

###Second idea:

Simply with a recursive algorithm it's easy to find a solution.
Not as nice/efficient, but it's ok on this small puzzle.

###Third idea:


Integer programming model. Each cell is a node in a graph. Each node in the
solution must have one incoming and one outgoing arc (except for the starting
and ending cell). Each node in the path is labeled from 1 to 10, so to avoid
cycles. Cells not in the solution are labeled 0.
