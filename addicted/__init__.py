# -*- coding: utf-8 -*-
'''
Création : 30 juin 2015

@author: Eric Lapouyade
'''

__version__ = '0.0.2'

from addict import Dict
from noattr import NoAttr
import re
import pprint
from inspect import isgenerator
pp = pprint.PrettyPrinter(indent=4)


class DictExt(Dict):
    def _update_kv(self,k,v):
        if ((k not in self) or
            (not isinstance(self[k], dict)) or
            (not isinstance(v, dict))):
            self[k] = v
        else:
            self[k].update(v)

    def update(self, *args, **kwargs):
        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, dict):
                for k, v in arg.items():
                    self._update_kv(k, v)
            elif isinstance(arg, (list, tuple)) and (not isinstance(arg[0], (list, tuple))):
                k = arg[0]
                v = arg[1]
                self._update_kv(k, v)
            elif isinstance(arg, (list, tuple)) or isgenerator(arg):
                for k, v in arg:
                    self._update_kv(k, v)
            else:
                raise TypeError("update does not understand "
                                "{0} types".format(type(arg)))

        for k, v in kwargs.items():
            self._update_kv(k, v)

    @property
    def pprint(self):
        pp.pprint(self)

    def find(self,pattern,**kwargs):
        dct=DictExt()
        key_prefix = kwargs.get('key_prefix','')
        deep = kwargs.get('deep',True)
        if key_prefix:
            key_prefix += '.'
        search_keys = kwargs.get('keys',True)
        search_values = kwargs.get('values',False)
        parent_values = kwargs.get('parent',False)
        parent_dict = kwargs.get('parent_dict')
        look_key = kwargs.get('look')

        for k,v in self.items():
            if search_keys:
                m = pattern.search(k)
                if m :
                    dct[key_prefix + k] = v
                    continue
            if isinstance(v,DictExt):
                if deep:
                    kwargs['key_prefix'] = key_prefix + k
                    kwargs['parent_dict'] = v
                    dct.update(v.find(pattern,**kwargs))
            elif type(v) == list:
                if deep:
                    n = 0
                    for i in v:
                        n += 1
                        if isinstance(i,DictExt):
                            kwargs['key_prefix'] = '%s%d' % (key_prefix, n)
                            kwargs['parent_dict'] = i
                            dct.update(i.find(pattern,**kwargs))
            else:
                if search_values:
                    if (not look_key) or (look_key == k) :
                        if isinstance(v,dict):
                            test_value = v.values()
                        else:
                            test_value = v
                        m = pattern.search(str(test_value))
                        if m :
                            if parent_values:
                                dct[key_prefix[:-1]] = parent_dict
                            else:
                                dct[key_prefix + k] = v
        return dct

    def count_some_values(self,pattern,ignore_case=False):
        if isinstance(pattern,basestring):
            pattern = re.compile(pattern, re.I if ignore_case else 0)
        if callable(pattern):
            return sum(( 1 if pattern(v) else 0 for v in self.itervalues()))
        else:
            return sum(( 1 if pattern.search(str(v)) else 0 for v in self.itervalues()))

    def count_some_keys(self,pattern,ignore_case=False):
        if isinstance(pattern,basestring):
            pattern = re.compile(pattern, re.I if ignore_case else 0)
        if callable(pattern):
            return sum(( 1 if pattern(v) else 0 for v in self.iterkeys()))
        else:
            return sum(( 1 if pattern.search(str(k)) else 0 for k in self.iterkeys()))

    def count_some_items(self,filter):
        return sum(( 1 if filter(k,v) else 0 for k,v in self.iteritems()))

    def iter_some_items(self,pattern,ignore_case=False):
        if isinstance(pattern,basestring):
            pattern = re.compile(pattern, re.I if ignore_case else 0)
        if callable(pattern):
            return ( (k,v) for k,v in self.iteritems() if pattern(k,v) )
        else:
            return ( (k,v) for k,v in self.iteritems() if pattern.search(str(k)) )

    def iter_some_values(self,pattern,ignore_case=False):
        if isinstance(pattern,basestring):
            pattern = re.compile(pattern, re.I if ignore_case else 0)
        if callable(pattern):
            return ( v for v in self.itervalues() if pattern(v) )
        else:
            return ( v for v in self.itervalues() if pattern.search(str(v)) )

    def iter_some_keys(self,pattern,ignore_case=False):
        if isinstance(pattern,basestring):
            pattern = re.compile(pattern, re.I if ignore_case else 0)
        if callable(pattern):
            return ( k for k in self.iterkeys() if pattern(k) )
        else:
            return ( k for k in self.iterkeys() if pattern.search(str(k)) )

    def get_some_items(self,pattern,ignore_case=False):
        return list(self.iter_some_items(self,pattern,ignore_case))

    def get_some_values(self,pattern,ignore_case=False):
        return list(self.iter_some_values(self,pattern,ignore_case))

    def get_some_keys(self,pattern,ignore_case=False):
        return list(self.iter_some_keys(self,pattern,ignore_case))

    def mget(self,*key_list):
        if isinstance(key_list,basestring):
            key_list = key_list.split(',')
        # le string formatting veut absolument un tupple...
        return tuple([ self[k] for k in key_list ])

    def extract(self,key_list):
        """ >>> d = {'a':1,'b':2,'c':3}
            >>> print d.extract('b,c,d')
            >>> {'b':2,'c':3}
            >>> print d.extract(['b','c','d'])
            >>> {'b':2,'c':3} """
        if isinstance(key_list,basestring):
            key_list = key_list.split(',')
        return self.__class__([ (k,self[k]) for k in key_list if k in self ])

    def parse_booleans(self,key_list):
        if isinstance(key_list,basestring):
            key_list = key_list.split(',')
        for k in key_list:
            if k in self:
                val = self[k]
                if isinstance(val,basestring):
                    if val.lower() == 'false':
                        self[k] = False
                    elif val.lower() == 'true':
                        self[k] = True

    def parse_numbers(self,key_list):
        if isinstance(key_list,basestring):
            key_list = key_list.split(',')
        for k in key_list:
            if k in self:
                val = self[k]
                if isinstance(val,basestring):
                    try:
                        self[k] = float(val) if '.' in val else int(val)
                    except ValueError:
                        self[k] = None

class NoAttrDict(DictExt):
    def __getitem__(self, name):
        if name not in self:
            return NoAttr
        val = super(Dict, self).__getitem__(name)
        if val is None:
            return NoAttr
        return val