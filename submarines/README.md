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

      10| | | | | |s| | | |b|
      9 | | | |b| | | | | | |
      8 | | | | | |b|b| | | |
      7 | | | |s| | | |b|s| |
      6 | |s| | | | |b| | |s|
      5 | | | | | |b|b| |s| |
      4 | | |b| | | |s| | |b|
      3 | | | |s| |b| | | |s|
      2 | |s| |s| |b| | | |s|
      1 |s|b| | | |b|s| |s|b|
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
