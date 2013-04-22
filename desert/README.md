Desert crossing - La traversata del deserto
=========================

Puzzle from:
http://xmau.com/notiziole/arch/201304/008401.html

Nove amici, ciascuno con la sua jeep, sono al margine est di un deserto. Vogliono avventurarsi al suo interno il più possibile: però le loro jeep hanno un'autonomia di soli sessanta chilometri, perché il serbatoio contiene solo dieci litri di benzina. Ogni jeep però ha anche nove taniche da dieci litri piene di benzina; gli unici problemi sono che non si può usare una tanica solo in parte, ma bisogna versarla tutta in un unico serbatoio, e che non è possibile creare dei depositi di benzina all'interno del deserto. Qual è la distanza massima che può essere esplorata almeno da uno degli amici, tenendo conto che tutti vogliono ritornare alla base?

Nine friends, with a jeep each, are at the eastern border of a desert.
They want to travel in the desert as far as possible.
Each jeep can go as far as 60 km with a tank of fuel. Gas tanks are full at the start. Only one person is allowed on each jeep.
Each jeep can hold 9 additional fuel cans. 
A fuel can can be used only to completely refill a tank, provided that the tank is empty.
What is the farthest distance (at least) one of them can travel?
All friends obviously need to return safely to the base camp.

Solution
--------

Not hard to find that the solution is 540 - i.e., 9 'fuel units'.

Generalizing, the problem is easy enough to be solved intuitively. 
Indeed, there is a rather simple optimal policy.
Suppose w.l.o.g. that we stop and evaluate the situation at each 'fuel unit' (i.e., each 60 km).
Consider the fuel in excess for each jeep (current fuel - fuel they need to come back). 
Then, send back as many jeeps as possible such that, for each of them, either:
- all its excess fuel can be stored by the other jeeps in the group 
- the (partial) excess fuel that can't be stored is greater than 2.

This is optimal because:

1. sending back fewer jeeps than advised implies wasting fuel that could be saved. 
2. sending back more cars than needed does not improve the solution.

Dynamic programming
-------------------

Though it's not really necessary, it seemed the puzzle could be a good fit for either a search algorithm and a dynamic programming approach.

With DP, build a table L where `L[K,F]` is the max length that can be reached with K cars and F total excess fuel. 
The excess fuel, as mentioned above, is defined as the available fuel in the gas tanks or fuel cans reduced by the amount of fuel needed to get back to the base camp. In other words, the remaining fuel after all cars are back.

Since we are not interested in saving fuel, referring to the original problem, `L[1,0]` is going to be the solution we want. 
Of course, we also get _for free_ the optimal distances reached with at least `K=1..9` cars.

The update is computed according to the equation:

    L[K,F] = max {0, L[K+1,F], 1 + L[K,F+2K]}

where the last option is possible only under the constraint that `F+2K+K*L[K,F+2K]` is smaller or equal than the total capacity of `K` cars.

This means that the distance reachable with `K` cars, and leaving excess fuel `F`, is either: 

1. the same reached by `K+1` cars with the same excess `F`, if that excess is not enough to guarantee a step forward
2. 1 step further than the distance reached by the same number of cars at the previous stop, if `K` cars can store enough fuel (excess+fuel needed to come back) to take a step forward and reach the current state

The table is computed starting from the bottom row, with all `K_max` cars and all fuel `F_total` in excess, and then reducing `F`. 

It would also be possible to see the problem from the opposite point of view, i.e., considering needed fuel (used or to-be-used) instead of the excess fuel. It makes no difference (possibly the equation would be simpler to understand?).
