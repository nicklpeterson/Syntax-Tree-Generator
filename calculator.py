import re


class InputParser:
    """
    A class to parse mathematical expressions from strings
    """
    def __init__(self, constants = {}):
        self.constants = constants
        self.constants['pi'] = 3.141592653589793
        self.constants['e'] = 2.718281828459045
        self.pemdas = ['*', '/', '+', '-']

    def make_tree(self, token_list, index)
        for i in range(token_list)
            if token_list[i] == pemdas[index]:
                new_tree = Node(token_list[i], token_list[i - 1], token_list[i + 1])
                token_list[i - 1] = new_tree
                del token_list[i]
                del token_list[i + 1]
                break
        if pemdas[index] in token_list:
            self.make_tree(token_list, index)
        if index < len(self.pemdas) - 1:
            self.make_tree(token_list, index + 1)
        return token_list[0]
        
    def _is_operand(self, value):
        return value.isnumeric()
    
    def _is_operator(self, value):
        operator_regex = '^(\+|\-|\*|\\|\^)$'
        return re.match(operator_regex, value)

    def _check_operator(self, value, operator):
        return value == operator


class Node:
    """
    A node in the expression tree
    """
    def __init__(self, value, left_child, right_child):
        self.value = value
        self.left = left_child
        self.right = right_child


def print_tree(root):
    h = get_height(root)
    for i in range(1, h + 1):
        print_level(root, i)

def print_level(root, level):
    if root is None:
        return
    if level == 1:
        print(root.value)
        print("\n")
    elif level > 1:
        print_level(root.left, level - 1)
        print_level(root.right, level - 1)


def get_height(root):
    """
    Method to calulate the height of a tree
    """
    if root is None:
        return 0
    else:
        left_height = height(root.left)
        right_height = height(root.right)
        return left_height + 1 if left_height > right_height else right_height + 1


if __name__ = "__main__":
    parser = InputParser()
    expression = ['2', '+', '2', '*', '8', '/', '2', '*', '4']
    print_tree(parser.make_tree(expression, 3))
