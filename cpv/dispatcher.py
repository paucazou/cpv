#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module
contains
functions intended to be used
as decorators of rules
"""
import itertools
import tools

def one_voice(func):
    """Apply func to one voice at a time"""
    def __wrapper(data):
        for s in data:
            func(s)
    return __wrapper

def two_voices(func):
    """Apply func to two voices at a time.
    Each voice is linked with every other one
    """
    def __wrapper(data):
        for s1,s2 in itertools.combinations(data,2):
            func(s1,s2)
    return __wrapper

def counterpoint_only(func):
    """Extracts only the counterpoints
    parts and pass them to func"""
    def __wrapper(data):
        for s in data:
            if 'cp' in s.title:
                func(s)

    return __wrapper

def cantus_firmus_only(func):
    """When the canti firmi
    only are expected
    """
    def __wrapper(data):
        cf = next(x for x in data if x.title == "cantus firmus")
        for s in data:
            if 'cf' in s.title:
                func(s, cf)

    return __wrapper

def cp_cf(func):
    """Return the counterpoint and
    the cantus firmus
    as two parts
    """
    def __wrapper(data):
        for s in data:
            if not ('cp' in s.title):
                continue
            cf = tools.get_matching_cf(s,data)
            func(s, cf)

    return __wrapper


