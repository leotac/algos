Some notes on the compression algorithm
==========

Suppose 'a' is the most frequent character, then 'b', and so on.
I want:
a -> 01
b -> 001
c -> 011
etc.

Constant, 1 byte ASCII encoding:
256 characters
8x256=2048 = 2^11 bits to write all characters once

My silly encoding:

bits? -  sum_i(ix(i+1))
            sum i^2 * sum i
n(n + 1) = 512
sum i^2 = n(n*1)/2 (2n+1)/3 = 256*15 + 256 = 256*16 = 2^12, DOUBLE.

Worst case (all characters with no repetitions), the file is more or less TWICE as big.

x
xx
xx
xxx
xxx
xxx
xxxx    |
xxxx    | Group
xxxx    | "n"
xxxx    |
xxxxx
xxxxx
xxxxx
xxxxx
xxxxx

Encoding of character number 'n':
The "group" is floor(x) with x : (x+1)x/2  = n

x^2 + x -2n = 0
x = (-1 +- sqrt(1 + 8n))/2

Length of bits is floor(x) + 2 -->  "0_ _ _ _1"
Number of 'ones': n - (floor(x)+1)(floor(x))/2

Example:
Char number 4 => x = 2.something
floor(x) = 2 -> length of encoding is floor(x) + 2 = 4
New representation is: 0 _ _ 1
Putting floor(x)=2 in the formula, I get 3.
In order to reach n=4 we need 1 'one', then 0011.

Char n=0 => x=0. Representation length 0+2 = 2 01
Char n=8 => x=3.something. Then 3+2 = 5 bits are needed. 
Number of ones in the middle is 8 - (6) = 2
0_ _ _1 --> 00111

0: 01
1: 001
2: 011
3: 0001
4: 0011
5: 0111
6: 00001
7: 00011
8: 00111
9: 01111
10: 000001
11: 000011
12: 000111
13: 001111
14: 011111
15: 0000001
16: 0000011


Encoding
========

Write bytes to files. Start with byte 0x00.
Build the byte to write incrementally adding compressed encoding
of each ASCII character we read.

First bit arrives. counter is 0. add first bit with mask 0x80 (OR).
Second bit arrives. counter is 1. add second bit with mask 0x40.
Finish character. new character. counter is 2. add first bit with mask 0x20.
Array of 1-bit-to-1 masks.
0x80    10000000
0x40    01000000
0x20    00100000
0x10    00010000
0x08    00001000
0x04    00000100
0x02    00000010
0x01    00000001


DECODING
========

Similar.
Read bit by bit using counter/mask and building bit vector.
When the current bit is 1 and next is 0, a character is complete: decode.
Formula to get the index of the character in the sorted list of 
most frequent characters:
((length - 2) +1)(length-2)/2 + number of ones.



0010 0110 0010 0100
