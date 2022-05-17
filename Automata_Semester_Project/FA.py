from graphviz import *
from collections import defaultdict

# a list of all printable ASCII characters
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
           [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
           [chr(i) for i in range(ord('0'), ord('9') + 1)] + \
           [ ':', ';', '=', '!', '#', '$', '%', '^', '{', '}',
            '[', ']', '/', '!', '&', '-', '_', '^', '~', '<', '>']
# Special characters
leftBracket = '('
rightBracket = ')'
Or = '+'
Concatenate = '.'
Astric = '*'
Epsilon = 'ε'


######## This class represents a general finite automata from which other classes(NFA and DFA) can be derived from############
class FiniteAutomata:
    def __init__(self, symbol):
        self.allStates = set()     # all states in FA
        self.symbol = symbol    # input symbol/alphabet
        self.transitions = defaultdict(defaultdict)     # transitions dictionary between states
        self.startState = None  # the start state of the FA
        self.finalStates = []   # a list of final states of the FA

################## sets the start state of the FA##################
    def set_start_state(self, state):
        self.startState = state
        self.allStates.add(state)

#################### adds a given state to the list of final states#############
    def add_final_state(self, state):
        if isinstance(state, int):
            state = [state] #convert the state into a list of states
        for s in state:
            if s not in self.finalStates:       # add to final state if not already in the list of final states
                self.finalStates.append(s)

################# Adds transitions between states#################
    def add_transition(self, from_state, to_state, inputSymbol):
        if isinstance(inputSymbol, str):
            inputSymbol = set([inputSymbol])
        self.allStates.add(from_state)
        self.allStates.add(to_state)
        #############################Law already mawgod benhom arrow abl kda##############
        if from_state in self.transitions and to_state in self.transitions[from_state]:
            self.transitions[from_state][to_state] = self.transitions[from_state][to_state].union(inputSymbol)
        else:
            self.transitions[from_state][to_state] = inputSymbol

############################# save a new transition dictionary to dictionary############
    def add_transition_dict(self, transitions):
        for from_state, to_states in transitions.items():
            for state in to_states:
                self.add_transition(from_state, state, to_states[state])

    #########change states' representing number to start with the given start number#############
    def new_NFA_from_number(self, start_num):
        translations = {}
        for i in self.allStates:
            translations[i] = start_num
            start_num += 1
        newNFA = FiniteAutomata(self.symbol)
        newNFA.set_start_state(translations[self.startState])
        newNFA.add_final_state(translations[self.finalStates[0]])
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                newNFA.add_transition(translations[from_state], translations[state], to_states[state])
        return [newNFA, start_num]

####################set of states which are reachable from state P on ε-transitions.############
    def get_epsilon_closure(self, find_state):
        all_states = set()
        states = [find_state]
        while len(states):
            state = states.pop()
            all_states.add(state)
            if state in self.transitions:
                for to_state in self.transitions[state]:
                    if Epsilon in self.transitions[state][to_state] and to_state not in all_states:
                        states.append(to_state)
        return all_states

    def get_move(self, state, state_key):   # state_key refers to an alphabet in the symbol
        if isinstance(state, int):
            state = [state]
        traversed_states = set()
        for s in state:
            if s in self.transitions:
                for tns in self.transitions[s]:
                    if state_key in self.transitions[s][tns]:
                        traversed_states.add(tns)
        return traversed_states


######################### creates an image of the corresponding FA('png' format)###############
    def create(self, fileName, pname):
        automaton = Digraph(pname, filename=fileName, format='png')
        automaton.attr(rankdir='LR')

        automaton.attr('node', shape='doublecircle')
        for final_state in self.finalStates:
            automaton.node('S' + str(final_state))

        automaton.attr('node', shape='circle')
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                tmp = ''
                for s in to_states[state]:
                    tmp += s + '|'
                automaton.edge('S' + str(from_state), 'S' + str(state), label=tmp[:-1])

        automaton.attr('node', shape='point')
        automaton.edge('', 'S' + str(self.startState))
        automaton.render(view=False)


class Regex2NFA:
 ###############Class Constructor##################
    def __init__(self, regex):
        self.regex = regex
        self.createNFA()     # Create the NFA

    ################## create an image of the equivalent NFA of the given regex###########
    def create_nfa(self):
        self.nfa.create('nfa.gv', 'Non Deterministic Finite Automata')

    @staticmethod
    def get_priority(p):
        if p == Or:      # least priority
            return 10
        elif p == Concatenate:
            return 20
        elif p == Astric:    # highest priority
            return 30
        else:                   # left bracket
            return 0

    @staticmethod
    def singleStruct(inputSymbol):   # constructs basic NFA. Regex = a -> NFA
        state1 = 1
        state2 = 2
        basic_nfa = FiniteAutomata({inputSymbol})
        basic_nfa.set_start_state(state1)
        basic_nfa.add_final_state(state2)
        basic_nfa.add_transition(state1, state2, inputSymbol)
        return basic_nfa

    @staticmethod
    def astricStruct(a):  # converting a regex of the form  'a*' to an NFA
        [a, m1] = a.new_NFA_from_number(2)
        state1 = 1
        state2 = m1
        star_nfa = FiniteAutomata(a.symbol)
        star_nfa.set_start_state(state1)
        star_nfa.add_final_state(state2)
        star_nfa.add_transition(star_nfa.startState, a.startState, Epsilon)
        star_nfa.add_transition(star_nfa.startState, star_nfa.finalStates[0], Epsilon)
        star_nfa.add_transition(a.finalStates[0], star_nfa.finalStates[0], Epsilon)
        star_nfa.add_transition(a.finalStates[0], a.startState, Epsilon)
        star_nfa.add_transition_dict(a.transitions)
        return star_nfa

    @staticmethod
    def concatenateStruct(a, b):    # converting a regex of the form 'a·b' to an  NFA
        [a, m1] = a.new_NFA_from_number(1)
        [b, m2] = b.new_NFA_from_number(m1)
        state1 = 1
        state2 = m2 - 1
        dot_nfa = FiniteAutomata(a.symbol.union(b.symbol)) #set both symbols within FA
        dot_nfa.set_start_state(state1)
        dot_nfa.add_final_state(state2)
        dot_nfa.add_transition(a.finalStates[0], b.startState, Epsilon)
        dot_nfa.add_transition_dict(a.transitions)
        dot_nfa.add_transition_dict(b.transitions)
        return dot_nfa

    @staticmethod
    def or_Struct(a, b):   # converting  the form 'a+b' to an NFA
        [a, m1] = a.new_NFA_from_number(2)
        [b, m2] = b.new_NFA_from_number(m1)
        state1 = 1
        state2 = m2
        line_nfa = FiniteAutomata(a.symbol.union(b.symbol))
        line_nfa.set_start_state(state1)
        line_nfa.add_final_state(state2)
        line_nfa.add_transition(line_nfa.startState, a.startState, Epsilon)
        line_nfa.add_transition(line_nfa.startState, b.startState, Epsilon)
        line_nfa.add_transition(a.finalStates[0], line_nfa.finalStates[0], Epsilon)
        line_nfa.add_transition(b.finalStates[0], line_nfa.finalStates[0], Epsilon)
        line_nfa.add_transition_dict(a.transitions)
        line_nfa.add_transition_dict(b.transitions)
        return line_nfa

    def createNFA(self):
        symbol = set()
        prev = ''
        transformed_word = ''

        # explicitly add dot to the expression
        for ch in self.regex:
            if ch in alphabet:
                symbol.add(ch)
            if ch in alphabet or ch == leftBracket:
                if prev != Concatenate and (prev in alphabet or prev in [Astric, rightBracket]):
                    transformed_word += Concatenate
            transformed_word += ch
            prev = ch
        self.regex = transformed_word

        # convert infix expression to postfix expression
        t_word = ''
        stack = []
        for ch in self.regex:
            if ch in alphabet:
                t_word += ch
            elif ch == leftBracket:
                stack.append(ch)
            elif ch == rightBracket:
                while stack[-1] != leftBracket:
                    t_word += stack[-1]
                    stack.pop()
                stack.pop()    # pop left bracket
            else:
                while len(stack) and Regex2NFA.get_priority(stack[-1]) >= Regex2NFA.get_priority(ch):
                    t_word += stack[-1]
                    stack.pop()
                stack.append(ch)
        while len(stack) > 0:
            t_word += stack.pop()
        self.regex = t_word

        # build ε-NFA (epsilon-NFA) from postfix expression
        self.automata = []
        for ch in self.regex:
            if ch in alphabet:
                self.automata.append(Regex2NFA.singleStruct(ch))
                #make a basic nfa struct and add it to the automata stack. Go to next character

            elif ch == Or:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex2NFA.or_Struct(a, b))
            elif ch == Concatenate:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex2NFA.concatenateStruct(a, b))
            elif ch == Astric:
                a = self.automata.pop()
                self.automata.append(Regex2NFA.astricStruct(a))
        self.nfa = self.automata.pop()
        self.nfa.symbol = symbol


class NFA2DFA:

    def __init__(self, nfa):     #  subset construction technique
        self.build_dfa(nfa)     # takes an NFA object as an argument so that DFA can be constructed from it

    def create_dfa(self):
        self.dfa.create('dfa.gv', 'Deterministic Finite Automata')

    def build_dfa(self, nfa):    # subset construction method
        Visited_Subset_all_states = dict()   # visited subset
        # every state's ε-closure (epsilon closure)
        epsilon_closure_dict = dict()
        #take e-closure of the start state of NFA and that will be the start state of DFA.
        state1 = nfa.get_epsilon_closure(nfa.startState)
        #Map the start state of NFA to  the E-closure of it in the Dict
        epsilon_closure_dict[nfa.startState] = state1
        Count = 1     # dfa state id
        dfa = FiniteAutomata(nfa.symbol) #create new FA
        dfa.set_start_state(Count) #set the start state of FA
        #
        states_w = [[state1, dfa.startState]] #W == E-Closure of state1 >> dfa Start state
        Visited_Subset_all_states[Count] = state1 #S ==  set state1 at index 1
        Count += 1
        while len(states_w):
            [state, from_index] = states_w.pop() ##pop states starting from index 1
            for ch in dfa.symbol: #For each character in the input symbol

                #the epsilon closure moves made from ‘s’ upon receiving the current character.
                traversed_states = nfa.get_move(state, ch)
                for s in list(traversed_states):
                    if s not in epsilon_closure_dict: ##Evaluate epsilon closure of all the states of NFA
                        epsilon_closure_dict[s] = nfa.get_epsilon_closure(s)
                    traversed_states = traversed_states.union(epsilon_closure_dict[s])

                if len(traversed_states): #If the traversed states are not yet in visited subset of all states
                    if traversed_states not in Visited_Subset_all_states.values():
                        states_w.append([traversed_states, Count]) #add the traversed states to the dict of states_w
                        Visited_Subset_all_states[Count] = traversed_states #add the traversed state to the visited list at index count
                        to_index = Count
                        Count += 1 #increment the count
                    else: #if the traversed state is already in the visited subset  then add transition from the from index
                        # to the to index upon the input character
                        to_index = [k for k, v in Visited_Subset_all_states.items() if v == traversed_states][0]
                    dfa.add_transition(from_index, to_index, ch)
            for value, state in Visited_Subset_all_states.items():
                if nfa.finalStates[0] in state: #check if the final state is within the visited dict
                    dfa.add_final_state(value) #when found add the final state to the dfa
            self.dfa = dfa #map the dfa to the class dfa


