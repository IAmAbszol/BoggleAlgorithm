import itertools
import datetime
import argparse
from collections import defaultdict
from copy import deepcopy


class Stack:
    def __init__(self):
        self.items = []

    # I have changed method name isEmpty to is_empty
    # because in your code you have used is_empty
    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def __str__(self):
        return "{}".format(self.items)

class Board:

    def __init__(self, board, dict):
        self._board = deepcopy(board)
        self._dict = dict

    def BFS(self, index, depth, stack, the_list):
        if the_list is None:
            the_list = []
        if stack is None:
            stack = Stack()
        if stack.size() >= depth:
            return
        if stack.is_empty():
            stack.push(index)
            the_list.append(self.getElementByIndex(index))
        for x in range(len(self._dict[index])):
            stack.push(self._dict[index][x])
            the_list.append(the_list[len(the_list) - 1] + self.getElementByIndex(self._dict[index][x]))
            list_index = len(the_list) - 1
            self.BFS(self._dict[index][x], depth, stack, the_list)
            stack.pop()
            the_list.append(the_list[list_index][:-1])
        return the_list

    def getElementByRowColumn(self, row, col):
        return self._board[row][col]

    def getElementByIndex(self, index):
        return self._board[self.getRowColumn(index)[0]][self.getRowColumn(index)[1]]

    def getIndex(self, row, col):
        return row * len(self._board) + col

    def getRowColumn(self, index):
        return int(index / len(self._board[0])), (index % len(self._board[0]))

    # use the __str__ method later on
    def display(self):
        for row in range(self.Rows):
            print("{}".format(board[row]))

class Main:

    def __init__(self, board, words, depth):
        self.my_board = deepcopy(board)
        self.my_words = deepcopy(words)
        self.my_depth = depth
        self.instructions_list = [ "L", "UL", "U", "UR", "R", "DR", "D", "DL" ]

    def convert(self, instruction, index):
        if instruction == "L":
            if (index % len(self.my_board._board[0])) == 0 or index == 0:
                return -1
            return index - 1

        if instruction == "UL":
            if (index % len(self.my_board._board[0])) == 0 or index == 0 or (index - (1 + len(self.my_board._board[0]))) < 0:
                return -1
            index -= (1 + len(self.my_board._board[0]))
            return index

        if instruction == "U":
            index -= len(self.my_board._board[0])
            if index < 0:
                return -1
            return index

        if instruction == "UR":
            if (index % len(self.my_board._board[0])) == len(self.my_board._board[0]) -1 or (index - (len(self.my_board._board[0]) - 1)) < 0:
                return -1
            index -= (len(self.my_board._board[0]) - 1)
            return index

        if instruction == "R":
            if (index % len(self.my_board._board[0])) == len(self.my_board._board[0]) -1:
                return -1
            return index + 1

        if instruction == "DR":
            if (index % len(self.my_board._board[0])) == len(self.my_board._board[0]) -1 or (index +  (1 + len(self.my_board._board[0]))) >= (len(self.my_board._board) * len(self.my_board._board[0])):
                return -1
            index += (len(self.my_board._board[0]) + 1)
            return index

        if instruction == "D":
            index += len(self.my_board._board[0])
            if index >= (len(self.my_board._board) * len(self.my_board._board[0])):
                return -1
            return index

        if instruction == "DL":
            if (index % len(self.my_board._board[0])) == 0 or (index + (len(self.my_board._board[0]) - 1)) >= (len(self.my_board._board) * len(self.my_board._board[0])):
                return -1
            index += (len(self.my_board._board[0]) - 1)
            return index

    def boggle(self):
        print("Starting Boggle")
        startTime = datetime.datetime.now()
        longestWord = len(max(self.my_words, key=len))
        found_strings = []
        product_of_instructions = [ p for p in itertools.product(self.instructions_list, repeat=self.my_depth) ]
        for row in range(len(self.my_board._board)):
            for col in range(len(self.my_board._board[row])):
                index = self.my_board.getIndex(row, col)
                print("Assessing index ({}) that holds value {}.".format(index, self.my_board.getElementByIndex(index)))
                # cartesian product of instructions given n depth, iterate through each instruction set
                # a combination of a powerset and covering/allowing duplication would
                # prove more optimal in assessing depth 0 to n rather than n.
                # - food for thought
                for instruction_set in product_of_instructions:
                    index = self.my_board.getIndex(row, col)
                    developing_list = [ self.my_board.getElementByIndex(index) ]
                    for iter in range(len(instruction_set)):
                        #print("Index : {} \t On instruction : {}\tReturned : {}".format(index, instruction_set[iter], self.convert(instruction_set[iter], index)))
                        index = self.convert(instruction_set[iter], index)
                        if index == -1:
                            break
                        developing_list.append(developing_list[len(developing_list) - 1] + self.my_board.getElementByIndex(index))
                        if len(developing_list[len(developing_list) - 1]) > longestWord:
                            break
                    found_strings.extend(developing_list)
                found_strings = list(set(found_strings))

        self.display(found_strings, self.my_words, startTime)

    def optimal_boggle(self):
        print("Starting optimal boggle")
        startTime = datetime.datetime.now()
        found_strings = []
        for row in range(len(self.my_board._board)):
            for col in range(len(self.my_board._board[row])):
                print("Assessing index ({}) that holds value {}.".format(self.my_board.getIndex(row, col), self.my_board.getElementByRowColumn(row, col)))
                mylist = self.my_board.BFS(self.my_board.getIndex(row, col), self.my_depth, None, None)
                found_strings.extend(list(set(mylist)))
        self.display(found_strings, self.my_words, startTime)


    def display(self, list, words, startTime):
        timeDiff = datetime.datetime.now() - startTime
        print("Total time taken : {}".format(timeDiff))
        for x in range(len(words)):
            try:
                if list.index(words[x]) >= 0:
                    print("Found : {}, Index : {}".format(words[x], list.index(words[x])))
            except:
                print("Word : {} not in list.".format(words[x]))
        print("")

# @param board_loc : Refers to board.cnf which contains the closed normal form approach to file structure
# RETURN : 2-D board
def parse_board(board_loc):

    def adjacencies(board, index):
        adjacent = []
        if (index % len(board[0])) != 0 and index != 0:
            adjacent.append((index - 1))

        if (index % len(board[0])) != 0 and index != 0 and (index - (1 + len(board[0]))) >= 0:
            adjacent.append((index - (1 + len(board[0]))))

        if (index - len(board[0])) >= 0:
            adjacent.append((index - len(board[0])))

        if (index % len(board[0])) != len(board[0]) - 1 and (index - (len(board[0]) - 1)) >= 0:
            adjacent.append((index - (len(board[0]) - 1)))

        if (index % len(board[0])) != len(board[0]) - 1:
            adjacent.append((index + 1))

        if (index % len(board[0])) != len(board[0]) - 1 and (
                index + (1 + len(board[0]))) < (
                len(board) * len(board[0])):
            adjacent.append((index + (len(board[0]) + 1)))

        if (index + len(board[0])) < (len(board) * len(board[0])):
            adjacent.append((index + len(board[0])))

        if (index % len(board[0])) != 0 and (index + (len(board[0]) - 1)) < (
                len(board) * len(board[0])):
            adjacent.append((index + (len(board[0]) - 1)))

        return adjacent

    dict = defaultdict(list)
    board = None
    with open(board_loc) as f:
        line = f.readline().rstrip()
        while line:
            if "p cnf" in line:
                rows, columns = int(line.split(" ")[2]), int(line.split(" ")[3])
                board = [ [""] * columns for x in range(rows) ]
                data = f.readline().rstrip()
                while data:
                    if rows <= 0:
                        f.close()
                        for row in range(len(board)):
                            for col in range(len(board[row])):
                                index = (row * len(board)) + col
                                dict[index] = adjacencies(board, index)
                        return Board(board, dict)
                    for index in range(len(data.split(" "))):
                        board[len(board) - rows][index] = data.split(" ")[index]
                    rows -= 1
                    data = f.readline().rstrip()
                f.close()
                for row in range(len(board)):
                    for col in range(len(board[row])):
                        index = (row * len(board[0])) + col
                        dict[index] = adjacencies(board, index)
                return Board(board, dict)
            line = f.readline().rstrip()
        f.close()
    return Board(board, dict)

# @param words_loc : Refers to words.cnf which contains the closed normal form approach file structure
# RETURN : list of words contained inside board
def parse_words(words_loc):
    words = None
    with open(words_loc) as f:
        line = f.readline().rstrip()
        while line:
            if "p cnf" in line:
                rows = int(line.split(" ")[2])
                words = [ "" ] * rows
                data = f.readline().rstrip()
                while data:
                    if rows <= 0:
                        f.close()
                        return words
                    words[len(words) - rows] = data
                    rows -= 1
                    data = f.readline().rstrip()
                f.close()
                return words
            line = f.readline().rstrip()
        f.close()
    return words


# parse arguments according to prerequisite files being available
parse = argparse.ArgumentParser()
parse.add_argument("-b", "--board", required=True, help="path to board.")
parse.add_argument("-w", "--words", required=True, help="path to words.")
parse.add_argument("-d", "--depth", type=int, required=True, help="length of developing word.")
args = vars(parse.parse_args())

board = parse_board(args["board"])
words = parse_words(args["words"])

runner = Main(board, words, args["depth"])
runner.optimal_boggle()
