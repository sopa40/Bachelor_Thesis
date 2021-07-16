import random



### DFA representation: as dictionary key value
### {start-state: [(symbol, end_state)]}
### For beginning I don't need symbol, only start-end-states. Just added it for possible future uses

max_states_number = 10
max_alphabet_number = 2
alphabet = set(range(max_alphabet_number))
max_transition_number = 20

def generate_transitions():
    begin_state = str(random.randint(0, max_states_number - 1))
    end_state = str(random.randint(0, max_states_number - 1))
    letter = random.randint(0, max_alphabet_number - 1)
    return (begin_state, letter, end_state)

def add_transition(dfa, transition):
    start_state = transition[0]
    end_state = transition[2]
    letter = transition[1]
    #existing transition symbols
    transition_letters = []
    for exist_trans in dfa.get(start_state):
        transition_letters.append(exist_trans[0])
    
    # max number of transitions condition is included here as well
    if letter not in transition_letters:
        dfa[start_state].append((letter, end_state))
        return 1
    else:
        return 0

def generate_DFA():
    failed_tries = 0
    transition_number = 0
    dfa = {str(k):[] for k in range(0, max_states_number)}
    while (transition_number < max_transition_number):
        transition = generate_transitions()
        if (not add_transition(dfa, transition)):
            failed_tries += 1
            if failed_tries > 3:
                pass
                #print("failed tries:", failed_tries)
        else:
            transition_number += 1
            failed_tries = 0
    return dfa
    

def add_complicated_transition(dfa, state_one, state_two):
    new_state = state_one + state_two
    transition_letters = []
    for exist_trans in dfa.get(state_one):
        transition_letters.append(exist_trans[0])
    for exist_trans in dfa.get(state_two):
        transition_letters.append(exist_trans[0])
    for letter in transition_letters:
        
    
    
def generate_double(dfa):
    states = list(dfa.keys())
    dfa_double = dfa.copy()
    for state_one in states:
        for state_two in states:
            if state_one == state_two:
                continue
                
            if (state_one + state_two in dfa.keys() or 
                    state_two + state_one in dfa.keys()):
                continue
            
            dfa_double = add_complicated_transition(dfa_double, state_one, state_two )
            
    return dfa_double



def bfs(dfa, state): #function for BFS
    visited = []    
    queue = []      
    reset_len = 0
    visited.append(state)
    queue.append(state)
    while queue:          # Creating loop to visit each node
        m = queue.pop(0) 
        if (len(m) == 1):
            #print("checking path from singleton while bfs!")
            continue
 #       print (m, end = " ") 
        for neighbour in dfa[m]:
        
            if neighbour[1] not in visited:
                reset_len += 1
                if (len(neighbour[1]) == 1):
                    return (state, neighbour[1], reset_len)
                visited.append(neighbour[1])
                queue.append(neighbour[1])
                
    return 0
        
def check_synchro(dfa):
    dfa_extended = generate_double(dfa)
    states_to_compress = set(dfa_extended.keys())
    temp_states = states_to_compress.copy()
    for state in temp_states:
        reduced_to = bfs(dfa_extended, state)
#        if (reduced_to):
#            print("path from, path to, reset length", reduced_to)
            
    print(dfa_extended)

    











dfa_src = generate_DFA()
dfa_double = generate_double(dfa_src)
check_synchro(dfa_src)
#bfs(dfa_double, '01')    # function calling



























































