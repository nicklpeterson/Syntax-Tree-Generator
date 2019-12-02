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
        regex_string = self._build_regex_string()
        # regex_string = re.compile(regex_string)
        token_list = re.findall(regex_string, expression)
        for i in range(len(token_list)):
            if token_list[i] in self.constants:
                token_list[i] = self.constants[token_list[i]]
        token_list = [x if x is not "^" else "**" for x in token_list]
        return self._make_tree(token_list, 0)
    
    def _build_regex_string(self):
        """
        Method to create a reg_ex string that matches all known expressions
        """
        regex_string = "(["
        # match known expressions
        for exp in self.pemdas:
            regex_string = regex_string + "\\" + exp + "|"
        regex_string = regex_string + "]|"
        # Match Constants
        for k in self.constants:
            regex_string = regex_string + k + "|"
        # Match numbers
        regex_string = regex_string + "[0-9]*\.?[0-9]+)"
        return regex_string

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
        if self._is_number(root.value):
            return float(root.value)
        elif self._is_operator(root.value):
            eval_string = str(self._evaluate_tree(root.left)) + str(root.value) + str(self._evaluate_tree(root.right))
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
        try:
            expression = input()
            parser = InputParser()
            if expression.lower() == "exit":
                return
            tree = parser.parse_input(expression)
            print("RESULT = " + str(parser.evaluate(tree)))
        except:
            print("I am unable to evaluate that expression.")


if __name__ == "__main__":
    run()
