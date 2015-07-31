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
pp = pprint.PrettyPrinter(indent=4)


class DictExt(Dict):
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

    def count_items(self,filter):
        n = 0
        for v in self.itervalues():
            try:
                if filter(v):
                    n += 1
            except:
                pass
        return n

    def get_items(self,filter):
        items=[]
        for k,v in self.iteritems():
            try:
                if filter(k,v):
                    items.append((k, v))
            except:
                pass
        return items

    def get_items_iter(self,filter):
        for k,v in self.iteritems():
            try:
                if filter(k,v):
                    yield (k, v)
            except:
                pass
            
    def get_items_key_re(self,pattern):
        items=[]
        for k,v in self.iteritems():
            try:
                if pattern.match(k):
                    items.append((k, v))
            except:
                pass
        return items

    def get_items_key_re_iter(self,pattern):
        for k,v in self.iteritems():
            try:
                if pattern.match(k):
                    yield (k, v)
            except:
                pass
            
    def get_items_val_re(self,pattern):
        items=[]
        for k,v in self.iteritems():
            try:
                if pattern.match(v):
                    items.append((k, v))
            except:
                pass
        return items

    def get_items_val_re_iter(self,pattern):
        for k,v in self.iteritems():
            try:
                if pattern.match(v):
                    yield (k, v)
            except:
                pass
            
    def gets(self,*keys):
        out=[]
        for k in keys:
            out.append(self.get(k))
        # le string formatting veut absolument un tupple...
        return tuple(out)

    def format_items(self,format_func,default=None):
        out=''
        for k,v in sorted(self.items()):
            out += format_func(k,v)
        else:
            if default:
                return default
        return out
    
    def extract(self,key_list):
        """ Si le dict contient {'a':1,'b':2,'c':3}
            alors dict.extract(['b','c','d'])
            renverra {'b':2,'c':3}"""
        if isinstance(key_list,basestring):
            key_list = key_list.split(',')
        out = type(self)({})
        for k in key_list:
            if k in self:
                out[k] = self[k]
        return out
    
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