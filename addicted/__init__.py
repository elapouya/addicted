# -*- coding: utf-8 -*-
'''
Création : 30 juin 2015

@author: Eric Lapouyade
'''

__version__ = '0.0.1'

from addict import Dict
from noattr import NoAttr

class DictExt(Dict):
    pass

class NoAttrDict(DictExt):
    def __getitem__(self, name):
        if name not in self:
            return NoAttr
        return super(Dict, self).__getitem__(name)    