#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Contains the error"""
import warnings
class CompositionError(Exception):
    def __init__(self,msg: str, *elts):
        self.msg = msg + f"At: {elts}"

class CompositionWarning(UserWarning):
    def __init__(self,msg: str):
        self.msg = msg 

def warn(*args,**kwargs):
    def _fmt_msg(msg, *elts):
        return msg + f"At: {elts}"
    msg = _fmt_msg(*args,**kwargs)
    warnings.warn(msg,CompositionWarning)

