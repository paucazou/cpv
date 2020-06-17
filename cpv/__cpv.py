#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""Main module"""
from collections import OrderedDict
import cp2_note_against_note
import cp2_note_against_two_notes
import cantus_firmus
import dupre_improvisation_ex_3
import functools
import harmony
import note
import tools
import stave

functions = "cf cp_2_1_1 cp_2_1_2 dupre_improvisation_3 harmony_koechlin".split()

def __get_rules(lib):
    """Takes a module and return a dict
    with functions called rule_X, where X
    is an integer which becomes the key
    in the dict
    """
    rules = {
            int(elt[5:]) : getattr(lib, elt)
            for elt in dir(lib)
            if "rule_" in elt
            }
    return OrderedDict(sorted(rules.items()))

def __exclude_rules(rules, not_followed_rules):
    """Exlude every rule which is
    in not_followed_rules
    """
    new_rules = OrderedDict([(i,r) for i, r in rules.items() if i not in not_followed_rules])

    return new_rules

def cf(string : str, not_followed_rules=[]) -> bool:
    """Takes a string with special syntax as main argument.
    The second one is the list of rules no to be followed,
    starting by 1
    No title required.
    """
    return __rules_checker(string,not_followed_rules,cantus_firmus)


# for counterpoints, functions should be called:
# cp_{number of voices}_1_{nb of notes for one note of cantus firmus}
def cp_2_1_1(string: str, not_followed_rules=[],only_one=False) -> bool:
    """This function takes a string with a special
    syntax as main argument. The second argument
    is a list of ints of rules to forget, starting by 1
    It returns a bool, True if the string matchs the rules
    selected.
    Syntax of the string:
    General: it must follow the syntax explained in the
    stave.py and note.py fromString methods.
    It must have 13 parts, but some of these parts
    can be optional.
    Every part has a title in lower case.
    The first one is the cantus firmus:
        * cantus firmus
    Every other part is linked to another one. Since the
    counterpoint must have 6 parts, the string must contain
    12 parts named that way:
        * 1cf
        * 1cp
    'cf' stands for cantus firmus, 'cp' for counterpoint.
    The number can be 1, 2, 3, 4, 5, 6. The order is unimportant.
    It is not necessary to repeat the cantus firmus each time
    but this must be done if and only if the cantus firmus
    is transposed.
    Each part must restart from 0.
    Are also included three rules described by Michel Baron in his
    Traité de Contrepoint rigoureux.
    More info in cp2_note_against_note.py
    They can be excluded by adding 23, 24 or 25 to not_followed_rules
    If only_one is set, the string must contain
    only one cantus firmus and one counterpoint
    """
    not_followed_rules = list(not_followed_rules)

    # rule that checks that every part is present is disabled
    # if only one counterpoint is expected
    if only_one:
        not_followed_rules.append(2)
    
    lib = cp2_note_against_note
    return __rules_checker(string,not_followed_rules,lib)

def cp_2_1_2(string: str, not_followed_rules=[],only_one=False) -> False:
    """
    Similar to cp_2_note_vs_note, but with the counterpoint with two notes
    for one whole
    """
    not_followed_rules = list(not_followed_rules)
    if 2 in not_followed_rules:
        not_followed_rules += [22,23,24,26] + [i for i in range(210,222)]
    not_followed_rules = __unfollow_linked_rules(not_followed_rules,14,15)
    not_followed_rules = __unfollow_linked_rules(not_followed_rules,17,18)

    # rule that checks that every part is present is disabled
    # if only one counterpoint is expected
    if only_one:
        not_followed_rules.append(22)
    
    lib = cp2_note_against_two_notes
    return __rules_checker(string,not_followed_rules,lib)

def dupre_improvisation_3(string : str, not_followed_rules=[]) -> bool:
    """This function checks that the rules created by Dupré for the third exercise
    of improvisation are followed.
    It requires a string with the usual syntax with three parts
    named: Soprano, Center, Bass (case sensitive).
    """
    not_followed_rules = list(not_followed_rules)
    lib = dupre_improvisation_ex_3
    return __rules_checker(string,not_followed_rules,lib)

def harmony_koechlin(string : str, not_followed_rules=[],start=0,end=None) -> bool:
    """This function checks that the rules followed by Charles Koechlin are followed.
    It requires a string with the usual syntax with four pats:
    Soprano, Alto, Tenor, Bass (case sensitive)."""
    not_followed_rules = list(not_followed_rules)
    lib = harmony
    return __rules_checker(string, not_followed_rules,lib,start,end)



def __rules_checker(string : str, not_followed_rules,lib,start=0,end=None) -> bool:
    """Generic function"""
    rules =  __get_rules(lib)
    rules = __exclude_rules(rules,not_followed_rules)

    data = stave.Stave.fromString(string)
    data = [tools.cut_stave(s,start,end,by_measure=True) for s in data]
    # rules application...
    for i,rule in rules.items():
        print(f"Checking rule {i}...")
        rule(data)
    return True

def __unfollow_linked_rules(rule_list,*rules):
    """If one of the rule in rules is found in rule_list,
    rule_list is added every other rules in rules.
    Return rule_list"""
    for i in rule_list:
        if i in rules:
            rule_list.extend(rules)
            return list(set(rule_list))

    return rule_list

__current_module = __import__(__name__)

__functions_following_rules = []
for fun_name in functions:
    fun = getattr(__current_module,fun_name)
    def decorator(func):
        @functools.wraps(func)
        def wrapper(string, rules, *arg,**kwarg):
            """Only 'rules' are followed."""
            # I think no module should have more than 50 rules, but if necessary...
            max_rules = 1000
            not_followed_rules = [x for x in range(1,1000) if x not in rules]
            return func(string,not_followed_rules=not_followed_rules,*arg,**kwarg)
        return wrapper
    new_fun_name = f"{fun_name}_following_only_rules"
    __functions_following_rules.append(new_fun_name)

    setattr(__current_module,new_fun_name,decorator(fun))

functions.extend(__functions_following_rules)



