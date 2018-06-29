import random
import math
import itertools
import argparse
from copy import deepcopy


class Board:

    def __init__(self, board):
        self._board = deepcopy(board)

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
        found_strings = []
        product_of_instructions = [ p for p in itertools.product(self.instructions_list, repeat=self.my_depth)]
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
                        found_strings.extend(developing_list)
                        found_strings = list(set(found_strings))
                    #print("Instruction Set : {}\tDeveloped List : {}\n\nCurrent List : {}".format(instruction_set, developing_list, found_strings))
        self.find(found_strings, self.my_words)

    def find(self, list, words):
        for x in range(len(words)):
            try:
                if list.index(words[x]) >= 0:
                    print("Found : {}, Index : {}".format(words[x], list.index(words[x])))
            except:
                print("Word : {} not in list.".format(words[x]))


# @param board_loc : Refers to board.cnf which contains the closed normal form approach to file structure
# RETURN : 2-D board
def parse_board(board_loc):
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
                        return Board(board)
                    for index in range(len(data.split(" "))):
                        board[len(board) - rows][index] = data.split(" ")[index]
                    rows -= 1
                    data = f.readline().rstrip()
                f.close()
                return Board(board)
            line = f.readline().rstrip()
        f.close()
    return Board(board)

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
args = vars(parse.parse_args())

board = parse_board(args["board"])
words = parse_words(args["words"])

runner = Main(board, words, 4)
runner.boggle()
