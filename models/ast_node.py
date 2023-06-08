# Conversion from Regex to NFA

import json
import sys

non_symbols = ['+', '*', '.', '(', ')']
nfa = {}


class charType:
    SYMBOL = 1
    CONCAT = 2
    UNION = 3
    KLEENE = 4


class NFAState:
    def __init__(self):
        self.next_state = {}


class ExpressionTree:

    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None
