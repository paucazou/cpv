#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module
contains
functions intended to be used
as decorators of rules
"""

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
        for s in data:
            for s2 in data:
                if s is not s2:
                    func(s,s2)
    return __wrapper
