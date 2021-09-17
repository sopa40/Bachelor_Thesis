import time
import DFA_config 
from progress.bar import IncrementalBar
from progress.spinner import Spinner
from DFA_functionality import *
    


### Experiment 0: How many among random @DFA_config.max_count are synchro
"""
def test_0(): 
    generated_automata = 0
    non_synchro_count = 0
    bar = Spinner("While loops looking for non_synchro  ")
    while generated_automata < DFA_config.max_count:
        bar.next()
        generated_automata += find_non_synchro()
        non_synchro_count += 1
        
    bar.finish()
    print("Ex0. Among {} random DFA (with empty) synchro is {}".format(generated_automata, (DFA_config.max_count - non_synchro_count)))
"""


### Experiment 1: How many NON_EMPTY unique DFA among @DFA_config.max_count are synchro

### RESULT: number of unique (NON_EMPTY) automata raises very quickly, for example for (states, transitions, alphabet)
### (4 4 1) it's 256, (4 4 2) it's 4096, (4 4 3) it's 20736?, (5 5 1 3125), witn (n n 1) it's n^n
### (20 20 1) it's more than 170k
### Without NON_EMPTY restriction number of unique DFAs raises even more drastic
def test_1():  
    print()
    print("Test 1")
    ### to avoid infinite loops if @DFA_config.max_count is bigger than unique possible
    failed_count_loop = 0 
    failed_count_total = 0
    max_failed_count = DFA_config.max_count
    added_dfa = 0
    unique_dfa_arr = []
    synchro_unique = 0
    look_bar = IncrementalBar('looking for unique automata ', max = DFA_config.max_count)
    while added_dfa < DFA_config.max_count:
        if failed_count_loop >= DFA_config.max_count:
            print()
            print ("in experiment 1 @DFA_config.max_count is bigger than unique DFA possible")
            print("Found unique DFA number is ", len(unique_dfa_arr))
            break
        unique_dfa = generate_non_empty_DFA()
        unique_dfa = reorder_transitions(unique_dfa)
        if unique_dfa in unique_dfa_arr:
            failed_count_total += 1
            failed_count_loop += 1
        else:
            unique_dfa_arr.append(unique_dfa)
            added_dfa += 1
            look_bar.next()
            failed_count_loop = 0
            
    print()
    check_bar = IncrementalBar('checking unique automata', max = DFA_config.max_count)
    for dfa in unique_dfa_arr:
        check_bar.next()
        if check_synchro(dfa) == 1:
            synchro_unique += 1
    
    print()
    print("Among {} unique DFA (without empty) synchro is {}".format(added_dfa, synchro_unique))
    print("Meanwhile generated repeating DFA {}".format(failed_count_total))


### RESULT of comparing Experiment 0 and Experiment 1: almost no difference if we use unique automata or random
### because with number big enough numbers (let's say starting with 8) chance of collision is less than 1/8^8


### Experiment 2: how many random NON_EMPTY DFAs among @DFA_config.max_count are synchro
def test_2():
    print()
    print("Test 2")
    tested_dfa = 0
    synchro_random = 0
    bar2 = IncrementalBar("Searching ", max = DFA_config.max_count)
    empty_generated = 0
    while tested_dfa < DFA_config.max_count:
        random_dfa = generate_non_empty_DFA()
        if check_synchro(random_dfa) == 1:
            synchro_random += 1
        bar2.next()
        tested_dfa += 1
    print()
    print('''Among {} random DFA (without empty) synchro is {}
            '''.format(tested_dfa, synchro_random))
    return synchro_random


### Experiment 3: how many random DFAs (with empty DFA inclusive) among @DFA_config.max_count are synchro
def test_3(): 
    print()
    print("Test 3")
    tested_dfa = 0
    synchro_random = 0
    bar3 = IncrementalBar('Searching', max = DFA_config.max_count)
    while tested_dfa < DFA_config.max_count:
        random_dfa = generate_DFA()
        if check_synchro(random_dfa) == 1:
            synchro_random += 1
        
        bar3.next()
        tested_dfa += 1
    
    print()
    print("Among {} random DFA (with empty) synchro is {}".format(tested_dfa, synchro_random))
    return synchro_random

""" 
    ALERT: 
    Experiment 0 and 3 have identic aim, but different approaches. 
    Looks like values are different. To be tested   
"""

### Experiment 4: how many DFA with at least one empty state among @DFA_config.max_count are synchro 

### Important: if @DFA_config.max_transition_number == @DFA_config.max_states_number * @DFA_config.max_alphabet_number, empty DFA doesn't exist
### So be sure to pick up number suitable for this test
def test_4():
    print()
    print("Test 4")
    empty_tested = 0
    synchro_empty = 0
    non_empty_generated = 0
    bar4 = IncrementalBar("Searching ", max = DFA_config.max_count)
    while empty_tested < DFA_config.max_count:
        failed_count = 0
        bar4.next()
        empty_dfa = generate_DFA()
        while not check_if_empty(empty_dfa):
            if failed_count > DFA_config.max_count * 100:
                print()
                print("a lot of non empty generated. No more empties found. Exit with data obtained so long")
                print("Among {} empty DFA synchro is {}". format(empty_tested, synchro_empty))
                print("Meanwhile generated non empty DFA {}".format(non_empty_generated))
                return synchro_empty
            failed_count += 1
            non_empty_generated += 1
            empty_dfa = generate_DFA()
        if (check_synchro(empty_dfa) == 1):
            synchro_empty += 1
        empty_tested += 1
    print()
    print("Among {} empty DFA synchro is {}". format(empty_tested, synchro_empty))
    print("Meanwhile generated non empty DFA {}".format(non_empty_generated))
    return synchro_empty
    
### Experiment 4: how many DFA with at least one empty state among @DFA_config.max_count are synchro 

### Important: if @DFA_config.max_transition_number == @DFA_config.max_states_number * @DFA_config.max_alphabet_number, empty DFA doesn't exist
### So be sure to pick up number suitable for this test
def test_5():
    print()
    print("Test 5")
    empty_tested = 0
    synchro_empty = 0
    non_empty_generated = 0
    bar4 = IncrementalBar("Searching ", max = DFA_config.max_count)
    while empty_tested < DFA_config.max_count:
        failed_count = 0
        bar4.next()
        empty_dfa = generate_DFA()
        while not check_if_one_empty(empty_dfa):
            if failed_count > DFA_config.max_count * 150:
                print()
                print("a lot of non empty generated. No more empties found. Exit with data obtained so long")
                print("Among {} empty DFA synchro is {}". format(empty_tested, synchro_empty))
                print("Meanwhile generated non empty DFA {}".format(non_empty_generated))
                return synchro_empty
            failed_count += 1
            non_empty_generated += 1
            empty_dfa = generate_DFA()
            
        if check_synchro(empty_dfa) == 1:
            synchro_empty += 1
        empty_tested += 1
    print()
    print("Among {} empty DFA with ONE empty state synchro is {}". format(empty_tested, synchro_empty))
    print("Meanwhile generated non empty DFA {}".format(non_empty_generated))
    return synchro_empty 

### Experiment 5: find a not fully connected DFA with doubled states, but still synchro 
### assuming it should be connected to some strongly connected component of the DFA
def test_6():
    """TODO"""


### Experiment 6: find fully connected DFA,  but non synchro
def test_7():
    """TODO"""

### Experiment 7: how many tries to generate fully connected
def test_8():
    """TODO"""  

def take_median(func):
    loops_total = 10
    synchro_found = 0
    for i in range(loops_total):
        synchro_found += func()
    return (synchro_found /(DFA_config.max_count * loops_total)) * 100
if __name__ == "__main__":
    
    start_time = time.time()
    
    ### checking the algorithm with 100% synchronizable automaton. 1 is expected
    # dfa_synchro = {0: {1: 1, 0: 1}, 1: {0: 2, 1: 1}, 2: {0: 3, 1: 2}, 3: {0: 0, 1: 3}}
    # print("IT MUST BE 1! Result", check_synchro(dfa_synchro))

    if DFA_config.max_transition_number < DFA_config.max_states_number:
        print("Unable to generate strongly connected component")
        print("Please increase @DFA_config.max_transition_number to be at least @DFA_config.max_states_number")
        exit()

    if DFA_config.max_transition_number > DFA_config.max_states_number * DFA_config.max_alphabet_number:
        print("too many transitions, infinite loop while generating automaton")
        exit()
    

    print("Parameters are:")
    print("Max number of suitable tested DFA ", DFA_config.max_count)
    print("DFA_config.max_states_number ", DFA_config.max_states_number)
    print("DFA_config.max_transition_number ", DFA_config.max_transition_number)
    print("DFA_config.max_alphabet_number ", DFA_config.max_alphabet_number)
    print("Let's get the party started")
    print()
    """
    test_1()
    test_2()
    test_3()
    test_4()
    """
    
    while (DFA_config.max_transition_number <= DFA_config.max_states_number * DFA_config.max_alphabet_number):
        print()
        print("----New iteration----")
        print("max transition number is ", DFA_config.max_transition_number)
        test_4()
        test_5()
        DFA_config.max_transition_number += 1
    print()
    print("--- Execution took {} seconds ---".format(time.time() - start_time))