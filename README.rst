========
addicted
========

addicted = addict ExtendeD

This library extends ‘addict‘ with some features.

DictExt
-------

in development...

NoAttrDict
----------

Works like DictExt, except that it returns a ‘NoAttr‘ value when an attribute is missing.
Please read `noattr <https://pypi.python.org/pypi/noattr/>`_ package notes for explaination about ‘NoAttr‘ ::

    from addicted import Dict,NoAttrDict
    d1 = DictExt()
    d2 = NoAttrDict()
    
    print type(d1.a.b.c.d)
    >>> <class 'addicted.DictExt'>
    
    print type(d2.a.b.c.d)
    >>> <class 'noattr.NoAttrType'>

    