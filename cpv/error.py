#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Contains the error"""

class CompositionError(Exception):
    def __init__(self,msg: str, bar, bar_nb):
        self.msg = msg + f"Bar: {bar_nb}: {bar}"

class CompositionWarning(UserWarning):
    def __init__(self,msg: str, bar, bar_nb):
        self.msg = msg + f"Bar: {bar_nb}: {bar}"

