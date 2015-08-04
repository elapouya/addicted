========
addicted
========

addicted = addict ExtendeD

This library comes from ‘mewwts/addict‘ with some more features.

Dict
----

Same as Dict from ‘mewwts/addict‘ except that update() method accept list,tuple and kwargs like usual python dict.
The use of ‘inspect‘ module has been removed for performance reason.


DictExt
-------

Dict with these additional methods : ::

    pprint()
    find(pattern,**kwargs)
    count_some_values(pattern,ignore_case=False)
    count_some_keys(pattern,ignore_case=False)
    count_some_items(filter)
    iter_some_items(pattern,ignore_case=False)
    iter_some_values(pattern,ignore_case=False)
    iter_some_keys(pattern,ignore_case=False)
    get_some_items(pattern,ignore_case=False)
    get_some_values(pattern,ignore_case=False)
    get_some_keys(pattern,ignore_case=False)
    mget(*key_list)
    extract(key_list)
    parse_booleans(key_list)
    parse_numbers(key_list)

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

