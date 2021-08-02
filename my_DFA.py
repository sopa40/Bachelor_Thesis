import random



### DFA representation: as dictionary key value
### {start_state: {transition_symbol: end_state} }
### doubled states are notated as (state_1, state_2), singletones as state_1
### symbols are needed mainly to concatenate two states, short path is not calculated yet


# if there are more max_transitions than possible with current max_states and alphabet, the program will fall in infinite loop
# so choose the numbers carefully. Maybe later checking will be added

max_states_number = 4
max_transition_number = 2
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

# to concatenate all transitions of singletones to a doubled state
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
             

    for (letter, transition) in dfa[state_two].items():
        if letter in dfa[state_one]:
            pass
        else:
            dfa[new_state][letter] = transition
    
    return dfa 


# A question: should only strongly connected graphs be generated? 
def generate_DFA():
    failed_tries = 0
    transition_number = 0
    dfa = {str(k):dict() for k in range(0, max_states_number)}
    while (transition_number < max_transition_number):
        transition = generate_transitions()
        if (not add_transition(dfa, transition)):
            failed_tries += 1
        else:
            transition_number += 1
            failed_tries = 0
    return dfa    


# generates DFA with all doubled states    
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

# bfs to find a path from one state (e.g. doubled) to another (e.g. singleton)
def bfs(dfa, state): 
    visited = []    
    queue = []      
    reset_len = 0
    visited.append(state)
    queue.append(state)
    while queue:          # visiting each node
        m = queue.pop(0) 
        
        # printing path for debugging needs
        # print (m, end = " ") 
        
        print("m is", m, " dfa[m] are ", dfa[m].items())
        
        if (not len(dfa[m].items())):
            print("going through a state with no transitions")
            continue
        
        for (letter, destination) in dfa[m].items():
            
        
            if destination not in visited:
                reset_len += 1
                
                # if singleton found --> reduction happens
                if (type(destination) == str):
                    return (state, destination, reset_len)
                visited.append(destination)
                queue.append(destination)
                
    return 0

# assuming states_to_remove is doubled state
def remove_states(all_states, reduction):
    
    states_to_remove = reduction[0]
    reduction_dest = reduction[1]
    
    print("start state is ", states_to_remove, " destination is ", reduction_dest)
    
    print("removing ", states_to_remove)
    all_states.remove(states_to_remove)
    
    # if reduced to one of two states, it stays in all_states to be (possibly) removed later
    if reduction_dest in states_to_remove:
        states_to_remove = tuple(x for x in states_to_remove if x != reduction_dest)
        
    # deleting the doubled state
    
    print(" new states to remove is ", states_to_remove)
    
    # deleting all states containing first or second state
    temp_states = all_states.copy()
    for remove_state in states_to_remove:
        for state in temp_states:
            if remove_state in state:
                print("removing ", state)
                all_states.remove(state)
                      
    return all_states
            
    
        
# Singletones are not in states_to_compress

# Finding only a pass to a random singleton. 
# Assuming one can synchronize it to one state for all later. Connected component 
def check_synchro(dfa):
    dfa_extended = generate_double(dfa)
    
    
    print("simple is ", dfa)
    print("extended is ", dfa_extended)
    
    states_to_compress = set(dfa_extended.keys())
    temp_states = states_to_compress.copy()
    
    # removing all singletones, leaving only doubled (not sure if this should be done)
    for state in temp_states:
        if (len(state) == 1):
            states_to_compress.remove(state)
    
    temp_states = set()
    while (len(states_to_compress)):
        if (len(temp_states) == len(states_to_compress)):       # no reduction happened (no possible)
            return 0
            
        temp_states = states_to_compress.copy()
        for state in temp_states:
            reduced_to = bfs(dfa_extended, state)   # searching for the reduction from any doubled state
            if reduced_to:
                states_to_compress = remove_states(states_to_compress, reduced_to)
                break
    
    return 1



count = 0

dfa_src = generate_DFA()
while (check_synchro(dfa_src)):
    count += 1
    print()
    dfa_src = generate_DFA()
    
print("not sychro, passed tries ", count)

