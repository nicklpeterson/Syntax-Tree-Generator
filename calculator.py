#!/usr/bin/python

import re
import math
import copy
from collections import deque

class InputParser:
    """
    A class to parse mathematical expressions from strings
    """
    def __init__(self, constants = {}):
        """
        :attribute constants: known constants
        :attribute pemdas: known expressions that will be evaluated in the order of this list.
        """
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
        token_list = re.findall(regex_string, expression)
        for i in range(len(token_list)):
            if token_list[i] in self.constants:
                token_list[i] = self.constants[token_list[i]]
        token_list = [x if x is not "^" else "**" for x in token_list]
        return self._make_tree(token_list, 0)

    def evaluate(self, root):
        """
        Recursively evaluate a mathematical syntax tree.
        :param root: the root of a syntax tree
        :returns the result
        """
        return self._evaluate_tree(root)

    def _build_regex_string(self):
        """
        Create a reg_ex string that matches all known expressions
        """
        regex_string = "([\(|\)"
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
        """
        Recursively build a syntax tree from a list of tokens
        :param token_list: a list of syntax tokens that are numbers, parenthesis or in self.pemdas
        :returns index: the index of the current expression that is being searched for.
        """
        if "(" in token_list or ")" in token_list:
            self._check_parenthesis(token_list)
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

    def _check_parenthesis(self, token_list):
        """
        Recursively ensure that all expressions in parenthesis are evaluated first
        :param token_list: a list of syntax tokens that are numbers, parenthesis, or in self.pemdas 
        """
        start = None 
        end = None 
        sub_tree = None
        d = deque()
        # Find the open parenthesis
        for i in range(len(token_list)):
            if token_list[i] == "(":
                start = i
                break
    
        # If there is no open parenthesis remove closing parenthesis and return
        if start is None:
            while ")" in token_list :
                token_list.remove(")")
            return

        # If there is no closing parenthesis remove open parenthesis
        if not ")" in token_list:
            while "(" in token_list:
                token_list.remove("(")
            return

        # Find the location of the closing parenthesis
        for i in range(start, len(token_list)):
            if token_list[i] == ')':
                d.popleft()
            if token_list[i] == '(':
                d.append(token_list[i])
            if not d:
                end = i
                break

        # Replace the expression in parenthesis with a syntax sub_tree
        sub_tree = self._make_tree(token_list[start + 1 : end], 0)
        if sub_tree:
            token_list[start] = sub_tree
            del token_list[start + 1: end + 1]
    
    def _evaluate_tree(self, root):
        """
        Helper method for evaluate..
        :param root: the root of a syntax tree
        :returns the result
        """
        if self._is_number(root.value):
            return float(root.value)
        elif self._is_operator(root.value):
            eval_string = str(self._evaluate_tree(root.left)) + str(root.value) + str(self._evaluate_tree(root.right))
            return eval(eval_string)
    
    def _is_number(self, value):
        """
        Check if a string is a number
        :param value: value to check
        :returns boolean
        """
        # TODO This is ugly, fix
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _is_operator(self, value):
        """
        Check if value is a known operator
        :param value: the value to check
        """
        return value in self.pemdas

class Node:
    """
    A node in the expression tree
    """
    def __init__(self, value, left_child, right_child):
        """
        Create a Node. If a child is a string create a new Node for that child.
        :param value: the value stored by this node
        :param left_child: this Node's left child
        :param right_child: this Node's right child
        """
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
    """
    Print a tree using a level order traversal
    :params root: the root of a binary tree
    """
    this_level = [root]
    print_level_order(this_level)


def print_level_order(this_level):
    """
    Helper method for print tree
    :params this_level: a list of nodes on the current level
    """
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


def run_console():
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
    run_console()
