#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Contains the error"""
import warnings
class CompositionError(Exception):
    def __init__(self,msg: str, *bars):
        self.msg = msg + f"Bar: {bars}"

class CompositionWarning(UserWarning):
    def __init__(self,msg: str):
        self.msg = msg 

def warn(*args,**kwargs):
    def _fmt_msg(msg, *bars):
        return msg + f"Bars: {bars}"
    ms = _fmt_msg(*args,**kwargs)
    warnings.warn(msg,CompositionWarning)

