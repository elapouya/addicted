========
addicted
========

addicted = addict ExtendeD

This library extends ‘addict‘ with some features.

NoAttrDict
----------

    Works like addict DictExt, except that it returns a ‘NoAttr‘ value when an attribute is missing.
    Please read noattr package notes for explaination about ‘NoAttr‘ 

    from addicted import Dict,NoAttrDict
    d1 = DictExt()
    d2 = NoAttrDict()

    print type(d1.a.b.c.d)
    >>> <class 'addicted.DictExt'>
    
    print type(d2.a.b.c.d)
    >>> <class 'noattr.NoAttrType'>

    