Submarines and battleships
----------

Naval warfare is a complicated undertaking due
to the varying capabilities and vulnerabilities of both
friendly and enemy ships. Deciding who should attack
who is a critical decision that can determine the
outcome of the battle.
Figure 1 shows a map of 15 blue, friendly submarines
and 15 red, enemy battleships. Your goal is to
move each submarine so that it occupies the same
cell as a battleship. When a submarine occupies the
same cell as a battleship, the battleship is destroyed.
Each submarine can only destroy one battleship. Battleships
cannot move.

      10 o o o o o s o o o b  
      9  o o o b o o o o o o  
      8  o o o o o b b o o o  
      7  o o o s o o o b s o  
      6  o s o o o o b o o s  
      5  o o o o o b b o s o  
      4  o o b o o o s o o b  
      3  o o o s o b o o o s  
      2  o s o s o b o o o s  
      1  s b o o o b s o s b  
         A B C D E F G H I J

Use Pythagorean theorem to calculate the distance
between cells. For example, the distance between
cells A1 and B3 is 2.236 km.

**QUESTION**: What is the minimum total distance
the submarines need to travel to destroy all of the
battleships?

###Solution
Some kind of minimum-weight perfect matching problem in a bipartite graph. 
Small instance, just build a MIP and solve it.
