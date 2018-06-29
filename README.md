Boggle Algorithm

Description
------------
Being explorative on difference ways of traversing boards and allowing for faster data tracing, I wanted to try my hand at the well known game 'Boggle'. 

Though I'm not entirely sure of the actual games name/origin, the nature of the game is to find as many words as possible in a given list.

I decided to go through a step by step process into organizing/writing a program that would traverse the indices of the board to eventually find said words.

Currently the program is restricted to a given board and words, eventually I plan to implement customizable depth searching and evaluate the possibility of using the UNIX/Linux dictionary as a basis for the possible words.

Complexities
------------
The space complexity by considering the board is O(n^2) while the space complexity of the list is quite astromical.

The time complexity can be measured by O(row * column * product(instructions^depth) * depth).

For the future, it's advised that a space complexity for the board
being O(n + e) would be more optimal and the list to be evaluated after each iteration. Though this would increase the time, space wouldn't be as large as it currently is. 

Dependencies
------------
* python3

Running
------------
python3 -b/--board board.cnf -w/--words words.cnf


