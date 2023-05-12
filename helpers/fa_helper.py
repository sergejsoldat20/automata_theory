from models.dfa import DFA
from models.nfa import NFA
from models.epsylon_nfa import EpsylonNFA

class FiniteAutomataHelper:
    def dfa_to_regex(dfa):
        # Step 1: Convert DFA to GNFA by adding a new start state and a new final state
        start_state = 'S'
        final_state = 'F'
        gnfa = {
            start_state: {},
            final_state: {}
        }
        gnfa[start_state][final_state] = ''
        
        # Include all states in the GNFA dictionary
        for state in dfa:
            gnfa[state] = {}
            for symbol in dfa[state]:
                next_state = dfa[state][symbol]
                gnfa[state][next_state] = ''
        
        # State elimination
        for k in dfa:
            if k != start_state and k != final_state:
                for i in dfa:
                    if i != start_state and i != final_state:
                        for j in dfa:
                            if j != start_state and j != final_state:
                                gnfa[i][j] = f'({gnfa[i][j]}) + ({gnfa[i][k]})({gnfa[k][k]})*({gnfa[k][j]})'
        
        return gnfa[start_state][final_state]
