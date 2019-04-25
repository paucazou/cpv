#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""Main module"""
import cp2_note_against_note
import note
import stave

def get_rules(lib):
    """Takes a module and return a dict
    with functions called rule_X, where X
    is an integer which becomes the key
    in the dict
    """
    return {
            int(elt[5]) : getattr(lib, elt)
            for elt in dir(lib)
            if "rule_" in elt
            }

def exclude_rules(rules, not_followed_rules):
    """Exlude very rule which is
    in not_followed_rules
    """
    for rule in not_followed_rules:
        del(rules[rule])

    return rules




def cp_2_note_vs_note(file: str, not_followed_rules=[],only_one=False) -> bool:
    """This function takes a file with a special
    syntax as main argument. The second argument
    is a list of ints of rules to forget, starting by 1
    It returns a bool, True if the file matchs the rules
    selected.
    Syntax of the file:
    General: it must follow the syntax explained in the
    stave.py and note.py fromString methods.
    It must have 13 parts, but some of these parts
    can be optional.
    Every part has a title in lower case.
    The first one is the cantus firmus:
        * cantus firmus
    Every other part is linked to another one. Since the
    counterpoint must have 6 parts, the file must contain
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
    If only_one is set, the file must contain
    only one cantus firmus and one counterpoint
    """
    lib = cp2_note_against_note
    rules =  get_rules(lib)
    rules = exclude_rules(rules,not_followed_rules)

    data = stave.Stave.fromFile(file)
    # rules application...
    for rule in rules:
        rule(data,only_one)

    return True



