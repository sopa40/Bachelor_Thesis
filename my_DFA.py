import random



### DFA representation: as dictionary key value
### {start_state: {symbol: end_state} }
### doubled states are notated as (state_1, state_2)
### symbols are needed mainly to concatenate two states, short path is not calculated yet

max_states_number = 10
max_transition_number = 20
max_alphabet_number = 2
alphabet = set(range(max_alphabet_number))

def generate_transitions():
    begin_state = str(random.randint(0, max_states_number - 1))
    end_state = str(random.randint(0, max_states_number - 1))
    letter = random.randint(0, max_alphabet_number - 1)
    return (begin_state, letter, end_state)

def add_transition(dfa, transition):
    start_state = transition[0]
    end_state = transition[2]
    letter = transition[1]
    
    if letter not in dfa[start_state]:
        dfa[start_state][letter] = end_state
        return 1
    else:
        return 0

def add_complicated_transition(dfa, state_one, state_two):
    
    new_state = (state_one, state_two)
    dfa[new_state] = dict()

    for (letter, transition) in dfa[state_one].items():
        if letter in dfa[state_two]:
            if transition > dfa[state_two][letter]:
                new_transition = (dfa[state_two][letter], transition)
                
            elif transition < dfa[state_two][letter]:
                new_transition = (transition, dfa[state_two][letter])
            
            else:
                new_transition = transition
                
            dfa[new_state][letter] = new_transition
            
        else:
            dfa[new_state][letter] = transition
             

    for (letter, transitions) in dfa[state_two].items():
        if letter in dfa[state_one]:
            pass
        else:
            dfa[new_state][letter] = transition
    
    return dfa 

def generate_DFA():
    failed_tries = 0
    transition_number = 0
    dfa = {str(k):dict() for k in range(0, max_states_number)}
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
    
def generate_double(dfa):
    states = list(dfa.keys())
    dfa_double = dfa.copy()
    for state_one in states:
        for state_two in states:
            if (state_one == state_two or state_one == {} or state_two == {}):
                continue
                
            if ( (state_one, state_two) in dfa_double or 
                    (state_two, state_one) in dfa_double):
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
            # print("checking path from singleton while bfs!")
            pass
        else: 
            #print("it's not a singleton!")
            pass
        print (m, end = " ") 
        for (letter, destination) in dfa[m].items():
            if destination not in visited:
                reset_len += 1
                if (type(destination) == str):
                    print()
                    return (state, destination, reset_len)
                visited.append(destination)
                queue.append(destination)
                
    return 0
        
        
# Do singletones should be compressed?        
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
#check_synchro(dfa_src)
print(bfs(dfa_double, ('0', '1')))

