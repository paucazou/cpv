#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import __cpv

__current_module = __import__(__name__)

for fun_name in __cpv.functions:
    fun = getattr(__cpv,fun_name)
    def decorator(func):
        def wrapper(file, *a, **kw):
            with open(file) as f:
                content = f.read()
            return func(content,*a,**kw)
        return wrapper

    setattr(__current_module,fun_name,decorator(fun))
