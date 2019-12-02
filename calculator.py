#!/usr/bin/python

import re
import math

class InputParser:
    """
    A class to parse mathematical expressions from strings
    """
    def __init__(self, constants = {}):
        self.constants = constants
        self.constants['pi'] = "3.141592653589793"
        self.constants['e'] = "2.718281828459045"
        self.pemdas = ['^', '**', '*', '/', '+', '-']
    
    def parse_input(self, expression):
        """
        Parse user input and return the root of a syntax tree
        :param expression a mathematical expression
        :returns the root of a syntax tree
        """
        # token_list = []
        token_list = expression.split(' ')
        for i in range(len(token_list)):
            if token_list[i] in self.constants:
                token_list[i] = self.constants[token_list[i]]
        # print(token_list)
        # no_spaces = ''.join(init_list)
        # print(no_spaces)
        # for char in no_spaces:
        #     if char in self.constants:
        #         token_list.append(self.constants[char])
        #     else:
        #         token_list.append(char)
        return self._make_tree(token_list, 0)

    def _make_tree(self, token_list, index):
        while self.pemdas[index] in token_list:
            for i in range(len(token_list) - 1):
                if token_list[i] == self.pemdas[index]:
                    new_node = Node(token_list[i], token_list[i-1], token_list[i+1])
                    token_list[i-1] = new_node
                    del token_list[i]
                    del token_list[i]
                    break
        if index < len(self.pemdas) - 1:
            return self._make_tree(token_list, index + 1)
        else:
            return token_list[0]
    
    def evaluate(self, root):
        return self._evaluate_tree(root)
    
    def _evaluate_tree(self, root):
        if root.value == '^':
            root.value = "**"
        if self._is_number(root.value):
            return float(root.value)
        elif self._is_operator(root.value):
            eval_string = "self._evaluate_tree(root.left)" + str(root.value) + "self._evaluate_tree(root.right)"
            return eval(eval_string)
    
    def _is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _is_operator(self, value):
        return value in self.pemdas

class Node:
    """
    A node in the expression tree
    """
    def __init__(self, value, left_child, right_child):
        self.value = value
        if isinstance(left_child, str):
            self.left = Node(left_child, None, None)
        else:
            self.left = left_child
        if isinstance(right_child, str):
            self.right = Node(right_child, None, None)
        else:
            self.right = right_child


def print_tree(root):
    this_level = [root]
    print_level(this_level)


def print_level(this_level):
    next_level = []
    for n in this_level:
        print(n.value, end = ' '),
        if n.left:
            next_level.append(n.left)
        if n.right:
            next_level.append(n.right)
    if next_level:
        print("\n")
        print_level(next_level)


def run():
    print("Type Exit to Quit")
    print("Calculator: ")
    while True:
        expression = input()
        parser = InputParser()
        if expression.lower() == "exit":
            return
        tree = parser.parse_input(expression)
        # print_tree(tree)
        # calc = Evaluator()
        print("RESULT = " + str(parser.evaluate(tree)))


if __name__ == "__main__":
    run()
