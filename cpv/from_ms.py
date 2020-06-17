#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import __cpv
import functools
import importer

__current_module = __import__(__name__)

for fun_name in __cpv.functions:
    fun = getattr(__cpv,fun_name)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(file, *a, **kw):
            content = importer.import_msx(file)
            return func(content,*a,**kw)
        return wrapper

    setattr(__current_module,fun_name,decorator(fun))
