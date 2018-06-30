import itertools

def display(version, total):
    print("Version : {}, Total = {}".format(version, total))

def calculateVersion1(rows, columns, depth):
    instruction_list = [ i for i in range(8) ]
    product_of_instructions = [p for p in itertools.product(instruction_list, repeat=depth)]
    equation_total = len(product_of_instructions) * rows * columns * depth

    display("Version 1", equation_total)

calculateVersion1(5,5,2)